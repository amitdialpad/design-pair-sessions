"""Failure-email delivery with optional per-local-day deduplication."""

from __future__ import annotations

import imaplib
import os
import re
import smtplib
import ssl
from dataclasses import dataclass
from datetime import datetime
from email.message import EmailMessage
from typing import Any, Callable, Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


RECIPIENT = "amit.ayre@dialpad.com"
DEFAULT_REPOSITORY = "amitdialpad/design-pair-sessions"


class FailureNotificationError(RuntimeError):
    """The failure notifier could not confirm suppression or delivery."""


@dataclass(frozen=True)
class FailureNotificationResult:
    status: str
    message_id: str | None = None
    local_date: str | None = None


def _parse_bool(value: str | None) -> bool:
    if value is None or not value.strip():
        return False
    normalized = value.strip().casefold()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise FailureNotificationError(f"Invalid FAILURE_DEDUPE_DAILY value: {value!r}")


def deterministic_failure_message_id(workflow: str, local_date: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", workflow.casefold()).strip("-") or "workflow"
    return f"<{slug}-failure-{local_date}@design-pair-sessions.github>"


def _special_mailbox(client: Any, flag: str, fallback: str) -> str:
    status, rows = client.list()
    if status == "OK" and rows:
        for row in rows:
            decoded = row.decode("utf-8", errors="replace")
            if flag.casefold() not in decoded.casefold():
                continue
            match = re.match(r'^\((?P<flags>[^)]*)\)\s+"[^"]*"\s+(?P<name>.+)$', decoded)
            if match:
                name = match.group("name").strip()
                if name.startswith('"') and name.endswith('"'):
                    name = name[1:-1].replace(r'\"', '"')
                return name
    return fallback


def _quote_mailbox(mailbox: str) -> str:
    escaped = mailbox.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _sent_message_exists(
    *,
    user: str,
    password: str,
    message_id: str,
    imap_factory: Callable[..., Any],
) -> bool:
    client = None
    try:
        client = imap_factory("imap.gmail.com", 993, ssl_context=ssl.create_default_context())
        client.login(user, password)
        mailbox = _special_mailbox(client, r"\Sent", "[Gmail]/Sent Mail")
        status, _ = client.select(_quote_mailbox(mailbox), readonly=True)
        if status != "OK":
            raise FailureNotificationError("Could not select Gmail Sent for failure-alert deduplication")
        status, data = client.uid("search", None, "HEADER", "Message-ID", f'"{message_id}"')
        if status != "OK":
            raise FailureNotificationError("Gmail failure-alert deduplication search failed")
        return bool(data and data[0].strip())
    except FailureNotificationError:
        raise
    except (imaplib.IMAP4.error, OSError) as error:
        raise FailureNotificationError(f"Gmail failure-alert deduplication failed: {error}") from error
    finally:
        if client is not None:
            try:
                client.logout()
            except Exception:
                pass


def _build_message(
    *,
    user: str,
    workflow: str,
    run_url: str,
    subject_prefix: str,
    description: str,
    common_fixes: str,
    repository: str,
    message_id: str | None,
    local_date: str | None,
) -> EmailMessage:
    message = EmailMessage()
    if local_date:
        message["Subject"] = f"{subject_prefix} — {local_date}"
        body = (
            f"Today's Daily Agentic Business Pulse could not be sent.\n\n"
            f"{description}\n\n"
            "No normal report was sent, and no stale or invented business data was used. "
            "The next scheduled fallback will retry automatically.\n\n"
            f"View the workflow run:\n{run_url}\n"
        )
    else:
        message["Subject"] = f"{subject_prefix}: {workflow}"
        body = (
            f"The '{workflow}' workflow failed on {repository}.\n\n"
            f"{description}\n\n"
            f"View the failed run:\n{run_url}\n\n"
            f"Common fixes:\n{common_fixes}\n"
        )
    message["From"] = user
    message["To"] = RECIPIENT
    if message_id:
        message["Message-ID"] = message_id
        message["X-Dialpad-Failure-Date"] = local_date
    message.set_content(body)
    return message


def notify_failure(
    environment: Mapping[str, str] | None = None,
    *,
    current_time: datetime | None = None,
    imap_factory: Callable[..., Any] = imaplib.IMAP4_SSL,
    smtp_factory: Callable[..., Any] = smtplib.SMTP_SSL,
) -> FailureNotificationResult:
    """Send the configured failure email, optionally once per local date.

    The default path intentionally preserves the existing Beacon notifier: it
    does no IMAP work and skips when credentials are absent. Daily deduplication
    is opt-in and fail-closed because Gmail Sent is then part of the contract.
    """

    env = os.environ if environment is None else environment
    user = env.get("GMAIL_USER", "").strip()
    password = env.get("GMAIL_APP_PASSWORD", "").strip()
    workflow = env.get("WORKFLOW_NAME", "Unknown workflow")
    run_url = env.get("RUN_URL", "")
    repository = env.get("GITHUB_REPOSITORY", DEFAULT_REPOSITORY).strip() or DEFAULT_REPOSITORY
    subject_prefix = env.get("FAILURE_SUBJECT_PREFIX", "Beacon sync failed")
    description = env.get(
        "FAILURE_DESCRIPTION",
        "This means the site or Beacon app may not have received today's update.",
    )
    common_fixes = env.get(
        "FAILURE_COMMON_FIXES",
        "  - BEACON_PAT expired → rotate at github.com/settings/tokens and update the secret\n"
        "  - Anthropic API error → check usage at console.anthropic.com\n"
        "  - GitHub API rate limit → re-run the workflow in a few minutes",
    )
    dedupe_daily = _parse_bool(env.get("FAILURE_DEDUPE_DAILY"))

    if not user or not password:
        if dedupe_daily:
            raise FailureNotificationError("Gmail credentials are required for the daily failure alert")
        return FailureNotificationResult(status="skipped_missing_credentials")

    message_id = None
    local_date = None
    if dedupe_daily:
        timezone_name = env.get("FAILURE_TIMEZONE", "Asia/Kolkata").strip() or "Asia/Kolkata"
        if timezone_name != "Asia/Kolkata":
            raise FailureNotificationError("Daily failure alerts must use Asia/Kolkata")
        try:
            timezone = ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError as error:
            raise FailureNotificationError(f"Unknown failure-alert timezone: {timezone_name}") from error
        now = current_time or datetime.now(timezone)
        if now.tzinfo is None:
            raise FailureNotificationError("Injected failure-alert time must be timezone-aware")
        local_date = now.astimezone(timezone).date().isoformat()
        message_id = deterministic_failure_message_id(workflow, local_date)
        if _sent_message_exists(
            user=user,
            password=password,
            message_id=message_id,
            imap_factory=imap_factory,
        ):
            return FailureNotificationResult(
                status="duplicate_skipped",
                message_id=message_id,
                local_date=local_date,
            )

    message = _build_message(
        user=user,
        workflow=workflow,
        run_url=run_url,
        subject_prefix=subject_prefix,
        description=description,
        common_fixes=common_fixes,
        repository=repository,
        message_id=message_id,
        local_date=local_date,
    )
    try:
        with smtp_factory("smtp.gmail.com", 465) as server:
            server.login(user, password)
            refused = server.send_message(message)
    except (smtplib.SMTPException, OSError) as error:
        raise FailureNotificationError(f"Failure email could not be sent: {error}") from error
    if refused:
        raise FailureNotificationError("Gmail refused the failure-alert recipient")
    return FailureNotificationResult(status="sent", message_id=message_id, local_date=local_date)
