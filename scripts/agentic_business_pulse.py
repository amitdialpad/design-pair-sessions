#!/usr/bin/env python3
"""Generate, validate, archive, and email the Daily Agentic Business Pulse."""

from __future__ import annotations

import hashlib
import html
import imaplib
import json
import os
import re
import smtplib
import ssl
import tempfile
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from email import message_from_bytes
from email.message import EmailMessage, Message
from email.policy import default as default_email_policy
from email.utils import getaddresses
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


REQUIRED_SOURCES = ("salesforce", "jira", "glean", "production_code")
REQUIRED_SECTIONS = (
    "Bottom line",
    "Numbers that matter",
    "What matters",
    "Your focus",
    "Confidence",
)
LEGACY_REPORT_SECTIONS = (
    "Executive readout",
    "Revenue scoreboard",
    "Customer and EAP reality",
    "Jira and delivery risk",
    "Implementation reality",
    "Working / not working",
    "Decisions and actions",
    "Sources and confidence",
)
VISIBLE_EVIDENCE_LABELS = ("[Verified fact]", "[Signal]", "[Inference]", "[Unknown]", "[Decision]", "[Action]")
MAX_REPORT_WORDS = 650
IMPLEMENTATION_STATUSES = {
    "code_exists",
    "tested",
    "flagged",
    "instrumented",
    "deployed",
    "customer_exposed",
}
NON_PRODUCTION_ORIGINS = {"prototype", "mock", "fixture", "demo", "sandbox", "test_fixture"}
FORBIDDEN_KEYS = {
    "authorization",
    "credentials",
    "customer_payload",
    "password",
    "raw_customer_payload",
    "raw_payload",
    "request_body",
    "secret",
    "token",
    "tool_arguments",
    "transcript",
    "transcripts",
}
SECRET_PATTERNS = (
    re.compile(r"(?i)authorization\s*[:=]\s*(?:bearer|basic)\s+\S+"),
    re.compile(r"(?i)(?:api[_ -]?key|app[_ -]?password|access[_ -]?token|refresh[_ -]?token|secret)\s*[:=]\s*['\"]?\S{8,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
)
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
REPORT_SUBJECT_PREFIX = "Daily Agentic Business Pulse"
ONLY_ALLOWED_RECIPIENT = "amit.ayre@dialpad.com"
GLEAN_MACHINE_START = "---BEGIN PULSE MACHINE JSON---"
GLEAN_MACHINE_END = "---END PULSE MACHINE JSON---"


class PulseError(RuntimeError):
    """Base failure for safe, user-visible pulse errors."""


class IntegrationError(PulseError):
    """The approved company-data or email integration is unavailable."""


class ValidationError(PulseError):
    """Generated report data failed a send-blocking quality gate."""


def parse_bool(value: str | bool | None, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off", ""}:
        return False
    raise PulseError(f"Invalid boolean value: {value!r}")


def enforce_only_allowed_recipient(recipient: str) -> str:
    normalized = recipient.strip().casefold()
    if normalized != ONLY_ALLOWED_RECIPIENT:
        raise ValidationError(
            f"Pulse delivery is locked to {ONLY_ALLOWED_RECIPIENT}; refusing any other recipient"
        )
    return ONLY_ALLOWED_RECIPIENT


def enforce_message_recipient_contract(message: Message) -> None:
    recipient_headers = (
        message.get_all("To", [])
        + message.get_all("Cc", [])
        + message.get_all("Bcc", [])
    )
    addresses = [address.casefold() for _, address in getaddresses(recipient_headers) if address]
    if addresses != [ONLY_ALLOWED_RECIPIENT]:
        raise ValidationError(
            f"Pulse message must contain exactly one recipient: {ONLY_ALLOWED_RECIPIENT}"
        )


@dataclass(frozen=True)
class PulseConfig:
    recipient: str
    timezone_name: str
    agent_url: str
    agent_token: str
    gmail_user: str
    gmail_password: str
    source_context: tuple[str, ...]
    skill_path: Path
    reports_dir: Path
    dry_run: bool = False
    source_max_age_hours: int = 12
    agent_timeout_seconds: int = 600
    allow_insecure_agent_url: bool = False
    imap_host: str = "imap.gmail.com"
    smtp_host: str = "smtp.gmail.com"
    input_mode: str = "agent_api"
    glean_draft_wait_seconds: int = 900
    glean_draft_poll_seconds: int = 30

    @classmethod
    def from_env(cls, project_dir: Path) -> "PulseConfig":
        source_context_raw = os.environ.get("PULSE_SOURCE_CONTEXT_JSON", "").strip()
        try:
            source_context_value = json.loads(source_context_raw) if source_context_raw else []
        except json.JSONDecodeError as error:
            raise PulseError("PULSE_SOURCE_CONTEXT_JSON must be a JSON array of HTTPS links") from error
        if not isinstance(source_context_value, list) or not all(isinstance(item, str) for item in source_context_value):
            raise PulseError("PULSE_SOURCE_CONTEXT_JSON must be a JSON array of HTTPS links")
        return cls(
            recipient=enforce_only_allowed_recipient(
                os.environ.get("PULSE_RECIPIENT", ONLY_ALLOWED_RECIPIENT)
            ),
            timezone_name=os.environ.get("PULSE_TIMEZONE", "Asia/Kolkata").strip(),
            agent_url=os.environ.get("PULSE_AGENT_URL", "").strip(),
            agent_token=os.environ.get("PULSE_AGENT_TOKEN", "").strip(),
            gmail_user=os.environ.get("GMAIL_USER", "").strip(),
            gmail_password=os.environ.get("GMAIL_APP_PASSWORD", "").strip(),
            source_context=tuple(source_context_value),
            skill_path=Path(
                os.environ.get(
                    "PULSE_SKILL_PATH",
                    str(project_dir / "skills" / "daily-agentic-business-pulse" / "SKILL.md"),
                )
            ),
            reports_dir=Path(
                os.environ.get(
                    "PULSE_REPORTS_DIR",
                    str(project_dir / "reports" / "agentic_business_pulse"),
                )
            ),
            dry_run=parse_bool(os.environ.get("PULSE_DRY_RUN"), default=False),
            source_max_age_hours=int(os.environ.get("PULSE_SOURCE_MAX_AGE_HOURS", "12")),
            agent_timeout_seconds=int(os.environ.get("PULSE_AGENT_TIMEOUT_SECONDS", "600")),
            allow_insecure_agent_url=parse_bool(os.environ.get("PULSE_ALLOW_INSECURE_AGENT_URL"), default=False),
            imap_host=os.environ.get("PULSE_IMAP_HOST", "imap.gmail.com").strip(),
            smtp_host=os.environ.get("PULSE_SMTP_HOST", "smtp.gmail.com").strip(),
            input_mode=os.environ.get("PULSE_INPUT_MODE", "glean_gmail_draft").strip(),
            glean_draft_wait_seconds=int(os.environ.get("PULSE_GLEAN_DRAFT_WAIT_SECONDS", "900")),
            glean_draft_poll_seconds=int(os.environ.get("PULSE_GLEAN_DRAFT_POLL_SECONDS", "30")),
        )


def now_in_timezone(timezone_name: str, now: datetime | None = None) -> datetime:
    tz = ZoneInfo(timezone_name)
    if now is None:
        return datetime.now(tz)
    if now.tzinfo is None:
        raise PulseError("Injected current time must be timezone-aware")
    return now.astimezone(tz)


def workflow_url_from_env() -> str:
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
    repository = os.environ.get("GITHUB_REPOSITORY", "amitdialpad/design-pair-sessions").strip("/")
    run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
    return f"{server}/{repository}/actions/runs/{run_id}" if run_id else f"{server}/{repository}/actions"


def deterministic_message_id(report_date: str, dry_run: bool = False) -> str:
    mode = "dry-run-" if dry_run else ""
    return f"<{mode}daily-agentic-business-pulse-{report_date}@dialpad.com>"


def build_agent_request(
    *,
    report_now: datetime,
    skill_text: str,
    previous_snapshot: dict[str, Any] | None,
    workflow_url: str,
    source_context: tuple[str, ...],
) -> dict[str, Any]:
    report_date = report_now.date().isoformat()
    return {
        "task": "daily_agentic_business_pulse",
        "reporting": {
            "report_date": report_date,
            "generated_at": report_now.isoformat(),
            "timezone": str(report_now.tzinfo),
            "workflow_url": workflow_url,
        },
        "skill": {
            "name": "daily-agentic-business-pulse",
            "sha256": hashlib.sha256(skill_text.encode("utf-8")).hexdigest(),
            "instructions": skill_text,
        },
        "previous_snapshot": previous_snapshot,
        "source_context": list(source_context),
        "required_sources": list(REQUIRED_SOURCES),
        "response_contract": {
            "content_type": "application/json",
            "fields": ["report_markdown", "snapshot", "agent_request_id", "data_status", "failures"],
            "no_markdown_fence": True,
        },
    }


def invoke_company_agent(config: PulseConfig, payload: dict[str, Any]) -> dict[str, Any]:
    if not config.agent_url or not config.agent_token:
        raise IntegrationError(
            "Approved Glean Agent/API boundary is not configured. Set PULSE_AGENT_URL and "
            "PULSE_AGENT_TOKEN; no report was generated or sent."
        )

    parsed = urlparse(config.agent_url)
    if parsed.scheme != "https" and not config.allow_insecure_agent_url:
        raise IntegrationError("PULSE_AGENT_URL must use HTTPS")

    request = Request(
        config.agent_url,
        data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {config.agent_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "dialpad-agentic-business-pulse/1.0",
        },
    )

    try:
        with urlopen(request, timeout=config.agent_timeout_seconds, context=ssl.create_default_context()) as response:
            raw = response.read(5_000_001)
            if len(raw) > 5_000_000:
                raise IntegrationError("Glean Agent/API response exceeded 5 MB")
    except HTTPError as error:
        raise IntegrationError(f"Glean Agent/API returned HTTP {error.code}") from error
    except (URLError, TimeoutError) as error:
        raise IntegrationError(
            f"Glean Agent/API request failed: {error.reason if isinstance(error, URLError) else error}"
        ) from error

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as error:
        raise IntegrationError("Glean Agent/API returned invalid JSON") from error
    if not isinstance(result, dict):
        raise IntegrationError("Glean Agent/API response must be a JSON object")
    return result


def _require_mapping(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{path} must be an object")
    return value


def _require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValidationError(f"{path} must be a list")
    return value


def _require_number(value: Any, path: str, *, allow_null: bool = False) -> float | int | None:
    if value is None and allow_null:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{path} must be numeric, not unknown or bundled with another metric")
    return value


def _parse_datetime(value: Any, path: str) -> datetime:
    if not isinstance(value, str):
        raise ValidationError(f"{path} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValidationError(f"{path} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ValidationError(f"{path} must include a timezone")
    return parsed


def _valid_link(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _unwrap_gmail_redirect(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    parsed = urlparse(value)
    if parsed.netloc.casefold() not in {"google.com", "www.google.com"} or parsed.path != "/url":
        return value
    target = parse_qs(parsed.query).get("q", [None])[0]
    return target if _valid_link(target) else value


def _walk_forbidden_keys(value: Any, path: str = "snapshot") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_text = str(key).lower()
            if key_text in FORBIDDEN_KEYS:
                raise ValidationError(f"Sensitive or raw field is forbidden: {path}.{key}")
            _walk_forbidden_keys(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            _walk_forbidden_keys(nested, f"{path}[{index}]")


def _scan_sensitive_text(text: str, path: str) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise ValidationError(f"Potential credential or secret found in {path}")
    if EMAIL_PATTERN.search(text):
        raise ValidationError(f"Unredacted email address found in {path}")


def _visible_word_count(report: str) -> int:
    text = re.sub(r"\[([^]]+)]\(https://[^)]+\)", r"\1", report)
    text = re.sub(r"https://\S+", "", text)
    return len(re.findall(r"\b[\w$%.×'-]+\b", text))


def _report_section(report: str, section: str, next_section: str | None) -> str:
    start_match = re.search(rf"(?m)^## {re.escape(section)}\s*$", report)
    if not start_match:
        return ""
    end = len(report)
    if next_section:
        end_match = re.search(rf"(?m)^## {re.escape(next_section)}\s*$", report[start_match.end() :])
        if end_match:
            end = start_match.end() + end_match.start()
    return report[start_match.end() : end].strip()


def validate_agent_result(
    result: dict[str, Any],
    *,
    report_now: datetime,
    source_max_age_hours: int,
    workflow_url: str,
) -> tuple[str, dict[str, Any]]:
    failures = _require_list(result.get("failures", []), "failures")
    data_status = result.get("data_status")
    if data_status not in {"complete", "incomplete"}:
        raise ValidationError("data_status must be complete or incomplete")
    if data_status == "complete" and failures:
        raise ValidationError("A complete report cannot contain source or data failures")
    if data_status == "incomplete":
        failed_sources: list[str] = []
        for item in failures:
            item_source = item.get("source") if isinstance(item, dict) else str(item)
            matched = next((source for source in REQUIRED_SOURCES if source in str(item_source).lower()), None)
            if matched:
                failed_sources.append(matched)
        if failed_sources:
            labels = ", ".join(sorted(set(failed_sources)))
            raise IntegrationError(f"Required company source failed: {labels}. No report was sent.")

    report = result.get("report_markdown")
    if not isinstance(report, str) or not report.strip():
        raise ValidationError("report_markdown is required")
    report = report.rstrip() + "\n"
    snapshot = _require_mapping(result.get("snapshot"), "snapshot")
    report_date = report_now.date().isoformat()

    expected_title = f"# {REPORT_SUBJECT_PREFIX} — {report_date}"
    if not report.startswith(expected_title):
        raise ValidationError(f"Report must start with {expected_title!r}")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"(?m)^## {re.escape(section)}\s*$", report):
            raise ValidationError(f"Missing required report section: {section}")
    positions = [report.index(f"## {section}") for section in REQUIRED_SECTIONS]
    if positions != sorted(positions):
        raise ValidationError("Required report sections are out of order")
    for section in LEGACY_REPORT_SECTIONS:
        if re.search(rf"(?m)^## {re.escape(section)}\s*$", report):
            raise ValidationError(f"Legacy detail section is not allowed in the manager brief: {section}")
    for label in VISIBLE_EVIDENCE_LABELS:
        if label.casefold() in report.casefold():
            raise ValidationError(f"Evidence labels belong in the snapshot, not the human report: {label}")
    word_count = _visible_word_count(report)
    if word_count > MAX_REPORT_WORDS:
        raise ValidationError(f"Manager brief is {word_count} words; maximum is {MAX_REPORT_WORDS}")

    insight_body = _report_section(report, "What matters", "Your focus")
    insight_headings = re.findall(r"(?m)^### [^#\n].+$", insight_body)
    if len(insight_headings) != 3:
        raise ValidationError("What matters must contain exactly three insight headlines")
    if len(re.findall(r"(?m)^### [^#\n].+$", report)) != 3:
        raise ValidationError("Only the three What matters insight headlines may use level-three headings")

    numbers_body = _report_section(report, "Numbers that matter", "What matters")
    number_items = re.findall(r"(?m)^-\s+\S", numbers_body)
    if not 3 <= len(number_items) <= 4:
        raise ValidationError("Numbers that matter must contain three or four scannable metrics")

    focus_body = _report_section(report, "Your focus", "Confidence")
    focus_items = re.findall(r"(?m)^(?:-\s+|\d+[.)]\s+)\S", focus_body)
    if not 1 <= len(focus_items) <= 3:
        raise ValidationError("Your focus must contain one to three actions")

    if data_status == "incomplete":
        confidence_body = _report_section(report, "Confidence", None)
        if "data incomplete" not in confidence_body.casefold():
            raise ValidationError("An incomplete report must say Data incomplete in Confidence")

    if snapshot.get("schema_version") != 1:
        raise ValidationError("snapshot.schema_version must be 1")
    if snapshot.get("report_date") != report_date:
        raise ValidationError("Snapshot report date does not match the current IST date")

    generated_at = _parse_datetime(snapshot.get("generated_at"), "snapshot.generated_at")
    if generated_at.astimezone(report_now.tzinfo).date() != report_now.date():
        raise ValidationError("snapshot.generated_at is not on the current IST report date")

    comparison = _require_mapping(snapshot.get("comparison_window"), "snapshot.comparison_window")
    for field in ("start", "end", "label"):
        if not isinstance(comparison.get(field), str) or not comparison[field].strip():
            raise ValidationError(f"snapshot.comparison_window.{field} is required")
    try:
        comparison_start = date.fromisoformat(comparison["start"])
        comparison_end = date.fromisoformat(comparison["end"])
    except ValueError as error:
        raise ValidationError("Comparison-window start and end must be ISO dates") from error
    if comparison_start > comparison_end or comparison_end > report_now.date():
        raise ValidationError("Comparison window cannot end after the current report date")
    if comparison["label"] not in report:
        raise ValidationError("Report must state the snapshot comparison-window label")

    metrics = _require_mapping(snapshot.get("metrics"), "snapshot.metrics")
    revenue = _require_mapping(metrics.get("revenue"), "snapshot.metrics.revenue")
    pipeline = _require_mapping(metrics.get("pipeline"), "snapshot.metrics.pipeline")
    for field in (
        "booked_agentic_acv",
        "booked_total_bundled_amount",
        "target_agentic_acv",
        "gap_agentic_acv",
        "attainment_pct",
        "pace_agentic_acv",
    ):
        _require_number(
            revenue.get(field),
            f"snapshot.metrics.revenue.{field}",
            allow_null=data_status == "incomplete",
        )
    for field in (
        "qualified_agentic_acv",
        "total_bundled_opportunity_amount",
        "coverage_ratio",
    ):
        _require_number(
            pipeline.get(field),
            f"snapshot.metrics.pipeline.{field}",
            allow_null=data_status == "incomplete",
        )
    _require_mapping(metrics.get("onboarding"), "snapshot.metrics.onboarding")
    _require_mapping(metrics.get("eap"), "snapshot.metrics.eap")

    source_status = _require_mapping(snapshot.get("source_status"), "snapshot.source_status")
    freshness_cutoff = report_now.astimezone(timezone.utc) - timedelta(hours=source_max_age_hours)
    future_limit = report_now.astimezone(timezone.utc) + timedelta(minutes=10)
    for source in REQUIRED_SOURCES:
        state = _require_mapping(source_status.get(source), f"snapshot.source_status.{source}")
        if state.get("status") != "ok":
            raise IntegrationError(f"Required source {source} is not healthy; no report was sent")
        queried_at = _parse_datetime(state.get("queried_at"), f"snapshot.source_status.{source}.queried_at")
        queried_utc = queried_at.astimezone(timezone.utc)
        if queried_utc < freshness_cutoff or queried_utc > future_limit:
            raise ValidationError(f"Required source {source} is stale or future-dated")
        links = _require_list(state.get("links"), f"snapshot.source_status.{source}.links")
        if not links or not all(_valid_link(link) for link in links):
            raise ValidationError(f"Required source {source} needs at least one HTTPS evidence link")
        if not any(link in report for link in links):
            raise ValidationError(f"Report does not cite any registered {source} evidence link")

    customers = _require_list(snapshot.get("customers"), "snapshot.customers")
    for index, customer_value in enumerate(customers):
        customer = _require_mapping(customer_value, f"snapshot.customers[{index}]")
        if customer.get("name_permitted") is not True:
            raise ValidationError(f"snapshot.customers[{index}] must use a permitted or redacted account name")
        if not isinstance(customer.get("account_name"), str) or not customer["account_name"].strip():
            raise ValidationError(f"snapshot.customers[{index}].account_name is required")
        if len(str(customer.get("summary", ""))) > 500:
            raise ValidationError(f"snapshot.customers[{index}].summary is too long")

    _require_list(snapshot.get("jira_items"), "snapshot.jira_items")
    claims = _require_list(snapshot.get("implementation_claims"), "snapshot.implementation_claims")
    for index, claim_value in enumerate(claims):
        claim = _require_mapping(claim_value, f"snapshot.implementation_claims[{index}]")
        statuses = set(_require_list(claim.get("statuses"), f"snapshot.implementation_claims[{index}].statuses"))
        if not statuses or not statuses.issubset(IMPLEMENTATION_STATUSES):
            raise ValidationError(f"snapshot.implementation_claims[{index}] has invalid implementation statuses")
        origin = str(claim.get("evidence_origin", "")).lower()
        is_fixture = claim.get("is_fixture") is True or origin in NON_PRODUCTION_ORIGINS
        if is_fixture and statuses.intersection({"deployed", "customer_exposed"}):
            raise ValidationError("Prototype, mock, demo, or fixture evidence cannot be labeled deployed/customer-exposed")
        links = _require_list(claim.get("links"), f"snapshot.implementation_claims[{index}].links")
        if not links or not all(_valid_link(link) for link in links):
            raise ValidationError(f"snapshot.implementation_claims[{index}] needs HTTPS implementation evidence")

    for field in ("decisions", "changes_since_previous", "unknowns"):
        _require_list(snapshot.get(field), f"snapshot.{field}")
    if data_status == "incomplete" and not failures and not snapshot["unknowns"]:
        raise ValidationError("An incomplete report must identify at least one failure or unknown")
    snapshot["data_status"] = data_status

    if workflow_url not in report:
        raise ValidationError("Sources and confidence must include the workflow run URL")
    _walk_forbidden_keys(snapshot)
    _scan_sensitive_text(report, "report_markdown")
    _scan_sensitive_text(json.dumps(snapshot, sort_keys=True), "snapshot")

    snapshot["report_sha256"] = hashlib.sha256(report.encode("utf-8")).hexdigest()
    run_metadata = _require_mapping(snapshot.get("run", {}), "snapshot.run")
    agent_request_id = str(result.get("agent_request_id", ""))
    if agent_request_id:
        if not re.fullmatch(r"[A-Za-z0-9._:-]{1,200}", agent_request_id):
            raise ValidationError("agent_request_id contains unsafe characters")
        run_metadata["agent_request_id"] = agent_request_id
    run_metadata["workflow_url"] = workflow_url
    snapshot["run"] = run_metadata
    _walk_forbidden_keys(snapshot)
    _scan_sensitive_text(json.dumps(snapshot, sort_keys=True), "snapshot")
    return report, snapshot


def _inline_markdown(value: str) -> str:
    escaped = html.escape(value, quote=True)
    escaped = re.sub(
        r"\[([^]]+)]\((https://[^)]+)\)",
        r'<a href="\2" style="color:#5f45bd;text-decoration:underline">\1</a>',
        escaped,
    )
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    escaped = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code style=\"background:#f3f1f8;padding:1px 4px\">\1</code>", escaped)
    return escaped


def markdown_to_email_html(report: str) -> str:
    parts: list[str] = []
    in_list = False
    list_type = "ul"
    current_section = ""

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            parts.append(f"</{list_type}>")
            in_list = False

    for raw_line in report.splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            close_list()
            parts.append('<div style="width:48px;height:4px;background:#7c5ce7;border-radius:4px;margin:0 0 22px"></div>')
            parts.append(f'<h1 style="font-size:28px;line-height:1.2;letter-spacing:-0.4px;margin:0 0 12px;color:#19171c">{_inline_markdown(line[2:])}</h1>')
        elif line.startswith("## "):
            close_list()
            current_section = line[3:]
            parts.append(f'<h2 style="font-size:17px;line-height:1.3;margin:30px 0 12px;color:#19171c">{_inline_markdown(current_section)}</h2>')
        elif line.startswith("### "):
            close_list()
            parts.append(f'<h3 style="font-size:16px;line-height:1.35;margin:22px 0 6px;color:#33295c">{_inline_markdown(line[4:])}</h3>')
        elif line.startswith("- "):
            if current_section == "Numbers that matter":
                close_list()
                parts.append(
                    '<div style="border:1px solid #e7e2f2;border-radius:10px;padding:12px 14px;'
                    f'margin:0 0 8px;background:#faf9fd">{_inline_markdown(line[2:])}</div>'
                )
            else:
                if not in_list:
                    list_type = "ul"
                    parts.append('<ul style="padding-left:21px;margin:0 0 16px">')
                    in_list = True
                parts.append(f'<li style="margin:0 0 9px;padding-left:2px">{_inline_markdown(line[2:])}</li>')
        elif re.match(r"^\d+[.)]\s+", line):
            if not in_list:
                list_type = "ol"
                parts.append('<ol style="padding-left:24px;margin:0 0 16px">')
                in_list = True
            item = re.sub(r"^\d+[.)]\s+", "", line)
            parts.append(f'<li style="margin:0 0 11px;padding-left:3px">{_inline_markdown(item)}</li>')
        elif not line:
            close_list()
        else:
            close_list()
            if current_section == "Bottom line":
                style = "margin:0;padding:17px 18px;background:#f2effb;border-left:4px solid #7c5ce7;border-radius:8px;font-size:16px;line-height:1.55"
            elif current_section == "Confidence":
                style = "margin:0 0 8px;color:#65606d;font-size:13px;line-height:1.55"
            elif not current_section and line.startswith(("_", "*")):
                style = "margin:0 0 22px;color:#716b79;font-size:13px"
            else:
                style = "margin:0 0 14px"
            parts.append(f'<p style="{style}">{_inline_markdown(line)}</p>')
    close_list()
    body = "\n".join(parts)
    return (
        '<!doctype html><html><body style="margin:0;background:#f5f4f7;padding:24px 10px">'
        '<main style="max-width:680px;margin:0 auto;padding:38px 34px;background:#ffffff;border:1px solid #ebe8ef;border-radius:14px;'
        "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;"
        f'font-size:15px;line-height:1.6;color:#312e35">{body}</main></body></html>'
    )


def build_email_message(
    *,
    report_date: str,
    report: str,
    snapshot: dict[str, Any],
    sender: str,
    recipient: str,
    message_id: str,
    dry_run: bool,
) -> EmailMessage:
    recipient = enforce_only_allowed_recipient(recipient)
    subject_prefix = "[DRY RUN] " if dry_run else ""
    message = EmailMessage()
    message["Subject"] = f"{subject_prefix}{REPORT_SUBJECT_PREFIX} — {report_date}"
    message["From"] = f"Daily Agentic Business Pulse <{sender}>"
    message["To"] = recipient
    message["Message-ID"] = message_id
    message["X-Dialpad-Pulse-Date"] = report_date
    message["X-Dialpad-Pulse-Mode"] = "dry-run" if dry_run else "live"
    message.set_content(report)
    message.add_alternative(markdown_to_email_html(report), subtype="html")
    message.add_attachment(
        report.encode("utf-8"),
        maintype="text",
        subtype="markdown",
        filename=f"{report_date}.md",
    )
    message.add_attachment(
        (json.dumps(snapshot, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        maintype="application",
        subtype="json",
        filename=f"{report_date}.json",
    )
    return message


class _HTMLToText(HTMLParser):
    """Minimal HTML-to-text conversion for Gmail draft bodies."""

    BLOCK_TAGS = {"br", "div", "h1", "h2", "h3", "li", "p", "pre", "tr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts).replace("\r\n", "\n").replace("\r", "\n")


def _decoded_part_text(part: Message) -> str:
    payload = part.get_payload(decode=True)
    if not isinstance(payload, bytes):
        return str(part.get_payload())
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset)
    except (LookupError, UnicodeDecodeError):
        return payload.decode("utf-8", errors="replace")


def message_body_text(message: Message) -> str:
    """Return a draft body as text while preserving the machine JSON markers."""

    candidates: list[tuple[str, str]] = []
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_disposition() == "attachment":
                continue
            content_type = part.get_content_type()
            if content_type in {"text/plain", "text/html"}:
                candidates.append((content_type, _decoded_part_text(part)))
    else:
        candidates.append((message.get_content_type(), _decoded_part_text(message)))

    for content_type, body in candidates:
        if GLEAN_MACHINE_START not in body or GLEAN_MACHINE_END not in body:
            continue
        if content_type == "text/html":
            parser = _HTMLToText()
            parser.feed(body)
            return parser.text()
        return body.replace("\r\n", "\n").replace("\r", "\n")
    raise ValidationError("Glean Gmail draft is missing the machine-readable report block")


def parse_glean_draft(message: Message, *, report_date: str, workflow_url: str) -> dict[str, Any]:
    """Validate the Glean-created envelope and recover its structured agent result."""

    expected_subject = f"{REPORT_SUBJECT_PREFIX} — {report_date}"
    if str(message.get("Subject", "")).strip() != expected_subject:
        raise ValidationError(f"Glean Gmail draft subject must be {expected_subject!r}")
    enforce_message_recipient_contract(message)

    body = message_body_text(message)
    if body.count(GLEAN_MACHINE_START) != 1 or body.count(GLEAN_MACHINE_END) != 1:
        raise ValidationError("Glean Gmail draft must contain exactly one machine-readable report block")
    _, remainder = body.split(GLEAN_MACHINE_START, 1)
    machine_json, _ = remainder.split(GLEAN_MACHINE_END, 1)
    try:
        result = json.loads(machine_json.strip())
    except json.JSONDecodeError as error:
        raise ValidationError("Glean Gmail draft machine block is not valid JSON") from error
    if not isinstance(result, dict):
        raise ValidationError("Glean Gmail draft machine block must be a JSON object")

    report = result.get("report_markdown")
    if not isinstance(report, str) or not report.strip():
        raise ValidationError("Glean Gmail draft machine block must include report_markdown")
    report = report.rstrip() + "\n"
    report = re.sub(
        r"https://(?:www\.)?google\.com/url\?[^)\s\"']+",
        lambda match: str(_unwrap_gmail_redirect(match.group(0))),
        report,
    )
    report = re.sub(
        r"&(?:amp;)?source=gmail(?:&(?:amp;)?ust=\d+)?(?:&(?:amp;)?sa=[A-Za-z])?",
        "",
        report,
    )
    undated_title = f"# {REPORT_SUBJECT_PREFIX}\n"
    if report.startswith(undated_title):
        report = f"# {REPORT_SUBJECT_PREFIX} — {report_date}\n" + report[len(undated_title):]
    if workflow_url not in report:
        report += f"\n[Workflow run]({workflow_url})\n"
    result["report_markdown"] = report
    agent_request_id = result.get("agent_request_id")
    if isinstance(agent_request_id, str) and not re.fullmatch(r"[A-Za-z0-9._:-]{1,200}", agent_request_id):
        request_url = _unwrap_gmail_redirect(agent_request_id)
        request_path = urlparse(request_url).path if isinstance(request_url, str) else ""
        request_slug = request_path.rstrip("/").rsplit("/", 1)[-1]
        if re.fullmatch(r"[A-Za-z0-9._:-]{1,200}", request_slug):
            result["agent_request_id"] = request_slug
        else:
            result["agent_request_id"] = f"glean-{hashlib.sha256(agent_request_id.encode()).hexdigest()[:32]}"

    snapshot = _require_mapping(result.get("snapshot"), "snapshot")
    if isinstance(snapshot.get("changes_since_previous"), dict):
        snapshot["changes_since_previous"] = [snapshot["changes_since_previous"]]
    metrics = _require_mapping(snapshot.get("metrics"), "snapshot.metrics")
    aggregate = snapshot.get("aggregate")
    if isinstance(aggregate, dict):
        for field in ("onboarding", "eap"):
            if field not in metrics and isinstance(aggregate.get(field), dict):
                metrics[field] = aggregate[field]
    comparison = _require_mapping(snapshot.get("comparison_window"), "snapshot.comparison_window")
    for canonical, glean_name in (("start", "iso_start"), ("end", "iso_end")):
        if canonical not in comparison and isinstance(comparison.get(glean_name), str):
            comparison[canonical] = comparison.pop(glean_name)

    source_status = _require_mapping(snapshot.get("source_status"), "snapshot.source_status")
    for source in REQUIRED_SOURCES:
        state = _require_mapping(source_status.get(source), f"snapshot.source_status.{source}")
        if "links" not in state and isinstance(state.get("evidence_links"), list):
            state["links"] = state.pop("evidence_links")
        if isinstance(state.get("links"), list):
            state["links"] = [_unwrap_gmail_redirect(link) for link in state["links"]]
        status = state.get("status")
        if isinstance(status, str) and status != "ok":
            normalized = status.casefold().strip()
            if normalized.startswith(("complete", "partial", "refresh", "fresh")):
                state["detail"] = status
                state["status"] = "ok"

    customers = _require_list(snapshot.get("customers"), "snapshot.customers")
    for customer_value in customers:
        customer = _require_mapping(customer_value, "snapshot.customers[]")
        if "account_name" not in customer and isinstance(customer.get("name"), str):
            customer["account_name"] = customer.pop("name")
            customer.setdefault("name_permitted", True)
        account_name = customer.get("account_name")
        if (
            "name_permitted" not in customer
            and isinstance(account_name, str)
            and account_name.strip()
            and account_name in report
        ):
            customer["name_permitted"] = True

    jira_state = _require_mapping(source_status.get("jira"), "snapshot.source_status.jira")
    jira_links = _require_list(jira_state.get("links"), "snapshot.source_status.jira.links")
    for jira_value in _require_list(snapshot.get("jira_items"), "snapshot.jira_items"):
        jira_item = _require_mapping(jira_value, "snapshot.jira_items[]")
        item_links = jira_item.get("links", [])
        if isinstance(jira_item.get("link"), str):
            item_links = [*item_links, jira_item["link"]] if isinstance(item_links, list) else [jira_item["link"]]
        for link in item_links if isinstance(item_links, list) else []:
            normalized_link = _unwrap_gmail_redirect(link)
            if _valid_link(normalized_link) and normalized_link not in jira_links:
                jira_links.append(normalized_link)

    claims = _require_list(snapshot.get("implementation_claims"), "snapshot.implementation_claims")
    negative_statuses = (
        "unknown",
        "not applicable",
        "not verified",
        "not production",
        "not customer evidence",
        "no evidence",
        "none",
        "false",
    )
    for claim_value in claims:
        claim = _require_mapping(claim_value, "snapshot.implementation_claims[]")
        statuses = claim.get("statuses")
        if isinstance(claim.get("links"), list):
            claim["links"] = [_unwrap_gmail_redirect(link) for link in claim["links"]]
        if isinstance(statuses, dict):
            normalized_statuses: list[str] = []
            for status_name, evidence in statuses.items():
                evidence_text = str(evidence).casefold().strip()
                if status_name not in IMPLEMENTATION_STATUSES:
                    continue
                if not evidence_text or any(evidence_text.startswith(value) for value in negative_statuses):
                    continue
                normalized_statuses.append(status_name)
            claim["status_details"] = statuses
            claim["statuses"] = normalized_statuses
    return result


class GmailArchive:
    """Private report persistence and idempotency through the existing Gmail account."""

    def __init__(self, user: str, password: str, host: str = "imap.gmail.com") -> None:
        if not user or not password:
            raise IntegrationError("Gmail credentials are required for private persistence and idempotency")
        self.user = user
        self.password = password
        self.host = host

    def _connect(self) -> imaplib.IMAP4_SSL:
        try:
            client = imaplib.IMAP4_SSL(self.host, 993, ssl_context=ssl.create_default_context())
            client.login(self.user, self.password)
            return client
        except (imaplib.IMAP4.error, OSError) as error:
            raise IntegrationError(f"Gmail archive connection failed: {error}") from error

    @staticmethod
    def _special_mailbox(client: imaplib.IMAP4_SSL, flag: str, fallback: str) -> str:
        status, rows = client.list()
        if status == "OK" and rows:
            for row in rows:
                decoded = row.decode("utf-8", errors="replace")
                if flag.lower() not in decoded.lower():
                    continue
                match = re.match(r'^\((?P<flags>[^)]*)\)\s+"[^"]*"\s+(?P<name>.+)$', decoded)
                if match:
                    name = match.group("name").strip()
                    if name.startswith('"') and name.endswith('"'):
                        name = name[1:-1].replace(r'\"', '"')
                    return name
        return fallback

    @staticmethod
    def _select(client: imaplib.IMAP4_SSL, mailbox: str, readonly: bool) -> bool:
        mailbox_argument = mailbox
        if not (mailbox.startswith('"') and mailbox.endswith('"')):
            escaped = mailbox.replace("\\", "\\\\").replace('"', '\\"')
            mailbox_argument = f'"{escaped}"'
        status, _ = client.select(mailbox_argument, readonly=readonly)
        return status == "OK"

    def _message_exists(self, message_id: str, flag: str, fallback: str) -> bool:
        client = self._connect()
        try:
            mailbox = self._special_mailbox(client, flag, fallback)
            if not self._select(client, mailbox, readonly=True):
                raise IntegrationError(f"Could not select Gmail mailbox {mailbox!r} for idempotency check")
            status, data = client.uid("search", None, "HEADER", "Message-ID", f'"{message_id}"')
            if status != "OK":
                raise IntegrationError("Gmail idempotency search failed")
            return bool(data and data[0].strip())
        finally:
            try:
                client.logout()
            except Exception:
                pass

    def sent_message_exists(self, message_id: str) -> bool:
        try:
            return self._message_exists(message_id, r"\Sent", "[Gmail]/Sent Mail")
        except IntegrationError:
            return self._message_exists(message_id, r"\Inbox", "INBOX")

    def draft_message_exists(self, message_id: str) -> bool:
        return self._message_exists(message_id, r"\Drafts", "[Gmail]/Drafts")

    def find_glean_draft(self, report_date: str) -> tuple[str, Message] | None:
        """Find the one Glean-created draft for an IST report date."""

        client = self._connect()
        try:
            mailbox = self._special_mailbox(client, r"\Drafts", "[Gmail]/Drafts")
            if not self._select(client, mailbox, readonly=True):
                raise IntegrationError("Could not select Gmail Drafts for the Glean report")
            status, data = client.uid("search", None, "SUBJECT", f'"{REPORT_SUBJECT_PREFIX}"')
            if status != "OK":
                raise IntegrationError("Gmail Glean-draft search failed")
            expected_subject = f"{REPORT_SUBJECT_PREFIX} — {report_date}"
            matches: list[tuple[str, Message]] = []
            for uid in reversed((data[0].split() if data and data[0] else [])[-40:]):
                status, rows = client.uid("fetch", uid, "(RFC822)")
                if status != "OK" or not rows:
                    continue
                raw = next((item[1] for item in rows if isinstance(item, tuple) and len(item) > 1), None)
                if not raw:
                    continue
                message = message_from_bytes(raw, policy=default_email_policy)
                if str(message.get("Subject", "")).strip() != expected_subject:
                    continue
                try:
                    enforce_message_recipient_contract(message)
                except ValidationError:
                    continue
                matches.append((uid.decode("ascii"), message))
            if len(matches) > 1:
                raise IntegrationError(
                    f"Multiple Glean drafts exist for {report_date}; refusing an ambiguous or duplicate send"
                )
            return matches[0] if matches else None
        finally:
            try:
                client.logout()
            except Exception:
                pass

    def wait_for_glean_draft(
        self,
        report_date: str,
        *,
        wait_seconds: int,
        poll_seconds: int,
    ) -> tuple[str, Message]:
        if wait_seconds < 0 or poll_seconds < 1:
            raise PulseError("Glean draft wait must be non-negative and polling must be at least one second")
        deadline = time.monotonic() + wait_seconds
        while True:
            found = self.find_glean_draft(report_date)
            if found:
                return found
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise IntegrationError(
                    f"No validated Glean draft appeared for {report_date} within {wait_seconds} seconds"
                )
            time.sleep(min(poll_seconds, remaining))

    def load_previous_snapshot(self, current_report_date: str) -> dict[str, Any] | None:
        client = self._connect()
        try:
            mailbox = self._special_mailbox(client, r"\Sent", "INBOX")
            if not self._select(client, mailbox, readonly=True):
                if not self._select(client, "INBOX", readonly=True):
                    raise IntegrationError("Could not select Gmail Sent or Inbox for previous snapshot")
            status, data = client.uid("search", None, "SUBJECT", f'"{REPORT_SUBJECT_PREFIX}"')
            if status != "OK":
                raise IntegrationError("Gmail previous-snapshot search failed")
            message_uids = data[0].split() if data and data[0] else []
            candidates: list[tuple[str, dict[str, Any]]] = []
            for uid in reversed(message_uids[-40:]):
                status, rows = client.uid("fetch", uid, "(RFC822)")
                if status != "OK" or not rows:
                    continue
                raw = next((item[1] for item in rows if isinstance(item, tuple) and len(item) > 1), None)
                if not raw:
                    continue
                message = message_from_bytes(raw, policy=default_email_policy)
                for part in message.walk():
                    filename = part.get_filename() or ""
                    if not filename.endswith(".json"):
                        continue
                    try:
                        snapshot = json.loads(part.get_payload(decode=True).decode("utf-8"))
                    except (AttributeError, UnicodeDecodeError, json.JSONDecodeError):
                        continue
                    report_date_value = snapshot.get("report_date") if isinstance(snapshot, dict) else None
                    if isinstance(report_date_value, str) and report_date_value < current_report_date:
                        candidates.append((report_date_value, snapshot))
            return max(candidates, key=lambda item: item[0])[1] if candidates else None
        finally:
            try:
                client.logout()
            except Exception:
                pass

    def persist_draft(self, message: Message) -> str | None:
        client = self._connect()
        try:
            mailbox = self._special_mailbox(client, r"\Drafts", "[Gmail]/Drafts")
            status, data = client.append(
                mailbox,
                r"(\Draft \Seen)",
                imaplib.Time2Internaldate(datetime.now(timezone.utc)),
                message.as_bytes(),
            )
            if status != "OK":
                raise IntegrationError("Could not persist report and snapshot as a Gmail draft")
            response = b" ".join(item for item in data or [] if isinstance(item, bytes)).decode("ascii", errors="ignore")
            match = re.search(r"APPENDUID\s+\d+\s+(\d+)", response)
            return match.group(1) if match else None
        finally:
            try:
                client.logout()
            except Exception:
                pass

    def delete_draft(self, draft_uid: str | None) -> None:
        if not draft_uid:
            return
        client = self._connect()
        try:
            mailbox = self._special_mailbox(client, r"\Drafts", "[Gmail]/Drafts")
            if not self._select(client, mailbox, readonly=False):
                return
            status, _ = client.uid("store", draft_uid, "+FLAGS.SILENT", r"(\Deleted)")
            if status == "OK":
                client.expunge()
        finally:
            try:
                client.logout()
            except Exception:
                pass


def send_gmail(message: EmailMessage, config: PulseConfig) -> dict[str, Any]:
    enforce_only_allowed_recipient(config.recipient)
    enforce_message_recipient_contract(message)
    if not config.gmail_user or not config.gmail_password:
        raise IntegrationError("GMAIL_USER and GMAIL_APP_PASSWORD are required")
    try:
        with smtplib.SMTP(config.smtp_host, 587, timeout=60) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(config.gmail_user, config.gmail_password)
            refused = server.send_message(message)
    except (smtplib.SMTPException, OSError) as error:
        raise IntegrationError(f"Gmail send failed: {error}") from error
    if refused:
        raise IntegrationError("Gmail refused one or more recipients")
    return {
        "status": "accepted",
        "provider": "gmail_smtp",
        "message_id": str(message["Message-ID"]),
    }


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_name, 0o600)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def persist_output_files(reports_dir: Path, report_date: str, report: str, snapshot: dict[str, Any]) -> tuple[Path, Path]:
    report_path = reports_dir / f"{report_date}.md"
    snapshot_path = reports_dir / f"{report_date}.json"
    _atomic_write(report_path, report)
    _atomic_write(snapshot_path, json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    return report_path, snapshot_path


def write_run_result(reports_dir: Path, report_date: str, result: dict[str, Any]) -> Path:
    path = reports_dir / f"{report_date}.run.json"
    _atomic_write(path, json.dumps(result, indent=2, sort_keys=True) + "\n")
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "").strip()
    if summary_path:
        lines = [
            "## Daily Agentic Business Pulse",
            "",
            f"- Report date: `{report_date}`",
            f"- Run status: `{result.get('run_status', 'unknown')}`",
            f"- Email status: `{result.get('email_status', 'not_attempted')}`",
            f"- Message ID: `{result.get('message_id', 'none')}`",
            f"- Workflow: {result.get('workflow_url', workflow_url_from_env())}",
        ]
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
    return path


def run_pulse(
    config: PulseConfig,
    *,
    current_time: datetime | None = None,
    agent: Callable[[PulseConfig, dict[str, Any]], dict[str, Any]] = invoke_company_agent,
    archive: GmailArchive | None = None,
    sender: Callable[[EmailMessage, PulseConfig], dict[str, Any]] = send_gmail,
) -> dict[str, Any]:
    enforce_only_allowed_recipient(config.recipient)
    report_now = now_in_timezone(config.timezone_name, current_time)
    report_date = report_now.date().isoformat()
    workflow_url = workflow_url_from_env()
    live_message_id = deterministic_message_id(report_date, dry_run=False)

    if not config.skill_path.is_file():
        raise IntegrationError(f"Complete pulse skill is missing: {config.skill_path}")
    skill_text = config.skill_path.read_text(encoding="utf-8")
    if len(skill_text.splitlines()) < 100:
        raise IntegrationError("Pulse skill appears truncated; refusing to replace it with a short prompt")
    if len(config.source_context) != 3 or not all(_valid_link(link) for link in config.source_context):
        raise IntegrationError(
            "PULSE_SOURCE_CONTEXT_JSON must contain the three approved HTTPS document links; "
            "no report was generated or sent."
        )

    gmail_archive = archive or GmailArchive(config.gmail_user, config.gmail_password, config.imap_host)
    if not config.dry_run and gmail_archive.sent_message_exists(live_message_id):
        result = {
            "report_date": report_date,
            "run_status": "duplicate_skipped",
            "email_status": "already_sent",
            "message_id": live_message_id,
            "workflow_url": workflow_url,
        }
        write_run_result(config.reports_dir, report_date, result)
        return result
    if not config.dry_run and gmail_archive.draft_message_exists(live_message_id):
        raise IntegrationError(
            "A prepared live report already exists in Gmail Drafts but no Sent copy was confirmed. "
            "The prior delivery state is ambiguous, so this retry will not risk a duplicate send."
        )

    previous_snapshot = gmail_archive.load_previous_snapshot(report_date)
    payload = build_agent_request(
        report_now=report_now,
        skill_text=skill_text,
        previous_snapshot=previous_snapshot,
        workflow_url=workflow_url,
        source_context=config.source_context,
    )
    agent_result = agent(config, payload)
    report, snapshot = validate_agent_result(
        agent_result,
        report_now=report_now,
        source_max_age_hours=config.source_max_age_hours,
        workflow_url=workflow_url,
    )
    message_id = deterministic_message_id(report_date, dry_run=config.dry_run)
    snapshot["delivery"] = {
        "message_id": message_id,
        "mode": "dry_run" if config.dry_run else "live",
    }
    report_path, snapshot_path = persist_output_files(config.reports_dir, report_date, report, snapshot)

    message = build_email_message(
        report_date=report_date,
        report=report,
        snapshot=snapshot,
        sender=config.gmail_user,
        recipient=config.recipient,
        message_id=message_id,
        dry_run=config.dry_run,
    )
    draft_uid = gmail_archive.persist_draft(message)

    if config.dry_run:
        result = {
            "report_date": report_date,
            "run_status": "dry_run_complete",
            "email_status": "not_sent_draft_persisted",
            "message_id": message_id,
            "workflow_url": workflow_url,
            "report_path": str(report_path),
            "snapshot_path": str(snapshot_path),
            "source_freshness": {
                source: snapshot["source_status"][source]["queried_at"] for source in REQUIRED_SOURCES
            },
        }
        write_run_result(config.reports_dir, report_date, result)
        return result

    email_result = sender(message, config)
    gmail_archive.delete_draft(draft_uid)
    result = {
        "report_date": report_date,
        "run_status": "success",
        "email_status": email_result["status"],
        "email_provider": email_result["provider"],
        "message_id": email_result["message_id"],
        "workflow_url": workflow_url,
        "report_path": str(report_path),
        "snapshot_path": str(snapshot_path),
        "source_freshness": {
            source: snapshot["source_status"][source]["queried_at"] for source in REQUIRED_SOURCES
        },
    }
    write_run_result(config.reports_dir, report_date, result)
    return result


def run_pulse_from_glean_draft(
    config: PulseConfig,
    *,
    current_time: datetime | None = None,
    archive: GmailArchive | None = None,
    sender: Callable[[EmailMessage, PulseConfig], dict[str, Any]] = send_gmail,
) -> dict[str, Any]:
    """Validate and deliver the output of a native scheduled Glean Agent run."""

    enforce_only_allowed_recipient(config.recipient)
    report_now = now_in_timezone(config.timezone_name, current_time)
    report_date = report_now.date().isoformat()
    workflow_url = workflow_url_from_env()
    live_message_id = deterministic_message_id(report_date, dry_run=False)

    if not config.skill_path.is_file():
        raise IntegrationError(f"Complete pulse skill is missing: {config.skill_path}")
    if len(config.skill_path.read_text(encoding="utf-8").splitlines()) < 100:
        raise IntegrationError("Pulse skill appears truncated; refusing to validate a shortened prompt")

    gmail_archive = archive or GmailArchive(config.gmail_user, config.gmail_password, config.imap_host)
    if not config.dry_run and gmail_archive.sent_message_exists(live_message_id):
        result = {
            "report_date": report_date,
            "run_status": "duplicate_skipped",
            "email_status": "already_sent",
            "message_id": live_message_id,
            "workflow_url": workflow_url,
        }
        write_run_result(config.reports_dir, report_date, result)
        return result
    prepared_message_id = deterministic_message_id(report_date, dry_run=config.dry_run)
    if gmail_archive.draft_message_exists(prepared_message_id):
        raise IntegrationError(
            "A validated relay draft already exists but no matching Sent copy was confirmed. "
            "The prior delivery state is ambiguous, so this retry will not risk a duplicate."
        )

    source_draft_uid, source_message = gmail_archive.wait_for_glean_draft(
        report_date,
        wait_seconds=config.glean_draft_wait_seconds,
        poll_seconds=config.glean_draft_poll_seconds,
    )
    agent_result = parse_glean_draft(
        source_message,
        report_date=report_date,
        workflow_url=workflow_url,
    )
    report, snapshot = validate_agent_result(
        agent_result,
        report_now=report_now,
        source_max_age_hours=config.source_max_age_hours,
        workflow_url=workflow_url,
    )
    snapshot["delivery"] = {
        "message_id": prepared_message_id,
        "mode": "dry_run" if config.dry_run else "live",
        "input": "scheduled_glean_gmail_draft",
    }
    report_path, snapshot_path = persist_output_files(config.reports_dir, report_date, report, snapshot)
    message = build_email_message(
        report_date=report_date,
        report=report,
        snapshot=snapshot,
        sender=config.gmail_user,
        recipient=config.recipient,
        message_id=prepared_message_id,
        dry_run=config.dry_run,
    )
    prepared_draft_uid = gmail_archive.persist_draft(message)

    if config.dry_run:
        result = {
            "report_date": report_date,
            "run_status": "dry_run_complete",
            "email_status": "not_sent_draft_persisted",
            "message_id": prepared_message_id,
            "workflow_url": workflow_url,
            "report_path": str(report_path),
            "snapshot_path": str(snapshot_path),
            "source_freshness": {
                source: snapshot["source_status"][source]["queried_at"] for source in REQUIRED_SOURCES
            },
            "agent_request_id": agent_result.get("agent_request_id", "not_provided"),
        }
        write_run_result(config.reports_dir, report_date, result)
        return result

    email_result = sender(message, config)
    gmail_archive.delete_draft(prepared_draft_uid)
    gmail_archive.delete_draft(source_draft_uid)
    result = {
        "report_date": report_date,
        "run_status": "success",
        "email_status": email_result["status"],
        "email_provider": email_result["provider"],
        "message_id": email_result["message_id"],
        "workflow_url": workflow_url,
        "report_path": str(report_path),
        "snapshot_path": str(snapshot_path),
        "source_freshness": {
            source: snapshot["source_status"][source]["queried_at"] for source in REQUIRED_SOURCES
        },
        "agent_request_id": agent_result.get("agent_request_id", "not_provided"),
    }
    write_run_result(config.reports_dir, report_date, result)
    return result


def run_configured_pulse(config: PulseConfig) -> dict[str, Any]:
    if config.input_mode == "glean_gmail_draft":
        return run_pulse_from_glean_draft(config)
    if config.input_mode == "agent_api":
        return run_pulse(config)
    raise PulseError(f"Unsupported PULSE_INPUT_MODE: {config.input_mode!r}")
