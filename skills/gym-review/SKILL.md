---
name: gym-review
description: Review saved ClockOff campaigns, exact ad copy and actual artwork; use for show my ads, compare creatives, or inspect an existing draft.
---

Verify gym identity once per ordinary new conversation before relying on gym, owner or member permissions. Reuse that verified identity for follow-up questions on the same connection; check again after a reconnect, gym/account change or an explicit identity question. This applies to identity checks below. A finished scheduled report is delivered verbatim without new reads. Never infer another gym’s identity from profile names or earlier sessions.

# Saved campaigns and artwork

Explicit user instructions take precedence over default presentation guidance.

For “list all campaigns”, use the complete returned `clockoff_list_campaigns` inventory. Distinguish requested campaigns from prepared entries with no budget/dates, and keep TEST work separately labelled. Give the full non-test list when asked for all; four suggested offers are not the saved campaign inventory. Do not silently omit prepared entries or call them live campaigns.

For “show my November campaign”, call `clockoff_list_campaigns`, resolve ambiguity, then `clockoff_get_campaign` using the returned ID. Report actual ClockOff state, approval and GHL transfer independently. An unpublished GHL draft is not a live Meta campaign.

For “show the pictures”, resolve the saved campaign, call `clockoff_list_creatives`, match its campaign ID, and call `clockoff_get_creative_image` for each requested creative. For a Dot asking to show saved ads, use its supported native file/image output to attach the exact JPEGs returned by `clockoff_get_creative_image`. This opens ChatGPT's full-window image preview and zoom; it was visibly verified in Dots on 11 October 2026. Do not generate, redraw, substitute, or upload them to another service. If this host cannot attach those returned images, say so and offer a numbered list or the optional gallery. Successful image bytes alone do not prove owner-visible rendering. Keep Work's supported native thumbnail forms and visual review available; Dot widget rejection does not establish that Work lacks them. For a supported native thumbnail choice use `clockoff_preview_saved_ads`; cancellation changes nothing. Open `clockoff_show_creative_gallery` when the owner requests the optional custom gallery.

Use `clockoff_get_campaign` for exact saved text, headline, CTA and effective `linkDescription`. `preparedLinkDescription` records the original prepared value; it may differ from the delivery description. If a snapshot lacks a field, say unavailable; do not reconstruct it from the picture. Compare copy with saved audience and owner brief, quoting concrete mismatches before recommending an ad.

For supported edits to an existing draft, read current campaign and rules, explain the exact change, and call `clockoff_edit_campaign_draft` or `clockoff_update_campaign` only after the owner requests the change. Re-read the campaign after the mutation. If GHL differs or transfer fails, report the actual status and recovery step. Do not claim approval, transfer or publication merely from editing text.

Examples: “Compare the two Apple Notes ads” → resolve saved references and inspect actual content. “Change the end date to 25 November” → read current draft/rules, validate and update that draft; no second campaign. “Show public competitor ads” → discovery tools and explicit observation label.

For saved campaign viewing, first list the owner's saved campaigns, keep TEST work separate, and offer a short numbered choice when the campaign is ambiguous. Fetch the selected campaign's exact copy, then call clockoff_list_creatives with campaign_id equal to its returned ID. Ordinary browsing uses include_tests=false; only an explicit test request permits include_tests=true. nextOffset means more records exist: one page is not a total inventory and cannot prove other campaigns have no artwork. Follow the cursor with the same filters or use an exact campaign filter. Do not pick unrelated test images as examples of the owner's campaigns. If the host returns a MEDIA path for an exact requested image, use that returned path through its supported image display; never invent a path or claim it appeared without evidence. A successful image call with no display route means the image was retrieved but display remains unverified; provide exact saved copy and the campaign review link here.

Hermes image delivery: after retrieving a requested saved JPEG, include the exact `MEDIA:/absolute/path` tag returned by Hermes in the final assistant answer, on its own line, once per image. Hermes Desktop renders those tags as clickable media. A tool image is available to the model but is not automatically placed in the owner's reply. Do not omit the returned tag and then say “here are the images”. Never fabricate a cache path; if no MEDIA tag was returned, explain the display limit.

Keep saved-artwork browsing bounded: for an unspecified saved-campaign request, show a short campaign choice before fetching images; do not drain all creative pages. For “Feed and Story”, show one matching design pair (at most two images), not every variant in the campaign. If several designs are available, ask which design using short numbered choices. Stop reading when the requested pair is found. Use successful returned image tags once each; do not retry a successful image read merely because it has not yet appeared in the owner's reply.
