# client-onboard-kit

**One YAML brief about a new client becomes the whole first-week paperwork pack: service agreement, NDA, scoping questionnaire, kickoff doc and welcome email.**

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue) ![License MIT](https://img.shields.io/badge/license-MIT-green) ![Deps: Jinja2 + PyYAML](https://img.shields.io/badge/deps-Jinja2%20%2B%20PyYAML-lightgrey)

Every new client means the same documents rewritten by hand, with details forgotten or pasted from the last client. This renders them from one source of truth.

## What it does

- Writes five documents as Markdown and as self-contained printable HTML, plus an `index.html` that links them.
- Each HTML page has a print stylesheet and a Save as PDF button. There is deliberately no PDF library; your browser prints to PDF.
- Stops with a clear error naming the missing field and template instead of shipping a document with a hole in it.
- Templates live in `templates/` and are plain Markdown with Jinja2 fields, so you can edit the wording.
- A rendered example for a fictional client is in `examples/marlowe-and-finch/`.

## Quickstart

```bash
git clone https://github.com/waseemnasir2k26/client-onboard-kit
cd client-onboard-kit
pip install -e .
client-onboard-kit init                      # writes a commented client.example.yaml
cp client.example.yaml client.yaml           # fill in your details and theirs
client-onboard-kit build client.yaml --out ./pack
```

Open `pack/index.html` and use the Save as PDF button on each document.

## For you if

You are a freelancer or small agency that onboards clients repeatedly and wants consistent paperwork you control.

## Not legal advice

These are templates. They were not drafted by a lawyer, are not certified for any jurisdiction, and make no claim of enforceability. Setting `legal.jurisdiction` changes the words on the page, not whether the document is valid there. Have a qualified lawyer review them before use.

## Status and limits

- Not published to PyPI; install from the clone.
- Output quality depends on the details you put in the YAML.
- See `CHANGELOG.md` for version history.
- Last reviewed October 2026.

## Built by SkynetLabs

Built by [SkynetLabs](https://skynetjoe.com). Questions: info@skynetjoe.com

Need this wired into your business? SkynetLabs builds voice agents, n8n back offices and sites that convert → https://skynetjoe.com
