from __future__ import annotations

import hashlib
import html
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
    GLEAN_DRAFT_SUBJECT_PREFIX,
    GLEAN_MACHINE_END,
    GLEAN_MACHINE_START,
    GmailArchive,
    IntegrationError,
    PulseConfig,
    PulseError,
    ValidationError,
    build_email_message,
    deterministic_message_id,
    markdown_to_email_html,
    now_in_timezone,
    parse_glean_draft,
    run_pulse,
    run_pulse_from_glean_draft,
    validate_agent_result,
    wait_until_local_delivery_time,
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
    report = f"""# Daily Agentic Business Pulse — {REPORT_DATE}

_What this covers: 2026-09-14 to 2026-09-14 · Compared with: the previous successful report_

## TL;DR

Agentic has started to win business, but it is still far from the quarter's goal. One customer moved forward in onboarding; the next job is to prove that this progress creates a repeatable customer result, not just a successful setup. [Salesforce]({SOURCE_LINKS["salesforce"]})

## The numbers

- **$100 already booked for Agentic** — 10% of the $1K quarter goal.
- **$200 still in play** — possible Agentic business, not booked revenue.
- **1 customer actively onboarding** — movement is real, but value still needs to be proved.

## The story

### Money — interest is not turning into booked business fast enough

Booked revenue is still well below the quarter goal, and the deals still in play are not guaranteed money. Show booked Agentic business separately from possible deals so a large bundled deal cannot make progress look stronger than it is. [Salesforce opportunities]({SOURCE_LINKS["salesforce"]})

### Customers — setup progress is not the same as customer value

Permitted Account A passed a real onboarding checkpoint. That is encouraging, but we still need a simple definition of success that shows what improved for the customer and can be repeated with the next account. [Company evidence]({SOURCE_LINKS["glean"]})

### Product — the code exists, but we cannot yet prove customers can use it safely

The product path exists in code and has tests, while the main Jira risk is still active. Before calling it ready, the experience needs proof that a real customer can use it and recover when something goes wrong. [Production code]({SOURCE_LINKS["production_code"]}) · [DP-200000]({SOURCE_LINKS["jira"]})

## What this means for design

1. **Define what success looks like for one customer.** Why: the same measure can guide onboarding, the value review, and the decision to expand.
2. **Review the failure and recovery journey.** Why: tested code is not enough if a customer cannot understand what failed or safely try again.

## What to trust

Trust the revenue and delivery facts. Treat the customer-value story as early until we have a measured outcome, and do not assume the code is live for customers without direct proof. [Workflow run]({WORKFLOW_URL})
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
        self.replaced_message_ids: list[str] = []

    def sent_message_exists(self, message_id: str) -> bool:
        return self.duplicate

    def draft_message_exists(self, message_id: str) -> bool:
        return self.ambiguous_draft

    def delete_drafts_by_message_id(self, message_id: str) -> int:
        self.replaced_message_ids.append(message_id)
        return 1 if self.ambiguous_draft else 0

    def load_previous_snapshot(self, current_report_date: str):
        return {"report_date": "2026-09-14"}

    def persist_draft(self, message: EmailMessage) -> str:
        self.drafts.append(message)
        return "42"

    def delete_draft(self, draft_uid: str | None) -> None:
        self.deleted.append(draft_uid)


def glean_source_draft(result: dict | None = None, recipient: str = "amit.ayre@dialpad.com") -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = f"{GLEAN_DRAFT_SUBJECT_PREFIX} — {REPORT_DATE}"
    message["From"] = "amit.ayre@dialpad.com"
    message["To"] = recipient
    payload = result or valid_result()
    message.set_content(
        payload["report_markdown"]
        + "\n"
        + GLEAN_MACHINE_START
        + "\n"
        + json.dumps(payload)
        + "\n"
        + GLEAN_MACHINE_END
        + "\n"
    )
    return message


class FakeRelayArchive(FakeArchive):
    def __init__(self, source_message: EmailMessage | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.source_message = source_message or glean_source_draft()

    def wait_for_glean_draft(self, report_date: str, *, wait_seconds: int, poll_seconds: int):
        if report_date != REPORT_DATE:
            raise AssertionError(report_date)
        return "source-7", self.source_message


class PulseValidationTests(unittest.TestCase):
    def test_reporting_date_uses_ist_calendar_day(self):
        utc_time = datetime(2026, 9, 15, 3, 30, tzinfo=ZoneInfo("UTC"))
        report_now = now_in_timezone("Asia/Kolkata", utc_time)
        self.assertEqual(report_now.date().isoformat(), REPORT_DATE)
        self.assertEqual(report_now.strftime("%H:%M"), "09:00")

    def test_scheduled_runner_waits_until_nine_ist(self):
        slept = []
        early = datetime(2026, 9, 15, 4, 7, tzinfo=ZoneInfo("Asia/Kolkata"))
        ready = wait_until_local_delivery_time(
            "Asia/Kolkata",
            "09:00",
            current_time=early,
            sleeper=slept.append,
        )
        self.assertEqual(slept, [17580.0])
        self.assertEqual(ready, REPORT_NOW)

    def test_manual_runs_do_not_wait_for_a_delivery_window(self):
        slept = []
        early = datetime(2026, 9, 15, 4, 7, tzinfo=ZoneInfo("Asia/Kolkata"))
        ready = wait_until_local_delivery_time(
            "Asia/Kolkata",
            "",
            current_time=early,
            sleeper=slept.append,
        )
        self.assertEqual(slept, [])
        self.assertEqual(ready, early)

    def test_invalid_delivery_window_fails_closed(self):
        with self.assertRaisesRegex(PulseError, "24-hour HH:MM"):
            wait_until_local_delivery_time("Asia/Kolkata", "9am", current_time=REPORT_NOW)

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
        self.assertIn("already booked for Agentic", report)

    def test_legacy_evidence_labels_are_rejected_from_human_report(self):
        result = valid_result()
        result["report_markdown"] = result["report_markdown"].replace(
            "Agentic has started", "[Verified fact] Agentic has started"
        )
        with self.assertRaisesRegex(ValidationError, "Evidence labels belong in the snapshot"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_manager_brief_rejects_more_than_three_insights(self):
        result = valid_result()
        result["report_markdown"] = result["report_markdown"].replace(
            "## What this means for design",
            "### A fourth detail that does not belong\n\nThis would turn the brief back into a status dump.\n\n## What this means for design",
        )
        with self.assertRaisesRegex(ValidationError, "exactly three insight headlines"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_story_requires_money_customer_product_order(self):
        result = valid_result()
        result["report_markdown"] = result["report_markdown"].replace(
            "### Money —", "### Delivery —"
        )
        with self.assertRaisesRegex(ValidationError, "Money, Customers, Product order"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_manager_brief_rejects_untranslated_analyst_jargon(self):
        result = valid_result()
        result["report_markdown"] = result["report_markdown"].replace(
            "Agentic has started to win business", "Commercial health is conversion-constrained"
        )
        with self.assertRaisesRegex(ValidationError, "plain language"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_business_acronyms_are_rejected_from_human_report(self):
        result = valid_result()
        result["report_markdown"] = result["report_markdown"].replace(
            "$100 already booked for Agentic", "$100 Agentic ACV booked"
        )
        with self.assertRaisesRegex(ValidationError, "plain language instead of ACV"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_what_to_trust_rejects_source_inventory(self):
        result = valid_result()
        result["report_markdown"] = result["report_markdown"].replace(
            "Trust the revenue and delivery facts.",
            "Trust the Salesforce, Jira, and repository search results.",
        )
        with self.assertRaisesRegex(ValidationError, "must not inventory tools or sources"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_manager_brief_rejects_legacy_detail_sections(self):
        result = valid_result()
        result["report_markdown"] += "\n## Jira and delivery risk\n\nDP-200000 remains open.\n"
        with self.assertRaisesRegex(ValidationError, "Legacy detail section"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_manager_brief_rejects_more_than_650_words(self):
        result = valid_result()
        result["report_markdown"] = result["report_markdown"].replace(
            "Trust the revenue and delivery facts.",
            "Trust the revenue and delivery facts. " + "detail " * 700,
        )
        with self.assertRaisesRegex(ValidationError, "maximum is 650"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

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

    def test_incomplete_report_allows_unknown_metrics_when_all_sources_are_healthy(self):
        result = valid_result()
        result["data_status"] = "incomplete"
        result["failures"] = ["Previous successful snapshot is not available on the first run"]
        result["report_markdown"] = result["report_markdown"].replace(
            "Trust the revenue and delivery facts.",
            "Data incomplete: the weekly pace cannot be calculated because there is no earlier report to compare with.",
        )
        result["snapshot"]["metrics"]["revenue"]["pace_agentic_acv"] = None

        _, snapshot = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertEqual(snapshot["data_status"], "incomplete")
        self.assertIsNone(snapshot["metrics"]["revenue"]["pace_agentic_acv"])

    def test_complete_report_rejects_unknown_metric(self):
        result = valid_result()
        result["snapshot"]["metrics"]["revenue"]["pace_agentic_acv"] = None
        with self.assertRaisesRegex(ValidationError, "pace_agentic_acv must be numeric"):
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
        result = valid_result()
        current_workflow_url = payload["reporting"]["workflow_url"]
        result["report_markdown"] = result["report_markdown"].replace(WORKFLOW_URL, current_workflow_url)
        return result

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
        self.assertEqual(list(archive.drafts[0].iter_attachments()), [])
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
        self.assertEqual(list(archive.drafts[0].iter_attachments()), [])
        self.assertEqual(
            archive.replaced_message_ids,
            [deterministic_message_id(REPORT_DATE, dry_run=True)],
        )

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

    def test_email_contract_has_exact_recipient_subject_and_no_attachments(self):
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
            sender="amit.ayre@dialpad.com",
            recipient="amit.ayre@dialpad.com",
            message_id=deterministic_message_id(REPORT_DATE),
            dry_run=False,
        )
        self.assertEqual(message["To"], "amit.ayre@dialpad.com")
        self.assertEqual(message["Subject"], f"Daily Agentic Business Pulse — {REPORT_DATE}")
        self.assertEqual(list(message.iter_attachments()), [])
        plain_body = message.get_body(preferencelist=("plain",)).get_content()
        html_body = message.get_body(preferencelist=("html",)).get_content()
        self.assertIn("already booked for Agentic", plain_body)
        self.assertIn("<!doctype html>", html_body)
        self.assertNotIn(GLEAN_MACHINE_START, plain_body)
        self.assertNotIn(GLEAN_MACHINE_START, html_body)

    def test_email_html_prioritizes_bottom_line_metrics_and_insights(self):
        report, _ = validate_agent_result(
            valid_result(),
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )
        rendered = markdown_to_email_html(report)
        self.assertNotIn("border-left", rendered)
        self.assertIn("font-family:Georgia", rendered)
        self.assertIn("background:#f5f2ec", rendered)
        self.assertIn("background:#191718", rendered)
        self.assertIn("background:#ef5da8", rendered)
        self.assertIn('<meta charset="utf-8">', rendered)
        self.assertIn("Agentic / Daily pulse", rendered)
        self.assertIn("Business Pulse</h1>", rendered)
        self.assertIn("01</td>", rendered)
        self.assertNotIn("background:#faf9fd", rendered)
        self.assertNotIn("[Verified fact]", rendered)

    def test_email_contract_rejects_any_non_amit_recipient(self):
        result = valid_result()
        report, snapshot = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )
        with self.assertRaisesRegex(ValidationError, "locked to amit.ayre@dialpad.com"):
            build_email_message(
                report_date=REPORT_DATE,
                report=report,
                sender="amit.ayre@dialpad.com",
                recipient="someone-else@dialpad.com",
                message_id=deterministic_message_id(REPORT_DATE),
                dry_run=False,
            )

    def test_run_rejects_non_amit_recipient_before_agent_or_archive(self):
        config = PulseConfig(**{**self.config.__dict__, "recipient": "someone-else@dialpad.com"})
        calls = []

        def should_not_run(*args):
            calls.append(args)
            return valid_result()

        with self.assertRaisesRegex(ValidationError, "locked to amit.ayre@dialpad.com"):
            run_pulse(
                config,
                current_time=REPORT_NOW,
                agent=should_not_run,
                archive=FakeArchive(),
                sender=should_not_run,
            )
        self.assertFalse(calls)

    def test_gmail_mailbox_names_are_quoted_for_imap_selection(self):
        class FakeImapClient:
            def __init__(self):
                self.calls = []

            def select(self, mailbox, readonly):
                self.calls.append((mailbox, readonly))
                return "OK", []

        client = FakeImapClient()
        self.assertTrue(GmailArchive._select(client, "[Gmail]/Sent Mail", readonly=True))
        self.assertEqual(client.calls, [('"[Gmail]/Sent Mail"', True)])


class GleanDraftRelayTests(PulseDeliveryTests):
    def test_glean_draft_parses_machine_result_and_locks_recipient(self):
        parsed = parse_glean_draft(
            glean_source_draft(), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL
        )
        self.assertEqual(parsed["snapshot"]["report_date"], REPORT_DATE)
        self.assertIn(WORKFLOW_URL, parsed["report_markdown"])

        with self.assertRaisesRegex(ValidationError, "exactly one recipient"):
            parse_glean_draft(
                glean_source_draft(recipient="someone-else@dialpad.com"),
                report_date=REPORT_DATE,
                workflow_url=WORKFLOW_URL,
            )

    def test_html_only_glean_draft_preserves_machine_json(self):
        payload = valid_result()
        body = (
            payload["report_markdown"]
            + "\n"
            + GLEAN_MACHINE_START
            + "\n"
            + json.dumps(payload)
            + "\n"
            + GLEAN_MACHINE_END
        )
        message = EmailMessage()
        message["Subject"] = f"{GLEAN_DRAFT_SUBJECT_PREFIX} — {REPORT_DATE}"
        message["From"] = "amit.ayre@dialpad.com"
        message["To"] = "amit.ayre@dialpad.com"
        message.set_content(f"<html><body><pre>{html.escape(body)}</pre></body></html>", subtype="html")
        parsed = parse_glean_draft(message, report_date=REPORT_DATE, workflow_url=WORKFLOW_URL)
        self.assertEqual(parsed["data_status"], "complete")

    def test_glean_field_variants_are_normalized_before_validation(self):
        payload = valid_result()
        payload["data_status"] = "incomplete"
        payload["failures"] = ["Prior successful snapshot unavailable"]
        payload["agent_request_id"] = (
            "https://www.google.com/url?q=https://app.glean.com/chat/ae65479207fa42d39377ffdae6084ffd"
            "&source=gmail"
        )
        payload["report_markdown"] = payload["report_markdown"].replace(
            f"# Daily Agentic Business Pulse — {REPORT_DATE}",
            "# Daily Agentic Business Pulse",
        ).replace(
            "Trust the revenue and delivery facts.",
            "Data incomplete: the weekly pace cannot be calculated because there is no earlier report to compare with.",
        )
        comparison = payload["snapshot"]["comparison_window"]
        comparison["iso_start"] = comparison.pop("start")
        comparison["iso_end"] = REPORT_DATE
        comparison.pop("end")
        payload["snapshot"]["aggregate"] = {
            "onboarding": payload["snapshot"]["metrics"].pop("onboarding"),
            "eap": payload["snapshot"]["metrics"].pop("eap"),
        }
        payload["snapshot"]["changes_since_previous"] = {
            "status": "unknown",
            "reason": "No prior successful snapshot is available",
        }
        for index, state in enumerate(payload["snapshot"]["source_status"].values()):
            state["status"] = "refreshed_partial" if index == 3 else "refreshed"
            state["evidence_links"] = [
                f"https://www.google.com/url?q={link}&source=gmail" for link in state.pop("links")
            ]
        for link in SOURCE_LINKS.values():
            payload["report_markdown"] = payload["report_markdown"].replace(
                link, f"https://www.google.com/url?q={link}&source=gmail&ust=1"
            )
        customer = payload["snapshot"]["customers"][0]
        customer["name"] = customer.pop("account_name")
        customer.pop("name_permitted")
        payload["snapshot"]["customers"].append(
            {"name": "Permitted Account B", "summary": "Stored only in the private snapshot."}
        )
        jira_item = payload["snapshot"]["jira_items"][0]
        jira_item["link"] = jira_item.pop("links")[0]
        payload["snapshot"]["source_status"]["jira"]["evidence_links"] = [
            "https://dialpad.atlassian.net/issues/?jql=project%3DDP"
        ]
        claim = payload["snapshot"]["implementation_claims"][0]
        claim["statuses"] = {
            "exists": True,
            "tested": "verified",
            "flagged": "unknown",
            "instrumented": "not verified",
            "deployed": "not production",
            "customer_exposed": "not customer evidence",
        }

        parsed = parse_glean_draft(
            glean_source_draft(payload), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL
        )
        report, snapshot = validate_agent_result(
            parsed,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertTrue(report.startswith(f"# Daily Agentic Business Pulse — {REPORT_DATE}"))
        self.assertEqual(parsed["agent_request_id"], "ae65479207fa42d39377ffdae6084ffd")
        self.assertEqual(snapshot["comparison_window"]["end"], REPORT_DATE)
        self.assertEqual(snapshot["source_status"]["salesforce"]["status"], "ok")
        self.assertEqual(snapshot["source_status"]["salesforce"]["links"], [SOURCE_LINKS["salesforce"]])
        self.assertEqual(snapshot["metrics"]["onboarding"], {"active": 1})
        self.assertEqual(snapshot["metrics"]["eap"], {"active": 1})
        self.assertEqual(snapshot["changes_since_previous"][0]["status"], "unknown")
        self.assertTrue(snapshot["customers"][0]["name_permitted"])
        self.assertEqual(snapshot["customers"][0]["account_name"], "Permitted Account A")
        self.assertTrue(snapshot["customers"][1]["name_permitted"])
        self.assertEqual(snapshot["customers"][1]["account_name"], "Permitted Account B")
        self.assertIn(SOURCE_LINKS["jira"], snapshot["source_status"]["jira"]["links"])
        self.assertEqual(snapshot["implementation_claims"][0]["statuses"], ["code_exists", "tested"])
        self.assertNotIn("&source=gmail", report)
        self.assertNotIn("&ust=", report)

    def test_former_section_names_are_normalized_during_rollout(self):
        payload = valid_result()
        replacements = {
            "## TL;DR": "## Bottom line",
            "## The numbers": "## Numbers that matter",
            "## The story": "## What matters",
            "## What this means for design": "## Your focus",
            "## What to trust": "## Confidence",
        }
        for new_heading, old_heading in replacements.items():
            payload["report_markdown"] = payload["report_markdown"].replace(new_heading, old_heading)

        parsed = parse_glean_draft(
            glean_source_draft(payload), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL
        )
        report, _ = validate_agent_result(
            parsed,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        for heading in ("TL;DR", "The numbers", "The story", "What this means for design", "What to trust"):
            self.assertIn(f"## {heading}", report)

    def test_healthy_sources_with_secondary_gaps_do_not_mark_report_incomplete(self):
        payload = valid_result()
        payload["data_status"] = "incomplete"
        payload["failures"] = ["Prior successful pulse snapshot unavailable"]
        payload["snapshot"]["metrics"]["eap"] = {
            "customer_count": None,
            "usage_7d": None,
            "outcome_metric": None,
        }
        payload["snapshot"]["unknowns"] = [
            "Current EAP customer count and outcome baseline",
            "End-to-end deployment, flag state, and customer-exposure proof",
            "Prior successful pulse deltas",
        ]
        payload["report_markdown"] = payload["report_markdown"].replace(
            "Trust the revenue and delivery facts. Treat the customer-value story as early until we have a measured outcome, "
            "and do not assume the code is live for customers without direct proof.",
            "Data incomplete here: an old generic warning survived in the draft.",
        )

        parsed = parse_glean_draft(
            glean_source_draft(payload), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL
        )
        report, snapshot = validate_agent_result(
            parsed,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertEqual(parsed["data_status"], "complete")
        self.assertEqual(parsed["failures"], [])
        self.assertEqual(snapshot["data_status"], "complete")
        self.assertNotIn("Data incomplete", report)
        self.assertIn("revenue and delivery facts", report)
        self.assertIn("customer-value story is less certain", report)
        self.assertIn("usable by customers", report)
        self.assertEqual(report.count(f"[Workflow run]({WORKFLOW_URL})"), 1)

    def test_missing_core_metric_remains_incomplete(self):
        payload = valid_result()
        payload["data_status"] = "incomplete"
        payload["snapshot"]["metrics"]["revenue"]["target_agentic_acv"] = None
        payload["report_markdown"] = payload["report_markdown"].replace(
            "Trust the revenue and delivery facts.",
            "Data incomplete: we cannot tell whether bookings are ahead or behind plan because the current target was unavailable.",
        )

        parsed = parse_glean_draft(
            glean_source_draft(payload), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL
        )
        _, snapshot = validate_agent_result(
            parsed,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertEqual(snapshot["data_status"], "incomplete")

    def test_complete_healthy_result_cannot_deliver_stale_incomplete_copy(self):
        payload = valid_result()
        payload["report_markdown"] = payload["report_markdown"].replace(
            "Trust the revenue and delivery facts. Treat the customer-value story as early until we have a measured outcome, "
            "and do not assume the code is live for customers without direct proof.",
            "Data incomplete here: an old generic warning survived in the draft.",
        )

        parsed = parse_glean_draft(
            glean_source_draft(payload), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL
        )
        report, _ = validate_agent_result(
            parsed,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertNotIn("Data incomplete", report)
        self.assertIn("revenue and delivery facts", report)

    def test_live_relay_validates_persists_sends_once_and_removes_both_drafts(self):
        archive = FakeRelayArchive()
        result = run_pulse_from_glean_draft(
            self.config,
            current_time=REPORT_NOW,
            archive=archive,
            sender=self.fake_sender,
        )
        self.assertEqual(result["run_status"], "success")
        self.assertEqual(result["email_provider"], "gmail_smtp")
        self.assertEqual(len(archive.drafts), 1)
        self.assertEqual(archive.deleted, ["42", "source-7"])
        self.assertTrue((self.reports_dir / f"{REPORT_DATE}.md").is_file())
        snapshot = json.loads((self.reports_dir / f"{REPORT_DATE}.json").read_text())
        self.assertEqual(snapshot["delivery"]["input"], "scheduled_glean_gmail_draft")

    def test_dry_relay_never_sends_or_deletes_source_draft(self):
        archive = FakeRelayArchive()
        calls = []
        config = PulseConfig(**{**self.config.__dict__, "dry_run": True})

        result = run_pulse_from_glean_draft(
            config,
            current_time=REPORT_NOW,
            archive=archive,
            sender=lambda *args: calls.append(args),
        )
        self.assertEqual(result["run_status"], "dry_run_complete")
        self.assertEqual(result["email_status"], "not_sent_draft_persisted")
        self.assertFalse(calls)
        self.assertEqual(archive.deleted, [])
        self.assertEqual(len(archive.drafts), 1)
        self.assertEqual(list(archive.drafts[0].iter_attachments()), [])
        self.assertEqual(
            archive.replaced_message_ids,
            [deterministic_message_id(REPORT_DATE, dry_run=True)],
        )

    def test_missing_or_malformed_machine_block_fails_closed(self):
        message = glean_source_draft()
        message.set_content("# Daily Agentic Business Pulse — 2026-09-15\n")
        with self.assertRaisesRegex(ValidationError, "machine-readable"):
            parse_glean_draft(message, report_date=REPORT_DATE, workflow_url=WORKFLOW_URL)


class PulseWorkflowTests(unittest.TestCase):
    def test_workflow_has_daily_ist_schedule_manual_dry_run_and_read_only_permissions(self):
        workflow = (ROOT / ".github" / "workflows" / "daily-agentic-business-pulse.yml").read_text()
        self.assertIn("cron: '37 22 * * *'", workflow)
        self.assertIn("cron: '17 23 * * *'", workflow)
        self.assertIn("cron: '23 0 * * *'", workflow)
        self.assertIn("cron: '37 1 * * *'", workflow)
        self.assertIn("cron: '37 3 * * *'", workflow)
        self.assertEqual(workflow.count("cron:"), 5)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("pull_request:", workflow)
        self.assertIn("dry_run:", workflow)
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertIn("PULSE_INPUT_MODE: glean_gmail_draft", workflow)
        self.assertIn("PULSE_NOT_BEFORE_LOCAL_TIME:", workflow)
        self.assertIn("PULSE_GLEAN_DRAFT_WAIT_SECONDS: '1800'", workflow)
        self.assertIn("timeout-minutes: 345", workflow)
        self.assertIn("actions/checkout@v7", workflow)
        self.assertIn("actions/setup-python@v7", workflow)
        self.assertIn("actions/upload-artifact@v7", workflow)
        self.assertIn("retention-days: 90", workflow)
        self.assertNotIn("PULSE_AGENT_TOKEN", workflow)
        self.assertNotIn("/api/agents/", workflow)
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
