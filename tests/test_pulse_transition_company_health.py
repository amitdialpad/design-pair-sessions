"""Synthetic-only renderer fixtures; no live company or customer measures."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from pulse_transition_company_health import render_transition_company_health  # noqa: E402


def synthetic_business() -> dict:
    return {
        "verdict": "strengthening",
        "verdict_reason": "The opening cohort declined, while the available snapshot total increased.",
        "weekly_sales": {
            "total_bookings": 100_000,
            "core_bookings": 85_000,
            "agentic_bookings": 15_000,
            "agentic_share_pct": 15.0,
        },
        "salesforce_operational_snapshot": {
            "as_of_date": "2032-05-17",
            "quarter_label": "Q2 FY33",
            "quarter_start_arr": 1_200_000,
            "current_arr": 1_500_000,
            "net_arr_change": 300_000,
            "net_arr_change_pct": 25.0,
            "opening_cohort_current_arr": 1_100_000,
            "opening_cohort_change": -100_000,
            "new_or_unsnapshotted_arr": 400_000,
            "paying_accounts": 120,
            "paid_licenses": 4_200,
            "method_note": "Synthetic account-field estimate, with comparable quarter-opening fields.",
            "comparison": {
                "previous_snapshot_date": None,
                "arr_change_since_previous": None,
                "paying_account_change": None,
                "paid_license_change": None,
                "comparison_note": "A matching prior extraction is not available.",
            },
        },
        "latest_arr_period": {
            "label": "March 2032",
            "net_arr_change": 12_000,
            "new_plus_expansion": 20_000,
            "churn_plus_contraction": -8_000,
            "net_customers": 2,
            "paid_license_change": 18,
        },
        "quarter": {
            "label": "Q2 FY33 · through 2032-05-17",
            "actual_bookings": 500_000,
            "target_status": "verified",
            "target_bookings": 1_000_000,
            "attainment_pct": 50.0,
            "gap_to_target": 500_000,
            "required_weekly_pace": 50_000,
            "commit_forecast": 800_000,
            "best_case_forecast": 1_100_000,
            "previous_quarter_bookings": 650_000,
            "agentic_bookings": 100_000,
            "agentic_share_pct": 20.0,
        },
    }


class TransitionCompanyHealthTests(unittest.TestCase):
    def render(self, business: dict) -> str:
        lines = render_transition_company_health(business)
        self.assertIsInstance(lines, list)
        self.assertTrue(all(isinstance(line, str) for line in lines))
        return "\n".join(lines)

    def test_available_measures_keep_values_definitions_and_real_periods(self):
        text = self.render(synthetic_business())
        self.assertIn("## Company revenue and sales", text)
        self.assertIn("| Annual recurring contract value · Dialpad Salesforce accounts | $1.50M | As of 2032-05-17 |", text)
        self.assertIn("| Quarter-start comparable value | $1.20M | Start of Q2 FY33 |", text)
        self.assertIn("+$300.0K (+25.0%)", text)
        self.assertIn("120 accounts / 4,200 licenses", text)
        self.assertIn("| Weekly bookings · total | $100.0K | Unavailable |", text)
        self.assertIn("| Weekly bookings · core / non-Agentic | $85.0K | Unavailable |", text)
        self.assertIn("$15.0K (15.0% share)", text)
        self.assertIn("| Quarter bookings · actual | $500.0K | Q2 FY33 · through 2032-05-17 |", text)
        self.assertIn("| Quarter target / attainment | $1.00M / 50.0% |", text)
        self.assertIn("$100.0K (20.0% share)", text)
        self.assertIn("$500.0K / $50.0K", text)
        self.assertIn("$800.0K / $1.10M", text)
        self.assertIn("$650.0K | Previous quarter · exact period Unavailable", text)

    def test_explicit_null_measures_are_unavailable_and_keep_specific_notes(self):
        business = synthetic_business()
        business.update(
            weekly_sales=None,
            weekly_sales_note="Weekly ledger extraction is pending.",
            quarter=None,
            quarter_note="Current quarter bookings cannot be verified.",
            latest_arr_period=None,
            latest_arr_note="Finance has not supplied the bridge.",
        )
        text = self.render(business)
        self.assertIn("| Weekly bookings · total | Unavailable | Unavailable |", text)
        self.assertIn("| Quarter bookings · actual | Unavailable | Unavailable |", text)
        self.assertIn("Weekly ledger extraction is pending.", text)
        self.assertIn("Current quarter bookings cannot be verified.", text)
        self.assertIn("Finance ARR bridge: Unavailable — Finance has not supplied the bridge.", text)
        self.assertNotIn("**Latest Finance ARR bridge", text)
        self.assertNotIn("| Weekly bookings · total | $0", text)

    def test_zero_is_a_verified_value_not_unavailable(self):
        business = synthetic_business()
        business["weekly_sales"] = dict(total_bookings=0, core_bookings=0, agentic_bookings=0, agentic_share_pct=0)
        business["latest_arr_period"].update(net_arr_change=0, new_plus_expansion=0, churn_plus_contraction=0, net_customers=0, paid_license_change=0)
        business["quarter"].update(actual_bookings=0, agentic_bookings=0, agentic_share_pct=0, attainment_pct=0, gap_to_target=1_000_000, required_weekly_pace=0, commit_forecast=0, best_case_forecast=None)
        text = self.render(business)
        self.assertIn("| Weekly bookings · total | $0 |", text)
        self.assertIn("| Weekly bookings · Agentic | $0 (0.0% share) |", text)
        self.assertIn("$1.00M / 0.0%", text)
        self.assertIn("| Quarter bookings forecast · commit / best case | $0 / Unavailable |", text)
        self.assertIn("| Net ARR change | $0 | March 2032 |", text)
        self.assertIn("+0 customers / +0 licenses", text)

    def test_missing_target_does_not_hide_actual_forecast_or_agentic(self):
        business = synthetic_business()
        business["quarter"].update(target_status="unverified", target_bookings=None, attainment_pct=None, gap_to_target=None, required_weekly_pace=None, target_note="The quota extract omits one sales segment.")
        text = self.render(business)
        self.assertIn("| Quarter target / attainment | Unavailable / Unavailable |", text)
        self.assertIn("Quarter target and attainment: Unavailable (unverified)", text)
        self.assertIn("The quota extract omits one sales segment.", text)
        self.assertIn("| Quarter bookings · actual | $500.0K |", text)
        self.assertIn("$100.0K (20.0% share)", text)
        self.assertIn("$800.0K / $1.10M", text)
        self.assertNotIn("| Gap to quarter target", text)

    def test_missing_forecast_and_pace_never_become_zero(self):
        business = synthetic_business()
        business["quarter"].update(commit_forecast=None, best_case_forecast=None, required_weekly_pace=None, previous_quarter_bookings=None)
        text = self.render(business)
        self.assertIn("$500.0K / Unavailable", text)
        self.assertNotIn("Quarter bookings forecast", text)
        self.assertNotIn("Previous-quarter bookings", text)

    def test_prior_report_comparison_uses_its_dates_and_can_show_declines(self):
        business = synthetic_business()
        business["salesforce_operational_snapshot"]["comparison"] = {
            "previous_snapshot_date": "2032-05-10",
            "arr_change_since_previous": -5_000,
            "paying_account_change": -2,
            "paid_license_change": 0,
        }
        text = self.render(business)
        self.assertIn("−$5.0K / -2 accounts / +0 licenses | 2032-05-10 to 2032-05-17", text)
        self.assertNotIn("no comparable prior snapshot", text)

    def test_no_prior_snapshot_is_not_mislabeled_as_a_weekly_change(self):
        text = self.render(synthetic_business())
        self.assertIn("Prior-report comparison: Unavailable — no comparable prior snapshot.", text)
        self.assertIn("A matching prior extraction is not available.", text)
        self.assertIn("Weekly bookings period: Unavailable", text)
        self.assertNotIn("Change since prior Salesforce snapshot", text)

    def test_host_review_window_labels_weekly_measures_without_using_snapshot_date(self):
        business = synthetic_business()
        business["_review_window_label"] = "2032-05-10 to 2032-05-16"
        text = self.render(business)
        self.assertIn("| Weekly bookings · total | $100.0K | 2032-05-10 to 2032-05-16 |", text)
        self.assertIn("| Weekly bookings · Agentic | $15.0K (15.0% share) | 2032-05-10 to 2032-05-16 |", text)
        self.assertNotIn("Weekly bookings period: Unavailable", text)
        self.assertNotIn("| Weekly bookings · total | $100.0K | As of 2032-05-17", text)

    def test_estimate_and_finance_bridge_are_separate_and_verdict_is_scoped(self):
        text = self.render(synthetic_business())
        self.assertIn("not earned revenue or Finance-certified ARR", text)
        self.assertIn("Salesforce is Dialpad's own sales system", text)
        self.assertIn("Account-record perimeter has not been reconciled as a combined Dialpad + Ada total", text)
        self.assertIn("Latest Finance ARR bridge · separate from the Salesforce estimate", text)
        self.assertIn("| Net ARR change | +$12.0K | March 2032 |", text)
        self.assertIn("+$20.0K / −$8.0K", text)
        self.assertIn("What this tells us (interpretation of available measures)", text)
        self.assertNotIn("Strengthening", text)
        self.assertNotIn("strengthening", text)
        self.assertIn("quarter-opening cohort changed −$100.0K", text)
        self.assertIn("accounts without an opening snapshot currently hold $400.0K", text)
        self.assertIn("their full value is not all new growth", text)

    def test_renderer_does_not_combine_ada_values_or_modify_input(self):
        business = synthetic_business()
        business["ada_arr"] = 9_999_999
        business["migration_count"] = 987
        before = copy.deepcopy(business)
        text = self.render(business)
        self.assertEqual(business, before)
        self.assertNotIn("9,999,999", text)
        self.assertNotIn("987", text)
        self.assertIn("| Annual recurring contract value · Dialpad Salesforce accounts | $1.50M |", text)
        self.assertIn("has not been reconciled as a combined Dialpad + Ada total", text)

    def test_missing_optional_salesforce_snapshot_is_explicit(self):
        business = synthetic_business()
        business.pop("salesforce_operational_snapshot")
        text = self.render(business)
        self.assertIn("| Annual recurring contract value · Dialpad Salesforce accounts | Unavailable | Unavailable |", text)
        self.assertIn("Salesforce operational snapshot: Unavailable.", text)
        self.assertIn("| Quarter bookings · actual | $500.0K |", text)

    def test_notes_cannot_break_markdown_rows_or_create_new_sections(self):
        business = synthetic_business()
        business["quarter"]["label"] = "Synthetic quarter | verified\ncontinued"
        business["verdict_reason"] = "One source\n## Injected heading"
        text = self.render(business)
        self.assertIn("Synthetic quarter \\| verified continued", text)
        self.assertNotIn("\n## Injected heading", text)


if __name__ == "__main__":
    unittest.main()
