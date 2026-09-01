# Kickoff Document

**{{ engagement.title }}**  
{{ provider.legal_name }} and {{ client.legal_name }}  
Issued {{ today | date }}

This document is the operating manual for the engagement. The Service Agreement says what happens if things go wrong; this says how we work so that they do not. If something here conflicts with the Service Agreement, the Service Agreement wins.

---

## 1. Agreed scope

{{ engagement.summary }}

| Deliverable | What it includes | Target date |
| --- | --- | --- |
{% for d in engagement.deliverables %}
| {{ d.name }} | {{ d.description }} | {{ d.due | date }} |
{% endfor %}

Not included, and quoted separately if wanted:

{% for item in engagement.out_of_scope %}
- {{ item }}
{% endfor %}

## 2. Milestones and money

| Milestone | Date | Amount | Note |
| --- | --- | --- | --- |
{% for m in engagement.milestones %}
| {{ m.name }} | {{ m.date | date }} | {{ m.amount | money }} | {{ m.description }} |
{% endfor %}

Total: **{{ commercial.total_fee | money }}** ({{ format.currency_code }}). Invoices are due within {{ commercial.payment_terms_days }} days; after that, interest of {{ commercial.late_fee_percent_per_month | pct }} per month applies and work may be paused.

Out-of-scope work is quoted before it starts, at {{ commercial.change_request_rate | money }} per {{ commercial.change_request_unit }}. Nothing is ever added to an invoice as a surprise.

## 3. Who approves what

| | Name | Role |
| --- | --- | --- |
| Approves deliverables | {{ comms.approver_name }} | {{ comms.approver_title }} |
| Day-to-day contact, client side | {{ client.contact_name }} | {{ client.contact_title }} |
| Day-to-day contact, our side | {{ provider.contact_name }} | {{ provider.contact_title }} |
| Escalation | {{ comms.escalation_contact }} | |

Approval means a written "yes" from {{ comms.approver_name }} in the project channel or by email. A verbal "looks good" on a call is not approval, and neither is silence.

Approvals are due within **{{ comms.approval_window_days }} working days**. Beyond that, the schedule moves by the length of the delay.

## 4. How we communicate

| | |
| --- | --- |
| Primary channel | {{ comms.primary_channel | sentence }} |
| For anything formal | {{ comms.secondary_channel | sentence }} |
| Our response time | Within {{ comms.response_time_hours }} hours during working hours |
| Working hours | {{ comms.working_hours }} ({{ comms.timezone }}) |
| Standing check-in | {{ comms.weekly_checkin }} |

Two rules that save everyone time:

- Feedback comes in one consolidated batch per round, from one person, in the project channel. Scattered feedback from four people is how projects lose a fortnight.
- Anything that changes scope, price or a date goes in writing. If it was decided on a call, one of us writes it down afterwards.

## 5. What you owe us, and by when

The dates below are what the schedule is built on. If one slips, tell us early; we can usually re-sequence, but not retroactively.

| Item | Owner | Due |
| --- | --- | --- |
{% for item in onboarding.client_owes %}
| {{ item.item }} | {{ item.owner }} | {{ item.due | date }} |
{% endfor %}

### Access and credentials

Use delegated access with a named account wherever the platform supports it. Do not send passwords in chat or email; use a password manager share or a one-time secret link.

{% for item in onboarding.access_checklist %}
- [ ] {{ item }}
{% endfor %}

### Brand and content assets

{% for item in onboarding.brand_assets %}
- [ ] {{ item }}
{% endfor %}

## 6. What "done" looks like

{% for item in onboarding.success_criteria %}
- {{ item }}
{% endfor %}

### Hard deadlines

{% for d in onboarding.hard_deadlines %}
- **{{ d.name }}** - {{ d.date | date }}. {{ d.why }}
{% endfor %}

## 7. Revisions

{{ engagement.revision_rounds }} consolidated round{{ 's' if engagement.revision_rounds != 1 else '' }} of revisions per deliverable are included. A round is one batch of feedback, sent together, from {{ comms.approver_name }}. Further rounds are change requests.

## 8. If something goes wrong

Raise it in the project channel the day you notice it. If it is not resolved within two working days, escalate to {{ comms.escalation_contact }} on your side and to {{ provider.contact_name }} on ours. Nothing here is improved by waiting a week.

---

Questions on any of this: {{ provider.contact_name }}, {{ provider.email }}{% if has('provider.phone') %}, {{ provider.phone }}{% endif %}.
