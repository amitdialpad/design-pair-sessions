# Daily Agentic Business Pulse operations

Workflow: `Daily Agentic Business Pulse`

The user-facing subject remains `Daily Agentic Business Pulse — YYYY-MM-DD`, but schema version 2 changes the body into an Agentic customer operating dashboard. It leads with the complete active-customer matrix, measured movement, failures, and missing instrumentation. The relay, not Glean prose, deterministically creates the final Markdown and HTML from the validated snapshot.

## Schedule and idempotency

Delivery remains 09:00 in `Asia/Kolkata`. Five odd-minute cron events begin at 04:07, 04:47, 05:53, 07:07, and 09:07 IST because GitHub scheduled events may be delayed. The first released runner waits in the cloud until 09:00; later runs exit after the first accepted send.

A manual `workflow_dispatch` never waits and supports live or dry runs. Pull requests that change the workflow, skill, scripts, operations guide, or tests must pass validation without loading Actions secrets.

The live report and failure alert each use deterministic, IST-date Message-IDs. Gmail Sent is checked before delivery. A successful retry cannot send a second report, and later fallback runs suppress duplicate failure alerts.

## Runtime boundary

The public repository contains orchestration, deterministic rendering, validation, and tests only. It must not contain source credentials, internal identifiers, customer reports, snapshots, or raw evidence.

Company-data collection runs inside private Glean Agent `8f3fd6d966c64916b11b505a580ff64f` using the user's approved permissions. Company sources are strictly read-only:

- Agentic Analytics: conversations, skill starts, containment, transfer, resolution, handle time, and AI customer satisfaction.
- Salesforce: complete active roster, lifecycle/commercial state, use case, and Agentic-specific value.
- Jira: customer-impacting bugs and changed blockers.
- Glean search/documents/email: qualitative customer context.
- Production code: optional, only to explain a newly changed customer contradiction.
- BigQuery: only for a named, approved authoritative view; access alone is not sufficient.

No source-system writes, query-object creation, exports, configuration changes, permission changes, Jira transitions/comments, Salesforce updates, or Glean content edits are allowed. The only source-Agent write is its already approved Gmail `Create Draft` action for the internal relay envelope.

Required repository secrets remain:

- `GMAIL_USER`: existing Beacon Brief Gmail sender account.
- `GMAIL_APP_PASSWORD`: existing Beacon Brief Gmail app password with SMTP and IMAP access.

GitHub Actions requires no direct Agentic Analytics, BigQuery, Salesforce, Jira, Glean, or repository credential.

## Rollout gate

Do not switch production delivery to schema version 2 until the private Glean Agent has an approved read-only Agentic Analytics path. At the time of this implementation, its documented tools cover Salesforce, Jira, company search/documents, email/calendar, and production code; they do not prove access to the Pinot-backed Agentic Analytics data.

Until that read path exists:

1. Keep the implementation on a review branch.
2. Do not manufacture metrics from the weekly status email, old BigQuery tables, code, or test fixtures.
3. Do not edit the Glean Agent or analytics configuration as part of this repository change.
4. After an authorized owner configures the read-only path, run the Glean Agent manually and perform a GitHub dry run before any live delivery.

## Glean draft contract

The source Agent creates one internal draft with:

- Exact subject: `[INTERNAL RELAY — DO NOT SEND] Daily Agentic Business Pulse — YYYY-MM-DD`
- Exactly one recipient: `amit.ayre@dialpad.com`
- No Cc, Bcc, or attachments
- One JSON object between `---BEGIN PULSE MACHINE JSON---` and `---END PULSE MACHINE JSON---`

The source draft must never be sent manually.

Schema version 2 requires:

- Fresh, linked source receipts for `agentic_analytics`, `salesforce`, `jira`, and `glean`
- `access_mode: read_only` for each required source
- The complete active customer roster
- One lifecycle and movement state per customer
- Explicit metric coverage so zero cannot be confused with not instrumented
- Last-24-hour activity, trailing and preceding seven-day activity, governed outcomes, Jira status, and commercial status
- Short evidence-linked interpretations for changed rows only
- A summary derived exactly from the customer rows

`report_markdown` in the internal draft is a source preview. The relay ignores its narrative for schema version 2 and builds:

1. Today
2. Customer matrix
3. Analysis
4. Missing instrumentation
5. Evidence

The matrix is rendered as a real HTML table. The final report contains no machine JSON or attachments.

## Private persistence and delivery

Runtime files are written to:

- `reports/agentic_business_pulse/YYYY-MM-DD.md`
- `reports/agentic_business_pulse/YYYY-MM-DD.json`

The directory is gitignored. The Markdown report, compact snapshot, and run result are retained only in the private GitHub Actions artifact for 90 days.

Before live delivery, the exact body-only email is persisted as a Gmail draft. After Gmail SMTP accepts it, that prepared draft is removed. Dry runs retain a replaceable same-day `[DRY RUN]` draft and never call SMTP.

Gmail draft discovery searches using the ASCII-only phrase `Daily Agentic Business Pulse`, then requires the exact Unicode internal subject, current IST date, one allowed recipient, and no attachments on every candidate.

## Failure behavior

A normal dashboard fails closed when:

- a required source is missing, unhealthy, stale, or not marked read-only;
- the active customer roster is empty or cannot be claimed complete;
- rows cannot be joined by a safe canonical identity;
- governed behavioral metrics are unavailable;
- a value is supplied where its coverage says not instrumented or not applicable;
- a summary does not match its customer rows;
- a customer name, evidence link, date, or comparison window is invalid;
- credentials, raw payloads, tool arguments, transcripts, or unredacted email addresses are detected;
- private Gmail persistence or idempotency checks fail.

An expected application failure is recorded as `handled_failure` in the Actions summary and invokes the existing daily-deduplicated Gmail failure notification. If that notifier fails, the workflow remains failed so GitHub is the final alert path. Infrastructure and unexpected Python failures also remain failed workflow runs.

## Verification before production

1. Run the complete unit suite and pull-request validation.
2. Confirm the private Agent has an approved read-only Agentic Analytics path; do not infer this from BigQuery or Glean access.
3. Run the Glean Agent once and confirm exactly one valid schema-v2 internal draft.
4. Run `Daily Agentic Business Pulse` with `dry_run=true`.
5. Confirm `dry_run_complete`, no SMTP call, one recipient, no attachment, no machine JSON in the rendered body, and a readable customer matrix.
6. Verify source receipts are current and read-only and the customer rows reconcile to the summary.
7. Only after the dry run passes, run once with `dry_run=false`.
8. Confirm Gmail accepted one email only for `amit.ayre@dialpad.com`.
9. Re-run live and confirm `duplicate_skipped`.
10. Observe the next unattended schedule; later fallbacks must remain quiet duplicate skips.

Fixtures are test inputs only. They can validate structure and rendering but can never prove live customer activity or satisfy the production rollout gate.
