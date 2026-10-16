"""Tests for the customer integrations pulse's report contract."""

import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from customer_integrations_pulse import (  # noqa: E402
    PulseError,
    build_report,
    parse_rows,
    render_html,
    render_markdown,
    send_owner_only,
    window,
)


def row(day, provider, company, calls, name="Example customer", device="dialpad",
        client="unclassified client", manual=0):
    return {
        "day": day,
        "provider": provider,
        "company_id": company,
        "company_name": name,
        "device_type": device,
        "logged_calls": calls,
        "client_evidence": client,
        "manual_disposition_calls": manual,
    }


class CustomerIntegrationsPulseTests(unittest.TestCase):
    def test_daily_comparison_uses_same_weekday(self):
        self.assertEqual(
            window(date(2026, 10, 15), "daily"),
            (date(2026, 10, 14), date(2026, 10, 14), date(2026, 10, 7), date(2026, 10, 7)),
        )

    def test_provider_counts_and_company_movement_are_separate(self):
        rows = parse_rows([
            row("2026-10-07", "Salesforce", 1, 200),
            row("2026-10-07", "Slack", 1, 20),
            row("2026-10-14", "Salesforce", 1, 100),
            row("2026-10-14", "Slack", 1, 25),
            row("2026-10-14", "Salesforce", 2, 12, "Second company"),
        ])
        report = build_report(rows, date(2026, 10, 15), "daily")
        sf = report["providers"][0]
        slack = report["providers"][1]
        self.assertEqual((sf["confirmed_calls"], sf["active_companies"]), (112, 2))
        self.assertEqual((slack["confirmed_calls"], slack["active_companies"]), (25, 1))
        self.assertEqual(report["customer_movements"][0]["company_name"], "Example customer")
        self.assertEqual(report["customer_movements"][0]["change_percent"], -50.0)
        self.assertIn("not proof of a failure", render_markdown(report))

    def test_brief_separates_client_evidence_and_manual_dispositions(self):
        rows = parse_rows([
            row("2026-10-07", "Salesforce", 1, 100, client="Salesforce embedded client", manual=20),
            row("2026-10-07", "Salesforce", 1, 100, client="native desktop client", manual=20),
            row("2026-10-14", "Salesforce", 1, 120, client="Salesforce embedded client", manual=24),
            row("2026-10-14", "Salesforce", 1, 80, client="native desktop client", manual=16),
        ])
        report = build_report(rows, date(2026, 10, 15), "daily")
        self.assertEqual(report["providers"][0]["manual_disposition_calls"], 40)
        self.assertEqual(report["salesforce_client_evidence"][0]["confirmed_calls"], 120)
        self.assertIn("40 (20.0%)", render_markdown(report))
        self.assertIn("AI outcomes are not included", render_markdown(report))
        self.assertIn("Dialpad Everywhere is not identified separately", render_html(report))

    def test_invalid_manual_count_is_rejected(self):
        with self.assertRaisesRegex(PulseError, "Invalid manual"):
            parse_rows([row("2026-10-14", "Salesforce", 1, 1, manual=2)])

    def test_jira_context_is_linked_but_not_treated_as_cause(self):
        rows = parse_rows([
            row("2026-10-07", "HubSpot", 1, 200),
            row("2026-10-14", "HubSpot", 1, 100),
        ])
        report = build_report(rows, date(2026, 10, 15), "daily", jira_signals=[{
            "key": "DP-213645", "provider": "HubSpot", "status": "To Do",
            "summary": "A customer reports call logging trouble",
        }])
        markdown = render_markdown(report)
        self.assertIn("https://dialpad.atlassian.net/browse/DP-213645", markdown)
        self.assertIn("not proof of the measured volume change's cause", markdown)
        self.assertIn("Related issues", render_html(report))

    def test_missing_current_data_blocks_normal_report(self):
        with self.assertRaisesRegex(PulseError, "No confirmed records"):
            build_report(parse_rows([row("2026-10-07", "Salesforce", 1, 200)]), date(2026, 10, 15), "daily")

    def test_missing_baseline_blocks_normal_report(self):
        with self.assertRaisesRegex(PulseError, "comparison window"):
            build_report(parse_rows([row("2026-10-14", "Salesforce", 1, 200)]), date(2026, 10, 15), "daily")

    def test_unknown_provider_is_rejected(self):
        with self.assertRaisesRegex(PulseError, "Unknown provider"):
            parse_rows([row("2026-10-14", "Unknown", 1, 1)])

    def test_customer_name_cannot_inject_email_html(self):
        rows = parse_rows([
            row("2026-10-07", "Salesforce", 1, 200, "<script>alert(1)</script>"),
            row("2026-10-14", "Salesforce", 1, 100, "<script>alert(1)</script>"),
        ])
        email = render_html(build_report(rows, date(2026, 10, 15), "daily"))
        self.assertNotIn("<script>", email)
        self.assertIn("&lt;script&gt;", email)

    def test_email_cannot_be_redirected_from_owner(self):
        rows = parse_rows([
            row("2026-10-07", "Salesforce", 1, 200),
            row("2026-10-14", "Salesforce", 1, 100),
        ])
        report = build_report(rows, date(2026, 10, 15), "daily")
        with patch.dict("os.environ", {
            "GMAIL_USER": "sender@dialpad.com",
            "GMAIL_APP_PASSWORD": "placeholder",
            "PULSE_OWNER_EMAIL": "someone-else@dialpad.com",
        }):
            with self.assertRaisesRegex(PulseError, "Owner-only"):
                send_owner_only(report, render_markdown(report))


if __name__ == "__main__":
    unittest.main()
