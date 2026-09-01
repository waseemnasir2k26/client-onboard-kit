"""Command line interface for client-onboard-kit."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from . import DISCLAIMER, __version__
from .errors import KitError
from .render import DOCUMENTS, bundled_templates_dir, build_pack

_EPILOG = f"""
NOT LEGAL ADVICE
----------------
{DISCLAIMER}

Docs and issues: https://github.com/waseemnasir2k26/client-onboard-kit
"""


def example_config_path() -> Path:
    """The shipped client.example.yaml, whether installed or running from the repo."""
    installed = Path(__file__).resolve().parent / "client.example.yaml"
    if installed.is_file():
        return installed
    source = Path(__file__).resolve().parent.parent / "client.example.yaml"
    if source.is_file():
        return source
    raise KitError("Could not locate the bundled client.example.yaml. Reinstall the package.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="client-onboard-kit",
        description=(
            "Turn one YAML brief about a new client into a complete onboarding pack: "
            "service agreement, NDA, intake questionnaire, kickoff doc and welcome email. "
            "These are TEMPLATES, NOT LEGAL ADVICE - have a lawyer review before use."
        ),
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"client-onboard-kit {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser(
        "init",
        help="write a commented client.example.yaml you can fill in",
        description="Write a commented example config into the current directory.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_init.add_argument(
        "-o", "--out", default="client.example.yaml", help="where to write it (default: %(default)s)"
    )
    p_init.add_argument("-f", "--force", action="store_true", help="overwrite an existing file")

    p_build = sub.add_parser(
        "build",
        help="render the onboarding pack from a config file",
        description="Render every document in the pack from a YAML config.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_build.add_argument("config", help="path to your client YAML config")
    p_build.add_argument("--out", default="./pack", help="output directory (default: %(default)s)")
    p_build.add_argument(
        "--only",
        default=None,
        help="comma-separated document slugs to render (default: all). "
        + "Choices: " + ", ".join(d.slug for d in DOCUMENTS),
    )
    p_build.add_argument(
        "--templates",
        default=None,
        help="use your own templates directory instead of the bundled one",
    )
    p_build.add_argument(
        "--format",
        default="md,html",
        help="output formats, comma separated: md, html (default: %(default)s)",
    )

    sub.add_parser(
        "templates",
        help="show which documents exist and where the templates live",
        description="List the documents this tool can render and the directory they come from.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return parser


def _cmd_init(args: argparse.Namespace) -> int:
    dest = Path(args.out)
    if dest.exists() and not args.force:
        print(f"{dest} already exists. Pass --force to overwrite.", file=sys.stderr)
        return 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(example_config_path(), dest)
    print(f"Wrote {dest}")
    print("Edit it, then run: client-onboard-kit build " + str(dest) + " --out ./pack")
    print()
    print("Reminder: " + DISCLAIMER)
    return 0


def _cmd_build(args: argparse.Namespace) -> int:
    only = [s.strip() for s in args.only.split(",") if s.strip()] if args.only else None
    formats = tuple(s.strip() for s in args.format.split(",") if s.strip())
    bad = [f for f in formats if f not in ("md", "html")]
    if bad:
        print(f"Unknown output format(s): {', '.join(bad)}. Use md and/or html.", file=sys.stderr)
        return 2

    written = build_pack(
        args.config,
        args.out,
        templates_dir=args.templates,
        only=only,
        formats=formats,
    )
    out = Path(args.out)
    print(f"Built {len(written)} file(s) in {out}")
    for path in written:
        print(f"  {path.relative_to(out.parent) if out.parent in path.parents else path}")
    if "html" in formats:
        print()
        print(f"Open {out / 'index.html'} and use the Save as PDF button in each document.")
    print()
    print("Reminder: " + DISCLAIMER)
    return 0


def _cmd_templates(_: argparse.Namespace) -> int:
    print(f"Templates directory: {bundled_templates_dir()}")
    print()
    width = max(len(d.slug) for d in DOCUMENTS)
    for doc in DOCUMENTS:
        flag = " [legal]" if doc.legal else ""
        print(f"  {doc.slug.ljust(width)}  {doc.template}{flag}")
        print(f"  {' ' * width}  {doc.purpose}")
    print()
    print("Copy that directory, edit the Markdown, and pass --templates <dir> to build.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {"init": _cmd_init, "build": _cmd_build, "templates": _cmd_templates}
    try:
        return handlers[args.command](args)
    except KitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
