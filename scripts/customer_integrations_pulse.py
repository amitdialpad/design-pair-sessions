"""Evidence-first customer integration pulse.

The first source is persisted call-log IDs in Firespotter. These prove a
successful external artifact, not an attempted or failed integration action.
The report deliberately names this coverage instead of implying that it is
a census of every Dialpad integration.
"""

from __future__ import annotations

import argparse
import html
import imaplib
import json
import os
import smtplib
import ssl
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


ZONE = ZoneInfo("Asia/Kolkata")
PROVIDERS = ("Salesforce", "Slack", "Zendesk", "HubSpot")
MIN_CHANGE_CALLS = 25
MIN_CHANGE_PERCENT = 30
MIN_CURRENT_CALLS = 100

# CallInfo stores JSON as a string. The other observed key,
# agent-assist-conversation-id, is not an external logging destination.
QUERY = """
WITH calls AS (
  SELECT
    DATE(c.date_started, 'Asia/Kolkata') AS day,
    c.company_id,
    c.__key__.id AS call_id,
    LOWER(COALESCE(c.device_type, 'unknown')) AS device_type,
    NULLIF(TRIM(c.salesforce_activity_id), '') IS NOT NULL AS salesforce,
    SAFE.PARSE_JSON(ci.cloud_elements_call_ids) AS external_ids
  FROM `firespotter.com:firespotter-analytics.uv_entities.Call` AS c
  LEFT JOIN `firespotter.com:firespotter-analytics.uv_entities.CallInfo` AS ci
    ON SAFE_CAST(ci.__key__.name AS INT64) = c.__key__.id
    AND ci.date_created >= TIMESTAMP_SUB(@start_time, INTERVAL 2 DAY)
    AND ci.date_created < TIMESTAMP_ADD(@end_time, INTERVAL 2 DAY)
  WHERE c.date_started >= @start_time AND c.date_started < @end_time
), confirmed AS (
  SELECT day, company_id, call_id, device_type, provider
  FROM calls, UNNEST([
    STRUCT('Salesforce' AS provider, salesforce AS saved),
    STRUCT('Slack' AS provider, JSON_VALUE(external_ids, '$.slack') IS NOT NULL AS saved),
    STRUCT('Zendesk' AS provider, JSON_VALUE(external_ids, '$.zendesk') IS NOT NULL AS saved),
    STRUCT('HubSpot' AS provider, JSON_VALUE(external_ids, '$.hubspotcrm') IS NOT NULL AS saved)
  ])
  WHERE saved
), company_names AS (
  SELECT __key__.id AS company_id, name
  FROM `firespotter.com:firespotter-analytics.uv_entities.Company`
)
SELECT
  day, provider, confirmed.company_id,
  COALESCE(NULLIF(company_names.name, ''), 'Unknown company') AS company_name,
  device_type, COUNT(DISTINCT call_id) AS logged_calls
FROM confirmed
LEFT JOIN company_names USING (company_id)
GROUP BY 1, 2, 3, 4, 5
"""


class PulseError(RuntimeError):
    """The normal report must not be sent."""


@dataclass(frozen=True)
class Row:
    day: date
    provider: str
    company_id: int | None
    company_name: str
    device_type: str
    logged_calls: int


def parse_rows(raw: Iterable[dict[str, Any]]) -> list[Row]:
    rows: list[Row] = []
    for item in raw:
        provider = str(item["provider"])
        if provider not in PROVIDERS:
            raise PulseError(f"Unknown provider in source rows: {provider}")
        calls = int(item["logged_calls"])
        if calls < 0:
            raise PulseError("Negative logged-call count")
        rows.append(Row(
            day=date.fromisoformat(str(item["day"])),
            provider=provider,
            company_id=int(item["company_id"]) if item.get("company_id") is not None else None,
            company_name=str(item.get("company_name") or "Unknown company"),
            device_type=str(item.get("device_type") or "unknown"),
            logged_calls=calls,
        ))
    return rows


def window(report_date: date, cadence: str) -> tuple[date, date, date, date]:
    current_end = report_date - timedelta(days=1)
    length = 7 if cadence == "weekly" else 1
    current_start = current_end - timedelta(days=length - 1)
    # Daily compares the same weekday in the prior week. Weekly compares the
    # immediately preceding seven days.
    previous_end = current_end - timedelta(days=7)
    previous_start = previous_end - timedelta(days=length - 1)
    return current_start, current_end, previous_start, previous_end


def _total(rows: Iterable[Row], start: date, end: date) -> int:
    return sum(row.logged_calls for row in rows if start <= row.day <= end)


def _pct_change(current: int, previous: int) -> float | None:
    if previous == 0:
        return None
    return round((current - previous) * 100 / previous, 1)


def _change_label(current: int, change: float | None) -> str:
    if change is None:
        return "No activity" if current == 0 else "No baseline"
    return f"{change:+.1f}%"


def build_report(rows: list[Row], report_date: date, cadence: str, run_url: str = "") -> dict[str, Any]:
    if cadence not in {"daily", "weekly"}:
        raise PulseError("Cadence must be daily or weekly")
    current_start, current_end, previous_start, previous_end = window(report_date, cadence)
    if not rows or _total(rows, current_start, current_end) == 0:
        raise PulseError("No confirmed records in the current reporting window")
    if _total(rows, previous_start, previous_end) == 0:
        raise PulseError("No confirmed records in the comparison window")
    if any(row.day < previous_start or row.day > current_end for row in rows):
        raise PulseError("Source rows fall outside the requested windows")

    provider_stats: list[dict[str, Any]] = []
    for provider in PROVIDERS:
        own = [row for row in rows if row.provider == provider]
        current = _total(own, current_start, current_end)
        previous = _total(own, previous_start, previous_end)
        companies = {row.company_id for row in own if current_start <= row.day <= current_end and row.company_id is not None and row.logged_calls}
        provider_stats.append({
            "provider": provider,
            "confirmed_calls": current,
            "previous_confirmed_calls": previous,
            "change_percent": _pct_change(current, previous),
            "active_companies": len(companies),
        })

    by_customer: dict[tuple[str, int], dict[str, Any]] = defaultdict(lambda: {"current": 0, "previous": 0, "name": ""})
    for row in rows:
        if row.company_id is None:
            continue
        record = by_customer[(row.provider, row.company_id)]
        record["name"] = row.company_name
        if current_start <= row.day <= current_end:
            record["current"] += row.logged_calls
        elif previous_start <= row.day <= previous_end:
            record["previous"] += row.logged_calls

    movements = []
    for (provider, company_id), counts in by_customer.items():
        current, previous = counts["current"], counts["previous"]
        change = _pct_change(current, previous)
        if (
            counts["name"] == "Unknown company"
            or previous < MIN_CURRENT_CALLS
            or abs(current - previous) < MIN_CHANGE_CALLS
            or change is None
            or abs(change) < MIN_CHANGE_PERCENT
        ):
            continue
        movements.append({
            "provider": provider,
            "company_id": company_id,
            "company_name": counts["name"],
            "confirmed_calls": current,
            "previous_confirmed_calls": previous,
            "change_percent": change,
        })
    movements.sort(key=lambda value: (value["change_percent"] >= 0, -abs(value["confirmed_calls"] - value["previous_confirmed_calls"])))

    return {
        "report_date": report_date.isoformat(),
        "cadence": cadence,
        "current_window": [current_start.isoformat(), current_end.isoformat()],
        "comparison_window": [previous_start.isoformat(), previous_end.isoformat()],
        "source": "Firespotter persisted external record IDs",
        "source_job_url": run_url,
        "providers": provider_stats,
        "customer_movements": movements[:8],
        "coverage": [
            "Counts prove saved external records, not attempts, failures, retries, or logging latency.",
            "This source covers Salesforce, Slack, Zendesk, and HubSpot call artifacts. DialApp and other integrations are not included.",
            "Calls with two destinations count once under each provider; provider totals must not be added into a unique-call total.",
            "Device type is retained in source rows, but CTI, app, and Everywhere surface attribution is not yet verified.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    current = report["current_window"]
    previous = report["comparison_window"]
    lines = [
        f"# Customer Integrations Pulse — {report['report_date']}",
        f"{report['cadence'].title()} view: {current[0]} to {current[1]}; compared with {previous[0]} to {previous[1]}.",
        "",
        "## At a glance",
        "Confirmed call records by integration. Each integration is counted separately.",
        "",
        "| Integration | Confirmed calls | Active companies | Change |",
        "|---|---:|---:|---:|",
    ]
    for provider in report["providers"]:
        change = provider["change_percent"]
        change_text = _change_label(provider["confirmed_calls"], change)
        lines.append(f"| {provider['provider']} | {provider['confirmed_calls']:,} | {provider['active_companies']:,} | {change_text} |")
    lines += ["", "## Customer shifts worth checking"]
    if report["customer_movements"]:
        for item in report["customer_movements"]:
            company = " ".join(item["company_name"].split()).replace("\\", "\\\\").replace("`", "\\`")
            lines.append(
                f"- {company} · {item['provider']}: {item['confirmed_calls']:,} confirmed calls "
                f"versus {item['previous_confirmed_calls']:,} in the comparison window ({item['change_percent']:+.1f}%). "
                "This is a change in recorded volume, not proof of a failure or a customer decision."
            )
    else:
        lines.append("- No customer crossed the current volume-change threshold.")
    lines += ["", "## What this report can and cannot say"]
    lines += [f"- {note}" for note in report["coverage"]]
    if report.get("source_job_url"):
        lines += ["", f"Source query: {report['source_job_url']}"]
    return "\n".join(lines) + "\n"


def render_html(report: dict[str, Any]) -> str:
    """Render a readable email without interpreting customer text as HTML."""
    def safe(value: Any) -> str:
        return html.escape(str(value), quote=True)

    rows = []
    for item in report["providers"]:
        change = item["change_percent"]
        change_text = _change_label(item["confirmed_calls"], change)
        rows.append(
            "<tr>"
            f"<td>{safe(item['provider'])}</td>"
            f"<td align='right'>{item['confirmed_calls']:,}</td>"
            f"<td align='right'>{item['active_companies']:,}</td>"
            f"<td align='right'>{safe(change_text)}</td>"
            "</tr>"
        )
    movements = []
    for item in report["customer_movements"]:
        movements.append(
            "<li>"
            f"<strong>{safe(item['company_name'])}</strong> · {safe(item['provider'])}: "
            f"{item['confirmed_calls']:,} confirmed calls versus "
            f"{item['previous_confirmed_calls']:,} in the comparison window "
            f"({item['change_percent']:+.1f}%). This is a volume change, "
            "not proof of a failure or a customer decision.</li>"
        )
    if not movements:
        movements.append("<li>No customer crossed the current volume-change threshold.</li>")
    notes = "".join(f"<li>{safe(note)}</li>" for note in report["coverage"])
    current = report["current_window"]
    previous = report["comparison_window"]
    source = report.get("source_job_url", "")
    source_link = (
        f"<p><a href='{safe(source)}'>Source query</a></p>"
        if source.startswith("https://console.cloud.google.com/bigquery?") else ""
    )
    return (
        "<html><body style='font-family:Arial,sans-serif;max-width:720px;"
        "line-height:1.5;color:#252525'>"
        f"<h1>Customer Integrations Pulse</h1><p>{safe(report['cadence'].title())} view: "
        f"{safe(current[0])} to {safe(current[1])}; compared with "
        f"{safe(previous[0])} to {safe(previous[1])}.</p>"
        "<h2>At a glance</h2><p>Confirmed call records by integration. "
        "Each integration is counted separately.</p>"
        "<table cellpadding='8' cellspacing='0' border='1' "
        "style='border-collapse:collapse;border-color:#ddd'>"
        "<tr><th>Integration</th><th>Confirmed calls</th>"
        "<th>Active companies</th><th>Change</th></tr>"
        + "".join(rows) + "</table>"
        "<h2>Customer shifts worth checking</h2><ul>" + "".join(movements) + "</ul>"
        "<h2>What this report can and cannot say</h2><ul>" + notes + "</ul>"
        + source_link + "</body></html>"
    )


def _query_live(start: date, end: date) -> tuple[list[dict[str, Any]], str]:
    try:
        from google.cloud import bigquery
    except ImportError as error:
        raise PulseError("Install google-cloud-bigquery for live collection") from error
    client = bigquery.Client(project=os.environ.get("PULSE_BQ_BILLING_PROJECT", "uv-beta"))
    start_time = datetime.combine(start, datetime.min.time(), tzinfo=ZONE)
    end_time = datetime.combine(end + timedelta(days=1), datetime.min.time(), tzinfo=ZONE)
    config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start_time),
        bigquery.ScalarQueryParameter("end_time", "TIMESTAMP", end_time),
    ])
    job = client.query(QUERY, job_config=config, location="US")
    result = job.result(timeout=900)
    rows = [dict(row.items()) for row in result]
    job_url = f"https://console.cloud.google.com/bigquery?project={client.project}&j=bq:US:{job.job_id}"
    return rows, job_url


def _already_sent(message_id: str, user: str, password: str) -> bool:
    client = imaplib.IMAP4_SSL("imap.gmail.com", 993, ssl_context=ssl.create_default_context())
    try:
        client.login(user, password)
        status, _ = client.select('"[Gmail]/Sent Mail"', readonly=True)
        if status != "OK":
            raise PulseError("Cannot verify Gmail Sent before delivery")
        status, rows = client.uid("search", None, "HEADER", "Message-ID", f'"{message_id}"')
        if status != "OK":
            raise PulseError("Cannot search Gmail Sent before delivery")
        return bool(rows and rows[0].strip())
    finally:
        client.logout()


def send_owner_only(report: dict[str, Any], markdown: str) -> str:
    user = os.environ.get("GMAIL_USER", "").strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    owner = os.environ.get("PULSE_OWNER_EMAIL", "amit.ayre@dialpad.com").strip()
    if not user or not password or owner.casefold() != "amit.ayre@dialpad.com":
        raise PulseError("Owner-only Gmail credentials and recipient are required")
    message_id = f"<customer-integrations-pulse-{report['report_date']}-{report['cadence']}@dialpad.com>"
    if _already_sent(message_id, user, password):
        return "duplicate_skipped"
    message = EmailMessage()
    message["Subject"] = f"Customer Integrations Pulse — {report['cadence'].title()} — {report['report_date']}"
    message["From"] = user
    message["To"] = owner
    message["Message-ID"] = message_id
    message.set_content(markdown)
    message.add_alternative(render_html(report), subtype="html")
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=60) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(user, password)
        server.send_message(message, to_addrs=[owner])
    return "sent"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-date", type=date.fromisoformat, default=datetime.now(ZONE).date())
    parser.add_argument("--cadence", choices=["auto", "daily", "weekly"], default="auto")
    parser.add_argument("--input", type=Path, help="Read a source snapshot instead of querying BigQuery")
    parser.add_argument("--output-dir", type=Path, default=Path("reports/customer_integrations_pulse"))
    parser.add_argument("--send", action="store_true", help="Send only to the owner's approved address")
    parser.add_argument("--quiet", action="store_true", help="Do not print report contents")
    args = parser.parse_args()
    if args.cadence == "auto":
        args.cadence = "weekly" if args.report_date.weekday() == 0 else "daily"
    current_start, current_end, previous_start, _ = window(args.report_date, args.cadence)
    if args.input:
        source_rows = json.loads(args.input.read_text())
        job_url = ""
    else:
        source_rows, job_url = _query_live(previous_start, current_end)
    report = build_report(parse_rows(source_rows), args.report_date, args.cadence, job_url)
    markdown = render_markdown(report)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_dir / f"{args.report_date}-{args.cadence}"
    prefix.with_suffix(".md").write_text(markdown)
    prefix.with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
    if args.send:
        print(send_owner_only(report, markdown))
    elif args.quiet:
        print(f"Generated {args.cadence} integrations pulse for {args.report_date}")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
