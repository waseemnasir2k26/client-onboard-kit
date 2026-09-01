# Intake and Scoping Questionnaire

**Project:** {{ engagement.title }}  
**For:** {{ client.legal_name }}  
**Prepared by:** {{ provider.legal_name }}  
**Please return by:** {{ onboarding.questionnaire_due | date }}

This is the boring document that saves the project. Most overruns are not caused by hard problems; they are caused by a question nobody asked in week one. Answer what you can, write "don't know" where you don't, and flag anything you think we have misunderstood.

Twenty minutes now is worth a fortnight later.

---

## 1. The decision

**1.1** Who has final sign-off on this work? One name, not a committee.
We have this as {{ comms.approver_name }}, {{ comms.approver_title }}. Correct?

**1.2** Who else must be consulted before that person can sign off, and what do they care about?

**1.3** Who can stop this project, and under what circumstances?

**1.4** Has anyone attempted this before, internally or with another supplier? What happened?

## 2. Success

**2.1** We have written down these success criteria:

{% for item in onboarding.success_criteria %}
- {{ item }}
{% endfor %}

Are they right? Add, remove or correct anything.

**2.2** How will each of those be measured, by whom, and from what baseline?

**2.3** If this project delivers exactly what is described and nothing more, is that a success? If not, what is missing?

## 3. Deadlines

**3.1** These are the hard deadlines we have recorded:

{% for d in onboarding.hard_deadlines %}
- **{{ d.name }}** by {{ d.date | date }} - {{ d.why }}
{% endfor %}

Is any date above softer than it looks, or is there one we have missed?

**3.2** Are there dates when key people are unavailable (holidays, audits, peak trading, board meetings)?

**3.3** What happens to the business if the launch date slips by two weeks?

## 4. Scope boundaries

**4.1** The Service Agreement lists this as out of scope:

{% for item in engagement.out_of_scope %}
- {{ item }}
{% endfor %}

Does anything in that list surprise you? Better to argue about it now than in week six.

**4.2** Is there anything you assume is included that is not written down anywhere?

**4.3** Which existing systems must this work with, and who owns each of them?

## 5. Brand and content

**5.1** Please supply the following:

{% for item in onboarding.brand_assets %}
- [ ] {{ item }}
{% endfor %}

**5.2** Who writes the copy, and by when? If it is us, that is a change request; if it is you, we need a date.

**5.3** Are there brand, legal or regulatory rules we must follow (accessibility standards, disclaimers, tone, restricted claims)?

**5.4** Is there anything the brand must never do, say, or look like?

## 6. Access and credentials

We need working access before the start date, not on the day we need it. Please arrange delegated access wherever possible rather than sharing passwords.

{% for item in onboarding.access_checklist %}
- [ ] {{ item }} - owner: ______________________ - arranged by: ______________
{% endfor %}

**6.1** Who is the person who can actually grant each of these? Not who should be able to. Who can.

**6.2** Is any of the above controlled by a former supplier or an ex-employee? Say so now.

**6.3** Is there a change-control, security review or procurement process we must pass before we get access? How long does it usually take?

## 7. Data

**7.1** Will we handle personal data? If so, whose, what categories, and where does it live today?

**7.2** Do you have a data protection contact or a privacy policy we should be working to?

**7.3** What data has to be migrated, where is it now, and who owns its accuracy?

## 8. Anything else

**8.1** What is the one thing most likely to derail this project?

**8.2** What has annoyed you about working with agencies or freelancers before? We would rather not repeat it.

**8.3** Anything else we have not asked about?

---

Return this to {{ provider.email }}. If a question does not apply, write "n/a" rather than leaving it blank, so we know it was read.
