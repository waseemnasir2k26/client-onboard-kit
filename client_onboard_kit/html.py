"""Wrap rendered Markdown in a self-contained, printable HTML document.

There is no PDF binary anywhere in this project on purpose. Every OS ships a browser
with a "Save as PDF" print target that renders these documents correctly, and adding
WeasyPrint/wkhtmltopdf would trade one command for a system-library install that breaks
differently on every machine. Open the HTML, press the button, choose "Save as PDF".
"""

from __future__ import annotations

from . import DISCLAIMER
from .markdown import to_html

_CSS = """
:root{--ink:#1a1a1a;--muted:#5b5b5b;--rule:#d9d4c7;--paper:#ffffff;--wash:#f7f5ef;--flag:#b4471f}
*{box-sizing:border-box}
body{margin:0;background:var(--wash);color:var(--ink);
     font:16px/1.65 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
.sheet{max-width:46rem;margin:2.5rem auto;background:var(--paper);padding:3.5rem 3.5rem 4rem;
       border:1px solid var(--rule);box-shadow:0 1px 3px rgba(0,0,0,.06)}
h1{font-size:1.75rem;line-height:1.25;margin:0 0 .25rem}
h2{font-size:1.15rem;margin:2.2rem 0 .6rem;padding-bottom:.3rem;border-bottom:1px solid var(--rule)}
h3{font-size:1rem;margin:1.5rem 0 .4rem}
p{margin:.7rem 0}
ul,ol{margin:.7rem 0;padding-left:1.4rem}
li{margin:.3rem 0}
ul.checklist{list-style:none;padding-left:.2rem}
ul.checklist li{margin:.4rem 0}
table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.94rem}
th,td{border:1px solid var(--rule);padding:.5rem .65rem;text-align:left;vertical-align:top}
th{background:var(--wash);font-weight:600}
blockquote{margin:1rem 0;padding:.6rem 1rem;border-left:3px solid var(--rule);
           background:var(--wash);color:var(--muted)}
code{font:.9em/1.4 "IBM Plex Mono",ui-monospace,Consolas,monospace;background:var(--wash);
     padding:.1em .35em;border-radius:3px}
hr{border:0;border-top:1px solid var(--rule);margin:2rem 0}
a{color:#8a4a1f}
.toolbar{position:sticky;top:0;z-index:5;display:flex;gap:.75rem;align-items:center;
         justify-content:space-between;background:var(--ink);color:#fff;padding:.6rem 1rem;
         font:600 13px/1.4 ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif}
.toolbar button{font:inherit;cursor:pointer;border:0;border-radius:4px;padding:.45rem .9rem;
                background:var(--flag);color:#fff}
.review{max-width:46rem;margin:1.25rem auto -1rem;padding:.85rem 1.1rem;border:2px solid var(--flag);
        background:#fff4ef;color:#6b2a10;border-radius:4px;
        font:500 13px/1.5 ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif}
.review strong{display:block;letter-spacing:.06em;text-transform:uppercase;font-size:11px;margin-bottom:.3rem}
@media print{
  @page{margin:18mm 16mm}
  body{background:#fff;font-size:11.5pt}
  .toolbar,.review,.noprint{display:none !important}
  .sheet{max-width:none;margin:0;padding:0;border:0;box-shadow:none}
  h2,h3{page-break-after:avoid}
  table,blockquote,li{page-break-inside:avoid}
  a{color:inherit;text-decoration:none}
}
"""

_TOOLBAR = (
    '<div class="toolbar noprint"><span>{label}</span>'
    '<button type="button" onclick="window.print()">Save as PDF / Print</button></div>'
)

_REVIEW = (
    '<div class="review noprint"><strong>Draft &mdash; review before sending</strong>{body}</div>'
)


def document(title: str, markdown_body: str, *, legal: bool = False, label: str = "") -> str:
    body = to_html(markdown_body)
    banner = _REVIEW.format(body=DISCLAIMER) if legal else ""
    toolbar = _TOOLBAR.format(label=label or title)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f"<title>{title}</title>\n<style>{_CSS}</style>\n</head>\n<body>\n"
        f"{toolbar}\n{banner}\n<main class=\"sheet\">\n{body}\n</main>\n</body>\n</html>\n"
    )


def index(title: str, entries: list[tuple[str, str, str]]) -> str:
    """entries: (filename, human title, one-line 'what this prevents')."""
    rows = "\n".join(
        f'<tr><td><a href="{href}">{name}</a></td><td>{blurb}</td></tr>' for href, name, blurb in entries
    )
    body = (
        f"<h1>{title}</h1>"
        "<p>Every document in this pack, ready to read on screen or print to PDF.</p>"
        "<table><thead><tr><th>Document</th><th>What it is for</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        f"<hr><p><em>{DISCLAIMER}</em></p>"
    )
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f"<title>{title}</title>\n<style>{_CSS}</style>\n</head>\n<body>\n"
        f'<main class="sheet">\n{body}\n</main>\n</body>\n</html>\n'
    )
