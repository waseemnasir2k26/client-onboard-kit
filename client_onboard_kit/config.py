"""Loading and path-tracking of the YAML brief.

The point of the tracking wrapper: when a template asks for `legal.nda.disclosing_party`
and the config does not have it, we want the error to say exactly that dotted path and
nothing vaguer. Jinja2's own StrictUndefined only knows the leaf attribute name
("'dict object' has no attribute 'disclosing_party'"), which is not good enough when
five different tables have a `name` key.

Tracking is done at access time rather than by static analysis of the template, which
means a field referenced only inside a branch that is not taken (the one-way NDA clause
when you chose a mutual NDA) is correctly NOT required.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Any

import yaml

from .errors import ConfigError, MissingFieldError

# Keys that a template may legitimately omit are still not special-cased here: use the
# `opt()` global inside a template instead. Nothing is silently defaulted.


class TrackedMapping:
    """A mapping that raises MissingFieldError (with a full dotted path) on a miss.

    Deliberately NOT a dict subclass: a dict subclass would let `{{ client.items }}`
    resolve to the builtin `dict.items` method instead of failing loudly.
    """

    __slots__ = ("_data", "_path")

    def __init__(self, data: dict, path: str = ""):
        self._data = {k: wrap(v, _join(path, k)) for k, v in data.items()}
        self._path = path

    # -- attribute / item access are the same thing for templates ------------
    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        return self[name]

    def __getitem__(self, key: str) -> Any:
        try:
            return self._data[key]
        except KeyError:
            raise MissingFieldError(_join(self._path, str(key))) from None

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return f"TrackedMapping({self._path or '<root>'}, keys={sorted(self._data)})"

    def as_dict(self) -> dict:
        return {k: (v.as_dict() if isinstance(v, TrackedMapping) else v) for k, v in self._data.items()}


def _join(path: str, key: str) -> str:
    return f"{path}.{key}" if path else key


def wrap(value: Any, path: str = "") -> Any:
    if isinstance(value, dict):
        return TrackedMapping(value, path)
    if isinstance(value, list):
        return [wrap(v, f"{path}[{i}]") for i, v in enumerate(value)]
    return value


def load_config(path: str | Path) -> TrackedMapping:
    p = Path(path)
    if not p.is_file():
        raise ConfigError(f"Config file not found: {p}")
    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{p} is not valid YAML: {exc}") from None
    if raw is None:
        raise ConfigError(f"{p} is empty.")
    if not isinstance(raw, dict):
        raise ConfigError(f"{p} must contain a YAML mapping at the top level, got {type(raw).__name__}.")
    return TrackedMapping(raw)


# ---------------------------------------------------------------------------
# Formatting helpers driven by the `format:` block of the config.
# ---------------------------------------------------------------------------

_DEFAULT_FORMAT = {
    "date_format": "%d %B %Y",
    "currency_code": "USD",
    "currency_symbol": "$",
    "currency_position": "prefix",
    "decimals": 2,
    "thousands_separator": ",",
}


class Formatter:
    def __init__(self, fmt: dict | None = None):
        merged = dict(_DEFAULT_FORMAT)
        if fmt:
            unknown = set(fmt) - set(_DEFAULT_FORMAT)
            if unknown:
                raise ConfigError(
                    "Unknown key(s) in `format:` block: "
                    + ", ".join(sorted(unknown))
                    + ". Allowed: "
                    + ", ".join(sorted(_DEFAULT_FORMAT))
                )
            merged.update(fmt)
        if merged["currency_position"] not in ("prefix", "suffix"):
            raise ConfigError("format.currency_position must be 'prefix' or 'suffix'.")
        self.spec = merged

    def money(self, amount: Any, decimals: int | None = None) -> str:
        if amount is None or amount == "":
            raise ConfigError("money() was given an empty amount.")
        try:
            value = float(amount)
        except (TypeError, ValueError):
            raise ConfigError(f"money() expected a number, got {amount!r}.") from None
        dp = self.spec["decimals"] if decimals is None else decimals
        body = f"{value:,.{dp}f}"
        if self.spec["thousands_separator"] != ",":
            body = body.replace(",", "\x00").replace("\x00", self.spec["thousands_separator"])
        sym = self.spec["currency_symbol"]
        return f"{sym}{body}" if self.spec["currency_position"] == "prefix" else f"{body}{sym}"

    def date(self, value: Any) -> str:
        if isinstance(value, _dt.datetime):
            value = value.date()
        if isinstance(value, _dt.date):
            return value.strftime(self.spec["date_format"])
        if isinstance(value, str):
            for pattern in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                try:
                    return _dt.datetime.strptime(value, pattern).date().strftime(self.spec["date_format"])
                except ValueError:
                    continue
            return value  # already human-written, e.g. "on signature"
        raise ConfigError(f"date() cannot format {value!r}.")

    @staticmethod
    def pct(value: Any) -> str:
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ConfigError(f"pct() expected a number, got {value!r}.") from None
        return f"{number:g}%"
