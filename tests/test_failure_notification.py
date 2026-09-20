from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from agentic_business_pulse import PulseError  # noqa: E402
from failure_notification import (  # noqa: E402
    FailureNotificationError,
    FailureNotificationResult,
    deterministic_failure_message_id,
    notify_failure,
)


runner_spec = importlib.util.spec_from_file_location(
    "run_agentic_business_pulse", ROOT / "scripts" / "run-agentic-business-pulse.py"
)
assert runner_spec and runner_spec.loader
runner = importlib.util.module_from_spec(runner_spec)
runner_spec.loader.exec_module(runner)


WORKFLOW = "Daily Agentic Business Pulse"
LOCAL_DATE = "2026-09-20"


class FakeImapClient:
    def __init__(self, *, duplicate: bool = False) -> None:
        self.duplicate = duplicate
        self.search_arguments = None
        self.selected = None
        self.logged_out = False

    def login(self, user, password):
        self.login_values = (user, password)

    def list(self):
        return "OK", [b'(\\HasNoChildren \\Sent) "/" "[Gmail]/Sent Mail"']

    def select(self, mailbox, readonly):
        self.selected = (mailbox, readonly)
        return "OK", []

    def uid(self, command, *arguments):
        if command != "search":
            raise AssertionError(command)
        self.search_arguments = arguments
        return "OK", [b"91" if self.duplicate else b""]

    def logout(self):
        self.logged_out = True


class FakeSmtpClient:
    def __init__(self) -> None:
        self.message = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def login(self, user, password):
        self.login_values = (user, password)

    def send_message(self, message):
        self.message = message
        return {}


def pulse_environment() -> dict[str, str]:
    return {
        "GMAIL_USER": "amit.ayre@dialpad.com",
        "GMAIL_APP_PASSWORD": "test-password",
        "GITHUB_REPOSITORY": "amitdialpad/design-pair-sessions",
        "WORKFLOW_NAME": WORKFLOW,
        "RUN_URL": "https://github.com/amitdialpad/design-pair-sessions/actions/runs/456",
        "FAILURE_SUBJECT_PREFIX": "Daily Agentic Business Pulse needs attention",
        "FAILURE_DESCRIPTION": "The report did not pass its delivery checks.",
        "FAILURE_DEDUPE_DAILY": "true",
        "FAILURE_TIMEZONE": "Asia/Kolkata",
    }


class FailureNotificationTests(unittest.TestCase):
    def test_daily_failure_email_uses_ist_date_deterministic_id_and_one_recipient(self):
        imap = FakeImapClient()
        smtp = FakeSmtpClient()
        now = datetime(2026, 9, 19, 18, 45, tzinfo=ZoneInfo("UTC"))

        result = notify_failure(
            pulse_environment(),
            current_time=now,
            imap_factory=lambda *args, **kwargs: imap,
            smtp_factory=lambda *args, **kwargs: smtp,
        )

        expected_id = deterministic_failure_message_id(WORKFLOW, LOCAL_DATE)
        self.assertEqual(result.status, "sent")
        self.assertEqual(result.local_date, LOCAL_DATE)
        self.assertEqual(result.message_id, expected_id)
        self.assertEqual(imap.selected, ('"[Gmail]/Sent Mail"', True))
        self.assertEqual(
            imap.search_arguments,
            (None, "HEADER", "Message-ID", f'"{expected_id}"'),
        )
        self.assertTrue(imap.logged_out)
        self.assertEqual(smtp.message["To"], "amit.ayre@dialpad.com")
        self.assertEqual(smtp.message["Message-ID"], expected_id)
        self.assertEqual(list(smtp.message.iter_attachments()), [])
        body = smtp.message.get_content()
        self.assertIn("No normal report was sent", body)
        self.assertIn("no stale or invented business data", body)

    def test_later_fallback_suppresses_same_day_failure_alert(self):
        imap = FakeImapClient(duplicate=True)

        def smtp_must_not_run(*args, **kwargs):
            raise AssertionError("SMTP must not run after a matching Sent message")

        result = notify_failure(
            pulse_environment(),
            current_time=datetime(2026, 9, 20, 9, 20, tzinfo=ZoneInfo("Asia/Kolkata")),
            imap_factory=lambda *args, **kwargs: imap,
            smtp_factory=smtp_must_not_run,
        )

        self.assertEqual(result.status, "duplicate_skipped")
        self.assertEqual(result.local_date, LOCAL_DATE)

    def test_daily_deduplication_fails_closed_without_gmail_credentials(self):
        environment = pulse_environment()
        environment["GMAIL_APP_PASSWORD"] = ""
        with self.assertRaisesRegex(FailureNotificationError, "credentials are required"):
            notify_failure(environment)

    def test_existing_beacon_notifier_behavior_does_not_use_imap(self):
        smtp = FakeSmtpClient()
        environment = {
            "GMAIL_USER": "amit.ayre@dialpad.com",
            "GMAIL_APP_PASSWORD": "test-password",
            "WORKFLOW_NAME": "Sync Beacon",
            "RUN_URL": "https://github.com/example/run",
        }

        result = notify_failure(
            environment,
            imap_factory=lambda *args, **kwargs: (_ for _ in ()).throw(
                AssertionError("Beacon notification must not use IMAP")
            ),
            smtp_factory=lambda *args, **kwargs: smtp,
        )

        self.assertEqual(result.status, "sent")
        self.assertEqual(smtp.message["Subject"], "Beacon sync failed: Sync Beacon")
        self.assertIsNone(smtp.message["Message-ID"])


class PulseRunnerFailureHandlingTests(unittest.TestCase):
    def test_handled_pulse_failure_summarizes_and_returns_success(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = Path(temp_dir) / "summary.md"
            output = Path(temp_dir) / "output.txt"
            environment = {
                **pulse_environment(),
                "GITHUB_STEP_SUMMARY": str(summary),
                "GITHUB_OUTPUT": str(output),
            }
            notification = FailureNotificationResult(
                status="sent",
                message_id=deterministic_failure_message_id(WORKFLOW, LOCAL_DATE),
                local_date=LOCAL_DATE,
            )
            with patch.dict(runner.os.environ, environment, clear=True), patch.object(
                runner.PulseConfig, "from_env", return_value=object()
            ), patch.object(
                runner, "run_configured_pulse", side_effect=PulseError("Glean draft missing")
            ), patch.object(runner, "notify_failure", return_value=notification):
                exit_code = runner.main()

            self.assertEqual(exit_code, 0)
            self.assertIn("Run status: `handled_failure`", summary.read_text())
            self.assertIn("No normal report was sent", summary.read_text())
            self.assertIn("handled_failure=true", output.read_text())

    def test_notifier_failure_leaves_run_failed_for_github_alert(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = Path(temp_dir) / "summary.md"
            output = Path(temp_dir) / "output.txt"
            environment = {
                **pulse_environment(),
                "GITHUB_STEP_SUMMARY": str(summary),
                "GITHUB_OUTPUT": str(output),
            }
            with patch.dict(runner.os.environ, environment, clear=True), patch.object(
                runner.PulseConfig, "from_env", return_value=object()
            ), patch.object(
                runner, "run_configured_pulse", side_effect=PulseError("Glean draft missing")
            ), patch.object(
                runner,
                "notify_failure",
                side_effect=FailureNotificationError("IMAP unavailable"),
            ):
                exit_code = runner.main()

            self.assertEqual(exit_code, 1)
            self.assertIn("Run status: `failure_notification_failed`", summary.read_text())
            self.assertIn("GitHub can send its failure notification", summary.read_text())
            self.assertIn("handled_failure=false", output.read_text())


if __name__ == "__main__":
    unittest.main()
