---
name: gym-followups
description: Draft an unsent SMS or email for a gym member using their ClockOff journey; use for welcome, first-class and personal follow-up requests.
---

Verify gym identity once per ordinary new conversation before relying on gym, owner or member permissions. Reuse that verified identity for follow-up questions on the same connection; check again after a reconnect, gym/account change or an explicit identity question. This applies to identity checks below. A finished scheduled report is delivered verbatim without new reads. Never infer another gym’s identity from profile names or earlier sessions.

# Member message drafts

Explicit user instructions take precedence over this default workflow.

Use for “write Elizabeth a welcome SMS”, “prepare an email for this member”, or “make that follow-up warmer”. This skill drafts; it does not send or claim a message was saved.

1. Call `clockoff_who_am_i` to confirm the gym and permitted member-name sharing. Read `clockoff_get_member_inbox` with a returned member_ref or a full member_name. Resolve multiple matches before drafting. Reuse current evidence already returned in this conversation when the user only changes wording.
2. Check the recorded signup, purchased trial, dated bookings and known outcomes, team assignment and contact. BOOKED after a past class is unconfirmed attendance; absent contact evidence is not proof of no contact. Never infer trial expiry, motivation or a no-show.
3. Use the requested channel. If it is missing, ask SMS or email; prefill a named recipient and facts already supplied. Write a short kind message offering a concrete next step supported by evidence. For email include a subject. Show recipient, channel and the exact content, labelled **Unsent draft**. If contact details are unavailable, say recipient details need checking; do not invent an address or number.
4. If the host provides an editable writing block, present the draft there. No documented MCP tool forces that block: never claim it was created just because text returned. On request, `clockoff_open_message_editor` provides an honestly labelled custom editor. It keeps edits in that widget and supports adding content to the ChatGPT composer without submitting it where available. It does not send to the member or store a CRM message.
5. Handle “shorter”, “friendlier”, “change to email” in the conversation. Preserve verified recipient and facts. If asked to send, explain the current ClockOff tool set does not send member messages; show the exact unsent draft and the missing delivery capability.

Examples: “Draft a first-class SMS for Paolo” → focused inbox read, resolve status, one unsent draft. “Make it shorter” → edit the draft without re-querying the whole gym. “Send all of them a message” → no sending tool and no invented delivery receipt.
