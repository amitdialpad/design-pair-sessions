"""Numbers-first company section for validated schema 7 business health data.

This module only renders supplied measures. It does not fetch data, certify an
estimate, combine company totals, or infer a missing reporting period.
"""

from __future__ import annotations

from typing import Any


UNAVAILABLE = "Unavailable"


def _cell(value: Any) -> str:
    return " ".join(str(value).split()).replace("|", "\\|")


def _money(value: float | int | None, *, signed: bool = False) -> str:
    if value is None:
        return UNAVAILABLE
    sign = "−" if value < 0 else "+" if signed and value > 0 else ""
    amount = abs(value)
    if amount >= 1_000_000:
        return f"{sign}${amount / 1_000_000:,.2f}M"
    if amount >= 1_000:
        return f"{sign}${amount / 1_000:,.1f}K"
    return f"{sign}${amount:,.2f}".removesuffix(".00")


def _percent(value: float | int | None, *, signed: bool = False) -> str:
    if value is None:
        return UNAVAILABLE
    return f"{value:+.1f}%" if signed else f"{value:.1f}%"


def _count(value: int | None, *, signed: bool = False) -> str:
    if value is None:
        return UNAVAILABLE
    return f"{value:+,d}" if signed else f"{value:,d}"


def _row(metric: str, value: str, period: str) -> str:
    return "| " + " | ".join(_cell(part) for part in (metric, value, period)) + " |"


def _table() -> list[str]:
    return ["| Metric | Value | Period |", "|---|---|---|"]


def render_transition_company_health(business: dict) -> list[str]:
    """Render already-validated business_health without changing its input.

    The existing schema uses dollar-denominated money and supplies periods for
    Salesforce and Finance snapshots and quarter bookings. The host may add
    _review_window_label from its validated comparison window for weekly
    bookings. Without it, the weekly period is displayed as unavailable.
    """
    salesforce = business.get("salesforce_operational_snapshot")
    weekly = business["weekly_sales"]
    quarter = business["quarter"]
    finance = business["latest_arr_period"]
    source_gaps: list[str] = []
    unavailable_bookings: list[str] = []

    lines = ["", "## Company revenue and sales", "", *_table()]
    if salesforce is None:
        lines.extend(
            _row(metric, UNAVAILABLE, UNAVAILABLE)
            for metric in (
                "Annual recurring contract value · Dialpad Salesforce accounts",
                "Quarter-start comparable value",
                "Quarter change · same Salesforce measure",
                "Paying customer accounts / licenses",
            )
        )
        source_gaps.append("Salesforce operational snapshot: Unavailable.")
    else:
        as_of = f"As of {salesforce['as_of_date']}"
        quarter_start = f"Start of {salesforce['quarter_label']}"
        quarter_to_date = f"{salesforce['quarter_label']} to {salesforce['as_of_date']}"
        lines.extend(
            [
                _row(
                    "Annual recurring contract value · Dialpad Salesforce accounts",
                    _money(salesforce["current_arr"]),
                    as_of,
                ),
                _row("Quarter-start comparable value", _money(salesforce["quarter_start_arr"]), quarter_start),
                _row(
                    "Quarter change · same Salesforce measure",
                    f"{_money(salesforce['net_arr_change'], signed=True)} ({_percent(salesforce['net_arr_change_pct'], signed=True)})",
                    quarter_to_date,
                ),
                _row(
                    "Paying customer accounts / licenses",
                    f"{_count(salesforce['paying_accounts'])} accounts / {_count(salesforce['paid_licenses'])} licenses",
                    as_of,
                ),
            ]
        )
        comparison = salesforce["comparison"]
        previous = comparison["previous_snapshot_date"]
        if previous is None:
            source_gaps.append(
                "Prior-report comparison: Unavailable — no comparable prior snapshot. "
                + _cell(comparison["comparison_note"])
            )
        else:
            lines.append(
                _row(
                    "Change since prior Salesforce snapshot",
                    f"{_money(comparison['arr_change_since_previous'], signed=True)} / "
                    f"{_count(comparison['paying_account_change'], signed=True)} accounts / "
                    f"{_count(comparison['paid_license_change'], signed=True)} licenses",
                    f"{previous} to {salesforce['as_of_date']}",
                )
            )

    review_window = business.get("_review_window_label")
    weekly_period = review_window if isinstance(review_window, str) and review_window.strip() else UNAVAILABLE
    if weekly is None:
        unavailable_bookings.append(f"Weekly bookings: Unavailable — {_cell(business['weekly_sales_note'])}")
    else:
        weekly_values = (
            _money(weekly["total_bookings"]),
            _money(weekly["core_bookings"]),
            f"{_money(weekly['agentic_bookings'])} ({_percent(weekly['agentic_share_pct'])} share)",
        )
        if weekly_period == UNAVAILABLE:
            source_gaps.append("Weekly bookings period: Unavailable in the supplied measure.")
        for metric, value in zip(
            ("Weekly bookings · total", "Weekly bookings · core / non-Agentic", "Weekly bookings · Agentic"),
            weekly_values,
            strict=True,
        ):
            lines.append(_row(metric, value, weekly_period))

    if quarter is None:
        unavailable_bookings.append(f"Quarter bookings / target: Unavailable — {_cell(business['quarter_note'])}")
    else:
        period = quarter["label"]
        verified_target = quarter["target_status"] == "verified"
        target = _money(quarter["target_bookings"]) if verified_target else UNAVAILABLE
        attainment = _percent(quarter["attainment_pct"]) if verified_target else UNAVAILABLE
        lines.extend(
            [
                _row("Quarter bookings · actual", _money(quarter["actual_bookings"]), period),
                _row("Quarter target / attainment", f"{target} / {attainment}", period),
                _row(
                    "Quarter bookings · Agentic",
                    f"{_money(quarter['agentic_bookings'])} ({_percent(quarter['agentic_share_pct'])} share)",
                    period,
                ),
            ]
        )
        if verified_target:
            lines.append(
                _row(
                    "Gap to quarter target / required weekly bookings pace",
                    f"{_money(quarter['gap_to_target'])} / {_money(quarter['required_weekly_pace'])}",
                    period,
                )
            )
        else:
            source_gaps.append(
                f"Quarter target and attainment: Unavailable ({quarter['target_status']}) — "
                + _cell(quarter["target_note"])
            )
        if any(quarter[field] is not None for field in ("commit_forecast", "best_case_forecast")):
            lines.append(
                _row(
                    "Quarter bookings forecast · commit / best case",
                    f"{_money(quarter['commit_forecast'])} / {_money(quarter['best_case_forecast'])}",
                    period,
                )
            )
        if quarter["previous_quarter_bookings"] is not None:
            lines.append(
                _row(
                    "Previous-quarter bookings",
                    _money(quarter["previous_quarter_bookings"]),
                    "Previous quarter · exact period Unavailable",
                )
            )

    if unavailable_bookings:
        lines.extend(["", "**Bookings / target availability:** " + " ".join(unavailable_bookings)])

    if finance is None:
        source_gaps.append(f"Finance ARR bridge: Unavailable — {_cell(business['latest_arr_note'])}")
    else:
        period = finance["label"]
        lines.extend(
            [
                "",
                "**Latest Finance ARR bridge · separate from the Salesforce estimate**",
                "",
                *_table(),
                _row("Net ARR change", _money(finance["net_arr_change"], signed=True), period),
                _row(
                    "New + expansion / churn + contraction",
                    f"{_money(finance['new_plus_expansion'], signed=True)} / {_money(finance['churn_plus_contraction'], signed=True)}",
                    period,
                ),
                _row(
                    "Net customers / paid license change",
                    f"{_count(finance['net_customers'], signed=True)} customers / {_count(finance['paid_license_change'], signed=True)} licenses",
                    period,
                ),
            ]
        )

    interpretation = _cell(business["verdict_reason"])
    if salesforce is not None:
        interpretation += (
            f" The quarter-opening cohort changed {_money(salesforce['opening_cohort_change'], signed=True)}; "
            f"accounts without an opening snapshot currently hold {_money(salesforce['new_or_unsnapshotted_arr'])}. "
            "Those accounts may be new, reactivated or previously unsnapshotted; their full value is not all new growth."
        )
    lines.extend(["", f"**What this tells us (interpretation of available measures):** {interpretation}"])
    if source_gaps:
        lines.extend(["", "**Source gaps**", "", *(f"- {gap}" for gap in source_gaps)])
    lines.extend(
        [
            "",
            "**Data note:** Salesforce is Dialpad's own sales system. Its annual recurring contract value is an operational estimate, "
            "not earned revenue or Finance-certified ARR. Its Account-record perimeter has not been reconciled as a combined Dialpad + Ada total. "
            "Bookings, forecasts and the Finance ARR bridge are separate measures.",
        ]
    )
    if salesforce is not None:
        lines.append(f"Salesforce method: {_cell(salesforce['method_note'])}")
    return lines
