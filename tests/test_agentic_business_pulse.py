from __future__ import annotations

import hashlib
import copy
import html
import json
import re
import smtplib
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from unittest.mock import patch
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
    build_agent_request,
    deterministic_message_id,
    markdown_to_email_html,
    now_in_timezone,
    parse_glean_draft,
    run_pulse,
    send_gmail,
    run_pulse_from_glean_draft,
    validate_agent_result,
    wait_until_local_delivery_time,
)


REPORT_DATE = "2026-09-21"
REPORT_NOW = datetime(2026, 9, 21, 9, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
WORKFLOW_URL = "https://github.com/amitdialpad/design-pair-sessions/actions/runs/123"
TEST_REPORT_RECIPIENTS = "amit.ayre@dialpad.com"
SOURCE_LINKS = {
    "salesforce": "https://dialpad.lightning.force.com/lightning/o/Opportunity/list",
    "jira": "https://dialpad.atlassian.net/browse/DP-200000",
    "glean": "https://app.glean.com/search?q=agentic",
    "production_code": "https://github.com/dialpad/firespotter/pull/1",
}
DASHBOARD_SOURCE_LINKS = {
    "salesforce": SOURCE_LINKS["salesforce"],
    "jira": SOURCE_LINKS["jira"],
    "glean": SOURCE_LINKS["glean"],
    "production_code": SOURCE_LINKS["production_code"],
}
WEEKLY_SALES_NOTE = "The governed weekly bookings measure could not be verified from the current authorized source."
QUARTER_NOTE = "The governed quarter bookings measure could not be verified from the current authorized source."


def valid_result() -> dict:
    report = f"""# Weekly Agentic Customer Review — {REPORT_DATE}

_What this covers: 2026-09-20 to 2026-09-20 · Compared with: the previous successful report_

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
        source: {"status": "ok", "queried_at": "2026-09-21T08:55:00+05:30", "links": [link]}
        for source, link in SOURCE_LINKS.items()
    }
    return _legacy_result(report, source_status)


def valid_dashboard_result() -> dict:
    source_status = {
        source: {
            "status": "ok",
            "queried_at": "2026-09-21T08:55:00+05:30",
            "links": [link],
            "access_mode": "read_only",
        }
        for source, link in DASHBOARD_SOURCE_LINKS.items()
    }
    customers = [
        {
            "account_name": "Communicare IT",
            "name_permitted": True,
            "lifecycle_stage": "live",
            "movement": "moved",
            "agent_or_use_case": "IT support agent",
            "links": [SOURCE_LINKS["salesforce"]],
            "integrations": [{"name": "Salesforce", "status": "connected"}],
            "change_this_week": "Advanced to live support after the customer checkpoint was completed.",
            "next_watch": "Confirm the first post-launch customer review.",
            "metric_coverage": {
                "connector_actions": "not_instrumented",
                "conversation_outcomes": "available",
            },
            "activity": {
                "conversations_24h": 42,
                "conversations_7d": 120,
                "conversations_previous_7d": 100,
                "skill_starts_24h": 50,
                "connector_action_attempts_24h": None,
                "connector_action_successes_24h": None,
                "connector_action_failures_24h": None,
            },
            "outcomes_7d": {
                "contained": 90,
                "transferred": 20,
                "resolved": 106,
                "not_resolved": 10,
                "unknown_resolution": 4,
                "ai_csat": 4.3,
                "average_handle_seconds": 92,
            },
            "jira": {"new_or_changed_7d": 0, "open_customer_bugs": 0, "keys": []},
            "commercial": {"stage": "Early access", "movement_7d": "no_change", "agentic_acv": None},
        },
        {
            "account_name": "Batteries Plus",
            "name_permitted": True,
            "lifecycle_stage": "test",
            "movement": "failing",
            "agent_or_use_case": "Retail support agent",
            "links": [SOURCE_LINKS["salesforce"]],
            "integrations": [{"name": "Custom order API", "status": "failing"}],
            "change_this_week": "Customer testing exposed an authentication blocker in the publishing path.",
            "next_watch": "Confirm the fix owner and retest date.",
            "metric_coverage": {"connector_actions": "available", "conversation_outcomes": "available"},
            "activity": {
                "conversations_24h": 8,
                "conversations_7d": 30,
                "conversations_previous_7d": 25,
                "skill_starts_24h": 15,
                "connector_action_attempts_24h": 12,
                "connector_action_successes_24h": 10,
                "connector_action_failures_24h": 2,
            },
            "outcomes_7d": {
                "contained": 18,
                "transferred": 8,
                "resolved": 20,
                "not_resolved": 6,
                "unknown_resolution": 4,
                "ai_csat": 3.8,
                "average_handle_seconds": 130,
            },
            "jira": {"new_or_changed_7d": 1, "open_customer_bugs": 1, "keys": ["DP-200001"]},
            "commercial": {"stage": "UAT", "movement_7d": "no_change", "agentic_acv": None},
        },
        {
            "account_name": "Curri",
            "name_permitted": True,
            "lifecycle_stage": "build",
            "movement": "no_change",
            "agent_or_use_case": "Logistics agent",
            "links": ["https://dialpad.lightning.force.com/lightning/r/Account/curri/view"],
            "integrations": [{"name": "BYO MCP", "status": "building"}],
            "change_this_week": "No verified lifecycle or commercial change was recorded.",
            "next_watch": "Confirm the next build checkpoint.",
            "metric_coverage": {
                "connector_actions": "not_instrumented",
                "conversation_outcomes": "not_instrumented",
            },
            "activity": {
                "conversations_24h": 0,
                "conversations_7d": 0,
                "conversations_previous_7d": 0,
                "skill_starts_24h": 0,
                "connector_action_attempts_24h": None,
                "connector_action_successes_24h": None,
                "connector_action_failures_24h": None,
            },
            "outcomes_7d": {
                "contained": None,
                "transferred": None,
                "resolved": None,
                "not_resolved": None,
                "unknown_resolution": None,
                "ai_csat": None,
                "average_handle_seconds": None,
            },
            "jira": {"new_or_changed_7d": 0, "open_customer_bugs": 0, "keys": []},
            "commercial": {"stage": "Early access", "movement_7d": "no_change", "agentic_acv": None},
        },
        {
            "account_name": "Comprehensive Urology",
            "name_permitted": True,
            "lifecycle_stage": "validate",
            "movement": "moved",
            "agent_or_use_case": "Patient intake agent",
            "links": [SOURCE_LINKS["salesforce"]],
            "integrations": [{"name": "Scheduling API", "status": "testing"}],
            "change_this_week": "Customer sign-off moved the project into validation.",
            "next_watch": "Watch the first customer validation session.",
            "metric_coverage": {
                "connector_actions": "not_instrumented",
                "conversation_outcomes": "available",
            },
            "activity": {
                "conversations_24h": 4,
                "conversations_7d": 12,
                "conversations_previous_7d": 0,
                "skill_starts_24h": 5,
                "connector_action_attempts_24h": None,
                "connector_action_successes_24h": None,
                "connector_action_failures_24h": None,
            },
            "outcomes_7d": {
                "contained": 8,
                "transferred": 3,
                "resolved": 9,
                "not_resolved": 2,
                "unknown_resolution": 1,
                "ai_csat": 4.1,
                "average_handle_seconds": 105,
            },
            "jira": {"new_or_changed_7d": 0, "open_customer_bugs": 0, "keys": []},
            "commercial": {"stage": "UAT approved", "movement_7d": "advanced", "agentic_acv": None},
        },
    ]
    return {
        "report_markdown": f"# Weekly Agentic Customer Review — {REPORT_DATE}\n",
        "agent_request_id": "dashboard-request-123",
        "data_status": "complete",
        "failures": [],
        "snapshot": {
            "schema_version": 2,
            "report_date": REPORT_DATE,
            "generated_at": "2026-09-21T09:00:00+05:30",
            "comparison_window": {
                "start": "2026-09-14",
                "end": "2026-09-20",
                "label": "Monday September 14 through Sunday September 20",
            },
            "source_status": source_status,
            "summary": {
                "reported_deployment_count": 30,
                "active_customer_count": 4,
                "movers_7d": 3,
                "customers_with_changed_blockers_7d": 1,
                "customers_without_current_data": 0,
                "commercial_moves_7d": 1,
            },
            "customers": customers,
            "insights": [
                {
                    "account_name": "Batteries Plus",
                    "text": "Customer testing exposed a publishing blocker; the changed Jira defect now needs a confirmed owner and retest date.",
                    "links": ["https://dialpad.atlassian.net/browse/DP-200001"],
                },
                {
                    "account_name": "Communicare IT",
                    "text": "The customer advanced to live support after completing its checkpoint; the next proof is the first post-launch review.",
                    "links": [SOURCE_LINKS["salesforce"]],
                },
                {
                    "account_name": "Comprehensive Urology",
                    "text": "Customer sign-off moved the project into validation; the next meaningful evidence is the first customer validation session.",
                    "links": [SOURCE_LINKS["glean"]],
                },
            ],
            "commercial_changes": ["Comprehensive Urology advanced to UAT approved."],
            "unknowns": ["Curri has no verified lifecycle change in the current weekly window."],
            "changes_since_previous": ["Communicare IT moved live; Comprehensive Urology entered validation."],
        },
    }


def valid_ceo_view_result() -> dict:
    result = valid_dashboard_result()
    result["snapshot"]["schema_version"] = 5
    result["snapshot"]["executive_read"] = {
        "paragraph": "The signal this week is that Agentic activity is still not compounding: customer work increased, but the changed delivery evidence was another publishing blocker and commercial movement remained small. That keeps the company in transition rather than proving the new growth engine; the next meaningful change would be several customers advancing into dependable production or a sustained rise in won Agentic ACV.",
        "confidence": "medium",
        "links": [SOURCE_LINKS["salesforce"], "https://dialpad.atlassian.net/browse/DP-200001"],
    }
    result["snapshot"]["business_health"] = {
        "verdict": "stable",
        "verdict_reason": "Core bookings remain positive, while retention pressure needs watching.",
        "weekly_sales": {
            "total_bookings": 1_000_000,
            "core_bookings": 950_000,
            "agentic_bookings": 50_000,
            "agentic_share_pct": 5.0,
        },
        "salesforce_operational_snapshot": {
            "as_of_date": REPORT_DATE,
            "quarter_label": "Q3 FY27",
            "quarter_start_arr": 378_353_420.936,
            "current_arr": 392_077_094.28,
            "net_arr_change": 13_723_673.344,
            "net_arr_change_pct": 3.6272,
            "opening_cohort_current_arr": 376_372_129.8,
            "opening_cohort_change": -1_981_291.136,
            "new_or_unsnapshotted_arr": 15_704_964.48,
            "paying_accounts": 62_687,
            "paid_licenses": 1_010_826,
            "method_note": "Read-only Salesforce account fields; operational estimate, not the Finance-certified ARR bridge.",
            "comparison": {
                "previous_snapshot_date": None,
                "arr_change_since_previous": None,
                "paying_account_change": None,
                "paid_license_change": None,
                "comparison_note": "Baseline established; the first week-over-week comparison will appear next Monday.",
            },
        },
        "latest_arr_period": {
            "label": "September 2026",
            "net_arr_change": 250_000,
            "new_plus_expansion": 900_000,
            "churn_plus_contraction": -650_000,
            "net_customers": 24,
            "paid_license_change": 1_200,
        },
        "quarter": {
            "label": "Q3 FY27",
            "actual_bookings": 15_200_000,
            "target_status": "unverified",
            "target_bookings": None,
            "attainment_pct": None,
            "gap_to_target": None,
            "required_weekly_pace": None,
            "commit_forecast": 15_500_000,
            "best_case_forecast": 17_000_000,
            "previous_quarter_bookings": 14_800_000,
            "agentic_bookings": 1_100_000,
            "agentic_share_pct": 7.2,
            "target_note": "the available quota aggregate is incomplete",
        },
    }
    return result


def _legacy_result(report: str, source_status: dict) -> dict:
    return {
        "report_markdown": report,
        "agent_request_id": "agent-request-123",
        "data_status": "complete",
        "failures": [],
        "snapshot": {
            "schema_version": 1,
            "report_date": REPORT_DATE,
            "generated_at": "2026-09-21T09:00:00+05:30",
            "comparison_window": {"start": "2026-09-20", "end": "2026-09-20", "label": "2026-09-20 to 2026-09-20"},
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


def transition_claim(text="Synthetic source-backed position.", *, status="verified", evidence_date="2026-09-18"):
    return {
        "text": text,
        "status": status,
        "evidence_date": None if status == "unconfirmed" else evidence_date,
        "links": [] if status == "unconfirmed" else ["https://example.com/primary-evidence"],
    }


def valid_transition_result():
    customers = []
    for name, route, service_status, movement in (
        ("Aster Example", "ada_migration", "verified", "no_change"),
        ("Birch Example", "ada_new", "last_known", "moved"),
        ("Cedar Example", "undecided", "unconfirmed", "no_change"),
    ):
        milestone = transition_claim("Review the synthetic transition plan.", status="proposed")
        milestone.update(target_date="2026-10-05", date_status="proposed")
        if name == "Birch Example":
            milestone.update(status="verified", target_date="2026-10-12", date_status="committed")
        if name == "Cedar Example":
            milestone = transition_claim("A customer-approved next milestone was not located.", status="unconfirmed")
            milestone.update(target_date=None, date_status="none")
        customer = {
            "account_name": name,
            "name_permitted": True,
            "lifecycle_stage": "live" if name == "Aster Example" else "build",
            "movement": movement,
            "agent_or_use_case": "Synthetic service-desk routing.",
            "links": ["https://example.com/customer-record"],
            "integrations": [{"name": "Example CRM", "status": "connected"}],
            "change_this_week": "A synthetic fulfillment plan was approved." if movement == "moved" else "No new customer decision is established.",
            "next_watch": "Record the customer's next approved decision and accountable owner.",
            "jira": {"new_or_changed_7d": None, "open_customer_bugs": None, "keys": [], "note": "Complete customer issue coverage is not established."},
            "commercial": {"stage": "Synthetic signed agreement", "movement_7d": "no_change", "agentic_acv": 1234 if name == "Aster Example" else None},
            "transition": {
                "route": route,
                "current_service": transition_claim(
                    "Example voice service remains live." if name == "Aster Example" else "A dated service confirmation is missing." if service_status == "unconfirmed" else "The last source records an unlaunched pilot.",
                    status=service_status,
                ),
                "direction": transition_claim("Consider an Ada migration while the existing service stays live.", status="proposed") if name == "Aster Example" else transition_claim("An Ada fulfillment plan was approved.") if name == "Birch Example" else transition_claim("The customer has not approved a platform direction in the available sources.", status="unconfirmed"),
                "decision": transition_claim("A named customer approval of the transition baseline is missing.", status="unconfirmed"),
                "next_milestone": milestone,
                "accountability": transition_claim("Example delivery lead owns the next review."),
                "blocker": transition_claim("The specific customer approval gate is not evidenced.", status="unconfirmed"),
                "priority_cohorts": ["fulfillment", "vip"] if name == "Aster Example" else ["fulfillment"] if name == "Birch Example" else [],
                "attention": name == "Aster Example",
                "attention_reason": "Confirm approval before any customer cutover." if name == "Aster Example" else "",
            },
        }
        customers.append(customer)
    business = {
        "verdict": "stable", "verdict_reason": "Synthetic operational estimate is above its quarter-start baseline.",
        "weekly_sales": None, "weekly_sales_note": "A governed synthetic weekly sales cohort was not verified.",
        "latest_arr_period": None, "latest_arr_note": "A complete synthetic Finance ARR bridge was not verified.",
        "quarter": None, "quarter_note": "A governed synthetic quarter scoreboard was not verified.",
        "salesforce_operational_snapshot": {
            "as_of_date": REPORT_DATE, "quarter_label": "Q3 FY27", "quarter_start_arr": 1000,
            "current_arr": 1100, "net_arr_change": 100, "net_arr_change_pct": 10,
            "opening_cohort_current_arr": 900, "opening_cohort_change": -100,
            "new_or_unsnapshotted_arr": 200, "paying_accounts": 10, "paid_licenses": 15,
            "method_note": "Synthetic Salesforce operational estimate; not a Finance-certified ARR bridge.",
            "comparison": {"previous_snapshot_date": None, "arr_change_since_previous": None,
                           "paying_account_change": None, "paid_license_change": None,
                           "comparison_note": "A compatible precise prior synthetic snapshot is unavailable."},
        },
    }
    return {
        "report_markdown": f"# Weekly Agentic Customer Review — {REPORT_DATE}\n",
        "agent_request_id": "synthetic-transition-review", "data_status": "complete", "failures": [],
        "snapshot": {
            "schema_version": 7, "report_date": REPORT_DATE, "generated_at": REPORT_NOW.isoformat(),
            "comparison_window": {"start": "2026-09-14", "end": "2026-09-20", "label": "September 14–20, 2026"},
            "source_status": {source: {"status": "ok", "queried_at": REPORT_NOW.isoformat(), "links": [f"https://example.com/{source}"], "access_mode": "read_only"} for source in ("salesforce", "jira", "glean")},
            "executive_read": {"paragraph": "A synthetic fulfillment plan advanced while a live customer considers migration. A proposed migration does not establish customer acceptance or a completed cutover.", "confidence": "medium", "links": ["https://example.com/strategy"]},
            "coverage": {"status": "partial", "note": "Synthetic admitted roster retained; several decision claims still need primary evidence.", "links": ["https://example.com/roster"]},
            "summary": {"active_customer_count": 3, "movers_7d": 1, "customers_with_changed_blockers_7d": 0, "customers_without_current_data": 2, "commercial_moves_7d": 0},
            "customers": customers, "business_health": business,
            "strategy_updates": [transition_claim("A synthetic transition priority was agreed.")],
            "priority_cohorts": [
                {"key": "fulfillment", "label": "Synthetic signed fulfillment", "reported_count": 6,
                 "evidence_date": "2026-09-18", "links": ["https://example.com/fulfillment-priority"],
                 "matched_customers": ["Aster Example", "Birch Example"], "note": "Synthetic source count; not completed migrations."},
                {"key": "vip", "label": "Synthetic VIP migration", "reported_count": 2,
                 "evidence_date": "2026-09-18", "links": ["https://example.com/vip-priority"],
                 "matched_customers": ["Aster Example"], "note": "This priority overlaps the synthetic fulfillment cohort."},
            ],
            "unknowns": ["A precise approval gate is missing for individual claims, rather than the entire customer record."],
            "changes_since_previous": ["The synthetic admitted roster is unchanged."],
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
        return {"report_date": "2026-09-20"}

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


class TransitionReviewTests(unittest.TestCase):
    def validate(self, result=None):
        return validate_agent_result(
            result or valid_transition_result(), report_now=REPORT_NOW,
            source_max_age_hours=12, workflow_url=WORKFLOW_URL,
        )

    def test_transition_keeps_live_service_separate_from_proposed_vip_migration(self):
        report, snapshot = self.validate()
        customer = snapshot["customers"][0]
        self.assertEqual(customer["lifecycle_stage"], "live")
        self.assertEqual(customer["transition"]["route"], "ada_migration")
        self.assertNotIn("customer_insight", customer)
        self.assertIn("Example voice service remains live. (Verified · 2026-09-18", report)
        self.assertIn("Consider an Ada migration while the existing service stays live. (Proposed", report)
        self.assertIn("3 customer records · 1 with verified current-service evidence · 2 without verified current-service evidence", report)
        self.assertIn("Example CRM (connected)", report)
        self.assertIn("Recorded Agentic contract ACV: $1K.", report)
        self.assertIn("not recognized revenue or a new Ada sale", report)

    def test_transition_highlights_link_to_one_canonical_record_per_customer(self):
        report, _ = self.validate()
        changes = report.split("## What changed this week", 1)[1].split("## Priority context", 1)[0]
        highlights = report.split("## Customer transition", 1)[1].split("## Decisions needing attention", 1)[0]
        decisions = report.split("## Decisions needing attention", 1)[1].split("## Company", 1)[0]
        self.assertIn("Birch Example", changes)
        self.assertNotIn("Aster Example", changes)
        self.assertIn("Aster Example", highlights)
        self.assertIn("Birch Example", highlights)
        self.assertNotIn("Cedar Example", highlights)
        self.assertIn("Aster Example", decisions)
        self.assertNotIn("Birch Example", decisions)
        rendered = markdown_to_email_html(report)
        for customer in valid_transition_result()["snapshot"]["customers"]:
            self.assertEqual(report.count(f"### {customer['account_name']}\n"), 1)
        anchors = re.findall(r'<h3 id="(customer-[a-f0-9]{16})"', rendered)
        self.assertEqual(len(anchors), 3)
        self.assertTrue(set(re.findall(r'href="#(customer-[a-f0-9]{16})"', rendered)).issubset(set(anchors)))
        self.assertNotIn("| Customer |", report)

    def test_transition_missing_claim_proof_is_preserved_without_zero_fill(self):
        report, snapshot = self.validate()
        claim = snapshot["customers"][2]["transition"]["current_service"]
        self.assertIsNone(claim["evidence_date"])
        self.assertEqual(claim["links"], [])
        self.assertIn("A dated service confirmation is missing. (Unconfirmed)", report)
        self.assertIn("Missing amounts are not zero.", report)
        cedar = report.split("### Cedar Example\n", 1)[1]
        self.assertNotIn("Recorded Agentic contract ACV:", cedar)
        self.assertNotIn("ACV is not established", report)
        self.assertIn("The last source records an unlaunched pilot. (Last known · 2026-09-18", report)

    def test_transition_front_read_is_bounded_without_losing_attention_records(self):
        result = valid_transition_result()
        snapshot = result["snapshot"]
        customers = []
        for index in range(8):
            customer = copy.deepcopy(snapshot["customers"][0])
            customer["account_name"] = f"Priority Example {index + 1}"
            customer["transition"]["priority_cohorts"] = []
            customer["transition"]["attention_reason"] = f"Consequence {index + 1}."
            customer["transition"]["decision"]["text"] = f"Distinct decision {index + 1}."
            customers.append(customer)
        snapshot.update(customers=customers, priority_cohorts=[])
        snapshot["summary"].update(active_customer_count=8, movers_7d=0, customers_without_current_data=0)
        report, _ = self.validate(result)
        highlights = report.split("## Customer transition", 1)[1].split("## Decisions needing attention", 1)[0]
        decisions = report.split("## Decisions needing attention", 1)[1].split("## Company", 1)[0]
        roster = report.split("## Full roster and evidence gaps", 1)[1]
        self.assertIn("Consequence 5.", highlights)
        self.assertNotIn("Consequence 6.", highlights)
        self.assertIn("Other updates in the full roster:", highlights)
        self.assertIn("Distinct decision 5.", decisions)
        self.assertNotIn("Distinct decision 6.", decisions)
        self.assertIn("Priority Example 8", decisions)
        for index in range(8):
            self.assertIn(f"Distinct decision {index + 1}.", roster)
            self.assertEqual(report.count(f"### Priority Example {index + 1}\n"), 1)

    def test_transition_roster_pairs_all_claims_and_reuses_only_same_customer_sources(self):
        result = valid_transition_result()
        customer = result["snapshot"]["customers"][0]
        fields = ("current_service", "direction", "decision", "next_milestone", "accountability", "blocker")
        statuses = ("verified", "proposed", "unconfirmed", "last_known", "verified", "unconfirmed")
        shared = "https://example.com/shared-primary"
        claim_links = (
            [shared, "https://example.com/service-primary"], [shared],
            ["https://example.com/decision-primary"], [shared, "https://example.com/milestone-primary"],
            ["https://example.com/decision-primary"], ["https://example.com/blocker-primary"],
        )
        for index, (field, status, links) in enumerate(zip(fields, statuses, claim_links)):
            customer["transition"][field].update(
                text=f"Distinct synthetic {field} detail.", status=status,
                evidence_date=f"2026-09-{14 + index:02d}", links=links,
            )
        customer["links"] = [shared, "https://example.com/admission-primary"]
        result["snapshot"]["customers"][1]["transition"]["current_service"]["links"] = [shared]
        original = copy.deepcopy(customer)
        report, snapshot = self.validate(result)
        record = report.split("### Aster Example\n", 1)[1].split("### Birch Example\n", 1)[0]
        paragraphs = [paragraph for paragraph in record.strip().split("\n\n") if paragraph]
        self.assertEqual(len(paragraphs), 4)
        for index, (field, status) in enumerate(zip(fields, statuses)):
            self.assertIn(
                f"Distinct synthetic {field} detail. ({status.replace('_', ' ').capitalize()} · 2026-09-{14 + index:02d}",
                record,
            )
            self.assertEqual(snapshot["customers"][0]["transition"][field], original["transition"][field])
        for links in claim_links:
            for link in links:
                self.assertEqual(record.count(f"]({link})"), 1)
        self.assertIn("(Proposed · 2026-09-15 · source 1)", record)
        self.assertIn("(Verified · 2026-09-18 · source 3)", record)
        self.assertIn("Last known · 2026-09-17 · source 1, [source 4]", record)
        self.assertIn("Proposed target: 2026-10-05", record)
        self.assertIn("**Record evidence:** [source 6](https://example.com/admission-primary)", record)
        self.assertIn("**Use case:** Synthetic service-desk routing.", record)
        self.assertIn("Example CRM (connected)", record)
        self.assertIn("Recorded Agentic contract ACV: $1K.", record)
        self.assertIn("Synthetic VIP migration", record)
        birch = report.split("### Birch Example\n", 1)[1].split("### Cedar Example\n", 1)[0]
        self.assertIn(f"[source 1]({shared})", birch)
        rendered = markdown_to_email_html(report)
        anchor = "customer-" + hashlib.sha256(b"Aster Example").hexdigest()[:16]
        body = rendered.split(f'id="{anchor}"', 1)[1].split("</h3>", 1)[1].split("<h3", 1)[0]
        self.assertEqual(body.count('<p style="margin:0 0 8px">'), 4)
        self.assertEqual(body.count("<a "), 6)
        self.assertIn(f'href="#{anchor}"', rendered)

    def test_transition_representative_full_roster_html_stays_compact(self):
        result = valid_transition_result()
        snapshot = result["snapshot"]
        template = snapshot["customers"][0]
        customers = []
        for index in range(48):
            customer = copy.deepcopy(template)
            customer["account_name"] = f"Example Portfolio {index + 1:02d}"
            customer["movement"] = "no_change"
            customer["transition"].update(priority_cohorts=[], attention=False, attention_reason="")
            shared = f"https://example.com/source/{index}/" + "record" * 20
            customer["links"] = [shared]
            for field in ("current_service", "direction", "decision", "next_milestone", "accountability", "blocker"):
                customer["transition"][field]["links"] = [shared]
            customers.append(customer)
        snapshot.update(customers=customers, priority_cohorts=[])
        snapshot["summary"].update(active_customer_count=48, movers_7d=0, customers_without_current_data=0)
        report, _ = self.validate(result)
        rendered = markdown_to_email_html(report)
        self.assertLess(len(rendered.encode("utf-8")), 100_000)
        self.assertEqual(len(re.findall(r'<h3 id="customer-[a-f0-9]{16}"', rendered)), 48)
        self.assertIn('View entire message', rendered)
        for customer in customers:
            self.assertIn(customer["account_name"], report)
            self.assertIn(customer["links"][0], rendered)

    def test_transition_claim_status_and_evidence_checks(self):
        cases = (
            ("text", "", "text"), ("text", "x" * 321, "text"),
            ("status", "complete", "status"), ("evidence_date", None, "evidence_date"),
            ("evidence_date", "2026-09-22", "future dated"),
            ("evidence_date", "2026-02-30", "ISO date"),
            ("links", [], "HTTPS evidence"), ("links", ["http://example.com/source"], "HTTPS evidence"),
        )
        for field, value, reason in cases:
            with self.subTest(field=field, value=value):
                result = valid_transition_result()
                result["snapshot"]["customers"][0]["transition"]["current_service"][field] = value
                with self.assertRaisesRegex(ValidationError, reason):
                    self.validate(result)
        result = valid_transition_result()
        result["snapshot"]["customers"][0]["transition"]["blocker"].pop("evidence_date")
        with self.assertRaisesRegex(ValidationError, "explicit null"):
            self.validate(result)

    def test_transition_each_claim_retains_its_own_status(self):
        for status in ("verified", "last_known", "proposed", "unconfirmed"):
            with self.subTest(status=status):
                result = valid_transition_result()
                result["snapshot"]["customers"][0]["transition"]["decision"] = transition_claim("A synthetic decision position.", status=status)
                report, snapshot = self.validate(result)
                self.assertIn(f"A synthetic decision position. ({status.replace('_', ' ').capitalize()}", report)
                self.assertEqual(snapshot["customers"][0]["transition"]["current_service"]["status"], "verified")

    def test_transition_milestone_proposal_never_renders_as_a_commitment(self):
        report, _ = self.validate()
        aster = report.split("### Aster Example\n", 1)[1].split("### Birch Example\n", 1)[0]
        self.assertIn("Proposed target: 2026-10-05", aster)
        self.assertNotIn("Committed target", aster)
        self.assertIn("Committed target: 2026-10-12", report)
        result = valid_transition_result()
        result["snapshot"]["customers"][0]["transition"]["next_milestone"]["date_status"] = "committed"
        with self.assertRaisesRegex(ValidationError, "committed date requires verified"):
            self.validate(result)

    def test_transition_target_dates_and_evidence_dates_have_separate_rules(self):
        for target, date_status in ((None, "proposed"), ("2026-10-05", "none"), ("not-a-date", "committed")):
            with self.subTest(target=target, date_status=date_status):
                result = valid_transition_result()
                result["snapshot"]["customers"][0]["transition"]["next_milestone"].update(target_date=target, date_status=date_status)
                with self.assertRaisesRegex(ValidationError, "target_date"):
                    self.validate(result)
        result = valid_transition_result()
        result["snapshot"]["customers"][0]["transition"]["next_milestone"]["evidence_date"] = "2026-10-05"
        with self.assertRaisesRegex(ValidationError, "future dated"):
            self.validate(result)

    def test_transition_attention_needs_a_bounded_specific_reason(self):
        for field, value in (("attention", 1), ("attention_reason", ""), ("attention_reason", None), ("attention_reason", "x" * 321)):
            with self.subTest(field=field):
                result = valid_transition_result()
                result["snapshot"]["customers"][0]["transition"][field] = value
                with self.assertRaisesRegex(ValidationError, field):
                    self.validate(result)

    def test_transition_cohorts_allow_overlap_and_report_unmapped_without_adding_totals(self):
        report, _ = self.validate()
        section = report.split("## Priority context", 1)[1].split("## Customer transition", 1)[0]
        self.assertIn("6 reported · 2 matched · 4 unmapped", section)
        self.assertIn("2 reported · 1 matched · 1 unmapped", section)
        self.assertIn("not additive portfolio totals or completed migrations", section)
        self.assertNotIn("8 reported", section)
        self.assertNotIn("%", section)

    def test_transition_cohort_count_requires_reported_integer_evidence(self):
        for value in (-1, 1.5, True, None, "6"):
            with self.subTest(value=value):
                result = valid_transition_result()
                result["snapshot"]["priority_cohorts"][0]["reported_count"] = value
                with self.assertRaisesRegex(ValidationError, "nonnegative integer"):
                    self.validate(result)
        for field, value in (("evidence_date", None), ("links", [])):
            result = valid_transition_result()
            result["snapshot"]["priority_cohorts"][0][field] = value
            with self.assertRaisesRegex(ValidationError, field):
                self.validate(result)

    def test_transition_cohort_membership_rejects_duplicates_unknowns_and_inconsistency(self):
        cases = (
            ("matched_customers", ["Aster Example", "Aster Example"], "unique"),
            ("matched_customers", ["Absent Example"], "canonical"),
            ("matched_customers", ["Aster Example"], "reciprocal"),
            ("reported_count", 1, "cannot exceed"),
        )
        for field, value, reason in cases:
            with self.subTest(field=field, value=value):
                result = valid_transition_result()
                result["snapshot"]["priority_cohorts"][0][field] = value
                with self.assertRaisesRegex(ValidationError, reason):
                    self.validate(result)
        result = valid_transition_result()
        result["snapshot"]["priority_cohorts"].append(copy.deepcopy(result["snapshot"]["priority_cohorts"][0]))
        with self.assertRaisesRegex(ValidationError, "unique nonempty cohort key"):
            self.validate(result)
        for tags in (["vip", "vip"], ["missing-cohort"]):
            result = valid_transition_result()
            result["snapshot"]["customers"][2]["transition"]["priority_cohorts"] = tags
            with self.assertRaisesRegex(ValidationError, "cohort"):
                self.validate(result)

    def test_transition_rejects_casefold_duplicate_customers(self):
        result = valid_transition_result()
        result["snapshot"]["customers"][1]["account_name"] = "ASTER EXAMPLE"
        with self.assertRaisesRegex(ValidationError, "case-insensitive duplicate"):
            self.validate(result)

    def test_transition_strategy_updates_need_dated_evidence(self):
        result = valid_transition_result()
        result["snapshot"]["strategy_updates"][0] = transition_claim("A strategy source has not been located.", status="unconfirmed")
        with self.assertRaisesRegex(ValidationError, "evidence_date"):
            self.validate(result)

    def test_transition_source_health_freshness_and_privacy_still_gate_delivery(self):
        for source in ("salesforce", "jira", "glean"):
            result = valid_transition_result()
            result["snapshot"]["source_status"][source]["status"] = "timeout"
            with self.assertRaisesRegex(IntegrationError, source):
                self.validate(result)
        result = valid_transition_result()
        result["snapshot"]["source_status"]["salesforce"]["queried_at"] = "2026-09-20T08:00:00+05:30"
        with self.assertRaisesRegex(ValidationError, "stale"):
            self.validate(result)
        result = valid_transition_result()
        result["snapshot"]["customers"][0]["transition"]["credentials"] = "synthetic forbidden storage"
        with self.assertRaisesRegex(ValidationError, "forbidden"):
            self.validate(result)

    def test_transition_parser_and_request_route_to_schema7(self):
        result = valid_transition_result()
        customer = result["snapshot"]["customers"][0]
        customer["name"] = customer.pop("account_name")
        source = result["snapshot"]["source_status"]["glean"]
        source["evidence_links"] = source.pop("links")
        parsed = parse_glean_draft(glean_source_draft(result), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL)
        _, snapshot = self.validate(parsed)
        self.assertEqual(snapshot["schema_version"], 7)
        self.assertEqual(snapshot["customers"][0]["account_name"], "Aster Example")
        request = build_agent_request(report_now=REPORT_NOW, skill_text="Synthetic instructions.", previous_snapshot=None, workflow_url=WORKFLOW_URL, source_context=())
        self.assertEqual(request["response_contract"]["snapshot_schema_version"], 7)

    def test_transition_company_health_hook_gets_only_trusted_review_window(self):
        result = valid_transition_result()
        result["snapshot"]["business_health"]["_review_window_label"] = "Untrusted producer label"
        with patch("pulse_transition_company_health.render_transition_company_health", return_value=["", "## Company revenue and sales", "", "Synthetic company section."]) as render:
            report, snapshot = self.validate(result)
        business = render.call_args.args[0]
        self.assertEqual(business["_review_window_label"], "September 14–20, 2026")
        self.assertEqual(snapshot["business_health"]["_review_window_label"], "Untrusted producer label")
        self.assertIn("## Company revenue and sales", report)

    def test_transition_company_numbers_render_as_a_compact_metric_table(self):
        report, _ = self.validate()
        rendered = markdown_to_email_html(report)
        self.assertIn('class="pulse-company-metrics"', rendered)
        self.assertIn('<th align="left" scope="col"', rendered)
        self.assertNotIn('class="pulse-customer-card"', rendered)
        self.assertIn("Annual recurring contract value", rendered)

    def test_transition_preserves_producer_consequence_order_in_main_sections(self):
        result = valid_transition_result()
        customers = result["snapshot"]["customers"]
        customers[1]["transition"].update(attention=True, attention_reason="A committed customer checkpoint needs a decision.")
        result["snapshot"]["customers"] = [customers[1], customers[0], customers[2]]
        report, _ = self.validate(result)
        highlights = report.split("## Customer transition", 1)[1].split("## Decisions needing attention", 1)[0]
        decisions = report.split("## Decisions needing attention", 1)[1].split("## Company", 1)[0]
        self.assertLess(highlights.index("Birch Example"), highlights.index("Aster Example"))
        self.assertLess(decisions.index("Birch Example"), decisions.index("Aster Example"))
        self.assertIn("A synthetic fulfillment plan was approved.", highlights)
        self.assertIn("Confirm approval before any customer cutover.", highlights)
        self.assertIn("Next checkpoint: Review the synthetic transition plan. (committed target: 2026-10-12)", decisions)
        self.assertLess(report.index("### Aster Example"), report.index("### Birch Example"))

    def test_transition_renders_only_unique_optional_product_interpretations(self):
        result = valid_transition_result()
        customers = result["snapshot"]["customers"]
        result["snapshot"]["insights"] = [
            {"account_name": customers[0]["account_name"], "text": customers[0]["next_watch"].upper(), "links": ["https://example.com/repeated-context"]},
            {"account_name": customers[1]["account_name"], "text": "A shared approval summary could help customers distinguish a proposal from a committed cutover.", "links": ["https://example.com/design-context"]},
        ]
        report, _ = self.validate(result)
        section = report.split("### Product and design implications", 1)[1].split("## Company", 1)[0]
        self.assertIn("proposed consideration", section)
        self.assertIn("shared approval summary", section)
        self.assertNotIn(customers[0]["next_watch"].upper(), section)
        self.assertNotIn("Aster Example", section)
        result["snapshot"]["insights"] = result["snapshot"]["insights"][:1]
        report, _ = self.validate(result)
        self.assertNotIn("### Product and design implications", report)

    def test_transition_carries_forward_supported_commitments_without_new_research_tasks(self):
        result = valid_transition_result()
        result["snapshot"]["changes_since_previous"] = ["The previously committed synthetic checkpoint remains October 12; no earlier cutover was approved."]
        report, _ = self.validate(result)
        changes = report.split("## What changed this week", 1)[1].split("## Priority context", 1)[0]
        self.assertIn("Since the previous review", changes)
        self.assertIn("previously committed synthetic checkpoint remains October 12", changes)
        decisions = report.split("## Decisions needing attention", 1)[1].split("## Company", 1)[0]
        self.assertNotIn("Cedar Example", decisions)
        self.assertEqual(report.count("A dated service confirmation is missing."), 1)

    def test_transition_keeps_existing_jira_commercial_and_health_validation(self):
        result = valid_transition_result()
        result["snapshot"]["customers"][0]["jira"].pop("note")
        with self.assertRaisesRegex(ValidationError, "jira.note"):
            self.validate(result)
        result = valid_transition_result()
        result["snapshot"]["customers"][0]["commercial"]["agentic_acv"] = -1
        with self.assertRaisesRegex(ValidationError, "cannot be negative"):
            self.validate(result)
        result = valid_transition_result()
        result["snapshot"]["business_health"].pop("weekly_sales_note")
        with patch("pulse_transition_company_health.render_transition_company_health") as render:
            with self.assertRaisesRegex(ValidationError, "weekly_sales_note"):
                self.validate(result)
        render.assert_not_called()


class CompanyContextTests(unittest.TestCase):
    def validate(self, result):
        return validate_agent_result(
            result, report_now=REPORT_NOW, source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

    def test_dated_company_context_is_separate_from_weekly_change(self):
        result = valid_transition_result()
        text = "A prior-period combined run-rate was reported on a pro forma, unaudited basis."
        result["snapshot"]["company_context"] = [{
            "text": text, "status": "last_known", "evidence_date": "2026-07-31",
            "links": ["https://example.com/company-briefing"],
        }]
        report, _ = self.validate(result)
        self.assertNotIn(text, report.split("## What changed this week")[1].split("## Priority context")[0])
        self.assertIn(text, report.split("### Company context and outlook")[1])

    def test_unknown_company_profit_does_not_become_zero(self):
        result = valid_transition_result()
        result["snapshot"]["company_context"] = [{
            "text": "Current profit and cash-flow statements were not available in the authorized sources reviewed.",
            "status": "unconfirmed", "evidence_date": None, "links": [],
        }]
        report, _ = self.validate(result)
        self.assertIn("Current profit and cash-flow statements", report)
        self.assertNotIn("profit: $0", report)

    def test_company_context_retains_claim_evidence_and_size_gates(self):
        base = {"text": "A dated corporate update.", "status": "verified", "evidence_date": REPORT_DATE,
                "links": ["https://example.com/company-update"]}
        for change in ({"evidence_date": "2027-01-01"}, {"links": []}):
            with self.subTest(change=change):
                result = valid_transition_result()
                result["snapshot"]["company_context"] = [{**base, **change}]
                with self.assertRaisesRegex(ValidationError, "company_context"):
                    self.validate(result)
        result = valid_transition_result()
        result["snapshot"]["company_context"] = [base] * 9
        with self.assertRaisesRegex(ValidationError, "at most eight"):
            self.validate(result)

    def test_proposed_milestone_date_cannot_be_invented_without_support(self):
        result = valid_transition_result()
        result["snapshot"]["customers"][0]["transition"]["next_milestone"] = {
            "text": "An assessment date is not established.", "status": "unconfirmed",
            "evidence_date": None, "links": [], "target_date": "2026-10-05",
            "date_status": "proposed",
        }
        with self.assertRaisesRegex(ValidationError, "dated target requires sourced"):
            self.validate(result)


class PulseValidationTests(unittest.TestCase):
    def portfolio_result(self):
        result = valid_ceo_view_result()
        snapshot = result['snapshot']
        snapshot['schema_version'] = 6
        snapshot['coverage'] = {'status': 'partial', 'note': 'Known delivery roster reconciled; EAP coverage remains incomplete.', 'links': [SOURCE_LINKS['glean']]}
        for customer in snapshot['customers']:
            customer['customer_insight'] = {
                'engagement': 'Assigned delivery team for the paid pilot.',
                'current_position': 'Launch is waiting on partner onboarding.',
                'primary_dependency': 'Partner agreement must be executed before API onboarding.',
                'dependency_owner': 'Partner legal and onboarding teams',
                'business_implication': 'Launch timing remains unconfirmed until onboarding and acceptance finish.',
                'evidence_date': REPORT_DATE,
                'status': 'verified',
                'links': [SOURCE_LINKS['glean']],
            }
        return result

    def test_schema6_retains_existing_paragraph_style_and_direct_evidence(self):
        report, snapshot = validate_agent_result(
            self.portfolio_result(), report_now=REPORT_NOW,
            source_max_age_hours=12, workflow_url=WORKFLOW_URL,
        )
        rendered = markdown_to_email_html(report)
        self.assertEqual(snapshot["schema_version"], 6)
        self.assertNotIn("## Full roster and evidence gaps", report)
        self.assertNotIn('<p style="margin:0 0 8px">', rendered)
        self.assertNotIn("[source 1]", report)
        self.assertIn('style="margin:0 0 18px;font-size:17px;line-height:1.7;color:#45403b"', rendered)
        self.assertIn(SOURCE_LINKS["glean"], rendered)

    def test_portfolio_accepts_explicit_jira_count_gaps_without_rendering_counts(self):
        for unavailable in (("new_or_changed_7d",), ("open_customer_bugs",), ("new_or_changed_7d", "open_customer_bugs")):
            with self.subTest(unavailable=unavailable):
                result = self.portfolio_result()
                customer = result["snapshot"]["customers"][0]
                for field in unavailable:
                    customer["jira"][field] = None
                customer["jira"]["note"] = "Current authorized Jira evidence did not yield reconciled customer-level counts."

                report, snapshot = validate_agent_result(
                    result, report_now=REPORT_NOW,
                    source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                )

                for field in unavailable:
                    self.assertIsNone(snapshot["customers"][0]["jira"][field])
                self.assertIn(customer["account_name"], report)
                self.assertNotIn("Jira change", report)
                self.assertNotIn("open bug", report)

    def test_portfolio_requires_short_note_for_jira_count_gaps(self):
        missing = object()
        for invalid in (missing, None, "", "   ", 7, [], {}, True, "x" * 321):
            with self.subTest(note=repr(invalid)):
                result = self.portfolio_result()
                jira = result["snapshot"]["customers"][0]["jira"]
                jira["new_or_changed_7d"] = None
                jira["open_customer_bugs"] = None
                if invalid is not missing:
                    jira["note"] = invalid
                with self.assertRaisesRegex(ValidationError, "jira.note"):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_portfolio_rejects_missing_jira_count_fields(self):
        for missing, other in (("new_or_changed_7d", "open_customer_bugs"), ("open_customer_bugs", "new_or_changed_7d")):
            with self.subTest(missing=missing):
                result = self.portfolio_result()
                jira = result["snapshot"]["customers"][0]["jira"]
                jira.pop(missing)
                jira[other] = None
                jira["note"] = "Current authorized Jira evidence did not yield reconciled customer-level counts."
                with self.assertRaisesRegex(ValidationError, missing):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_schema5_rejects_null_jira_counts(self):
        result = valid_ceo_view_result()
        jira = result["snapshot"]["customers"][0]["jira"]
        jira["new_or_changed_7d"] = None
        jira["note"] = "Current authorized Jira evidence did not yield reconciled customer-level counts."
        with self.assertRaisesRegex(ValidationError, "jira.new_or_changed_7d"):
            validate_agent_result(
                result, report_now=REPORT_NOW,
                source_max_age_hours=12, workflow_url=WORKFLOW_URL,
            )

    def test_portfolio_jira_gap_does_not_bypass_provided_count_validation(self):
        for provided, unavailable in (("new_or_changed_7d", "open_customer_bugs"), ("open_customer_bugs", "new_or_changed_7d")):
            for invalid in (-1, float("inf"), float("nan"), "unknown", True, {}, []):
                with self.subTest(provided=provided, invalid=repr(invalid)):
                    result = self.portfolio_result()
                    jira = result["snapshot"]["customers"][0]["jira"]
                    jira[provided] = invalid
                    jira[unavailable] = None
                    jira["note"] = "Current authorized Jira evidence did not yield reconciled customer-level counts."
                    with self.assertRaisesRegex(ValidationError, provided):
                        validate_agent_result(
                            result, report_now=REPORT_NOW,
                            source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                        )

    def test_portfolio_jira_gap_does_not_bypass_key_validation(self):
        missing = object()
        for invalid in (missing, None, "DP-200001", ["not-a-jira-key"], [None]):
            with self.subTest(keys=repr(invalid)):
                result = self.portfolio_result()
                jira = result["snapshot"]["customers"][0]["jira"]
                jira["new_or_changed_7d"] = None
                jira["note"] = "Current authorized Jira evidence did not yield reconciled customer-level counts."
                if invalid is missing:
                    jira.pop("keys")
                else:
                    jira["keys"] = invalid
                with self.assertRaisesRegex(ValidationError, "jira.keys"):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_portfolio_accepts_optional_jira_note_with_numeric_counts(self):
        result = self.portfolio_result()
        result["snapshot"]["customers"][0]["jira"]["note"] = "Customer Jira counts were reconciled against current authorized issue evidence."
        report, snapshot = validate_agent_result(
            result, report_now=REPORT_NOW,
            source_max_age_hours=12, workflow_url=WORKFLOW_URL,
        )
        self.assertIsInstance(snapshot["customers"][0]["jira"]["new_or_changed_7d"], int)
        self.assertNotIn("Jira change", report)

    def bookings_gap_result(self, *, weekly: bool = True, quarter: bool = True, schema: int = 6):
        result = self.portfolio_result() if schema == 6 else valid_ceo_view_result()
        result["snapshot"]["schema_version"] = schema
        business = result["snapshot"]["business_health"]
        if weekly:
            business["weekly_sales"] = None
            business["weekly_sales_note"] = WEEKLY_SALES_NOTE
        if quarter:
            business["quarter"] = None
            business["quarter_note"] = QUARTER_NOTE
        return result

    def test_ceo_view_renders_unavailable_weekly_sales_and_preserves_quarter(self):
        report, snapshot = validate_agent_result(
            self.bookings_gap_result(quarter=False),
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertIsNone(snapshot["business_health"]["weekly_sales"])
        self.assertIn("This week's bookings unavailable", report)
        self.assertIn(WEEKLY_SALES_NOTE, report)
        self.assertIn("Q3 FY27: $15.20M booked", report)
        self.assertIn("Agentic share of quarter bookings", report)
        self.assertIn("Salesforce ARR snapshot", report)
        self.assertNotIn("core/non-Agentic", report)
        self.assertNotIn("None", report)
        self.assertNotIn("0.0%", report)

    def test_ceo_view_renders_unavailable_quarter_and_preserves_weekly_sales(self):
        report, snapshot = validate_agent_result(
            self.bookings_gap_result(weekly=False),
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertIsNone(snapshot["business_health"]["quarter"])
        self.assertIn("Quarter bookings unavailable", report)
        self.assertIn(QUARTER_NOTE, report)
        self.assertIn("This week's bookings:", report)
        self.assertIn("core/non-Agentic", report)
        self.assertIn("Salesforce ARR snapshot", report)
        for omitted in (
            "Agentic share of quarter bookings", "Quarter forecast", "Overall target",
            "required weekly pace", "$15.20M", "$14.80M", "None", "0.0%",
        ):
            self.assertNotIn(omitted, report)

    def test_ceo_view_renders_both_bookings_unavailable_for_schema5_and6(self):
        for schema in (5, 6):
            with self.subTest(schema=schema):
                report, snapshot = validate_agent_result(
                    self.bookings_gap_result(schema=schema),
                    report_now=REPORT_NOW,
                    source_max_age_hours=12,
                    workflow_url=WORKFLOW_URL,
                )

                self.assertIsNone(snapshot["business_health"]["weekly_sales"])
                self.assertIsNone(snapshot["business_health"]["quarter"])
                self.assertIn("This week's bookings unavailable", report)
                self.assertIn("Quarter bookings unavailable", report)
                self.assertIn(WEEKLY_SALES_NOTE, report)
                self.assertIn(QUARTER_NOTE, report)
                self.assertIn(snapshot["customers"][0]["account_name"], report)
                self.assertIn("Salesforce ARR snapshot", report)
                self.assertIn("Latest ARR movement", report)
                for omitted in ("Agentic share of quarter bookings", "Quarter forecast", "None", "0.0%"):
                    self.assertNotIn(omitted, report)

    def test_ceo_view_requires_short_notes_for_unavailable_bookings(self):
        missing = object()
        for field, note_field in (("weekly_sales", "weekly_sales_note"), ("quarter", "quarter_note")):
            for invalid in (missing, None, "", "   ", 7, [], {}, True, "x" * 321):
                with self.subTest(field=field, invalid=repr(invalid)):
                    result = self.portfolio_result()
                    business = result["snapshot"]["business_health"]
                    business[field] = None
                    if invalid is not missing:
                        business[note_field] = invalid
                    with self.assertRaisesRegex(ValidationError, note_field):
                        validate_agent_result(
                            result, report_now=REPORT_NOW,
                            source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                        )

    def test_bookings_gaps_require_explicit_null_instead_of_missing_measure(self):
        for field in ("weekly_sales", "quarter"):
            with self.subTest(field=field):
                result = self.bookings_gap_result()
                result["snapshot"]["business_health"].pop(field)
                with self.assertRaisesRegex(ValidationError, "must be an object or explicit null"):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_available_bookings_reject_unavailable_notes(self):
        for note_field in ("weekly_sales_note", "quarter_note"):
            with self.subTest(note_field=note_field):
                result = self.portfolio_result()
                result["snapshot"]["business_health"][note_field] = "This measure is unavailable."
                with self.assertRaisesRegex(ValidationError, f"must not include {note_field}"):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_available_bookings_accept_absent_or_empty_unavailable_notes(self):
        for empty_note in (None, ""):
            with self.subTest(note=repr(empty_note)):
                result = self.portfolio_result()
                business = result["snapshot"]["business_health"]
                business["weekly_sales_note"] = empty_note
                business["quarter_note"] = empty_note
                report, _ = validate_agent_result(
                    result, report_now=REPORT_NOW,
                    source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                )
                self.assertIn("This week's bookings:", report)
                self.assertIn("Agentic share of quarter bookings", report)
                self.assertNotIn("bookings unavailable", report)

    def test_ceo_view_accepts_320_character_unavailable_bookings_notes(self):
        result = self.bookings_gap_result()
        business = result["snapshot"]["business_health"]
        business["weekly_sales_note"] = "w" * 320
        business["quarter_note"] = "q" * 320

        report, _ = validate_agent_result(
            result, report_now=REPORT_NOW,
            source_max_age_hours=12, workflow_url=WORKFLOW_URL,
        )

        self.assertIn("w" * 320, report)
        self.assertIn("q" * 320, report)

    def test_bookings_gaps_keep_salesforce_snapshot_required(self):
        for schema in (3, 5, 6):
            for weekly, quarter in ((True, False), (False, True), (True, True)):
                with self.subTest(schema=schema, weekly_gap=weekly, quarter_gap=quarter):
                    result = self.bookings_gap_result(schema=schema, weekly=weekly, quarter=quarter)
                    result["snapshot"]["business_health"].pop("salesforce_operational_snapshot")
                    with self.assertRaisesRegex(ValidationError, "salesforce_operational_snapshot is required"):
                        validate_agent_result(
                            result, report_now=REPORT_NOW,
                            source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                        )

    def test_bookings_gaps_require_current_date_salesforce_snapshot(self):
        for weekly, quarter in ((True, False), (False, True), (True, True)):
            with self.subTest(weekly_gap=weekly, quarter_gap=quarter):
                result = self.bookings_gap_result(weekly=weekly, quarter=quarter)
                result["snapshot"]["business_health"]["salesforce_operational_snapshot"]["as_of_date"] = "2026-09-20"
                with self.assertRaisesRegex(ValidationError, "must match the current report date"):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_bookings_gaps_keep_source_receipts_required(self):
        for source in ("salesforce", "jira", "glean"):
            with self.subTest(source=source):
                result = self.bookings_gap_result()
                result["snapshot"]["source_status"][source]["status"] = "timeout"
                with self.assertRaisesRegex(IntegrationError, source):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_bookings_gap_preserves_available_weekly_sales_validation(self):
        cases = (
            ("total_bookings", -1, "cannot be negative"),
            ("total_bookings", float("inf"), "must be finite"),
            ("total_bookings", 1_000_100, "core plus Agentic must equal"),
            ("agentic_share_pct", 7.0, "share does not match"),
        )
        for field, invalid, reason in cases:
            with self.subTest(field=field, invalid=invalid):
                result = self.bookings_gap_result(weekly=False)
                result["snapshot"]["business_health"]["weekly_sales"][field] = invalid
                with self.assertRaisesRegex(ValidationError, reason):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_bookings_gap_preserves_available_quarter_validation(self):
        cases = (
            ("agentic_bookings", -1, "cannot be negative"),
            ("actual_bookings", float("inf"), "must be finite"),
            ("agentic_share_pct", 9.0, "share does not match"),
            ("attainment_pct", 99.0, "must not publish derived target metrics"),
        )
        for field, invalid, reason in cases:
            with self.subTest(field=field, invalid=invalid):
                result = self.bookings_gap_result(quarter=False)
                result["snapshot"]["business_health"]["quarter"][field] = invalid
                with self.assertRaisesRegex(ValidationError, reason):
                    validate_agent_result(
                        result, report_now=REPORT_NOW,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_unavailable_quarter_requires_actual_salesforce_fiscal_label(self):
        cases = (
            (2026, 1, 5, "Q4 FY26"), (2026, 2, 2, "Q1 FY27"),
            (2026, 4, 6, "Q1 FY27"), (2026, 5, 4, "Q2 FY27"),
            (2026, 7, 6, "Q2 FY27"), (2026, 8, 3, "Q3 FY27"),
            (2026, 10, 5, "Q3 FY27"), (2026, 11, 2, "Q4 FY27"),
            (2027, 1, 4, "Q4 FY27"),
        )
        for year, month, day, label in cases:
            with self.subTest(report_date=f"{year}-{month}-{day}", label=label):
                now = REPORT_NOW.replace(year=year, month=month, day=day)
                result = self.bookings_gap_result()
                snapshot = result["snapshot"]
                snapshot["report_date"] = now.date().isoformat()
                snapshot["generated_at"] = now.isoformat()
                snapshot["comparison_window"]["start"] = (now.date() - timedelta(days=7)).isoformat()
                snapshot["comparison_window"]["end"] = (now.date() - timedelta(days=1)).isoformat()
                for source in snapshot["source_status"].values():
                    source["queried_at"] = now.isoformat()
                for customer in snapshot["customers"]:
                    customer["customer_insight"]["evidence_date"] = now.date().isoformat()
                sf = snapshot["business_health"]["salesforce_operational_snapshot"]
                sf["as_of_date"] = now.date().isoformat()
                sf["quarter_label"] = label
                _, validated = validate_agent_result(
                    result, report_now=now,
                    source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                )
                self.assertEqual(validated["business_health"]["salesforce_operational_snapshot"]["quarter_label"], label)

                sf["quarter_label"] = "Q1 FY00"
                with self.assertRaisesRegex(ValidationError, "quarter_label"):
                    validate_agent_result(
                        result, report_now=now,
                        source_max_age_hours=12, workflow_url=WORKFLOW_URL,
                    )

    def test_portfolio_renders_dependency_instead_of_ticket_counts(self):
        result = self.portfolio_result()
        report, _ = validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)
        self.assertIn('Partner agreement must be executed', report)
        self.assertIn('EAP coverage remains incomplete', report)
        self.assertNotIn('Jira change', report)
        self.assertNotIn('open bug', report)
        self.assertNotIn('## Analysis', report)
        self.assertIn('pulse-customer-card', markdown_to_email_html(report))

    def test_portfolio_retains_quiet_customer_with_unconfirmed_status(self):
        result = self.portfolio_result()
        customer = result['snapshot']['customers'][0]
        old_movement = customer['movement']
        customer['movement'] = 'no_change'
        customer['customer_insight']['status'] = 'unconfirmed'
        summary = result['snapshot']['summary']
        summary['customers_without_current_data'] = 1
        summary['movers_7d'] -= int(old_movement in {'moved', 'failing'})
        summary['customers_with_changed_blockers_7d'] -= int(old_movement == 'failing')
        report, _ = validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)
        self.assertIn(customer['account_name'], report)
        self.assertIn('unconfirmed', report)

    def test_portfolio_requires_dependency_evidence(self):
        result = self.portfolio_result()
        result['snapshot']['customers'][0]['customer_insight']['links'] = []
        with self.assertRaisesRegex(ValidationError, 'customer_insight.links'):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_midweek_test_does_not_enable_midweek_live_delivery(self):
        result = self.portfolio_result()
        now = REPORT_NOW.replace(day=24)
        snapshot = result['snapshot']
        snapshot['report_date'] = '2026-09-24'
        snapshot['generated_at'] = now.isoformat()
        snapshot['comparison_window']['end'] = '2026-09-23'
        for source in snapshot['source_status'].values():
            source['queried_at'] = now.isoformat()
        with self.assertRaisesRegex(ValidationError, 'only on Monday'):
            validate_agent_result(result, report_now=now, source_max_age_hours=12, workflow_url=WORKFLOW_URL)
        report, _ = validate_agent_result(result, report_now=now, source_max_age_hours=12, workflow_url=WORKFLOW_URL, test_send=True)
        self.assertIn('2026-09-24', report)

    def test_ceo_view_renders_after_agentic_review_and_withholds_unverified_target(self):
        report, snapshot = validate_agent_result(
            valid_ceo_view_result(),
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertEqual(snapshot["schema_version"], 5)
        self.assertTrue(report.startswith(f"# Weekly Agentic Customer Review — {REPORT_DATE}"))
        self.assertIn("## Executive signal", report)
        self.assertIn("The signal this week", report)
        self.assertNotIn("**Why it matters:**", report)
        self.assertNotIn("**Watch next:**", report)
        self.assertNotIn("Dialpad Tap", report)
        self.assertNotIn("Next three months", report)
        self.assertLess(report.index("## Executive signal"), report.index("## This week"))
        self.assertIn("## CEO View — Company Health", report)
        self.assertIn("Salesforce ARR snapshot", report)
        self.assertIn("opening customer cohort", report)
        self.assertIn("Baseline established", report)
        self.assertIn("Overall target is withheld", report)
        self.assertNotIn("% of $", report)
        self.assertLess(report.index("## Analysis"), report.index("## CEO View — Company Health"))

    def test_executive_read_rejects_an_unsupported_signal(self):
        result = valid_ceo_view_result()
        result["snapshot"]["executive_read"]["links"] = []

        with self.assertRaisesRegex(ValidationError, "needs evidence"):
            validate_agent_result(
                result,
                report_now=REPORT_NOW,
                source_max_age_hours=12,
                workflow_url=WORKFLOW_URL,
            )

    def test_ceo_view_rejects_target_math_when_unverified(self):
        result = valid_ceo_view_result()
        result["snapshot"]["business_health"]["quarter"]["attainment_pct"] = 99.0

        with self.assertRaisesRegex(ValidationError, "must not publish derived target metrics"):
            validate_agent_result(
                result,
                report_now=REPORT_NOW,
                source_max_age_hours=12,
                workflow_url=WORKFLOW_URL,
            )

    def test_ceo_view_rejects_salesforce_snapshot_that_does_not_reconcile(self):
        result = valid_ceo_view_result()
        result["snapshot"]["business_health"]["salesforce_operational_snapshot"][
            "net_arr_change"
        ] += 100_000

        with self.assertRaisesRegex(ValidationError, "net ARR does not match"):
            validate_agent_result(
                result,
                report_now=REPORT_NOW,
                source_max_age_hours=12,
                workflow_url=WORKFLOW_URL,
            )

    def test_ceo_view_renders_week_over_week_salesforce_comparison(self):
        result = valid_ceo_view_result()
        comparison = result["snapshot"]["business_health"]["salesforce_operational_snapshot"][
            "comparison"
        ]
        comparison.update(
            {
                "previous_snapshot_date": "2026-09-14",
                "arr_change_since_previous": 1_250_000,
                "paying_account_change": 45,
                "paid_license_change": -120,
                "comparison_note": None,
            }
        )

        report, _ = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertIn("Since 2026-09-14", report)
        self.assertIn("ARR +$1.25M", report)
        self.assertIn("paying accounts +45", report)
        self.assertIn("licenses on paying accounts -120", report)

    def test_ceo_view_sends_verified_agentic_review_when_arr_bridge_is_unavailable(self):
        result = valid_ceo_view_result()
        business = result["snapshot"]["business_health"]
        business["latest_arr_period"] = None
        business["latest_arr_note"] = (
            "The latest monthly ARR bridge was not available from a current authorized source."
        )

        report, snapshot = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertIsNone(snapshot["business_health"]["latest_arr_period"])
        self.assertIn("Latest ARR movement unavailable", report)
        self.assertIn("## Verified customer movement", report)

    def test_ceo_view_rejects_unavailable_arr_bridge_without_a_reason(self):
        result = valid_ceo_view_result()
        result["snapshot"]["business_health"]["latest_arr_period"] = None

        with self.assertRaisesRegex(ValidationError, "requires latest_arr_note"):
            validate_agent_result(
                result,
                report_now=REPORT_NOW,
                source_max_age_hours=12,
                workflow_url=WORKFLOW_URL,
            )

    def test_reporting_date_uses_ist_calendar_day(self):
        utc_time = datetime(2026, 9, 21, 3, 30, tzinfo=ZoneInfo("UTC"))
        report_now = now_in_timezone("Asia/Kolkata", utc_time)
        self.assertEqual(report_now.date().isoformat(), REPORT_DATE)
        self.assertEqual(report_now.strftime("%H:%M"), "09:00")

    def test_scheduled_runner_waits_until_nine_ist(self):
        slept = []
        early = datetime(2026, 9, 21, 4, 7, tzinfo=ZoneInfo("Asia/Kolkata"))
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
        early = datetime(2026, 9, 21, 4, 7, tzinfo=ZoneInfo("Asia/Kolkata"))
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

    def test_what_to_trust_ignores_source_name_inside_workflow_link_url(self):
        result = valid_result()
        glean_workflow_url = "https://app.glean.com/chat/current-pulse-run"
        result["report_markdown"] = result["report_markdown"].replace(
            WORKFLOW_URL,
            glean_workflow_url,
        )

        report, _ = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=glean_workflow_url,
        )

        self.assertIn(f"[Workflow run]({glean_workflow_url})", report)

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
        result["snapshot"]["source_status"]["salesforce"]["queried_at"] = "2026-09-20T08:00:00+05:30"
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

    def test_customer_dashboard_is_deterministic_and_orders_attention_first(self):
        report, snapshot = validate_agent_result(
            valid_dashboard_result(),
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertTrue(report.startswith(f"# Weekly Agentic Customer Review — {REPORT_DATE}"))
        self.assertLess(report.index("Batteries Plus"), report.index("Communicare IT"))
        self.assertLess(report.index("Communicare IT"), report.index("Curri"))
        self.assertIn("30 deployments reported", report)
        self.assertIn("Customer testing exposed an authentication blocker", report)
        self.assertIn("No verified lifecycle or commercial change", report)
        self.assertNotIn("conversation", report.casefold())
        self.assertNotIn("## The story", report)
        self.assertNotIn("## What this means for design", report)
        self.assertEqual(snapshot["data_status"], "complete")
        self.assertIn("report_sha256", snapshot)

    def test_customer_dashboard_requires_read_only_sources(self):
        result = valid_dashboard_result()
        result["snapshot"]["source_status"]["salesforce"]["access_mode"] = "write"

        with self.assertRaisesRegex(ValidationError, "access_mode must be read_only"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_customer_dashboard_fails_closed_when_salesforce_is_unhealthy(self):
        result = valid_dashboard_result()
        result["snapshot"]["source_status"]["salesforce"]["status"] = "timeout"

        with self.assertRaisesRegex(IntegrationError, "salesforce"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_customer_dashboard_rejects_stale_salesforce(self):
        result = valid_dashboard_result()
        result["snapshot"]["source_status"]["salesforce"]["queried_at"] = "2026-09-20T08:00:00+05:30"

        with self.assertRaisesRegex(ValidationError, "salesforce.*stale"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_customer_dashboard_runs_only_on_monday(self):
        result = valid_dashboard_result()
        tuesday = datetime(2026, 9, 22, 9, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
        result["snapshot"]["report_date"] = "2026-09-22"
        result["snapshot"]["generated_at"] = "2026-09-22T09:00:00+05:30"

        with self.assertRaisesRegex(ValidationError, "only on Monday"):
            validate_agent_result(result, report_now=tuesday, source_max_age_hours=48, workflow_url=WORKFLOW_URL)

    def test_customer_dashboard_requires_previous_monday_through_sunday(self):
        result = valid_dashboard_result()
        result["snapshot"]["comparison_window"]["start"] = "2026-09-15"

        with self.assertRaisesRegex(ValidationError, "previous Monday through Sunday"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_customer_dashboard_requires_a_weekly_change_statement(self):
        result = valid_dashboard_result()
        customer = result["snapshot"]["customers"][0]
        customer["change_this_week"] = ""

        with self.assertRaisesRegex(ValidationError, "change_this_week"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_customer_dashboard_accepts_unknown_lifecycle_for_verified_customer_signal(self):
        result = valid_dashboard_result()
        customer = result["snapshot"]["customers"][2]
        customer["lifecycle_stage"] = "unknown"
        customer["change_this_week"] = (
            "Current approved evidence does not support a safe operating lifecycle mapping."
        )
        result["snapshot"]["unknowns"] = [
            "Curri has no safely verified operating lifecycle stage in the current weekly window."
        ]

        report, _ = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertIn("Unknown", report)
        self.assertIn("does not support a safe operating lifecycle mapping", report)

    def test_customer_dashboard_rejects_rows_without_a_verified_weekly_signal(self):
        result = valid_dashboard_result()
        result["snapshot"]["customers"][2]["movement"] = "no_data"

        with self.assertRaisesRegex(ValidationError, "movement is invalid"):
            validate_agent_result(
                result,
                report_now=REPORT_NOW,
                source_max_age_hours=12,
                workflow_url=WORKFLOW_URL,
            )

    def test_reported_deployment_count_cannot_be_smaller_than_verified_rows(self):
        result = valid_dashboard_result()
        result["snapshot"]["summary"]["reported_deployment_count"] = 3

        with self.assertRaisesRegex(ValidationError, "cannot be smaller"):
            validate_agent_result(
                result,
                report_now=REPORT_NOW,
                source_max_age_hours=12,
                workflow_url=WORKFLOW_URL,
            )

    def test_customer_dashboard_requires_a_next_watch(self):
        result = valid_dashboard_result()
        customer = result["snapshot"]["customers"][1]
        customer["next_watch"] = ""

        with self.assertRaisesRegex(ValidationError, "next_watch"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_customer_dashboard_rejects_summary_not_derived_from_rows(self):
        result = valid_dashboard_result()
        result["snapshot"]["summary"]["commercial_moves_7d"] = 999

        with self.assertRaisesRegex(ValidationError, "does not match customer rows"):
            validate_agent_result(result, report_now=REPORT_NOW, source_max_age_hours=12, workflow_url=WORKFLOW_URL)

    def test_customer_dashboard_allows_analysis_for_verified_no_change_signal(self):
        result = valid_dashboard_result()
        result["snapshot"]["customers"][0]["movement"] = "no_change"
        result["snapshot"]["summary"]["movers_7d"] = 2
        report, _ = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertIn("Communicare IT", report)

    def test_customer_dashboard_html_renders_readable_customer_cards(self):
        report, _ = validate_agent_result(
            valid_dashboard_result(),
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )
        rendered = markdown_to_email_html(report)

        self.assertEqual(rendered.count('class="pulse-customer-card"'), 4)
        self.assertIn("Journey and commercial state", rendered)
        self.assertIn("Batteries Plus", rendered)
        self.assertNotIn("| Customer |", rendered)


class PulseDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.reports_dir = Path(self.temp_dir.name) / "reports"
        self.config = PulseConfig(
            recipient=TEST_REPORT_RECIPIENTS,
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

    def test_test_send_uses_distinct_id_and_subject_and_sends_once(self):
        archive = FakeArchive()
        sent = []
        config = PulseConfig(**{**self.config.__dict__, "test_send": True})

        def capture_sender(message, config):
            sent.append(message)
            return self.fake_sender(message, config)

        result = run_pulse(
            config,
            current_time=REPORT_NOW,
            agent=self.fake_agent,
            archive=archive,
            sender=capture_sender,
        )
        self.assertEqual(result["run_status"], "success")
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0]["Subject"], f"[TEST] Weekly Agentic Customer Review — {REPORT_DATE}")
        self.assertEqual(sent[0]["X-Dialpad-Pulse-Mode"], "test")
        self.assertEqual(
            sent[0]["Message-ID"],
            deterministic_message_id(REPORT_DATE, test_send=True),
        )
        self.assertEqual(sent[0]["Bcc"], TEST_REPORT_RECIPIENTS)

    def test_test_send_is_not_blocked_by_existing_live_delivery(self):
        archive = FakeArchive(duplicate=False)
        config = PulseConfig(**{**self.config.__dict__, "test_send": True})
        result = run_pulse(
            config,
            current_time=REPORT_NOW,
            agent=self.fake_agent,
            archive=archive,
            sender=self.fake_sender,
        )
        self.assertEqual(result["run_status"], "success")
        self.assertEqual(result["message_id"], deterministic_message_id(REPORT_DATE, test_send=True))

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

    def test_email_contract_has_exact_recipients_subject_and_no_attachments(self):
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
            recipient=TEST_REPORT_RECIPIENTS,
            message_id=deterministic_message_id(REPORT_DATE),
            dry_run=False,
        )
        self.assertEqual(message["To"], "undisclosed-recipients:;")
        self.assertEqual(message["Bcc"], TEST_REPORT_RECIPIENTS)
        self.assertIsNone(message["Cc"])
        self.assertEqual(message["Subject"], f"Weekly Agentic Customer Review — {REPORT_DATE}")
        self.assertEqual(list(message.iter_attachments()), [])
        plain_body = message.get_body(preferencelist=("plain",)).get_content()
        html_body = message.get_body(preferencelist=("html",)).get_content()
        self.assertIn("already booked for Agentic", plain_body)
        self.assertIn("<!doctype html>", html_body)
        self.assertNotIn(GLEAN_MACHINE_START, plain_body)
        self.assertNotIn(GLEAN_MACHINE_START, html_body)

    def final_message(self):
        return build_email_message(
            report_date=REPORT_DATE,
            report="Weekly customer review",
            sender=self.config.gmail_user,
            recipient=TEST_REPORT_RECIPIENTS,
            message_id=deterministic_message_id(REPORT_DATE),
            dry_run=False,
        )

    def test_smtp_delivers_to_all_bcc_recipients_without_exposing_headers(self):
        message = self.final_message()
        smtp_send_message = smtplib.SMTP.send_message
        with patch("agentic_business_pulse.smtplib.SMTP") as smtp:
            server = smtp.return_value.__enter__.return_value
            server.send_message.side_effect = lambda msg, **kwargs: smtp_send_message(server, msg, **kwargs)
            server.sendmail.return_value = {}
            self.assertEqual(send_gmail(message, self.config)["status"], "accepted")
            sender, recipients, wire_message, *_ = server.sendmail.call_args.args
        self.assertEqual(sender, self.config.gmail_user)
        self.assertEqual(list(recipients), TEST_REPORT_RECIPIENTS.split(", "))
        headers = wire_message.split(b"\r\n\r\n", 1)[0]
        self.assertNotIn(b"Bcc:", headers)
        for address in recipients:
            self.assertNotIn(address.encode(), headers.split(b"To:", 1)[1])
        self.assertIn(b"To: undisclosed-recipients:;", headers)

    def test_smtp_rejects_visible_or_extra_recipients_before_connecting(self):
        for header, value in (
            ("To", TEST_REPORT_RECIPIENTS),
            ("Cc", "report.extra@dialpad.com"),
            ("Bcc", TEST_REPORT_RECIPIENTS + ", report.extra@dialpad.com"),
        ):
            with self.subTest(header=header):
                message = self.final_message()
                if header in message:
                    message.replace_header(header, value)
                else:
                    message[header] = value
                with patch("agentic_business_pulse.smtplib.SMTP") as smtp:
                    with self.assertRaises(ValidationError):
                        send_gmail(message, self.config)
                    smtp.assert_not_called()

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
        self.assertIn("Agentic / Weekly review", rendered)
        self.assertIn("Customer Review</h1>", rendered)
        self.assertIn("01</td>", rendered)
        self.assertNotIn("background:#faf9fd", rendered)
        self.assertNotIn("[Verified fact]", rendered)

    def test_email_preserves_source_urls_with_markdown_characters(self):
        from html.parser import HTMLParser

        class Links(HTMLParser):
            def __init__(self):
                super().__init__()
                self.targets = []

            def handle_starttag(self, tag, attrs):
                if tag == "a":
                    self.targets.append(dict(attrs)["href"])

        target = "https://example.com/document/a_b_c?view=one_two&tab=main"
        report = f"**Read [source]({target})** and _the note_."
        rendered = markdown_to_email_html(report)
        parser = Links()
        parser.feed(rendered)
        self.assertEqual(parser.targets, [target])
        self.assertIn("<strong>Read <a ", rendered)
        self.assertIn("<em>the note</em>", rendered)
        self.assertNotIn("PULSELINK", rendered)

    def test_customer_dashboard_email_uses_large_stacked_customer_cards(self):
        report, _ = validate_agent_result(
            valid_dashboard_result(),
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        rendered = markdown_to_email_html(report)

        self.assertEqual(rendered.count('class="pulse-customer-card"'), 4)
        self.assertIn("font-size:23px;line-height:1.35", rendered)
        self.assertIn("font-size:17px;line-height:1.6", rendered)
        self.assertIn("JOURNEY AND COMMERCIAL STATE", rendered.upper())
        self.assertIn("WHAT CHANGED THIS WEEK", rendered.upper())
        self.assertIn("RISK AND NEXT WATCH", rendered.upper())
        self.assertNotIn("min-width:720px", rendered)
        self.assertNotIn("font-size:11px;line-height:1.45", rendered)

    def test_email_contract_rejects_any_unapproved_recipient_list(self):
        result = valid_result()
        report, snapshot = validate_agent_result(
            result,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )
        unapproved_lists = (
            "",
            "someone-else@dialpad.com",
            TEST_REPORT_RECIPIENTS + ", report.extra@dialpad.com",
            TEST_REPORT_RECIPIENTS + ", external@example.com",
            TEST_REPORT_RECIPIENTS + ", " + TEST_REPORT_RECIPIENTS,
        )
        for recipients in unapproved_lists:
            with self.subTest(recipients=recipients):
                with self.assertRaisesRegex(ValidationError, "restricted to Amit only"):
                    build_email_message(
                        report_date=REPORT_DATE,
                        report=report,
                        sender="amit.ayre@dialpad.com",
                        recipient=recipients,
                        message_id=deterministic_message_id(REPORT_DATE),
                        dry_run=False,
                    )

    def test_run_rejects_unapproved_recipient_list_before_agent_or_archive(self):
        config = PulseConfig(**{**self.config.__dict__, "recipient": "someone-else@dialpad.com"})
        calls = []

        def should_not_run(*args):
            calls.append(args)
            return valid_result()

        with self.assertRaisesRegex(ValidationError, "restricted to Amit only"):
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

    def test_glean_search_is_ascii_then_enforces_exact_subject_date_and_recipient(self):
        correct = glean_source_draft()
        wrong_date = glean_source_draft()
        wrong_date.replace_header(
            "Subject", f"{GLEAN_DRAFT_SUBJECT_PREFIX} — 2026-09-20"
        )
        wrong_recipient = glean_source_draft(recipient="someone-else@dialpad.com")
        raw_messages = {
            b"1": correct.as_bytes(),
            b"2": wrong_date.as_bytes(),
            b"3": wrong_recipient.as_bytes(),
        }

        class AsciiOnlyImapClient:
            def __init__(self):
                self.search_arguments = None

            def list(self):
                return "OK", [b'(\\HasNoChildren \\Drafts) "/" "[Gmail]/Drafts"']

            def select(self, mailbox, readonly):
                return "OK", []

            def uid(self, command, *arguments):
                if command == "search":
                    self.search_arguments = arguments
                    for argument in arguments:
                        if isinstance(argument, str):
                            argument.encode("ascii")
                    return "OK", [b"1 2 3"]
                if command == "fetch":
                    uid = arguments[0]
                    return "OK", [(b"message", raw_messages[uid])]
                raise AssertionError(command)

            def logout(self):
                return "BYE", []

        client = AsciiOnlyImapClient()
        archive = GmailArchive("amit.ayre@dialpad.com", "password")
        with patch.object(archive, "_connect", return_value=client):
            found = archive.find_glean_draft(REPORT_DATE)

        self.assertIsNotNone(found)
        uid, message = found
        self.assertEqual(uid, "1")
        self.assertEqual(message["Subject"], f"{GLEAN_DRAFT_SUBJECT_PREFIX} — {REPORT_DATE}")
        self.assertEqual(
            client.search_arguments,
            (None, "SUBJECT", '"Weekly Agentic Customer Review"'),
        )


class GleanDraftRelayTests(PulseDeliveryTests):
    def test_schema_v2_glean_draft_dry_run_renders_customer_matrix(self):
        archive = FakeRelayArchive(source_message=glean_source_draft(valid_dashboard_result()))
        config = PulseConfig(**{**self.config.__dict__, "dry_run": True})
        calls = []

        result = run_pulse_from_glean_draft(
            config,
            current_time=REPORT_NOW,
            archive=archive,
            sender=lambda *args: calls.append(args),
        )

        self.assertEqual(result["run_status"], "dry_run_complete")
        self.assertFalse(calls)
        self.assertEqual(len(archive.drafts), 1)
        message = archive.drafts[0]
        self.assertEqual(list(message.iter_attachments()), [])
        plain_body = message.get_body(preferencelist=("plain",)).get_content()
        html_body = message.get_body(preferencelist=("html",)).get_content()
        self.assertIn("## Verified customer movement", plain_body)
        self.assertIn("Customer testing exposed an authentication blocker", plain_body)
        self.assertEqual(html_body.count('class="pulse-customer-card"'), 4)
        self.assertIn("font-size:17px;line-height:1.6", html_body)
        self.assertNotIn(GLEAN_MACHINE_START, plain_body)
        snapshot = json.loads((self.reports_dir / f"{REPORT_DATE}.json").read_text())
        self.assertEqual(snapshot["schema_version"], 2)

    def test_glean_draft_parses_machine_result_and_locks_recipient(self):
        parsed = parse_glean_draft(
            glean_source_draft(), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL
        )
        self.assertEqual(parsed["snapshot"]["report_date"], REPORT_DATE)
        self.assertIn(WORKFLOW_URL, parsed["report_markdown"])

        with self.assertRaisesRegex(ValidationError, "approved recipient contract"):
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
            f"# Weekly Agentic Customer Review — {REPORT_DATE}",
            "# Weekly Agentic Customer Review",
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

        self.assertTrue(report.startswith(f"# Weekly Agentic Customer Review — {REPORT_DATE}"))
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

    def test_glean_healthy_source_status_is_normalized_to_ok(self):
        payload = valid_result()
        for state in payload["snapshot"]["source_status"].values():
            state["status"] = "healthy"

        parsed = parse_glean_draft(
            glean_source_draft(payload), report_date=REPORT_DATE, workflow_url=WORKFLOW_URL
        )
        _, snapshot = validate_agent_result(
            parsed,
            report_now=REPORT_NOW,
            source_max_age_hours=12,
            workflow_url=WORKFLOW_URL,
        )

        self.assertTrue(
            all(state["status"] == "ok" for state in snapshot["source_status"].values())
        )

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

    def test_incomplete_consequence_is_moved_into_what_to_trust(self):
        payload = valid_result()
        payload["data_status"] = "incomplete"
        payload["snapshot"]["metrics"]["revenue"]["target_agentic_acv"] = None
        consequence = (
            "Data incomplete: the refreshed quarter goal is missing, so we cannot say "
            "whether bookings are ahead or behind plan."
        )
        payload["report_markdown"] = payload["report_markdown"].replace(
            "Show booked Agentic business separately from possible deals so a large bundled deal cannot make progress look stronger than it is.",
            "Show booked Agentic business separately from possible deals so a large bundled deal cannot make progress look stronger than it is. "
            + consequence,
        ).replace(
            "Trust the revenue and delivery facts.",
            "Trust today's booked and possible-deal numbers.",
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

        story = report.split("## What to trust", 1)[0]
        trust = report.split("## What to trust", 1)[1]
        self.assertNotIn(consequence, story)
        self.assertIn(consequence, trust)
        self.assertEqual(report.count(consequence), 1)
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

    def test_relay_accepts_fresh_source_receipts_from_late_draft(self):
        arrival_time = REPORT_NOW.replace(minute=30)
        payload = valid_dashboard_result()
        for source in payload["snapshot"]["source_status"].values():
            source["queried_at"] = arrival_time.replace(minute=25).isoformat()
        archive = FakeRelayArchive(source_message=glean_source_draft(payload))

        with patch(
            "agentic_business_pulse.now_in_timezone",
            side_effect=[REPORT_NOW, arrival_time],
        ):
            result = run_pulse_from_glean_draft(
                self.config, archive=archive, sender=self.fake_sender
            )

        self.assertEqual(result["run_status"], "success")
        self.assertEqual(result["email_status"], "accepted")
        self.assertEqual(archive.deleted, ["42", "source-7"])

    def test_relay_rejects_sources_that_become_stale_while_waiting(self):
        arrival_time = REPORT_NOW.replace(minute=30)
        payload = valid_dashboard_result()
        for source in payload["snapshot"]["source_status"].values():
            source["queried_at"] = REPORT_NOW.replace(
                day=20, hour=21, minute=15
            ).isoformat()
        archive = FakeRelayArchive(source_message=glean_source_draft(payload))

        with patch(
            "agentic_business_pulse.now_in_timezone",
            side_effect=[REPORT_NOW, arrival_time],
        ), self.assertRaisesRegex(ValidationError, "salesforce.*stale"):
            run_pulse_from_glean_draft(
                self.config, archive=archive, sender=self.fake_sender
            )

        self.assertEqual(archive.drafts, [])
        self.assertEqual(archive.deleted, [])

    def test_relay_fails_closed_when_draft_wait_crosses_report_date(self):
        start_time = REPORT_NOW.replace(hour=23, minute=50)
        arrival_time = REPORT_NOW.replace(day=22, hour=0, minute=10)
        payload = valid_dashboard_result()
        for source in payload["snapshot"]["source_status"].values():
            source["queried_at"] = start_time.isoformat()
        archive = FakeRelayArchive(source_message=glean_source_draft(payload))

        with patch(
            "agentic_business_pulse.now_in_timezone",
            side_effect=[start_time, arrival_time],
        ), self.assertRaisesRegex(ValidationError, "report date changed"):
            run_pulse_from_glean_draft(
                self.config, archive=archive, sender=self.fake_sender
            )

        self.assertEqual(archive.drafts, [])
        self.assertEqual(archive.deleted, [])

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
        message.set_content("# Weekly Agentic Customer Review — 2026-09-21\n")
        with self.assertRaisesRegex(ValidationError, "machine-readable"):
            parse_glean_draft(message, report_date=REPORT_DATE, workflow_url=WORKFLOW_URL)


class PulseWorkflowTests(unittest.TestCase):
    def test_workflow_has_weekly_monday_ist_schedule_manual_dry_run_and_read_only_permissions(self):
        workflow = (ROOT / ".github" / "workflows" / "daily-agentic-business-pulse.yml").read_text()
        self.assertIn("cron: '37 22 * * 0'", workflow)
        self.assertIn("cron: '17 23 * * 0'", workflow)
        self.assertIn("cron: '23 0 * * 1'", workflow)
        self.assertIn("cron: '37 1 * * 1'", workflow)
        self.assertIn("cron: '37 3 * * 1'", workflow)
        self.assertEqual(workflow.count("cron:"), 5)
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("pull_request:", workflow)
        self.assertIn("dry_run:", workflow)
        self.assertIn("test_send:", workflow)
        self.assertIn("PULSE_TEST_SEND:", workflow)
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertIn("PULSE_INPUT_MODE: glean_gmail_draft", workflow)
        self.assertIn("PULSE_NOT_BEFORE_LOCAL_TIME:", workflow)
        self.assertIn("PULSE_GLEAN_DRAFT_WAIT_SECONDS: '1800'", workflow)
        self.assertIn("FAILURE_DEDUPE_DAILY: 'true'", workflow)
        self.assertIn("FAILURE_TIMEZONE: Asia/Kolkata", workflow)
        self.assertIn("id: pulse", workflow)
        self.assertNotIn("\n  notify-failure:", workflow)
        self.assertIn("timeout-minutes: 345", workflow)
        self.assertIn("actions/checkout@v7", workflow)
        self.assertIn("actions/setup-python@v7", workflow)
        self.assertNotIn("PULSE_AGENT_TOKEN", workflow)
        self.assertNotIn("/api/agents/", workflow)
        self.assertNotIn("fixture", workflow.lower())
        self.assertIn("if: github.event_name != 'pull_request'", workflow)

    def test_workflow_never_uploads_pulse_report_artifacts(self):
        workflow = (ROOT / ".github" / "workflows" / "daily-agentic-business-pulse.yml").read_text()
        self.assertNotIn("actions/upload-artifact@", workflow)
        self.assertIn("python3 scripts/run-agentic-business-pulse.py", workflow)
        self.assertIn("PULSE_REPORTS_DIR: reports/agentic_business_pulse", workflow)

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
