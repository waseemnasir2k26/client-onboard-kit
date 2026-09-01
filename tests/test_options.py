"""Config-driven switches: NDA style, currency, dates, jurisdiction, optional clauses."""

from __future__ import annotations

import pytest

from client_onboard_kit.errors import MissingFieldError
from client_onboard_kit.render import build_pack


def _read(out, slug):
    return (out / f"{slug}.md").read_text(encoding="utf-8")


def test_nda_defaults_to_mutual(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out, only=["nda"], formats=("md",))
    nda = _read(out, "nda")
    assert "# Mutual Non-Disclosure Agreement" in nda
    assert "each party may act as **Disclosing Party**" in nda
    assert "Obligations run both ways" in nda


def test_nda_one_way_toggle_changes_the_document(tmp_path, write_config):
    def mutate(d):
        d["legal"]["nda"]["type"] = "one_way"
        d["legal"]["nda"]["disclosing_party"] = d["client"]["legal_name"]

    out = tmp_path / "pack"
    build_pack(write_config(mutate), out, only=["nda"], formats=("md",))
    nda = _read(out, "nda")
    assert "# One-Way Non-Disclosure Agreement" in nda
    assert "Obligations run one way only." in nda
    assert "Marlowe & Finch Roasters Ltd" in nda
    assert "Obligations run both ways" not in nda


def test_one_way_nda_without_a_disclosing_party_fails_precisely(tmp_path, write_config):
    config = write_config(lambda d: d["legal"]["nda"].__setitem__("type", "one_way"))
    with pytest.raises(MissingFieldError) as excinfo:
        build_pack(config, tmp_path / "pack", only=["nda"])
    message = str(excinfo.value)
    assert "legal.nda.disclosing_party" in message
    assert "nda.md" in message


def test_nda_can_be_dropped_from_the_pack(tmp_path, write_config):
    config = write_config(lambda d: d["legal"]["nda"].__setitem__("include_in_pack", False))
    out = tmp_path / "pack"
    build_pack(config, out, formats=("md",))
    assert not (out / "nda.md").exists()
    # ...and the service agreement stops cross-referencing a document that is not there.
    assert "A separate Non-Disclosure Agreement" not in _read(out, "service-agreement")


def test_currency_symbol_and_position_switch(tmp_path, write_config):
    def mutate(d):
        d["format"]["currency_code"] = "USD"
        d["format"]["currency_symbol"] = "$"
        d["format"]["currency_position"] = "prefix"

    out = tmp_path / "pack"
    build_pack(write_config(mutate), out, only=["service-agreement"], formats=("md",))
    agreement = _read(out, "service-agreement")
    assert "$18,000.00" in agreement
    assert "(USD)" in agreement
    assert "£" not in agreement


def test_suffix_currency_position(tmp_path, write_config):
    def mutate(d):
        d["format"]["currency_code"] = "SEK"
        d["format"]["currency_symbol"] = " kr"
        d["format"]["currency_position"] = "suffix"

    out = tmp_path / "pack"
    build_pack(write_config(mutate), out, only=["service-agreement"], formats=("md",))
    assert "18,000.00 kr" in _read(out, "service-agreement")


def test_date_format_switches(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out, only=["service-agreement"], formats=("md",))
    assert "14 September 2026" in _read(out, "service-agreement")

    us = tmp_path / "us"
    build_pack(
        write_config(lambda d: d["format"].__setitem__("date_format", "%B %d, %Y"), name="us.yaml"),
        us,
        only=["service-agreement"],
        formats=("md",),
    )
    assert "September 14, 2026" in _read(us, "service-agreement")


def test_free_text_dates_pass_through_untouched(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out, only=["service-agreement"], formats=("md",))
    assert "| Deposit | on signature |" in _read(out, "service-agreement")


def test_jurisdiction_switches(tmp_path, write_config):
    def mutate(d):
        d["legal"]["jurisdiction"] = "the State of Delaware, USA"
        d["legal"]["courts"] = "the state and federal courts located in Delaware"

    out = tmp_path / "pack"
    build_pack(write_config(mutate), out, formats=("md",))
    for slug in ("service-agreement", "nda"):
        text = _read(out, slug)
        assert "the State of Delaware, USA" in text
        assert "England and Wales" not in text


def test_ip_assignment_toggle_swaps_the_clause(tmp_path, write_config):
    out = tmp_path / "pack"
    build_pack(write_config(), out, only=["service-agreement"], formats=("md",))
    assert "the Provider assigns to the Client" in _read(out, "service-agreement")

    off = tmp_path / "off"
    config = write_config(
        lambda d: d["legal"].__setitem__("ip_assignment_on_final_payment", False), name="off.yaml"
    )
    build_pack(config, off, only=["service-agreement"], formats=("md",))
    text = _read(off, "service-agreement")
    assert "The Provider retains ownership" in text
    assert "the Provider assigns to the Client" not in text


def test_optional_clauses_disappear_when_switched_off(tmp_path, write_config):
    def mutate(d):
        d["legal"]["portfolio_rights"] = False
        d["commercial"].pop("kill_fee_percent")
        d["engagement"].pop("assumptions")

    out = tmp_path / "pack"
    build_pack(write_config(mutate), out, only=["service-agreement"], formats=("md",))
    text = _read(out, "service-agreement")
    assert "portfolio and marketing" not in text
    assert "cancellation fee" not in text
    assert "priced on the following assumptions" not in text


def test_revision_singular_and_plural(tmp_path, write_config):
    one = tmp_path / "one"
    build_pack(
        write_config(lambda d: d["engagement"].__setitem__("revision_rounds", 1), name="one.yaml"),
        one,
        only=["service-agreement"],
        formats=("md",),
    )
    assert "**1 round** of consolidated revisions" in _read(one, "service-agreement")

    many = tmp_path / "many"
    build_pack(write_config(name="many.yaml"), many, only=["service-agreement"], formats=("md",))
    assert "**2 rounds** of consolidated revisions" in _read(many, "service-agreement")
