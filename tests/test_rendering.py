"""Every template renders, and the output layout is what the README promises."""

from __future__ import annotations

import pytest

from client_onboard_kit.errors import ConfigError
from client_onboard_kit.render import DOCUMENTS, build_pack

ALL_SLUGS = [d.slug for d in DOCUMENTS]


def test_every_template_renders(tmp_path, write_config):
    out = tmp_path / "pack"
    written = build_pack(write_config(), out)

    for slug in ALL_SLUGS:
        md = out / f"{slug}.md"
        html = out / f"{slug}.html"
        assert md.is_file(), f"{slug}.md was not written"
        assert html.is_file(), f"{slug}.html was not written"
        assert len(md.read_text(encoding="utf-8")) > 800, f"{slug}.md is suspiciously short"
        assert "<main" in html.read_text(encoding="utf-8")

    assert (out / "index.html").is_file()
    assert len(written) == len(ALL_SLUGS) * 2 + 1


def test_output_file_layout_is_flat_and_exact(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out)
    expected = {f"{slug}.{ext}" for slug in ALL_SLUGS for ext in ("md", "html")} | {"index.html"}
    assert {p.name for p in out.iterdir()} == expected
    assert all(p.is_file() for p in out.iterdir())


def test_markdown_only_skips_html_and_index(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out, formats=("md",))
    assert {p.name for p in out.iterdir()} == {f"{slug}.md" for slug in ALL_SLUGS}


def test_only_flag_renders_a_subset(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out, only=["welcome-email"], formats=("md",))
    assert {p.name for p in out.iterdir()} == {"welcome-email.md"}


def test_unknown_document_slug_is_rejected(tmp_path, write_config):
    with pytest.raises(ConfigError) as excinfo:
        build_pack(write_config(), tmp_path / "pack", only=["invoice"])
    assert "invoice" in str(excinfo.value)


def test_every_document_carries_the_not_legal_advice_comment(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out, formats=("md",))
    for slug in ALL_SLUGS:
        head = (out / f"{slug}.md").read_text(encoding="utf-8")[:900]
        assert head.startswith("<!--")
        assert "NOT LEGAL ADVICE" in head


def test_legal_documents_get_a_screen_only_review_banner(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out)
    for slug, expect_banner in (
        ("service-agreement", True),
        ("nda", True),
        ("welcome-email", False),
    ):
        html = (out / f"{slug}.html").read_text(encoding="utf-8")
        assert ('class="review noprint"' in html) is expect_banner
    # ...and the banner is hidden when printed, so it never reaches the client PDF.
    assert ".review" in (out / "service-agreement.html").read_text(encoding="utf-8")
