---
name: setup
description: Welcome a gym owner after plugin installation or Start ClockOff; separately activate explicitly requested supported updates or adjust monitoring preferences.
---

Explicit user instructions take precedence over default workflow guidance.

Verify gym identity once per ordinary new conversation before relying on gym, owner or member permissions. Reuse that verified identity for follow-up questions on the same connection; check again after a reconnect, gym/account change or an explicit identity question. This applies to identity checks below. A finished scheduled report is delivered verbatim without new reads. Never infer another gym’s identity from profile names or earlier sessions.

# Welcome to ClockOff

This is the packaged onboarding skill declared by `extensions.com.openai.onboardingSkill`. ChatGPT documents users running setup after installation, in a new conversation or the existing installation conversation. Do not claim that installation alone posts an automatic welcome or activates notifications.

Call `clockoff_who_am_i` before using a name, gym, or capability. Display its complete `data.welcome.message` unchanged as the welcome. It already contains the personal introduction, authorised capabilities and starting questions. Do not paraphrase it, duplicate the questions, append a daily briefing or open a dashboard. Use only the saved owner, agent and gym names returned for this connection. On an older endpoint whose welcome lacks readable choices, show its `welcome.suggestedQuestions` once as short bullets. Where supported, native clickable choices may mirror those exact question strings without adding duplicate visible text.

If the connection needs authorization, explain the account-linking step in plain language. If a product grant is absent, describe only what this gym can actually use. Keep current findings and the daily brief for an explicit request. Setup is a read-only introduction; it does not create a schedule or a live alert.

Use the tool names advertised by this host; a host may add a server prefix. On an error, check `status`, `error.retryable` and `nextAction`: retry a temporary failure once, then report its request reference. Never answer from a previous gym or replace unavailable live data with old records. A missing tool may mean this connection lacks access; ask for the approved setup rather than trying another credential.

Examples: “Start ClockOff” → identity, exact welcome and its supported next choices. “Which gym am I connected to?” → identity only. “I am returning, show my campaigns” → go straight to the requested campaign workflow; no repeated setup. An expired connection requires the current host's supported ClockOff sign-in/reconnect action; never ask for keys in the conversation. Ordinary welcome does not change settings or create subscriptions; explicit monitoring setup below is a separate owner-requested action.

## Pushed gym updates in ChatGPT Work and dots

When the owner asks to activate or test updates, follow this flow instead of asking
gym questions. Use only the tools and event definitions actually advertised by
this connection; availability on another host or endpoint proves nothing here.

Read identity and `clockoff_get_monitoring_status`. Explain the saved choices:
morning07:30, evening20:00 in the gym timezone (Hillsborough Pacific/Auckland),
and new-signup alerts independently. Preserve existing choices. On the owner's
activation request save `enabled:true` with `clockoff_update_monitoring_preferences`.
Connecting alone does not activate monitoring; activating alone does not create
a host subscription.

Use this host's supported event-subscription action for the real protocol events
`clockoff.signup.recorded` and `clockoff.briefing.ready`. Omit the briefing kind
filter to receive both times. ClockOff owns the timers: do not add equivalent
host schedule automations. If a previous timer exists, preserve it until the
new event path is accepted and resolve duplicate ownership before normal use.
Keep an existing matching monitor; refresh its subscription rather than creating
duplicates. The host owns callback URLs/secrets and renewals; never ask the owner
to copy those into chat. If this host does not expose Events, explain that exact
limitation without pretending an ordinary tool created a subscription.

For explicitly requested full-class alerts, also inspect `clockoff_get_class_alert_settings`
and the advertised `clockoff.class.full` event. Preserve an existing authorised matching
subscription instead of creating a duplicate. Enabling the full rule and subscribing
are distinct actions; change the rule only when requested. This event queues independently
of daily times and other class quiet/cooldown rules. The exact monitoring-event reader
already rechecks class state and returns a finished `data.answerCard`; obey
`respondToEvent` and display that card unchanged. Preserve test labels; a delivery test
does not prove a natural full transition. Never promise zero host delay.

Re-read monitoring status and distinguish active required subscriptions, partial
setup, paused, expired/disconnected and delivery failed. Confirm only what the
backend and host actually established. Changes to times or signup choices use
the same backend preferences; changed host filters may still need a subscription
refresh. Pausing uses `enabled:false`; unsubscribing is separate. A message
already being processed cannot be recalled.

For an owner-requested test, call `clockoff_test_monitoring_event` once with
`confirmTest:true` and the chosen kind. A short `delaySeconds` tests a real future
delivery deadline without changing normal times. State queued versus receiver
accepted versus a visible Dot response separately. All test messages must be
labelled, create no actual members and trigger no customer contact. Do not keep
asking the Dot ordinary gym questions to test notifications. Do not repeat the
test tool just because acknowledgement is pending.

## Hermes installation and authorization

Apply this section only when the owner is using Hermes. Installing/enabling the
ClockOff package supplies skills and the server address; it does not authorize
access to a gym. If the package connector returns HTTP401 / no authorization,
explain that distinction briefly and give the supported setup route instead of
repeatedly suggesting Refresh:

“ClockOff is installed, but this Hermes profile still needs its gym connection.
Open Connectors → Add your own, choose Streamable HTTP, use the name clockoff
and https://clockoff-preview.appwrite.network/mcp, then complete secure authentication.”

Use the same server name so profile authentication overrides the package's
address; do not suggest a second server/installation or another gym's key.
Browser OAuth needs a compatible pre-registered client and the owner's ClockOff
sign-in/consent; automatic client registration is not advertised in the tested
server metadata, so do not promise a one-click OAuth journey. If this installation
uses a managed key, the owner generates their own gym/installation key in
ClockOff and enters it only in Hermes's secure Bearer-token form. Never request,
print, copy or paste credentials in conversation.

After secure connector configuration, verify identity with the advertised tool.
If giving CLI checks, explain that `hermes -p <profile> mcp test clockoff` checks
explicit profile configuration; plugin-only enable can report “not found in
config” although the package runtime has discovered the server.

When the owner asks whether skills are installed, distinguish package discovery,
actual loading and preload. The package contains eight skills; the tested
restricted F45 profile preloads six. Hermes Desktop's ordinary Skills page can
omit package skills even when its runtime loads them. Use actual plugin/version
and runtime loader evidence when available; do not claim the skills are missing
or loaded into a conversation from that page alone. Select the intended profile
in Plugins manager, enable ClockOff, and use Rescan for installed-package updates.
A new session adopts enable changes; `/reload-skills` is not supported by the
tested Desktop slash palette. Do not clear history or change credentials/model/
schedules to refresh a package. Fresh installation remains manual ZIP extraction
until a tested catalog/Git distribution is available.

## Showing saved ads in ChatGPT

For a Dot owner asking to see a saved campaign, read its exact copy and effective delivery description with `clockoff_get_campaign`, match its campaign ID in `clockoff_list_creatives`, and retrieve each requested JPEG with `clockoff_get_creative_image`. Use the Dot’s supported native file/image output to attach those exact JPEGs in the same answer; the owner can open ChatGPT’s full-window image preview and zoom. This route was visibly verified in Dots on 11 October 2026 when embedded widgets were unavailable. Image bytes alone do not prove rendering. Preserve Work’s separately supported native forms and visual review; a failed Dot widget is not a global capability result. A shared saved-plan link opens a human review view and does not save, transfer or publish another campaign.

For an incoming event, inspect each supplied event object if the host batches more
than one. The saved occurrence reference is in that object's `data.eventRef`; its
webhook delivery identity is the top-level `eventId`. Pass either exact supplied
value to `clockoff_get_monitoring_event`. Do not derive a reference, use a latest
event as a substitute or retry a delivered test. If neither identity is supplied,
report that this alert could not be verified; do not invent facts or change setup.
