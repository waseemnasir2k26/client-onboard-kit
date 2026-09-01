"""Guards on the repository itself.

This project is a lead magnet published in public. Two things must stay true: no real
person, client or domain leaks into it, and the shipped templates contain no lorem or
half-written clause.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = sorted((REPO_ROOT / "templates").glob("*.md"))
EXAMPLE_PACK = sorted((REPO_ROOT / "examples").rglob("*.md"))

DOMAIN = re.compile(r"(?:https?://|@)([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
# Anything that looks like a real destination has no business in a fictional example.
ALLOWED_SUFFIXES = (".example",)

BANNED = ("lorem ipsum", "todo:", "tbd", "xxx", "fixme", "placeholder text", "[insert ")


def _client_facing_files() -> list[Path]:
    return TEMPLATES + EXAMPLE_PACK + [REPO_ROOT / "client.example.yaml"]


def test_every_template_exists_and_is_substantial():
    assert {p.name for p in TEMPLATES} == {
        "service-agreement.md",
        "nda.md",
        "intake-questionnaire.md",
        "kickoff.md",
        "welcome-email.md",
    }
    for path in TEMPLATES:
        assert len(path.read_text(encoding="utf-8")) > 1000, f"{path.name} looks like a stub"


@pytest.mark.parametrize("path", _client_facing_files(), ids=lambda p: p.name)
def test_only_reserved_example_domains_appear(path):
    for host in DOMAIN.findall(path.read_text(encoding="utf-8")):
        assert host.endswith(ALLOWED_SUFFIXES), (
            f"{path.name} references '{host}', which is not a reserved .example domain"
        )


@pytest.mark.parametrize("path", _client_facing_files(), ids=lambda p: p.name)
def test_no_placeholder_or_unfinished_copy(path):
    text = path.read_text(encoding="utf-8").lower()
    for banned in BANNED:
        assert banned not in text, f"{path.name} contains '{banned}'"


def test_the_example_pack_is_committed_and_complete():
    pack = REPO_ROOT / "examples" / "marlowe-and-finch"
    assert pack.is_dir(), "examples/marlowe-and-finch is missing"
    names = {p.name for p in pack.iterdir()}
    for slug in ("service-agreement", "nda", "intake-questionnaire", "kickoff", "welcome-email"):
        assert f"{slug}.md" in names
        assert f"{slug}.html" in names
    assert "index.html" in names
