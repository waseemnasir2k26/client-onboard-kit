"""The two guarantees that matter: precise failures, and never a raw placeholder."""

from __future__ import annotations

import re

import pytest

from client_onboard_kit.errors import (
    ConfigError,
    MissingFieldError,
    UnrenderedPlaceholderError,
)
from client_onboard_kit.render import DOCUMENTS, assert_fully_rendered, build_pack

PLACEHOLDER = re.compile(r"\{\{|\}\}|\{%|%\}|\{#|#\}")


def test_missing_field_names_the_field_and_the_template(tmp_path, write_config):
    config = write_config(lambda d: d["legal"].pop("jurisdiction"))
    with pytest.raises(MissingFieldError) as excinfo:
        build_pack(config, tmp_path / "pack")
    message = str(excinfo.value)
    assert "legal.jurisdiction" in message
    assert "service-agreement.md" in message


def test_missing_nested_field_reports_the_full_dotted_path(tmp_path, write_config):
    config = write_config(lambda d: d["comms"].pop("approver_name"))
    with pytest.raises(MissingFieldError) as excinfo:
        build_pack(config, tmp_path / "pack")
    assert "comms.approver_name" in str(excinfo.value)


def test_missing_field_is_not_silently_blanked(tmp_path, write_config):
    """A missing field must fail the build, not produce a document with a hole in it."""
    config = write_config(lambda d: d["client"].pop("legal_name"))
    out = tmp_path / "pack"
    with pytest.raises(MissingFieldError):
        build_pack(config, out)
    assert not (out / "service-agreement.md").exists()


def test_a_branch_not_taken_does_not_require_its_fields(tmp_path, write_config):
    """`disclosing_party` is only needed for a one-way NDA, and the example omits it."""
    config = write_config(lambda d: d["legal"]["nda"].__setitem__("type", "mutual"))
    build_pack(config, tmp_path / "pack", formats=("md",))  # must not raise


def test_no_unrendered_placeholder_survives_into_any_output(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out)
    for path in sorted(out.iterdir()):
        text = path.read_text(encoding="utf-8")
        found = PLACEHOLDER.findall(text)
        assert not found, f"{path.name} contains template syntax: {found[:3]}"


def test_a_template_that_would_emit_a_placeholder_is_refused(tmp_path, write_config):
    """End-to-end proof of the guarantee, using a deliberately broken template."""
    templates = tmp_path / "templates"
    templates.mkdir()
    for doc in DOCUMENTS:
        templates.joinpath(doc.template).write_text("# ok\n\nbody\n", encoding="utf-8")
    # {% raw %} makes Jinja emit the literal placeholder text - exactly the failure mode
    # we must never ship to a client.
    templates.joinpath("welcome-email.md").write_text(
        "# Hello\n\nDear {% raw %}{{ client.name }}{% endraw %},\n", encoding="utf-8"
    )

    with pytest.raises(UnrenderedPlaceholderError) as excinfo:
        build_pack(write_config(), tmp_path / "pack", templates_dir=templates)
    assert "welcome-email.md" in str(excinfo.value)
    assert "{{ client.name }}" in str(excinfo.value)
    assert not (tmp_path / "pack" / "welcome-email.md").exists()


def test_assert_fully_rendered_is_strict_about_every_delimiter():
    for bad in ("{{ x }}", "{% if x %}", "{# note #}", "trailing }} here"):
        with pytest.raises(UnrenderedPlaceholderError):
            assert_fully_rendered(bad, "some-template.md")
    assert_fully_rendered("perfectly ordinary prose", "some-template.md") is None


def test_unknown_format_key_is_rejected(tmp_path, write_config):
    config = write_config(lambda d: d["format"].__setitem__("currency_prefix", "$"))
    with pytest.raises(ConfigError) as excinfo:
        build_pack(config, tmp_path / "pack")
    assert "currency_prefix" in str(excinfo.value)


def test_empty_and_broken_yaml_fail_clearly(tmp_path):
    empty = tmp_path / "empty.yaml"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ConfigError):
        build_pack(empty, tmp_path / "pack")

    broken = tmp_path / "broken.yaml"
    broken.write_text("client: [unclosed\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        build_pack(broken, tmp_path / "pack")

    with pytest.raises(ConfigError):
        build_pack(tmp_path / "nope.yaml", tmp_path / "pack")
