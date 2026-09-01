"""A deliberately small Markdown -> HTML converter.

Why not a Markdown library? Because the only dependencies this tool has are Jinja2 and
PyYAML, and the only Markdown that ever reaches this function is Markdown we wrote
ourselves in `templates/`. It supports exactly the subset the shipped templates use:

    ATX headings (#..######)      unordered lists (-, *) incl. `- [ ]` checkboxes
    ordered lists (1.)           tables (GitHub pipe style, with a header row)
    blockquotes (>)              horizontal rules (---)
    paragraphs                   raw HTML comments (passed through, never printed)
    inline: **bold**, *italic*, `code`, [text](url), trailing-two-spaces line break

Anything else is treated as paragraph text. If you extend the templates with new
Markdown, extend this too and add a test.
"""

from __future__ import annotations

import re

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
_ITALIC = re.compile(r"(?<![\*\w])\*(?!\s)([^\*]+?)(?<!\s)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_OL_ITEM = re.compile(r"^(\d+)\.\s+(.*)$")
_UL_ITEM = re.compile(r"^[-*]\s+(.*)$")
_TABLE_SEP = re.compile(r"^\|[\s:|-]+\|$")
_CHECKBOX = re.compile(r"^\[( |x|X)\]\s+")


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(text: str) -> str:
    out = escape(text)
    placeholders: list[str] = []

    def stash(html: str) -> str:
        placeholders.append(html)
        return f"\x00{len(placeholders) - 1}\x00"

    out = _INLINE_CODE.sub(lambda m: stash(f"<code>{m.group(1)}</code>"), out)
    out = _LINK.sub(lambda m: stash(f'<a href="{m.group(2)}">{m.group(1)}</a>'), out)
    out = _BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = _ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", out)
    for i, html in enumerate(placeholders):
        out = out.replace(f"\x00{i}\x00", html)
    return out


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _list_item_html(body: str) -> str:
    match = _CHECKBOX.match(body)
    if match:
        mark = "&#9745;" if match.group(1).lower() == "x" else "&#9744;"
        return f'<li class="task">{mark} {inline(body[match.end():])}</li>'
    return f"<li>{inline(body)}</li>"


def to_html(md: str) -> str:  # noqa: C901 - a line-oriented parser, flat by design
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # HTML comment block: emitted verbatim so it never prints.
        if stripped.startswith("<!--"):
            block = [line]
            while "-->" not in block[-1] and i + 1 < n:
                i += 1
                block.append(lines[i])
            out.append("\n".join(block))
            i += 1
            continue

        if stripped in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue

        heading = _HEADING.match(stripped)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        # Table: header row followed by a separator row.
        if stripped.startswith("|") and i + 1 < n and _TABLE_SEP.match(lines[i + 1].strip()):
            header = _cells(stripped)
            i += 2
            rows: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_cells(lines[i].strip()))
                i += 1
            head = "".join(f"<th>{inline(c)}</th>" for c in header)
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>" for row in rows
            )
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
            continue

        if stripped.startswith(">"):
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>")
            continue

        if _UL_ITEM.match(stripped):
            items: list[str] = []
            while i < n and _UL_ITEM.match(lines[i].strip()):
                items.append(_list_item_html(_UL_ITEM.match(lines[i].strip()).group(1)))
                i += 1
            has_task = any('class="task"' in it for it in items)
            css = ' class="checklist"' if has_task else ""
            out.append(f"<ul{css}>" + "".join(items) + "</ul>")
            continue

        if _OL_ITEM.match(stripped):
            items = []
            while i < n and _OL_ITEM.match(lines[i].strip()):
                items.append(_list_item_html(_OL_ITEM.match(lines[i].strip()).group(2)))
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue

        # Paragraph: consume until a blank line or the start of another block.
        para: list[str] = []
        while i < n and lines[i].strip():
            candidate = lines[i].strip()
            if candidate.startswith(("#", ">", "|", "<!--")) or candidate in ("---", "***", "___"):
                break
            if _UL_ITEM.match(candidate) or _OL_ITEM.match(candidate):
                break
            para.append(lines[i].rstrip("\n"))
            i += 1
        joined = "<br>\n".join(
            inline(p.strip()) for p in para
        ) if any(p.endswith("  ") for p in para) else inline(" ".join(p.strip() for p in para))
        out.append(f"<p>{joined}</p>")

    return "\n".join(out)
