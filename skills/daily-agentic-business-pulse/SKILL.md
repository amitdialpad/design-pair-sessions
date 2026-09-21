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

This is a customer operating review, not a design essay. Do not repeat a known product problem unless its affected customer, severity, owner, status, or commercial effect changed this week.

## Safety

All company-source access is read-only.

- Use only approved search, read, list, view, code-search, SOQL-query, Jira-search, email-search, and calendar-search operations.
- Never create, update, comment, transition, label, configure, grant, export, delete, or send in Salesforce, Jira, repositories, Glean content, or customer systems.
- Never use BigQuery, Pinot, Agentic Analytics, or another data platform for this review.
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

## Machine contract: schema version 2

`report_markdown` in the internal source draft may be a short preview. The GitHub relay deterministically creates the final email from `snapshot`.

```json
{
  "report_markdown": "# Weekly Agentic Customer Review — YYYY-MM-DD\n",
  "agent_request_id": "non-sensitive-runtime-id",
  "data_status": "complete",
  "failures": [],
  "snapshot": {
    "schema_version": 2,
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
    "changes_since_previous": []
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

## Deterministic email format

The relay creates:

1. **This week** — weekly mover, commercial, blocker, and missing-record counts.
2. **Verified customer movement** — only customers with specific current evidence, with journey/commercial state, weekly signal, and risk/next watch.
3. **Analysis** — short customer-by-customer interpretations focused on implications and ways Amit can help.
4. **Gaps to resolve** — specific missing joins or measurements that materially limit an included insight. No generic data disclaimer.
5. **Evidence** — one direct link per required source family plus the workflow run.

Keep the final review under 1,600 visible words. The matrix is primary; prose is secondary.

## Failure behavior

Do not create a normal draft when:

- Salesforce, Jira, Glean, or production-code search is missing, unhealthy, stale, or not read-only.
- No named customer has a specific verified signal in the weekly window.
- A claimed customer signal cannot be attributed safely enough to include.
- The report date is not Monday in `Asia/Kolkata`.
- The weekly window is invalid.
- A source would require a write or permission/configuration change.

Return `data_status: incomplete` with a concise failure entry. Never reuse an earlier report as current evidence, invent movement, or turn the newsletter into telemetry.

## Relay draft

After every gate passes, create exactly one Gmail draft:

- Subject: `[INTERNAL RELAY — DO NOT SEND] Weekly Agentic Customer Review — YYYY-MM-DD`
- To: `amit.ayre@dialpad.com`
- No Cc, Bcc, or attachments.
- Human preview followed by one JSON object between `---BEGIN PULSE MACHINE JSON---` and `---END PULSE MACHINE JSON---`.

Never send the internal draft manually. The approved GitHub relay validates it, removes the machine block, renders the verified-signal matrix as HTML, and sends only the body-only user email with the existing deterministic Message-ID.
