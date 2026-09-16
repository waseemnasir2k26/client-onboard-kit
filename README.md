# client-onboard-kit

One YAML brief about a new client turns into the whole first-week paperwork pack: service agreement, NDA, scoping questionnaire, kickoff doc and welcome email.

## Status

Last reviewed: September 2026 · release v2026.09


```console
$ client-onboard-kit init
Wrote client.example.yaml
Edit it, then run: client-onboard-kit build client.example.yaml --out ./pack

$ client-onboard-kit build client.yaml --out ./pack
Built 11 file(s) in pack
  pack\service-agreement.md
  pack\service-agreement.html
  pack\nda.md
  pack\nda.html
  pack\intake-questionnaire.md
  pack\intake-questionnaire.html
  pack\kickoff.md
  pack\kickoff.html
  pack\welcome-email.md
  pack\welcome-email.html
  pack\index.html

Open pack\index.html and use the Save as PDF button in each document.
```

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License MIT](https://img.shields.io/badge/license-MIT-green)
![Dependencies: Jinja2 + PyYAML](https://img.shields.io/badge/deps-Jinja2%20%2B%20PyYAML-lightgrey)
![Output: Markdown + printable HTML](https://img.shields.io/badge/output-Markdown%20%2B%20HTML-orange)

A real example pack, rendered for a completely fictional client, is committed at
[`examples/marlowe-and-finch/`](examples/marlowe-and-finch/).

## Quick start

```bash
pip install client-onboard-kit          # or: pip install -e . from a clone
client-onboard-kit init                 # writes a commented client.example.yaml
cp client.example.yaml client.yaml      # fill in your details and theirs
client-onboard-kit build client.yaml --out ./pack
open ./pack/index.html                  # then use the Save as PDF button
```

If a template needs a field your YAML does not have, the build stops and tells you
which field and which template, rather than shipping a document with a hole in it:

```console
$ client-onboard-kit build client.yaml --out ./pack
error: Missing required field 'legal.jurisdiction' in your config (needed by template
'service-agreement.md'). Run `client-onboard-kit init` to see a fully-populated example.
```

## What you get

| Document | What it is | What it prevents |
| --- | --- | --- |
| `service-agreement.md` | Scope, deliverables, timeline, fees, payment terms, late fees, revisions, change requests, IP assignment on final payment, confidentiality, termination, liability cap, governing law. | Scope creep with no price attached, and the argument about who owns the work. |
| `nda.md` | Mutual by default, one-way with a toggle. Purpose-limited, with carve-outs and a term. | Awkwardness about sharing real numbers and credentials before anything is signed. |
| `intake-questionnaire.md` | The scoping questions: decision-maker, success criteria, hard deadlines, out-of-scope confirmation, brand assets, access and credentials checklist, data handling. | Week-three change requests caused by a question nobody asked in week one. |
| `kickoff.md` | Agreed scope, milestone schedule, who approves what, channels and response times, and everything the client owes you with a date on it. | Unclear approvals, feedback arriving from four people at once, and credential chaos. |
| `welcome-email.md` | Short, warm, sets expectations, lists the next three actions. | The enthusiastic silence after signature where nothing actually happens. |

Every document is written to `./pack` twice: as Markdown, and as a self-contained HTML
page with a print stylesheet and a "Save as PDF" button. `index.html` links them all.

**There is no PDF library in this project, on purpose.** Every machine already has a
browser that prints to PDF correctly. Adding WeasyPrint or wkhtmltopdf would trade one
command for a system-library install that breaks differently on every OS, and would
render worse. Open the HTML, press the button, choose "Save as PDF".

## Configuration

`client-onboard-kit init` writes a fully-commented, fully-populated example. The blocks:

| Block | Holds |
| --- | --- |
| `format` | `date_format` (Python strftime), `currency_code`, `currency_symbol`, `currency_position` (`prefix` or `suffix`), `decimals`, `thousands_separator`. |
| `provider` | You: `legal_name`, `trading_name`, `company_number`, `contact_name`, `contact_title`, `email`, `phone`, `address`, `website`. |
| `client` | Them: `legal_name`, `short_name`, `contact_name`, `contact_title`, `email`, `address`, `website`. |
| `engagement` | `title`, `summary`, `start_date`, `end_date`, `revision_rounds`, and the lists `deliverables`, `milestones`, `out_of_scope`, `assumptions`. |
| `commercial` | `total_fee`, `deposit_percent`, `payment_terms_days`, `late_fee_percent_per_month`, `change_request_rate`, `change_request_unit`, `change_request_minimum_hours`, `expenses_policy`, `kill_fee_percent`. |
| `legal` | `jurisdiction`, `courts`, `termination_notice_days`, `confidentiality_term_years`, `ip_assignment_on_final_payment`, `liability_cap`, `portfolio_rights`, and the `nda` sub-block. |
| `legal.nda` | `include_in_pack`, `type` (`mutual` or `one_way`), `disclosing_party` (required only when `one_way`), `term_years`, `purpose`. |
| `comms` | `primary_channel`, `secondary_channel`, `response_time_hours`, `working_hours`, `timezone`, `weekly_checkin`, `approver_name`, `approver_title`, `approval_window_days`, `escalation_contact`. |
| `onboarding` | `questionnaire_due`, `client_owes`, `access_checklist`, `brand_assets`, `success_criteria`, `hard_deadlines`. |
| `welcome` | `signature_tool`, `next_actions`, `kickoff_call`. |

Three rules govern the file:

1. **Nothing is silently blanked.** If a template reaches for a field that is not there,
   the build fails and names the field and the template.
2. **A branch you did not take costs you nothing.** `legal.nda.disclosing_party` is only
   required when `legal.nda.type` is `one_way`, because validation happens as the
   document renders, not by scanning the template for every name it mentions.
3. **Dates are flexible.** A YAML date (`2026-09-14`) is reformatted with your
   `date_format`; free text (`on signature`) passes through untouched.

Switching jurisdiction, currency and date convention is a four-line edit:

```yaml
format:
  date_format: "%B %d, %Y"
  currency_code: USD
  currency_symbol: "$"
legal:
  jurisdiction: the State of Delaware, USA
  courts: the state and federal courts located in Delaware
```

Useful flags:

```bash
client-onboard-kit build client.yaml --out ./pack --only welcome-email,kickoff
client-onboard-kit build client.yaml --out ./pack --format md
client-onboard-kit build client.yaml --out ./pack --templates ./my-templates
client-onboard-kit templates            # what exists, and where it lives
```

## Customising the templates

The templates are data, not code. They live in [`templates/`](templates/) as plain
Markdown with Jinja2 placeholders:

```markdown
Invoices are payable within **{{ commercial.payment_terms_days }} days**.

{% if legal.portfolio_rights %}
The Provider may show the delivered work in its portfolio.
{% endif %}

{% for item in engagement.out_of_scope %}
- {{ item }}
{% endfor %}
```

Alongside the standard Jinja2 syntax there are these helpers:

| Helper | Does |
| --- | --- |
| `{{ amount \| money }}` | Formats using your `format` block: `£18,000.00`. |
| `{{ value \| date }}` | Formats a date, or passes free text through. |
| `{{ number \| pct }}` | `2` becomes `2%`. |
| `{{ text \| block }}` | Turns a multi-line YAML block (an address) into Markdown line breaks. |
| `{{ text \| sentence }}` | Upper-cases the first character only. |
| `{% if has('provider.phone') %}` | True when that dotted path exists and is not empty. |
| `{{ opt('client.website', 'n/a') }}` | Reads a dotted path with a fallback, for genuinely optional fields. |

To customise: copy `templates/` somewhere, edit, and pass `--templates ./my-templates`.
Adding a new document to the pack means adding a `Document(...)` entry in
`client_onboard_kit/render.py` next to the five that are already there.

The HTML converter supports the Markdown subset the shipped templates use: headings,
paragraphs, bold, italic, inline code, links, ordered and unordered lists, `- [ ]`
checkboxes, pipe tables, blockquotes, horizontal rules and HTML comments. If you extend
the templates past that, extend `client_onboard_kit/markdown.py` and add a test.

## Not legal advice

**These are templates. They are not legal advice, and they were not drafted by a lawyer.**

- Nobody here is your solicitor, attorney, or counsel, and using this tool does not
  create any professional relationship.
- The documents are not certified for any jurisdiction. Setting `legal.jurisdiction` to
  a place changes the words on the page; it does not make the document compliant there.
- No claim is made about enforceability, and no claim is made about compliance with any
  statute, regulation or professional code, anywhere.
- Some of these clauses will be void, unenforceable, or simply wrong in your
  jurisdiction, particularly the liability cap, the IP assignment and the late-payment
  interest rate, which are the three most commonly regulated terms.
- Consumer contracts, employment-adjacent arrangements, regulated industries and
  cross-border work all carry rules this tool knows nothing about.

**Have a qualified lawyer in the relevant jurisdiction review anything you intend to
sign or send.** A one-hour review of a document that is already 90% written is a great
deal cheaper than the same lawyer drafting from nothing, and that is the whole point of
this tool: it gets you to the review, not past it.

Every rendered document carries an HTML comment at the top saying the same thing. The
comment does not appear in the printed or PDF output, and the legal documents also show
a screen-only review banner in the HTML that is hidden when printed.

## Limitations

Being blunt about what this is not:

- **English-language only.** No translations, no localisation of legal terminology.
- **Common-law flavoured.** The drafting style and clause structure follow English and
  US commercial practice. Civil-law jurisdictions structure these documents differently.
- **No jurisdiction certification.** `legal.jurisdiction` is a string that gets printed.
  There is no rules engine behind it, and no per-country clause library.
- **Business-to-business assumptions throughout.** Consumer-facing engagements carry
  statutory protections that none of these documents account for.
- **No e-signature integration.** The pack names your signing tool in the welcome email
  and stops there. Take the PDF to whichever service you already use.
- **No invoicing, no CRM, no reminders.** This produces documents. That is all it does.
- **No Word or Google Docs output.** Markdown and printable HTML only. If a client
  insists on `.docx`, paste the Markdown into their editor of choice.
- **The Markdown-to-HTML converter is a subset**, not a full CommonMark implementation.
  It handles what the shipped templates use and nothing more, by design.

## Contributing

Issues and pull requests are welcome, especially:

- Clause improvements from people who have actually had these documents tested.
- Additional template packs (retainer agreement, statement of work, offboarding).
- Jurisdiction notes, clearly marked as notes rather than as certification.

Please do not send pull requests that claim a document is enforceable, compliant, or
lawyer-approved. That claim will not be merged.

Development:

```bash
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

The test suite covers rendering of every template, the missing-variable failure, the
guarantee that an unrendered placeholder can never reach the output, the mutual and
one-way NDA toggle, currency, date and jurisdiction switching, the output file layout,
and a repository hygiene check that no real person or domain leaks into the examples.

---

Built by SkynetLabs (Waseem Nasir) - we onboard and automate client delivery for
agencies. https://skynetjoe.com - hire on Fiverr https://fiverr.com/agencies/skynetjoellc

## License

MIT. See [LICENSE](LICENSE). Copyright (c) 2026 Waseem Nasir / SkynetLabs.
