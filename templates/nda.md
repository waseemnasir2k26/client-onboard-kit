{% set one_way = legal.nda.type == 'one_way' %}
# {% if one_way %}One-Way{% else %}Mutual{% endif %} Non-Disclosure Agreement

Made on {{ today | date }} between:

**{{ provider.legal_name }}**  
{{ provider.address | block }}

and

**{{ client.legal_name }}**  
{{ client.address | block }}

{% if one_way %}
In this Agreement the **Disclosing Party** is {{ legal.nda.disclosing_party }} and the **Receiving Party** is the other party named above. Obligations run one way only.
{% else %}
In this Agreement each party may act as **Disclosing Party** and as **Receiving Party**. Obligations run both ways, equally.
{% endif %}

---

## 1. Purpose

The parties wish to exchange confidential information for the following purpose, and for no other:

> {{ legal.nda.purpose }}

## 2. What counts as confidential information

Confidential information means non-public information disclosed by the Disclosing Party in connection with the purpose, in any form, whether or not it is labelled confidential. It includes business plans, pricing, customer and supplier lists, financial figures, source code, designs, credentials, and the fact and content of the parties' discussions.

## 3. What does not count

Confidential information does not include information that:

1. Is public, or becomes public, other than through a breach of this Agreement.
2. The Receiving Party already lawfully held, without a duty of confidence, before disclosure.
3. The Receiving Party lawfully receives from a third party who is free to disclose it.
4. The Receiving Party independently develops without using the confidential information.

## 4. Obligations of the Receiving Party

The Receiving Party will:

- Keep the confidential information confidential, and protect it with at least the care it applies to its own confidential information.
- Use it only for the purpose in clause 1.
- Disclose it only to those of its staff, contractors and professional advisers who need it for the purpose, and who are bound by equivalent obligations. The Receiving Party stays responsible for their compliance.
- Not copy it beyond what the purpose requires.

## 5. Required disclosure

If the Receiving Party is required by law, regulation or a court to disclose confidential information, it may do so, but will (where it is lawfully able) tell the Disclosing Party first so that the Disclosing Party can seek to limit the disclosure.

## 6. Return and destruction

On written request, the Receiving Party will return or destroy the confidential information and any copies, except where retention is required by law or by an automated backup system, in which case the confidentiality obligations continue for as long as the material is held.

## 7. No licence, no obligation

Nothing here transfers ownership of, or grants a licence to, any intellectual property. Nothing here obliges either party to disclose anything, to enter into any further agreement, or to proceed with the engagement.

## 8. Term

This Agreement takes effect on the date above. The confidentiality obligations continue for **{{ legal.nda.term_years }} years** from the date of the last disclosure made under it.

## 9. Remedies

The parties accept that damages alone may not be an adequate remedy for a breach, and that the Disclosing Party may seek injunctive relief in addition to any other remedy available to it.

## 10. General

This Agreement is governed by the law of {{ legal.jurisdiction }}, and the parties submit to the exclusive jurisdiction of {{ legal.courts }}. It may be signed in counterparts, including electronically. If a clause is unenforceable, the rest stays in force.

---

## Signatures

| | {{ provider.legal_name }} | {{ client.legal_name }} |
| --- | --- | --- |
| Signed by | {{ provider.contact_name }} | {{ client.contact_name }} |
| Title | {{ provider.contact_title }} | {{ client.contact_title }} |
| Signature | | |
| Date | | |
