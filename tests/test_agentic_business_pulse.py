from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from agentic_business_pulse import (  # noqa: E402
    IntegrationError,
    PulseConfig,
    ValidationError,
    build_email_message,
    deterministic_message_id,
    now_in_timezone,
    run_pulse,
    validate_agent_result,
)


REPORT_DATE = "2026-09-15"
REPORT_NOW = datetime(2026, 9, 15, 9, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
WORKFLOW_URL = "https://github.com/amitdialpad/design-pair-sessions/actions/runs/123"
SOURCE_LINKS = {
    "salesforce": "https://dialpad.lightning.force.com/lightning/o/Opportunity/list",
    "jira": "https://dialpad.atlassian.net/browse/DP-200000",
    "glean": "https://app.glean.com/search?q=agentic",
    "production_code": "https://github.com/dialpad/firespotter/pull/1",
}


def valid_result() -> dict:
    sources = "\n".join(f"- [{name}]({link}) — queried 2026-09-15 08:55 IST" for name, link in SOURCE_LINKS.items())
    report = f"""# Daily Agentic Business Pulse — {REPORT_DATE}

Reporting time: 2026-09-15 09:00 Asia/Kolkata. Comparison window: 2026-09-14 to 2026-09-14. Data status: complete.

## Executive readout

[Verified fact] Booked revenue and open pipeline are shown separately. [Signal] Onboarding moved. [Inference] Design follow-up is useful. [Unknown] One telemetry detail remains open.

## Revenue scoreboard

- Booked Agentic ACV: USD 100
- Total booked bundled amount: USD 300
- Qualified open pipeline Agentic ACV: USD 200
- Total bundled open opportunity amount: USD 500

## Customer and EAP reality

[Verified fact] Permitted Account A has a linked onboarding record.

## Jira and delivery risk

[Signal] DP-200000 is the material delivery risk today.

## Implementation reality

[Verified fact] Production code exists and is tested; deployment remains [Unknown].

## Working / not working

[Inference] The verified onboarding movement is working; telemetry completeness is not.

## Decisions and actions

- Confirm telemetry ownership today.

## Sources and confidence

{sources}
- Workflow: {WORKFLOW_URL}
"""
    source_status = {
        source: {"status": "ok", "queried_at": "2026-09-15T08:55:00+05:30", "links": [link]}
        for source, link in SOURCE_LINKS.items()
    }
    return {
        "report_markdown": report,
        "agent_request_id": "agent-request-123",
        "data_status": "complete",
        "failures": [],
        "snapshot": {
            "schema_version": 1,
            "report_date": REPORT_DATE,
            "generated_at": "2026-09-15T09:00:00+05:30",
            "comparison_window": {"start": "2026-09-14", "end": "2026-09-14", "label": "2026-09-14 to 2026-09-14"},
            "metrics": {
                "revenue": {
                    "booked_agentic_acv": 100,
                    "booked_total_bundled_amount": 300,
                    "target_agentic_acv": 1000,
                    "gap_agentic_acv": 900,
                    "attainment_pct": 10,
                    "pace_agentic_acv": 100,
                },
                "pipeline": {
                    "qualified_agentic_acv": 200,
                    "total_bundled_opportunity_amount": 500,
                    "coverage_ratio": 0.22,
                },
                "onboarding": {"active": 1},
                "eap": {"active": 1},
            },
            "source_status": source_status,
            "customers": [
                {
                    "account_name": "Permitted Account A",
                    "name_permitted": True,
                    "summary": "Onboarding moved after a verified checkpoint.",
                    "links": [SOURCE_LINKS["salesforce"]],
                }
            ],
            "jira_items": [
                {
                    "key": "DP-200000",
                    "summary": "Short redacted summary",
                    "status": "In Progress",
                    "age_days": 2,
                    "links": [SOURCE_LINKS["jira"]],
                }
            ],
            "implementation_claims": [
                {
                    "claim": "Production path exists and is tested",
                    "evidence_origin": "production_code",
                    "statuses": ["code_exists", "tested"],
                    "is_fixture": False,
                    "links": [SOURCE_LINKS["production_code"]],
                }
            ],
            "decisions": ["Confirm telemetry ownership"],
            "changes_since_previous": ["Onboarding checkpoint advanced"],
            "unknowns": ["Deployment telemetry detail"],
        },
    }


class FakeArchive:
    def __init__(self, duplicate: bool = False, ambiguous_draft: bool = False) -> None:
        self.duplicate = duplicate
        self.ambiguous_draft = ambiguous_draft
        self.drafts: list[EmailMessage] = []
        self.deleted: list[str | None] = []

    def sent_message_exists(self, message_id: str) -> bool:
        return self.duplicate

    def draft_message_exists(self, message_id: str) -> bool:
        return self.ambiguous_draft

    def load_previous_snapshot(self, current_report_date: str):
        return {"report_date": "2026-09-14"}

    def persist_draft(self, message: EmailMessage) -> str:
        self.drafts.append(message)
        return "42"

    def delete_draft(self, draft_uid: str | None) -> None:
        self.deleted.append(draft_uid)


class PulseValidationTests(unittest.TestCase):
    def test_reporting_date_uses_ist_calendar_day(self):
        utc_time = datetime(2026, 9, 15, 3, 30, tzinfo=ZoneInfo("UTC"))
        report_now = now_in_timezone("Asia/Kolkata", utc_time)
        self.assertEqual(report_now.date().isoformat(), REPORT_DATE)
        self.assertEqual(report_now.strftime("%H:%M"), "09:00")

    def test_valid_report_preserves_separate_revenue_and_pipeline_metrics(self):
        report, snapshot = validate_agent_result(
            valid_result(),
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )
        self.assertEqual(snapshot["metrics"]["revenue"]["booked_agentic_acv"], 100)
        self.assertEqual(snapshot["metrics"]["pipeline"]["qualified_agentic_acv"], 200)
        self.assertNotEqual(
            snapshot["metrics"]["revenue"]["booked_agentic_acv"],
            snapshot["metrics"]["pipeline"]["qualified_agentic_acv"],
        )
        self.assertIn("report_sha256", snapshot)
        self.assertIn("Booked Agentic ACV", report)

    def test_missing_pipeline_contract_is_rejected(self):
        result = valid_result()
        result["snapshot"]["metrics"].pop("pipeline")
        with self.assertRaisesRegex(ValidationError, "metrics.pipeline"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_failed_company_source_is_surfaced(self):
        result = valid_result()
        result["data_status"] = "incomplete"
        result["failures"] = ["salesforce: timeout"]
        with self.assertRaisesRegex(IntegrationError, "salesforce"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_stale_source_is_rejected(self):
        result = valid_result()
        result["snapshot"]["source_status"]["salesforce"]["queried_at"] = "2026-09-14T08:00:00+05:30"
        with self.assertRaisesRegex(ValidationError, "salesforce is stale"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_secret_is_not_persisted(self):
        result = valid_result()
        result["snapshot"]["notes"] = "api_key=EXAMPLE_REDACT_ME"
        with self.assertRaisesRegex(ValidationError, "credential or secret"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_raw_tool_arguments_are_not_persisted(self):
        result = valid_result()
        result["snapshot"]["tool_arguments"] = {"query": "sensitive"}
        with self.assertRaisesRegex(ValidationError, "forbidden"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_fixture_cannot_be_labeled_deployed(self):
        result = valid_result()
        claim = result["snapshot"]["implementation_claims"][0]
        claim["evidence_origin"] = "fixture"
        claim["is_fixture"] = True
        claim["statuses"] = ["code_exists", "deployed"]
        with self.assertRaisesRegex(ValidationError, "cannot be labeled deployed"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_unredacted_email_is_rejected(self):
        result = valid_result()
        result["snapshot"]["customers"][0]["summary"] = "Contact person@example.com"
        with self.assertRaisesRegex(ValidationError, "email address"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)


class PulseDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.reports_dir = Path(self.temp_dir.name) / "reports"
        self.config = PulseConfig(
            recipient="amit.ayre@dialpad.com",
            timezone_name="Asia/Kolkata",
            agent_url="https://company-agent.example/run",
            agent_token="not-used-by-fake",
            gmail_user="amit.ayre@dialpad.com",
            gmail_password="not-used-by-fake",
            source_context=(
                "https://docs.google.com/document/d/example-production-plan",
                "https://docs.google.com/presentation/d/example-customer-journey",
                "https://docs.google.com/document/d/example-impact-prd",
            ),
            skill_path=ROOT / "skills" / "daily-agentic-business-pulse" / "SKILL.md",
            reports_dir=self.reports_dir,
            dry_run=False,
        )

    @staticmethod
    def fake_agent(config, payload):
        return valid_result()

    @staticmethod
    def fake_sender(message, config):
        return {"status": "accepted", "provider": "gmail_smtp", "message_id": str(message["Message-ID"])}

    def test_live_run_sends_once_and_persists_matching_files(self):
        archive = FakeArchive()
        result = run_pulse(
            self.config,
            current_time=REPORT_NOW,
            agent=self.fake_agent,
            archive=archive,
            sender=self.fake_sender,
        )
        self.assertEqual(result["run_status"], "success")
        self.assertEqual(len(archive.drafts), 1)
        self.assertEqual(archive.deleted, ["42"])
        self.assertTrue((self.reports_dir / f"{REPORT_DATE}.md").is_file())
        self.assertTrue((self.reports_dir / f"{REPORT_DATE}.json").is_file())
        saved_report = (self.reports_dir / f"{REPORT_DATE}.md").read_text()
        saved_snapshot = json.loads((self.reports_dir / f"{REPORT_DATE}.json").read_text())
        self.assertEqual(saved_snapshot["report_sha256"], hashlib.sha256(saved_report.encode()).hexdigest())
        self.assertEqual(result["email_provider"], "gmail_smtp")
        self.assertEqual(set(result["source_freshness"]), set(SOURCE_LINKS))

    def test_dry_run_persists_draft_without_sending(self):
        archive = FakeArchive()
        calls = []
        config = PulseConfig(**{**self.config.__dict__, "dry_run": True})

        def should_not_send(message, config):
            calls.append(message)
            return {}

        result = run_pulse(
            config,
            current_time=REPORT_NOW,
            agent=self.fake_agent,
            archive=archive,
            sender=should_not_send,
        )
        self.assertEqual(result["run_status"], "dry_run_complete")
        self.assertEqual(result["email_status"], "not_sent_draft_persisted")
        self.assertFalse(calls)
        self.assertEqual(len(archive.drafts), 1)

    def test_retry_skips_duplicate_before_agent_or_sender(self):
        archive = FakeArchive(duplicate=True)
        calls = []

        def should_not_run(*args):
            calls.append(args)
            return valid_result()

        result = run_pulse(
            self.config,
            current_time=REPORT_NOW,
            agent=should_not_run,
            archive=archive,
            sender=should_not_run,
        )
        self.assertEqual(result["run_status"], "duplicate_skipped")
        self.assertEqual(result["message_id"], deterministic_message_id(REPORT_DATE))
        self.assertFalse(calls)

    def test_ambiguous_prepared_draft_fails_closed_before_duplicate_send(self):
        archive = FakeArchive(ambiguous_draft=True)
        calls = []

        def should_not_run(*args):
            calls.append(args)
            return valid_result()

        with self.assertRaisesRegex(IntegrationError, "ambiguous"):
            run_pulse(
                self.config,
                current_time=REPORT_NOW,
                agent=should_not_run,
                archive=archive,
                sender=should_not_run,
            )
        self.assertFalse(calls)

    def test_email_contract_has_exact_recipient_subject_and_attachments(self):
        result = valid_result()
        report, snapshot = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )
        message = build_email_message(
            report_date=REPORT_DATE,
            report=report,
            snapshot=snapshot,
            sender="amit.ayre@dialpad.com",
            recipient="amit.ayre@dialpad.com",
            message_id=deterministic_message_id(REPORT_DATE),
            dry_run=False,
        )
        self.assertEqual(message["To"], "amit.ayre@dialpad.com")
        self.assertEqual(message["Subject"], f"Daily Agentic Business Pulse — {REPORT_DATE}")
        filenames = {part.get_filename() for part in message.iter_attachments()}
        self.assertEqual(filenames, {f"{REPORT_DATE}.md", f"{REPORT_DATE}.json"})


class PulseWorkflowTests(unittest.TestCase):
    def test_workflow_has_daily_ist_schedule_manual_dry_run_and_read_only_permissions(self):
        workflow = (ROOT / ".github" / "workflows" / "daily-agentic-business-pulse.yml").read_text()
        self.assertIn("cron: '30 3 * * *'", workflow)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("pull_request:", workflow)
        self.assertIn("dry_run:", workflow)
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertIn("PULSE_AGENT_URL", workflow)
        self.assertIn("PULSE_SOURCE_CONTEXT_JSON", workflow)
        self.assertNotIn("fixture", workflow.lower())
        self.assertIn("if: github.event_name != 'pull_request'", workflow)

    def test_internal_source_document_ids_are_not_in_public_files(self):
        forbidden_direct_link_prefixes = (
            "https://docs.google.com/document/d/",
            "https://docs.google.com/presentation/d/",
        )
        public_text = "\n".join(
            path.read_text(errors="replace")
            for path in (
                ROOT / ".github" / "workflows" / "daily-agentic-business-pulse.yml",
                ROOT / "scripts" / "agentic_business_pulse.py",
                ROOT / "skills" / "daily-agentic-business-pulse" / "SKILL.md",
                ROOT / "operations" / "daily-agentic-business-pulse.md",
            )
        )
        for direct_link_prefix in forbidden_direct_link_prefixes:
            self.assertNotIn(direct_link_prefix, public_text)


if __name__ == "__main__":
    unittest.main()
