# Service Agreement

**{{ engagement.title }}**

This Agreement is made on {{ today | date }} between:

**The Provider:** {{ provider.legal_name }}{% if has('provider.trading_name') %}, trading as {{ provider.trading_name }}{% endif %}{% if has('provider.company_number') %} (company number {{ provider.company_number }}){% endif %}  
{{ provider.address | block }}

**The Client:** {{ client.legal_name }}  
{{ client.address | block }}

Together, "the parties".

---

## 1. What is being built

{{ engagement.summary }}

The Provider will deliver the following:

| Deliverable | What it includes | Target date |
| --- | --- | --- |
{% for d in engagement.deliverables %}
| {{ d.name }} | {{ d.description }} | {{ d.due | date }} |
{% endfor %}

Work starts on {{ engagement.start_date | date }}{% if has('engagement.end_date') %} and is scheduled to complete by {{ engagement.end_date | date }}{% endif %}. Dates assume the Client meets its own obligations under clause 5.

## 2. What is not being built

The following sit outside this Agreement. They are not refusals; they are simply not covered by the fee, and each would be quoted separately.

{% for item in engagement.out_of_scope %}
- {{ item }}
{% endfor %}
{% if has('engagement.assumptions') %}

This Agreement is priced on the following assumptions. If one turns out to be wrong, clause 6 applies.

{% for item in engagement.assumptions %}
- {{ item }}
{% endfor %}
{% endif %}

## 3. Fees

The total fee for the work in clause 1 is **{{ commercial.total_fee | money }}** ({{ format.currency_code }}), payable as follows:

| Milestone | When | Amount |
| --- | --- | --- |
{% for m in engagement.milestones %}
| {{ m.name }} | {{ m.date | date }} | {{ m.amount | money }} |
{% endfor %}

A deposit of {{ commercial.deposit_percent | pct }} of the total fee is due before work begins. The Provider is not obliged to start, or to continue, before a due payment has cleared.

{{ commercial.expenses_policy }}

## 4. Payment terms

Invoices are payable within **{{ commercial.payment_terms_days }} days** of the invoice date.

Sums unpaid after that date carry interest at {{ commercial.late_fee_percent_per_month | pct }} per month, or part month, on the outstanding balance, from the due date until payment is received.

If an invoice is more than {{ commercial.payment_terms_days }} days overdue, the Provider may suspend work on written notice. Suspension does not move the delivery dates earlier; the timeline shifts by at least the length of the suspension.

## 5. What the Client provides

The Client will provide, in a usable form and by the dates agreed in the Kickoff Document:

- Brand assets, content, product data and any third-party credentials the work depends on.
- A single named person with authority to approve work. For this engagement that person is {{ comms.approver_name }}, {{ comms.approver_title }}.
- Decisions and approvals within {{ comms.approval_window_days }} working days of being asked.

Where the Client is late, the Provider's dates move by at least the length of the delay. Repeated delay is a ground for termination under clause 10.

## 6. Revisions and change requests

The fee includes **{{ engagement.revision_rounds }} round{{ 's' if engagement.revision_rounds != 1 else '' }}** of consolidated revisions per deliverable. A round is one set of feedback, gathered and sent together. Feedback that arrives in pieces after a round has been actioned counts as a new round.

Anything that changes agreed scope, including work listed in clause 2, is a change request. Change requests are quoted in writing before any work on them begins, and are charged at {{ commercial.change_request_rate | money }} per {{ commercial.change_request_unit }}{% if has('commercial.change_request_minimum_hours') %}, with a minimum of {{ commercial.change_request_minimum_hours }} {{ commercial.change_request_unit }}s per request{% endif %}. No change request is started before the quote is approved in writing.

## 7. Intellectual property

{% if legal.ip_assignment_on_final_payment %}
On receipt of the final payment in full, the Provider assigns to the Client all intellectual property rights it holds in the deliverables produced specifically for the Client under this Agreement. Until final payment is received, the Client holds a licence to use the deliverables for review and internal evaluation only, and no rights transfer.
{% else %}
The Provider retains ownership of the intellectual property in the deliverables and grants the Client a perpetual, non-exclusive licence to use them for the purpose described in clause 1.
{% endif %}

The Provider keeps ownership of its own pre-existing tools, libraries, code and methods, and grants the Client a perpetual, non-exclusive, royalty-free licence to use them to the extent they are embedded in the deliverables.

Third-party components (open-source libraries, fonts, stock assets, hosted services) remain under their own licences, and those licences pass to the Client unchanged.
{% if legal.portfolio_rights %}

The Provider may describe the engagement and show the delivered work in its portfolio and marketing, using material that is already public. The Client may withdraw that permission in writing at any time.
{% endif %}

## 8. Confidentiality

Each party will keep the other's confidential information confidential, use it only for this engagement, and disclose it only to staff and contractors who need it and are under equivalent obligations. This survives the end of this Agreement for {{ legal.confidentiality_term_years }} years.

Confidential information does not include information that is public through no fault of the receiving party, was already lawfully held, or must be disclosed by law or by a court.
{% if legal.nda.include_in_pack %}

A separate Non-Disclosure Agreement accompanies this pack. Where the two conflict on confidentiality, the Non-Disclosure Agreement governs.
{% endif %}

## 9. Warranties and limitation of liability

The Provider warrants that it will perform the work with reasonable skill and care, and that to the best of its knowledge the deliverables do not infringe a third party's intellectual property rights.

Beyond that warranty, the deliverables are provided as they are. The Provider does not warrant that they will be free of every defect, or that they will produce any particular commercial result.

Neither party is liable to the other for loss of profit, loss of business, loss of data, or any indirect or consequential loss.

Each party's total liability under this Agreement is limited to {{ legal.liability_cap }}.

Nothing in this Agreement limits liability for death or personal injury caused by negligence, for fraud, or for anything else that cannot lawfully be limited.

## 10. Termination

Either party may terminate this Agreement on **{{ legal.termination_notice_days }} days of written notice**.

Either party may terminate immediately, in writing, if the other is in material breach and has not fixed it within {{ legal.termination_notice_days }} days of being told about it in writing.

On termination:

- The Client pays for all work completed and all work in progress up to the termination date.
{% if has('commercial.kill_fee_percent') %}
- Where the Client terminates for convenience after work has started, a cancellation fee of {{ commercial.kill_fee_percent | pct }} of the remaining unbilled fee is also payable, covering reserved capacity the Provider cannot re-let at short notice.
{% endif %}
- The deposit is non-refundable.
- Clauses 7, 8, 9 and 11 survive termination.

## 11. General

**Independent contractor.** The Provider is an independent contractor, not an employee, partner or agent of the Client, and is responsible for its own taxes and insurance.

**Subcontracting.** The Provider may use subcontractors, remains responsible for their work, and will bind them to equivalent confidentiality obligations.

**Notices.** Written notice means email to {{ provider.email }} for the Provider and {{ client.email }} for the Client, and is treated as received on the next working day.

**Entire agreement.** This Agreement, together with the Kickoff Document and any written change requests, is the whole agreement between the parties on this engagement and replaces anything discussed before it.

**Variation.** A change to this Agreement is only effective if it is in writing and agreed by both parties.

**Severability.** If a clause is unenforceable, the rest stays in force.

**Governing law.** This Agreement is governed by the law of {{ legal.jurisdiction }}, and the parties submit to the exclusive jurisdiction of {{ legal.courts }}.

---

## Signatures

| | The Provider | The Client |
| --- | --- | --- |
| Company | {{ provider.legal_name }} | {{ client.legal_name }} |
| Signed by | {{ provider.contact_name }} | {{ client.contact_name }} |
| Title | {{ provider.contact_title }} | {{ client.contact_title }} |
| Signature | | |
| Date | | |
