---
name: daily-agentic-business-pulse
description: Produces a weekly, evidence-based Agentic customer review showing verified movement, systems in use, delivery risks, Jira changes, commercial movement, and practical ways Amit can help.
---
# Weekly Agentic Customer Review

## Mission

Run every Monday at 08:00 `Asia/Kolkata` so the approved relay can deliver at 09:00. Cover the previous Monday through Sunday and compare with the preceding weekly review.

Answer from specific, current evidence:

- Which named customers visibly moved, remained blocked, or produced another useful operating signal?
- Where are those customers in `Build → Test → Validate → Publish → Live`, when the source says so?
- Which agent, use case, connector, skill, or system is involved?
- What changed during the week?
- Which customer blockers or Jira issues changed?
- Which commercial records advanced, slipped, won, lost, or changed value?
- What can Amit clarify, design, unblock, or follow up on?

This is a verified-movement review, not a portfolio census. Include only named customers with a specific, current, safely attributable signal. A source-reported aggregate such as `30 deployments` may appear as context, but never claim that the included rows are the complete cohort. Sort failing customers first, then movers, then other useful current signals.

This is a customer operating review, not a design essay. Do not repeat a known product problem unless its affected customer, severity, owner, status, or commercial effect changed this week. Open with an evidence-gated `Executive signal`, then present the Agentic customer review and one compact `CEO View — Company Health` for company-level direction.

## Safety

All company-source access is read-only.

- Use only approved search, read, list, view, code-search, SOQL-query, Jira-search, email-search, and calendar-search operations.
- Never create, update, comment, transition, label, configure, grant, export, delete, or send in Salesforce, Jira, repositories, Glean content, or customer systems.
- Never bypass a permission boundary. Company-health metrics may use only already-authorized read-only Salesforce, billing/ARR, Finance, RevOps, Glean, or governed analytics sources.
- Never infer usage, action success, containment, resolution, CSAT, or other product telemetry.
- Never store raw conversations, transcripts, prompts, tool arguments, customer payloads, credentials, or secrets.
- The only permitted write is the existing Gmail MCP `Create Draft` action for the private relay envelope, addressed only to `amit.ayre@dialpad.com`.

## Required sources

Use each current source for the fact it owns and preserve its direct link and query time.

1. **Salesforce** — exact-match identity, customer and commercial stage, Agentic-specific value, and recorded use case for named customers already found in current evidence.
2. **Jira** — customer-impacting bugs, current status, and issues created or materially changed during the weekly window.
3. **Glean company search, documents, email, and calendar** — current customer context, implementation updates, Helena's weekly Agentic newsletter, meetings, and decisions.
4. **Production code (optional)** — implementation context only when a changed customer blocker needs explanation. Never use code existence as proof that a customer is live.

A normal report requires Salesforce, Jira, and Glean to be healthy, fresh, linked, and recorded with `access_mode: read_only`. Include a production-code receipt only when Code Search was needed.

## Weekly procedure

### 1. Establish verified customer signals

Start with current weekly operating material, Glean documents, email, and meetings. Include a customer only when those sources or an explicitly linked Jira/Salesforce record provide a specific current movement, blocker, milestone, decision, system, or commercial signal.

Use Salesforce only to enrich an already named customer. Join records using a canonical account/company identifier or an exact, unambiguous name. Never guess from an abbreviation, domain, contact, opportunity title, or similar name. Omit an unsafe enrichment; do not drop an otherwise verified customer signal.

When an authoritative source reports a total deployment count, record it as `summary.reported_deployment_count`. This number is context only and is not derived from the included rows.

### 2. Assign one journey stage

Use exactly one:

- `build`
- `test`
- `validate`
- `publish`
- `live`
- `paused`
- `unknown` — current approved evidence does not support a safe lifecycle mapping.

This is the customer's current journey stage, not a claim about general product readiness. Use `unknown` rather than mapping a Salesforce sales stage to an operating lifecycle without explicit evidence.

### 3. Record systems and weekly movement

For every included customer signal:

- Record the agent or use case.
- Record each known connector, skill, or system and status: `building`, `testing`, `connected`, `failing`, or `unknown`.
- Write one short `change_this_week` statement naming the specific verified signal. Do not add a row merely to say nothing was found.
- Count Jira issues created or materially changed in the weekly window.
- Count currently open customer-impacting Jira bugs and retain their keys.
- Record the Salesforce commercial stage.
- Record commercial movement as `advanced`, `slipped`, `won`, `lost`, `value_changed`, or `no_change`.
- Record Agentic-specific contract value only when its governed field exists. Never substitute the total bundled opportunity amount.
- Write one short `next_watch` describing the next customer proof, blocker decision, checkpoint, or concrete way Amit can help.

Assign one row movement:

- `failing` — a changed customer blocker needs attention.
- `moved` — lifecycle, customer, delivery, or commercial state materially changed.
- `no_change` — a useful current signal confirms an ongoing blocker, hold, risk, or state even though its category did not change.

### 4. Interpret every included signal

Write at most one analysis item for each included customer when a concise interpretation helps Amit understand the implication or act on it.

Each item must:

- Name the verified change or exact missing record.
- Explain why it matters to the customer or business.
- Include at least one direct evidence link.
- Stay under 320 characters.

Do not repeat generic product guidance, list tools, or explain access limitations in the human email.

## CEO View — Company Health

Keep Agentic as the main story. Then show only the executive signals that changed or matter now:

- This week's total bookings, core/non-Agentic bookings, Agentic bookings, and Agentic share.
- A fresh read-only Salesforce operational snapshot every Monday: current account ARR, quarter-start ARR, the opening-cohort movement, ARR from new/reactivated/previously unsnapshotted accounts, paying-account count, and paid-license count.
- A week-over-week comparison to the prior Monday's Salesforce operational snapshot when that prior snapshot is available. The first run establishes a baseline and says so explicitly.
- The latest available ARR movement period, explicitly labeled with its real grain and date: net ARR, new plus expansion, churn plus contraction, net customers, and paid-license change. Do not describe monthly data as weekly.
- The fiscal-quarter scoreboard using Dialpad's calendar: Q1 February–April, Q2 May–July, Q3 August–October, Q4 November–January.
- Quarter-to-date actual bookings, official full-quarter target, attainment, gap, required weekly pace, commit, best case, previous-quarter comparison, and Agentic share.

The official target must come from an authoritative Finance or RevOps planning source. Never use sample dashboard data, sum incomplete Salesforce quotas, or treat a suspected subset target as the company target. When the target is unverified, set it and every derived target metric to `null`, explain the specific source problem in `target_note`, and still report verified actuals and forecast values.

Company-health metrics degrade independently. If the latest ARR bridge cannot be verified from a current authorized source, set `latest_arr_period` to `null`, add a specific non-empty `latest_arr_note`, and continue with the verified Agentic review, bookings, and quarter data. Never substitute an older bridge, zeros, or estimates. Missing company-health context must not suppress otherwise valid customer evidence.

The Salesforce operational snapshot is not the Finance-certified ARR bridge. Build it only from current read-only Account fields and label it `Salesforce operational estimate` in `method_note`:

- `quarter_start_arr`: sum of `First_Day_FQ_ARR__c` for accounts with a positive quarter-start value.
- `opening_cohort_current_arr`: current `ARR__c` for that same positive quarter-start cohort.
- `new_or_unsnapshotted_arr`: current `ARR__c` for positive-ARR accounts whose quarter-start ARR is null or zero. This bucket can contain new, reactivated, or previously unsnapshotted accounts; never call all of it new ARR.
- `current_arr`: opening-cohort current ARR plus new/reactivated/previously unsnapshotted ARR.
- `net_arr_change`: current ARR minus quarter-start ARR; `net_arr_change_pct` uses quarter-start ARR as the denominator.
- `paying_accounts` and `paid_licenses`: count accounts and sum `Total_Dialpad_License__c` where `Customer__c` is true and `ARR__c` is positive.

Do not describe the opening-cohort movement as churn or retention. It is a net of expansion, contraction, churn, reactivation, and Salesforce corrections. Retrieve the previous Monday's delivered review and compare only the three like-for-like stored values: current ARR, paying accounts, and paid licenses. If no prior operational snapshot is safely available, leave the comparison values null and state that the baseline was established.

## Executive signal

Lead the email with one short paragraph containing the strongest decision-relevant signal from the current week. This is an authored point of view, not a metric summary or fixed checklist.

- Select the change that best explains whether the business or Agentic trajectory materially improved, weakened, or remained stuck.
- Synthesize what matters in natural prose. Explain the implication or next proof only when it sharpens the signal; do not render fixed labels or a watch list.
- Use one to four direct HTTPS evidence links and set confidence to `low`, `medium`, or `high`.
- Compare against prior reviews and known context, but do not repeat layoffs, strategy shifts, core scale, or other stable background unless new evidence changes their implication.
- Mention the three- or six-month outlook only when the current week's evidence materially changes that outlook.
- Do not include Dialpad Tap or Amit's personal work. It is context shared for discussion, not part of this business report.
- Current public market evidence may be used when it materially changes the interpretation. Prefer primary sources, retain the direct links in `executive_read.links`, and never use a market trend as proof of a private Dialpad fact.

Use official written company material for restructuring or strategy facts. Sensitive user-supplied context may guide what to investigate, but it must not appear as a report fact unless an approved source verifies it. When no single signal is strong enough, say that the trajectory is unchanged and name the one next proof that matters most; do not manufacture novelty.

## Machine contract: schema version 5

`report_markdown` in the internal source draft may be a short preview. The GitHub relay deterministically creates the final email from `snapshot`.

```json
{
  "report_markdown": "# Weekly Agentic Customer Review — YYYY-MM-DD\n",
  "agent_request_id": "non-sensitive-runtime-id",
  "data_status": "complete",
  "failures": [],
  "snapshot": {
      "schema_version": 5,
    "report_date": "YYYY-MM-DD",
    "generated_at": "ISO-8601 timestamp",
    "comparison_window": {
      "start": "YYYY-MM-DD",
      "end": "YYYY-MM-DD",
      "label": "Monday DATE through Sunday DATE"
    },
    "source_status": {},
    "summary": {},
    "customers": [],
    "insights": [],
    "commercial_changes": [],
    "unknowns": [],
    "changes_since_previous": [],
    "executive_read": {
      "paragraph": "One concise, evidence-grounded paragraph containing the strongest weekly signal and its implication.",
      "confidence": "medium",
      "links": ["https://..."]
    },
    "business_health": {
      "verdict": "stable",
      "verdict_reason": "Short evidence-based explanation",
      "weekly_sales": {},
        "salesforce_operational_snapshot": {
          "as_of_date": "YYYY-MM-DD",
          "quarter_label": "Q3 FY27",
          "quarter_start_arr": 0,
          "current_arr": 0,
          "net_arr_change": 0,
          "net_arr_change_pct": 0,
          "opening_cohort_current_arr": 0,
          "opening_cohort_change": 0,
          "new_or_unsnapshotted_arr": 0,
          "paying_accounts": 0,
          "paid_licenses": 0,
          "method_note": "Salesforce operational estimate from read-only Account fields; not the Finance-certified ARR bridge.",
          "comparison": {
            "previous_snapshot_date": null,
            "arr_change_since_previous": null,
            "paying_account_change": null,
            "paid_license_change": null,
            "comparison_note": "Baseline established; the first week-over-week comparison will appear next Monday."
          }
        },
      "latest_arr_period": null,
      "latest_arr_note": "The latest monthly ARR bridge was not available from a current authorized source.",
      "quarter": {}
    }
  }
}
```

Each required source receipt:

```json
{
  "status": "ok",
  "queried_at": "ISO-8601 timestamp",
  "links": ["https://..."],
  "access_mode": "read_only"
}
```

Each customer:

```json
{
  "account_name": "Permitted customer name",
  "name_permitted": true,
  "lifecycle_stage": "validate",
  "movement": "moved",
  "agent_or_use_case": "Patient intake agent",
  "links": ["https://..."],
  "integrations": [
    {"name": "Scheduling API", "status": "testing"}
  ],
  "change_this_week": "Customer sign-off moved the project into validation.",
  "next_watch": "Watch the first customer validation session.",
  "jira": {
    "new_or_changed_7d": 0,
    "open_customer_bugs": 0,
    "keys": []
  },
  "commercial": {
    "stage": "Customer validation",
    "movement_7d": "advanced",
    "agentic_acv": null
  }
}
```

`summary` must be calculated exactly from the customer rows:

- `reported_deployment_count` — optional source-reported portfolio total; must be greater than or equal to the included row count.
- `active_customer_count`
- `movers_7d`
- `customers_with_changed_blockers_7d`
- `customers_without_current_data` — always `0`; customers without a verified signal are not included as rows.
- `commercial_moves_7d`

The relay rejects an empty verified-signal set, duplicate names, mismatched summaries, stale or writable sources, unsafe links, invalid Jira keys, negative or non-finite values, secrets, raw payloads, transcripts, and unsupported recipients.

`executive_read` and `business_health.salesforce_operational_snapshot` are required in schema version 5. The executive signal needs direct HTTPS evidence and must remain one concise paragraph in the rendered report. The Salesforce snapshot must reconcile arithmetically. `business_health.latest_arr_period` may be `null` only when `business_health.latest_arr_note` gives the specific current-source gap. This is a visible unavailable state, not a reason to fail the complete report.

## Deterministic email format

The relay creates:

1. **This week** — weekly mover, commercial, blocker, and missing-record counts.
2. **Verified customer movement** — only customers with specific current evidence, with journey/commercial state, weekly signal, and risk/next watch.
3. **Analysis** — short customer-by-customer interpretations focused on implications and ways Amit can help.
4. **Gaps to resolve** — specific missing joins or measurements that materially limit an included insight. No generic data disclaimer.
5. **Evidence** — one direct link per required source family plus the workflow run.
6. **CEO View — Company Health** — executive company direction after the Agentic story, with target metrics withheld whenever the official target is not verified.

Keep the final review under 1,600 visible words. The matrix is primary; prose is secondary.

## Failure behavior

Do not create a normal draft when:

- Salesforce, Jira, Glean, or production-code search is missing, unhealthy, stale, or not read-only.
- No named customer has a specific verified signal in the weekly window.
- A claimed customer signal cannot be attributed safely enough to include.
- The report date is not Monday in `Asia/Kolkata`.
- The weekly window is invalid.
- A source would require a write or permission/configuration change.

Do not fail the complete report solely because the latest ARR bridge is unavailable. Preserve the verified Agentic review and render the explicit ARR-unavailable note in `CEO View — Company Health`.

Return `data_status: incomplete` with a concise failure entry. Never reuse an earlier report as current evidence, invent movement, or turn the newsletter into telemetry.

## Relay draft

After every gate passes, create exactly one Gmail draft:

- Subject: `[INTERNAL RELAY — DO NOT SEND] Weekly Agentic Customer Review — YYYY-MM-DD`
- To: `amit.ayre@dialpad.com`
- No Cc, Bcc, or attachments.
- Human preview followed by one JSON object between `---BEGIN PULSE MACHINE JSON---` and `---END PULSE MACHINE JSON---`.

Never send the internal draft manually. The approved GitHub relay validates it, removes the machine block, renders the verified-signal matrix as HTML, and sends only the body-only user email with the existing deterministic Message-ID.

The final user-facing email is addressed only to Amit using the single approved address stored in the protected workflow configuration. Amit is placed in Bcc; To contains only `undisclosed-recipients:;` and Cc is absent. The recipient address is removed from the transmitted headers. The private internal relay draft also remains addressed only to Amit.
