"""Shared fixtures. Every test builds from the shipped example config, mutated in a tmpdir."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_CONFIG = REPO_ROOT / "client.example.yaml"
TEMPLATES_DIR = REPO_ROOT / "templates"


@pytest.fixture(scope="session")
def base_config() -> dict:
    return yaml.safe_load(EXAMPLE_CONFIG.read_text(encoding="utf-8"))


@pytest.fixture
def write_config(tmp_path, base_config):
    """Return a callable: mutate(dict) -> path to a YAML file on disk."""

    def _write(mutate=None, name="client.yaml") -> Path:
        data = copy.deepcopy(base_config)
        if mutate is not None:
            mutate(data)
        path = tmp_path / name
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        return path

    return _write
