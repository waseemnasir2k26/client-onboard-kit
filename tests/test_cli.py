"""The CLI surface: init, build, templates, --help, and the disclaimer in all of them."""

from __future__ import annotations

import pytest
import yaml

from client_onboard_kit import DISCLAIMER
from client_onboard_kit.cli import build_parser, main


def test_help_carries_the_not_legal_advice_warning(capsys):
    with pytest.raises(SystemExit):
        build_parser().parse_args(["--help"])
    out = capsys.readouterr().out
    assert "NOT LEGAL ADVICE" in out
    assert "have a lawyer review" in out.lower()


def test_build_help_carries_it_too(capsys):
    with pytest.raises(SystemExit):
        build_parser().parse_args(["build", "--help"])
    assert "NOT LEGAL ADVICE" in capsys.readouterr().out


def test_init_writes_a_loadable_commented_example(tmp_path, capsys):
    dest = tmp_path / "client.example.yaml"
    assert main(["init", "-o", str(dest)]) == 0
    text = dest.read_text(encoding="utf-8")
    assert text.lstrip().startswith("#")
    assert "NOT LEGAL ADVICE" in text
    data = yaml.safe_load(text)
    assert {"provider", "client", "engagement", "commercial", "legal"} <= set(data)
    assert DISCLAIMER in capsys.readouterr().out


def test_init_refuses_to_clobber_without_force(tmp_path, capsys):
    dest = tmp_path / "client.example.yaml"
    dest.write_text("mine\n", encoding="utf-8")
    assert main(["init", "-o", str(dest)]) == 1
    assert dest.read_text(encoding="utf-8") == "mine\n"
    assert main(["init", "-o", str(dest), "--force"]) == 0
    assert dest.read_text(encoding="utf-8") != "mine\n"


def test_build_end_to_end_through_the_cli(tmp_path, write_config, capsys):
    out = tmp_path / "pack"
    assert main(["build", str(write_config()), "--out", str(out)]) == 0
    printed = capsys.readouterr().out
    assert "Built 11 file(s)" in printed
    assert DISCLAIMER in printed
    assert (out / "index.html").is_file()


def test_build_reports_a_missing_field_without_a_traceback(tmp_path, write_config, capsys):
    config = write_config(lambda d: d["commercial"].pop("total_fee"))
    assert main(["build", str(config), "--out", str(tmp_path / "pack")]) == 1
    err = capsys.readouterr().err
    assert err.startswith("error: ")
    assert "commercial.total_fee" in err
    assert "service-agreement.md" in err


def test_build_rejects_an_unknown_format(tmp_path, write_config, capsys):
    assert main(["build", str(write_config()), "--out", str(tmp_path / "p"), "--format", "docx"]) == 2
    assert "docx" in capsys.readouterr().err


def test_templates_command_lists_every_document(capsys):
    assert main(["templates"]) == 0
    out = capsys.readouterr().out
    for slug in ("service-agreement", "nda", "intake-questionnaire", "kickoff", "welcome-email"):
        assert slug in out


def test_custom_templates_directory_is_used(tmp_path, write_config, capsys):
    from client_onboard_kit.render import DOCUMENTS

    custom = tmp_path / "mine"
    custom.mkdir()
    for doc in DOCUMENTS:
        custom.joinpath(doc.template).write_text(
            "# Custom\n\nFor {{ client.legal_name }}.\n", encoding="utf-8"
        )
    out = tmp_path / "pack"
    assert main(
        ["build", str(write_config()), "--out", str(out), "--templates", str(custom), "--format", "md"]
    ) == 0
    assert "For Marlowe & Finch Roasters Ltd." in (out / "kickoff.md").read_text(encoding="utf-8")
