"""Local managed-Hermes adapter. No provider/database calls or transcript edits."""
import json
import re
import threading
import time
from pathlib import Path

HEADER = re.compile(r'^\[Cronjob "[^"\n]+: (morning brief|evening wrap|weekly review)" output — [^\n]*\]\n\n')
REQUIRED = ("🏋️", "🆕", "💰", "📣", "Data current to:")
_lock = threading.Lock()
_reports = {}
_brief_reads = {}
_attendance_reads = {}
_report_sources = {}
ATTENDANCE_REQUEST = re.compile(r"\b(?:attendance|late[ -]?(?:cancel|cancellation)|no[ -]?show(?:s|ed)?\b)", re.I)


def owner_rules(**kwargs):
    return {"context": "Trusted ClockOff owner rules:\n" + (Path(__file__).resolve().parent / "OWNER_RULES.md").read_text()}


def finished_report(message):
    if not isinstance(message, str):
        return None
    match = HEADER.match(message)
    if not match:
        return None
    header = message[:match.end()].split("output — ", 1)[1].split("]\n", 1)[0]
    if header not in {"scheduled job, not the user. Review it, act on anything that needs action, and summarize for the chat.", "scheduled job, not the user. Review it and summarize."}:
        return None
    body = message[match.end():]
    if len(body) > 50_000 or not all(marker in body for marker in REQUIRED) or not re.search(r"(?m)^Data current to: .+\((?:UTC|[A-Za-z_+-]+/[A-Za-z_+/-]+)\)", body):
        return None
    return body


def skill_for(message):
    text = str(message).lower()
    if any(word in text for word in ("start clockoff", "set up clockoff", "connect clockoff", "who am i connected")):
        return "setup"
    if any(word in text for word in ("draft", "write", "wording")) and any(word in text for word in ("sms", "email", "message", "follow-up", "follow up", "welcome")):
        return "gym-followups"
    if any(word in text for word in ("five minutes", "ten minutes", "5 minutes", "10 minutes", "staff handoff")):
        return "gym-daily"
    if ("saved" in text and any(word in text for word in ("campaign", "ad"))) or any(word in text for word in ("artwork", "picture", "image", "creative", "exact copy")):
        return "gym-review"
    if any(word in text for word in ("campaign", "offer", "budget", "advert", "ad draft")):
        return "gym-campaigns"
    if any(word in text for word in ("daily update", "evening update")):
        return "gym-daily"
    if re.search(r"\b(?:late[ -]?(?:cancel|cancellation)|no[ -]?show(?:s|ed)?\b)", text):
        return "gym-members"
    if any(word in text for word in ("class", "coach", "bookings", "waitlist", "spaces")) and not any(word in text for word in ("first class", "first-class", "member", "trial")):
        return "gym-classes"
    if any(word in text for word in ("member", "trial", "contact", "sign-up", "signup", "follow-up", "follow up", "risk", "expiry", "first class", "first-class")):
        return "gym-members"
    if any(word in text for word in ("sell", "sales", "revenue", "summary", "brief", "attention", "priority", "gym", "month", "week", "today")):
        return "gym-daily"
    return None


def before(*, user_message="", session_id="", turn_id="", **kwargs):
    key = (session_id, turn_id)
    report = finished_report(user_message) if session_id and turn_id else None
    with _lock:
        text = str(user_message).lower()
        if session_id and turn_id and any(phrase in text for phrase in ("morning brief", "evening wrap", "daily update", "evening update", "weekly review", "today’s brief", "today's brief", "get_briefing with kind")) and not any(word in text for word in ("schedule", "timer", "five minutes", "ten minutes")):
            _brief_reads[key] = time.monotonic()
            _report_sources[key] = user_message
        elif session_id and turn_id and ATTENDANCE_REQUEST.search(text):
            _attendance_reads[key] = time.monotonic()
            _report_sources[key] = user_message
        # Expiry bounds abandoned hooks; exact turn keys isolate interleaved requests.
        now = time.monotonic()
        for reads in (_brief_reads, _attendance_reads):
            for old, created in list(reads.items()):
                if now - created > 300:
                    del reads[old]
                    _report_sources.pop(old, None)
        for old, (_, created) in list(_reports.items()):
            if now - created > 300:
                del _reports[old]
                _report_sources.pop(old, None)
        if report:
            _reports[key] = (report, now)
            _report_sources[key] = user_message
    if report:
        return {"context": "This is finished ClockOff report delivery. Do not call tools or investigate. Finish this turn immediately with the supplied report only. The delivery adapter will preserve its exact original text."}
    here = Path(__file__).resolve().parent
    package = here / "skills"
    if not package.is_dir():
        package = here.parent / "clockoff" / "skills"
    workflow = skill_for(user_message)
    if workflow is None:
        return None
    path = package / workflow / "SKILL.md"
    if path.is_file():
        return {"context": path.read_text()}
    return None


def observe_current_request(*, conversation_history=None, session_id="", turn_id="", **kwargs):
    # Barge-in can redirect a running turn without another pre_llm_call. Never
    # replace that newer owner's answer with the original scheduled report.
    key = (session_id, turn_id)
    latest = next((message.get("content") for message in reversed(conversation_history or [])
                   if isinstance(message, dict) and message.get("role") == "user"), None)
    with _lock:
        source = _report_sources.get(key)
        if source is not None and isinstance(latest, str) and latest != source:
            _reports.pop(key, None)
            _brief_reads.pop(key, None)
            _attendance_reads.pop(key, None)
            _report_sources.pop(key, None)


def capture_brief(*, tool_name="", result=None, args=None, session_id="", turn_id="", **kwargs):
    key = (session_id, turn_id)
    args = args if isinstance(args, dict) else {}
    if kwargs.get("status", "ok") != "ok":
        return None
    field = {
        "mcp__clockoff__clockoff_get_briefing": "ownerBrief",
        "mcp__clockoff__clockoff_ask_gym_database": "ownerAttendance",
        "mcp__clockoff__clockoff_get_attendance_outcomes": "ownerAttendance",
    }.get(tool_name)
    if field is None or args.get("focus") == "staff_task":
        return None
    reads = _brief_reads if field == "ownerBrief" else _attendance_reads
    with _lock:
        created = reads.get(key)
        source = _report_sources.get(key)
    if created is None or time.monotonic() - created > 300:
        return None
    if tool_name == "mcp__clockoff__clockoff_ask_gym_database" and args.get("question") != source:
        return None
    try:
        # post_tool_call receives the handler JSON, before transcript trust wrapping.
        # Do not scrape prose, wrapped transcripts, or arbitrary nested tool results.
        payload = json.loads(result) if isinstance(result, str) else result
        if not isinstance(payload, dict) or payload.get("isError") or payload.get("error"):
            return None
        structured = payload.get("structuredContent")
        if not isinstance(structured, dict):
            return None
        data = structured.get("data", {})
        if not isinstance(data, dict):
            return None
        body = data.get(field)
        if structured.get("status") != "ok" or structured.get("error") or not isinstance(body, str):
            return None
        if not body.strip() or len(body) > 50_000:
            return None
        if field == "ownerBrief" and not all(marker in body for marker in REQUIRED):
            return None
        if field == "ownerAttendance" and data.get("attendanceOutcomes", data).get("evidenceSource") != "webhooks":
            return None
    except (ValueError, TypeError, AttributeError):
        return None
    with _lock:
        # A barge-in may have invalidated this read while its result was parsed.
        if reads.get(key) == created and _report_sources.get(key) == source:
            _reports[key] = (body, time.monotonic())
    return None


def block_report_tools(*, session_id="", turn_id="", **kwargs):
    with _lock:
        pending = (session_id, turn_id) in _reports
    if pending:
        return {"action": "block", "message": "Finished-report delivery needs no tools. Finish the reply now; the original report will be delivered unchanged."}
    return None


def transform(*, response_text="", session_id="", turn_id="", **kwargs):
    with _lock:
        saved = _reports.pop((session_id, turn_id), None)
    if str(response_text).startswith("Operation interrupted"):
        return None
    return saved[0] if saved else None


def after(*, session_id="", turn_id="", **kwargs):
    with _lock:
        _reports.pop((session_id, turn_id), None)
        _brief_reads.pop((session_id, turn_id), None)
        _attendance_reads.pop((session_id, turn_id), None)
        _report_sources.pop((session_id, turn_id), None)


def end(*, session_id="", **kwargs):
    with _lock:
        for reads in (_brief_reads, _attendance_reads):
            for key in list(reads):
                if key[0] == session_id:
                    del reads[key]
        for key in list(_reports):
            if key[0] == session_id:
                del _reports[key]
        for key in list(_report_sources):
            if key[0] == session_id:
                del _report_sources[key]


def register(ctx):
    ctx.register_hook("pre_llm_call", owner_rules)
    ctx.register_hook("pre_llm_call", before)
    ctx.register_hook("pre_api_request", observe_current_request)
    ctx.register_hook("pre_tool_call", block_report_tools)
    ctx.register_hook("post_tool_call", capture_brief)
    ctx.register_hook("transform_llm_output", transform)
    ctx.register_hook("post_llm_call", after)
    ctx.register_hook("on_session_end", end)
