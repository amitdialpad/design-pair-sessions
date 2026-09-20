#!/usr/bin/env python3
"""GitHub Actions entry point for the Daily Agentic Business Pulse."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from agentic_business_pulse import PulseConfig, PulseError, run_configured_pulse
from failure_notification import FailureNotificationError, notify_failure


PROJECT_DIR = Path(__file__).resolve().parent.parent


def _append_github_file(variable: str, content: str) -> None:
    path = os.environ.get(variable, "").strip()
    if path:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(content)


def _write_handled_failure_summary(error: PulseError, notification_status: str) -> None:
    safe_error = " ".join(str(error).splitlines()).replace("`", "'")
    _append_github_file(
        "GITHUB_STEP_SUMMARY",
        "\n".join(
            (
                "## Daily Agentic Business Pulse",
                "",
                "- Run status: `handled_failure`",
                f"- Failure alert: `{notification_status}`",
                f"- Reason: `{safe_error}`",
                "- Safety: No normal report was sent; no stale or invented data was substituted.",
                "- Retry: The next scheduled fallback may try the Gmail draft path again.",
                "",
            )
        ),
    )


def _write_notifier_failure_summary(error: PulseError, notification_error: Exception) -> None:
    safe_error = " ".join(str(error).splitlines()).replace("`", "'")
    safe_notification_error = " ".join(str(notification_error).splitlines()).replace("`", "'")
    _append_github_file(
        "GITHUB_STEP_SUMMARY",
        "\n".join(
            (
                "## Daily Agentic Business Pulse",
                "",
                "- Run status: `failure_notification_failed`",
                f"- Pulse failure: `{safe_error}`",
                f"- Notifier failure: `{safe_notification_error}`",
                "- Alert path: This run remains failed so GitHub can send its failure notification.",
                "",
            )
        ),
    )


def _write_handled_failure_output(value: bool) -> None:
    _append_github_file("GITHUB_OUTPUT", f"handled_failure={'true' if value else 'false'}\n")


def main() -> int:
    try:
        config = PulseConfig.from_env(PROJECT_DIR)
        result = run_configured_pulse(config)
    except PulseError as error:
        print(f"[pulse:error] {error}", file=sys.stderr)
        if os.environ.get("FAILURE_DEDUPE_DAILY", "").strip().casefold() not in {
            "1",
            "true",
            "yes",
            "on",
        }:
            _write_handled_failure_output(False)
            return 1
        try:
            notification = notify_failure()
        except FailureNotificationError as notification_error:
            print(f"[pulse:notifier-error] {notification_error}", file=sys.stderr)
            _write_notifier_failure_summary(error, notification_error)
            _write_handled_failure_output(False)
            return 1
        _write_handled_failure_summary(error, notification.status)
        _write_handled_failure_output(True)
        print(
            "[pulse:handled-failure] "
            + json.dumps(
                {
                    "run_status": "handled_failure",
                    "failure_alert_status": notification.status,
                    "failure_alert_message_id": notification.message_id,
                    "failure_alert_date": notification.local_date,
                },
                sort_keys=True,
            )
        )
        return 0
    _write_handled_failure_output(False)
    print("[pulse:result] " + json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
