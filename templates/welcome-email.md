**Subject:** Welcome aboard - {{ engagement.title }}

**To:** {{ client.contact_name }} <{{ client.email }}>  
**From:** {{ provider.contact_name }} <{{ provider.email }}>

---

Hi {{ client.contact_name.split(' ')[0] }},

Delighted to be working with {{ client.short_name }} on the {{ engagement.title | lower }}. Here is everything you need to get us started, and nothing you don't.

**What we're doing.** {{ engagement.summary }} We start on {{ engagement.start_date | date }}{% if has('engagement.end_date') %} and the plan has us finished by {{ engagement.end_date | date }}{% endif %}.

**Three things from you this week:**

{% for action in welcome.next_actions %}
{{ loop.index }}. {{ action }}
{% endfor %}

{% if has('welcome.signature_tool') %}
The agreements come through {{ welcome.signature_tool }}, so signing takes about a minute on a phone.
{% endif %}
{% if has('welcome.kickoff_call.date') %}

**Kickoff call:** {{ welcome.kickoff_call.date | date }} at {{ welcome.kickoff_call.time }} ({{ comms.timezone }}), {{ welcome.kickoff_call.duration_minutes }} minutes - {{ welcome.kickoff_call.link }}.{% if comms.approver_name != client.contact_name %} Bring {{ comms.approver_name }} if you can; the call is much more useful with the decision-maker in it.{% endif %}
{% endif %}

**How we'll work.** Day to day we'll use {{ comms.primary_channel }}, and you'll hear back from us within {{ comms.response_time_hours }} hours during {{ comms.working_hours }} ({{ comms.timezone }}). Anything that changes scope, price or a date goes in writing, so there are no surprises on an invoice. The full detail is in the Kickoff Document in this pack.

**One ask.** The single biggest cause of delay on projects like this isn't the build, it's waiting on access and assets. The checklist in the questionnaire looks tedious, but getting through it this week is what keeps the schedule realistic.

Anything at all, just reply to this email or ping me at {{ provider.email }}{% if has('provider.phone') %} or {{ provider.phone }}{% endif %}.

Looking forward to it.

{{ provider.contact_name }}  
{{ provider.contact_title }}, {{ provider.legal_name }}  
{{ provider.website }}
