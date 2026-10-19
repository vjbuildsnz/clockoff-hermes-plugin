---
name: gym-classes
description: Answer a ClockOff gym owner's class availability, historical booking, and class-alert questions from dated Mindbody observations.
---

Verify gym identity once per ordinary new conversation before relying on gym, owner or member permissions. Reuse that verified identity for follow-up questions on the same connection; check again after a reconnect, gym/account change or an explicit identity question. This applies to identity checks below. A finished scheduled report is delivered verbatim without new reads. Never infer another gym’s identity from profile names or earlier sessions.

# Classes in the conversation

Confirm the connected gym with `clockoff_who_am_i`. For upcoming class spaces, use `clockoff_get_class_availability`; distinguish provider-confirmed capacity from unknown or stale counts. For a historical time such as “Who booked the 5 am classes in the last two weeks?”, call `clockoff_get_class_bookings` with `hour: 5`, `minute: 0`, and `days: 14`, following its cursor until the requested list is complete. Lead with the distinct-person count and an outcome summary, then pair every observed class date with that booking's recorded outcome for each person. Preserve the full roster when the owner requests it. A past `BOOKED` row has unconfirmed attendance; only an explicit missed outcome is a no-show. Say where the saved feed may be incomplete. Respect the gym's member-name setting.

For alert preferences, read `clockoff_get_class_alert_settings`. Explain the class issue and give one practical next step in the conversation. Use native choices when the host offers them, such as inspect the affected class, review bookings, or change the alert rule. Name each choice in text so the owner can reply if a button is absent or unresponsive while streaming. Change a saved rule through `clockoff_update_class_alert_settings` only when the owner asks for that exact change and the tool authorizes it.

Proactive `clockoff.class_attention.created` events need a confirmed ChatGPT Work or dot subscription. An available event type, an enabled ClockOff alert rule, and an actual host subscription are three different facts. Personal chats cannot receive these events. An event is a reason to recheck the current class facts, not permission to contact members or edit bookings.

Fully booked classes use the separately advertised `clockoff.class.full` event. On an
explicit owner activation request, preserve other class rules and establish or refresh
that exact subscription; do not add a timer. Read an incoming event once through
`clockoff_get_monitoring_event` with its exact reference. This already checks current
enabled/tenant/class state, reopening, cancellation and start. Honour `respondToEvent`;
when false stay quiet. Display a supplied `data.answerCard` unchanged as the whole alert.
Do not fetch class data again, invent a full count, call providers or publish a proposed
post. Controlled tests remain labelled and prove no real class became full. Immediate
server queuing does not guarantee immediate host processing or an owner-visible reply.

Use the tool names advertised by this host; a host may add a server prefix. On an error, check `status`, `error.retryable` and `nextAction`: retry a temporary failure once, then report its request reference. Never answer from a previous gym or replace unavailable live data with old records. A missing tool may mean this connection lacks access; ask for the approved setup rather than trying another credential.

For tomorrow/today, pass the explicit day selector when advertised. Always name the requested civil date in the gym timezone. An empty date-specific result means no saved counts for that date, not no scheduled classes. Never answer tomorrow with the next available day's classes. If the date selector is unavailable, filter the returned dates yourself and state the missing requested date; another day's availability requires a separate owner choice.

If no count rows are returned for the requested date, say count freshness cannot be assessed. Do not label nonexistent counts stale. A timetable baseline refresh date describes retrieval coverage; individual class counts may have later signed updates and their own Last confirmed dates.

Owners should not need internal class IDs. If a particular class needs clarification, ask for its day/time or name and resolve its reference using advertised read tools. If the requested day has no saved availability counts, explain that limit briefly rather than asking for a class ID or promising a live refresh.

For “which classes today were fullest?” or earlier classes today, use `clockoff_get_class_availability` with `day: today` and `include_elapsed_today: true`. Its normal today selector excludes elapsed classes. Report saved booking counts and their observation times; these do not prove final attendance or peak occupancy. Use the exact gym-local civil date returned by the tool, even if the host date differs.

Use the server-computed confirmation age when supplied, or give the exact last-confirmed date/time. Never estimate elapsed age mentally. Preserve the returned usable/unknown/cancelled row totals consistently; include every usable count relevant to the requested day.

For proactive class updates use the absolute gym-local class weekday/date/time and last-confirmed time from the current tool result. Avoid today/tomorrow in an unattended alert, because delivery can cross midnight or arrive late. A class on Monday is not “today” in a Sunday delivery.

For an incoming event, inspect each supplied event object if the host batches more
than one. The saved occurrence reference is in that object's `data.eventRef`; its
webhook delivery identity is the top-level `eventId`. Pass either exact supplied
value to `clockoff_get_monitoring_event`. Do not derive a reference, use a latest
event as a substitute or retry a delivered test. If neither identity is supplied,
report that this alert could not be verified; do not invent facts or change setup.
