# Changelog

All notable changes to this project are documented in this file.

## [2026.10] - 2026-10-12

- Public MIT Python 3.11+ CLI (`init` / `build`) that turns one YAML client brief into a first-week pack: agreement, NDA, scoping questionnaire, kickoff doc and welcome email as Markdown plus printable HTML.
- Reviewed October 2026: README external links checked (skynetjoe.com and the Fiverr agency page respond 200); LICENSE already present. No code, template or test changes.
- A 'Work with SkynetLabs' section was added to the README with Fiverr, Upwork and Calendly links; the existing one-line credit at the bottom was left as is.
- `pyproject.toml` version (0.1.0) deliberately untouched: this tag is a repo maintenance release, not a new package version.
- Known gaps (as the README states): templates are not legal advice, English/common-law and B2B assumptions only, no e-signature, invoicing or CRM integration; only one commit of history (initial v1 on 2026-09-01).

## [2026.09] - 2026-09-16

- Maintenance review of `client-onboard-kit` — a Python CLI that turns one YAML brief about a new client into a first-week paperwork pack: service agreement, NDA, scoping questionnaire, kickoff doc and welcome email, as Markdown plus printable HTML.
- Status: packaged as `client-onboard-kit` (Python 3.11+, Jinja2 + PyYAML) with `init` and `build` commands, five Jinja templates under `templates/`, a rendered example pack for a fictional client in `examples/marlowe-and-finch/`, and a pytest suite covering the CLI, options, rendering, validation and repo hygiene. MIT licensed.
- Reviewed September 2026: documentation refreshed, CHANGELOG added and the project versioned as v2026.09.
- Known gaps, as the README already states plainly: the documents are templates and not legal advice, with no jurisdiction certification or rules engine behind `legal.jurisdiction`; English-language and common-law flavoured only; B2B assumptions throughout; no e-signature, invoicing or CRM integration; no Word/Google Docs output; and the Markdown-to-HTML converter is a deliberate subset, not full CommonMark. There is also no CI workflow in the repo.
- The `pyproject.toml` version (0.1.0) was deliberately left untouched: this release tags the repo as v2026.09 and does not cut a new PyPI package version.
- No code, templates or packaging changes were made in this release — documentation only.
