---
name: daily-agentic-business-pulse
description: Produces a daily, evidence-based Agentic customer operating dashboard showing who moved, how they moved, what they used, where they failed, and what happened after publishing.
---
# Daily Agentic Customer Dashboard

## Mission

Run daily at 09:00 `Asia/Kolkata`. Show the complete active Agentic customer roster and answer:

- Who moved in the last 24 hours?
- Where is each customer in `Build → Test → Validate → Publish → Live`?
- Which agent, use case, skill, connector, or system is being used?
- What happened in the last 24 hours and trailing seven days?
- Where are actions, conversations, or customer outcomes failing?
- Which customer bugs or commercial records changed?
- What is genuinely unknown or not instrumented?

This is a customer operating dashboard, not a recurring design essay. Do not repeat a known product problem unless its measurable customer effect, affected account, severity, owner, or status changed today.

## Safety and access boundary

All company-source access is read-only.

- Use only approved search, read, list, view, or `SELECT` operations.
- Never run DML, DDL, create/replace, export, load, write, update, comment, transition, label, configure, grant, delete, or send operations against analytics, BigQuery, Pinot, Salesforce, Jira, Glean content, repositories, or customer systems.
- Never change source-system permissions, connectors, dashboards, queries, datasets, agents, or configuration.
- Never request broader access to fill a report gap.
- The only allowed write in the source Agent is its existing Gmail `Create Draft` action for the private relay envelope, addressed only to `amit.ayre@dialpad.com`.
- Never store raw conversations, transcripts, prompts, tool arguments, customer payloads, credentials, or secrets.

If a safe approved read path does not exist, mark the integration unavailable and use the failure path. Do not improvise a new source or manually manufacture a metric.

## Authoritative source map

Use the source that owns each fact. Preserve its link and query time.

1. **Agentic Analytics** — the approved read-only, Pinot-backed analytics path for conversations, skill starts, containment, transfer, resolution, handle time, and AI customer-satisfaction measures. This is the required behavioral source.
2. **Salesforce** — the active customer roster, account identity, customer/commercial stage, opportunity movement, Agentic-specific contract value, and named use case when recorded.
3. **Jira** — customer-impacting bugs, new or changed blockers, current status, and ticket identity.
4. **Glean company search and documents** — qualitative customer context, implementation updates, meeting decisions, and weekly status statements. Use this to explain numbers, never to replace them.
5. **Production code** — optional and conditional. Inspect only when a newly changed customer failure or contradiction needs implementation context. Do not search code every day by default.
6. **BigQuery** — use only when a named, approved view is documented as authoritative for a specific report metric. BigQuery access by itself does not make a dataset current, complete, or suitable. Never substitute a stale event table for Agentic Analytics.

Required source families are `agentic_analytics`, `salesforce`, `jira`, and `glean`. A normal report requires all four to be healthy, fresh, linked, and recorded with `access_mode: read_only`.

## Daily procedure

### 1. Establish the roster and time window

Use the current IST date. Start from the complete active Agentic customer roster in Salesforce, including early access, build, validation, UAT, published, and live customers. Do not include only customers mentioned in the latest weekly email.

Compare:

- Last 24 hours for activity, failures, Jira changes, stage changes, and commercial movement.
- Trailing seven days against the preceding seven days for usage and outcomes.

Use the canonical company/account identifier for joins. If two systems cannot be joined safely and deterministically, do not guess from a similar name. Record the customer row as `no_data` and explain the identity gap in `unknowns`.

### 2. Place every customer in one journey stage

Use exactly one current stage:

- `build`
- `test`
- `validate`
- `publish`
- `live`
- `paused`

This is the current customer journey position, not a product-readiness claim. A published connector is not customer value until an agent uses it and an outcome is measured.

### 3. Refresh behavioral activity and outcomes

For every customer, retrieve when available:

- Conversations in the last 24 hours.
- Skill starts in the last 24 hours.
- Conversations in the trailing seven days and preceding seven days.
- Connector/action attempts, successes, and failures in the last 24 hours.
- Seven-day contained, transferred, resolved, not resolved, and unknown-resolution counts.
- Seven-day AI customer-satisfaction and average handle time.

Use definitions governed by the analytics source. Never infer successful actions from skill starts, conversations, or a qualitative statement such as “performing well.”

For `connector_actions` and `conversation_outcomes`, record one coverage state:

- `available` — the source supplies governed numeric values.
- `not_instrumented` — the source does not record the measure.
- `not_applicable` — the measure does not apply to this customer/use case.

Zero is a measured value. It is not interchangeable with `null` or `not_instrumented`. When coverage is not `available`, all associated metrics must be `null`; never insert plausible numbers.

### 4. Refresh product, customer, and commercial movement

For each customer:

- Record the agent or use case.
- Record the connectors, systems, or skills and their status: `building`, `testing`, `connected`, `failing`, or `unknown`.
- Count Jira issues created or materially changed in the last 24 hours.
- Count currently open customer-impacting Jira bugs and retain their keys.
- Record the Salesforce commercial stage and movement: `advanced`, `slipped`, `won`, `lost`, `value_changed`, or `no_change`.
- Record Agentic-specific contract value only when the governed field exists; do not use the total bundled opportunity amount as Agentic value.

Assign one movement label:

- `failing` — a measured action failure or newly changed customer blocker needs attention.
- `moved` — a lifecycle, behavioral, outcome, or commercial measure materially changed.
- `no_data` — the customer belongs on the roster but current behavioral evidence cannot be retrieved.
- `no_change` — current evidence was retrieved and no material change occurred.

Order the dashboard `failing`, `moved`, `no_data`, then `no_change`.

### 5. Interpret only changed rows

Write one short analysis item only for customers marked `failing`, `moved`, or `no_data`. Each item must:

- State the measured change or exact missing measure.
- Explain why it matters to this customer or the business.
- Include at least one direct evidence link.
- Stay under 320 characters.

Do not write an analysis item for `no_change`. Do not restate generic product principles. Do not turn the matrix into paragraphs.

### 6. Produce schema version 2

The machine JSON is authoritative. `report_markdown` in the source draft may contain only a short preview; the GitHub relay renders the final email deterministically from `snapshot`.

Required top-level shape:

```json
{
  "report_markdown": "# Agentic Customer Dashboard — YYYY-MM-DD\n",
  "snapshot": {
    "schema_version": 2,
    "report_date": "YYYY-MM-DD",
    "generated_at": "ISO-8601 timestamp",
    "comparison_window": {
      "start": "YYYY-MM-DD",
      "end": "YYYY-MM-DD",
      "label": "last 24 hours and trailing seven days"
    },
    "source_status": {},
    "summary": {},
    "customers": [],
    "insights": [],
    "commercial_changes": [],
    "unknowns": [],
    "changes_since_previous": []
  },
  "agent_request_id": "non-sensitive-runtime-id",
  "data_status": "complete",
  "failures": []
}
```

Each required `source_status` item:

```json
{
  "status": "ok",
  "queried_at": "ISO-8601 timestamp",
  "links": ["https://..."],
  "access_mode": "read_only"
}
```

Each customer row:

```json
{
  "account_name": "Permitted customer name",
  "name_permitted": true,
  "lifecycle_stage": "live",
  "movement": "moved",
  "agent_or_use_case": "Customer support agent",
  "links": ["https://..."],
  "integrations": [{"name": "Salesforce", "status": "connected"}],
  "metric_coverage": {
    "connector_actions": "not_instrumented",
    "conversation_outcomes": "available"
  },
  "activity": {
    "conversations_24h": 42,
    "conversations_7d": 120,
    "conversations_previous_7d": 100,
    "skill_starts_24h": 50,
    "connector_action_attempts_24h": null,
    "connector_action_successes_24h": null,
    "connector_action_failures_24h": null
  },
  "outcomes_7d": {
    "contained": 90,
    "transferred": 20,
    "resolved": 106,
    "not_resolved": 10,
    "unknown_resolution": 4,
    "ai_csat": 4.3,
    "average_handle_seconds": 92
  },
  "jira": {
    "new_or_changed_24h": 0,
    "open_customer_bugs": 0,
    "keys": []
  },
  "commercial": {
    "stage": "Early access",
    "movement_24h": "no_change",
    "agentic_acv": null
  }
}
```

`summary` must be calculated from the customer rows and contain:

- `active_customer_count`
- `movers_24h`
- `conversations_24h`
- `customers_with_failures_24h`
- `customers_without_current_data`

The relay rejects mismatched summaries, negative or non-finite numbers, values that exceed their denominators, invented values under unavailable coverage, duplicate customer names, missing evidence, stale sources, and writable source access.

## Deterministic human report

The relay produces these sections; the Agent must not improvise another layout:

1. `Today` — four derived summary lines.
2. `Customer matrix` — customer, journey/commercial state, last-24-hour activity, seven-day result, and risk.
3. `Analysis` — short changed-customer interpretations only.
4. `Missing instrumentation` — explicit gaps that change what can be concluded.
5. `Evidence` — one link per source family plus the workflow run.

Keep the final report under 700 visible words. The matrix is the primary artifact; prose is secondary.

## Failure behavior

Do not produce a normal report when:

- Agentic Analytics, Salesforce, Jira, or Glean is missing, unhealthy, stale, or not read-only.
- The complete active roster cannot be established.
- Customer identity cannot be joined safely for enough rows to claim completeness.
- Required governed metrics cannot be retrieved from their authoritative source.
- The current IST date or comparison window is invalid.
- A source would require a write or configuration change.

Return `data_status: incomplete` with a concise failure entry and let the relay invoke its once-per-IST-date failure notification. Never reuse yesterday's metrics as today's data and never turn a weekly email into fabricated telemetry.

## Email and continuity

Create exactly one internal Gmail relay draft with:

- Subject: `[INTERNAL RELAY — DO NOT SEND] Daily Agentic Business Pulse — YYYY-MM-DD`
- To: `amit.ayre@dialpad.com`
- No Cc, Bcc, or attachments.
- One JSON object between `---BEGIN PULSE MACHINE JSON---` and `---END PULSE MACHINE JSON---`.

The internal draft must never be sent manually. The approved GitHub relay validates the snapshot, removes the machine block, renders the customer matrix as HTML, and uses the existing deterministic Message-ID. The user-facing subject remains `Daily Agentic Business Pulse — YYYY-MM-DD` for continuity.

Save only the dated Markdown report and compact JSON snapshot in the private runtime artifact. Prior snapshots are comparison inputs only, never substitutes for current source reads.
