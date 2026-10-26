# Weekly Agentic Customer Review operations

Workflow: `Daily Agentic Business Pulse` (repository workflow name retained)

Delivery is Monday at 09:00 `Asia/Kolkata`. The user-facing email is `Weekly Agentic Customer Review — YYYY-MM-DD`.

The review keeps named Agentic customers and their verified movement as the main story. After that, `CEO View — Company Health` provides a compact company-level scorecard: current bookings mix, latest correctly labeled ARR movement, customer and license direction, and fiscal-quarter progress. It is not a copy of the restricted CEO dashboard.

## Schedule

The private Glean Agent runs Mondays at 08:00 IST. GitHub has five Monday-only fallback cron events beginning at 04:07, 04:47, 05:53, 07:07, and 09:07 IST. The first runner released waits until 09:00 before checking Gmail; later runs exit after the first accepted send.

Manual `workflow_dispatch` supports a no-send dry run and never waits for 09:00.

## Source and safety boundary

Company-data collection runs inside private Glean Agent `8f3fd6d966c64916b11b505a580ff64f`.

Required read-only sources:

- Salesforce for exact-match identity, journey/commercial stage, use case, and Agentic-specific value for customers already named in current evidence.
- Jira for customer-impacting bugs and issues changed in the weekly window.
- Glean company search, documents, email, and calendar for customer context and the weekly Agentic newsletter.
- Already-authorized Finance, RevOps, billing/ARR, or governed analytics sources for company-health metrics. Never bypass a permission boundary.
- Production code only when a changed customer blocker needs implementation context; it is not required for an unchanged review.

The review does not use BigQuery, Pinot, or Agentic Analytics. It never claims conversations, action-success, containment, resolution, CSAT, or other product telemetry.

No Salesforce or Jira writes, repository writes, source-system configuration, permissions changes, exports, or customer-system mutations are allowed. The only Glean Agent write is Gmail MCP `Create Draft` for the internal relay envelope.

## Internal source draft

The Glean Agent creates exactly one draft:

- Subject: `[INTERNAL RELAY — DO NOT SEND] Weekly Agentic Customer Review — YYYY-MM-DD`
- To: `amit.ayre@dialpad.com`
- No Cc, Bcc, or attachments
- One schema-version-3 JSON block between the established machine markers

The internal draft must never be sent manually. The GitHub relay ignores its narrative, validates the structured snapshot, and deterministically renders the final matrix.

Schema version 3 requires everything in version 2 plus:

- Fresh read-only receipts for Salesforce, Jira, and Glean, plus production code only when used.
- The previous Monday-through-Sunday comparison window.
- At least one named customer with a specific verified weekly signal.
- One lifecycle and movement state per customer.
- Agent/use case, integrations, weekly change, Jira state, commercial state, and next watch.
- A summary derived exactly from customer rows.
- Evidence-linked analysis for included customer signals when it clarifies implications or how Amit can help.
- A `business_health` object rendered after the Agentic story.
- Dialpad fiscal quarters: Q1 February–April, Q2 May–July, Q3 August–October, Q4 November–January.
- An authoritative Finance or RevOps source for the overall quarterly target. Sample dashboard values, incomplete quota aggregates, and inferred targets are rejected.
- When the target is unverified, actual and forecast values may still appear, but target, attainment, gap, and required pace remain null with a specific target note.
- When the latest monthly ARR bridge is unavailable from a current authorized source, `latest_arr_period` is null and `latest_arr_note` states the precise gap. The verified Agentic review, bookings, and quarter data remain deliverable; old, zero-filled, or estimated ARR values are never substituted.

## Delivery protection

The final report recipient is stored in the protected `PULSE_RECIPIENTS` repository secret rather than exposed as workflow configuration. It must contain only Amit's approved Dialpad address. Amit is placed in Bcc; To contains only `undisclosed-recipients:;` and Cc is absent. SMTP removes the Bcc header from the transmitted message. Any missing, additional, duplicate, different, or visible final recipient fails before SMTP. The internal Glean relay draft also remains addressed only to Amit.

The live email and failure notification use deterministic IST-date Message-IDs. Gmail Sent is checked before delivery, so retries and fallback schedules cannot send duplicates. The email contains no attachments or machine JSON.

Runtime files remain private:

- `reports/agentic_business_pulse/YYYY-MM-DD.md`
- `reports/agentic_business_pulse/YYYY-MM-DD.json`

They are retained only in the private GitHub Actions artifact.

## Failure behavior

The normal review fails closed when:

- a required source is missing, unhealthy, stale, or not marked read-only;
- no named customer has a specific verified signal in the weekly window;
- a claimed signal cannot be attributed safely enough to include;
- the run is not Monday in `Asia/Kolkata`;
- the comparison window is not the previous Monday through Sunday;
- summary counts do not match customer rows;
- customer names, links, Jira keys, or commercial values are invalid;
- credentials, raw payloads, tool arguments, transcripts, or unredacted email addresses are detected;
- Gmail persistence, recipient validation, or idempotency checks fail.

Expected application failures use the existing once-per-IST-date failure alert. If the notifier fails, the workflow remains failed so GitHub is the final alert path.

## Release verification

1. Run all repository tests and pull-request validation.
2. Update the private Glean Agent instructions and schedule in draft.
3. Preview the Agent and confirm a complete schema-v3 snapshot with no source writes.
4. Publish only after the preview validates.
5. Run GitHub with `dry_run=true`.
6. Confirm one private body-only draft, no SMTP call, only Amit in Bcc, no attachments, no machine JSON, and a readable verified-signal matrix.
7. Only then run live once.
8. Confirm Gmail accepts one email delivered only to Amit without exposing the recipient address.
9. Re-run live and confirm `duplicate_skipped`.

Fixtures prove structure only. They never prove real customer facts.
