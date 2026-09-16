# Changelog

All notable changes to this project are documented in this file.

## [2026.09] - 2026-09-16

- Maintenance review of `client-onboard-kit` — a Python CLI that turns one YAML brief about a new client into a first-week paperwork pack: service agreement, NDA, scoping questionnaire, kickoff doc and welcome email, as Markdown plus printable HTML.
- Status: packaged as `client-onboard-kit` (Python 3.11+, Jinja2 + PyYAML) with `init` and `build` commands, five Jinja templates under `templates/`, a rendered example pack for a fictional client in `examples/marlowe-and-finch/`, and a pytest suite covering the CLI, options, rendering, validation and repo hygiene. MIT licensed.
- Reviewed September 2026: documentation refreshed, CHANGELOG added and the project versioned as v2026.09.
- Known gaps, as the README already states plainly: the documents are templates and not legal advice, with no jurisdiction certification or rules engine behind `legal.jurisdiction`; English-language and common-law flavoured only; B2B assumptions throughout; no e-signature, invoicing or CRM integration; no Word/Google Docs output; and the Markdown-to-HTML converter is a deliberate subset, not full CommonMark. There is also no CI workflow in the repo.
- The `pyproject.toml` version (0.1.0) was deliberately left untouched: this release tags the repo as v2026.09 and does not cut a new PyPI package version.
- No code, templates or packaging changes were made in this release — documentation only.
