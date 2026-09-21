# Weekly Agentic Customer Review operations

Workflow: `Daily Agentic Business Pulse` (repository workflow name retained)

Delivery is Monday at 09:00 `Asia/Kolkata`. The user-facing email is `Weekly Agentic Customer Review — YYYY-MM-DD`.

The review contains only named customers with specific, current, safely attributable signals, ordered by failing, moved, then other useful current states. It reports lifecycle when known, use case, connectors/systems, weekly movement, Jira risk, commercial movement, and the next item Amit can watch or help unblock. It is not a portfolio census and contains no unsupported product-usage telemetry or generic data disclaimer.

## Schedule

The private Glean Agent runs Mondays at 08:00 IST. GitHub has five Monday-only fallback cron events beginning at 04:07, 04:47, 05:53, 07:07, and 09:07 IST. The first runner released waits until 09:00 before checking Gmail; later runs exit after the first accepted send.

Manual `workflow_dispatch` supports a no-send dry run and never waits for 09:00.

## Source and safety boundary

Company-data collection runs inside private Glean Agent `8f3fd6d966c64916b11b505a580ff64f`.

Required read-only sources:

- Salesforce for exact-match identity, journey/commercial stage, use case, and Agentic-specific value for customers already named in current evidence.
- Jira for customer-impacting bugs and issues changed in the weekly window.
- Glean company search, documents, email, and calendar for customer context and the weekly Agentic newsletter.
- Production code only when a changed customer blocker needs implementation context; it is not required for an unchanged review.

The review does not use BigQuery, Pinot, or Agentic Analytics. It never claims conversations, action-success, containment, resolution, CSAT, or other product telemetry.

No Salesforce or Jira writes, repository writes, source-system configuration, permissions changes, exports, or customer-system mutations are allowed. The only Glean Agent write is Gmail MCP `Create Draft` for the internal relay envelope.

## Internal source draft

The Glean Agent creates exactly one draft:

- Subject: `[INTERNAL RELAY — DO NOT SEND] Weekly Agentic Customer Review — YYYY-MM-DD`
- To: `amit.ayre@dialpad.com`
- No Cc, Bcc, or attachments
- One schema-version-2 JSON block between the established machine markers

The internal draft must never be sent manually. The GitHub relay ignores its narrative, validates the structured snapshot, and deterministically renders the final matrix.

Schema version 2 requires:

- Fresh read-only receipts for Salesforce, Jira, and Glean, plus production code only when used.
- The previous Monday-through-Sunday comparison window.
- At least one named customer with a specific verified weekly signal.
- One lifecycle and movement state per customer.
- Agent/use case, integrations, weekly change, Jira state, commercial state, and next watch.
- A summary derived exactly from customer rows.
- Evidence-linked analysis for included customer signals when it clarifies implications or how Amit can help.

## Delivery protection

The recipient is immutable: `amit.ayre@dialpad.com`. Any other To, Cc, or Bcc fails before SMTP.

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
3. Preview the Agent and confirm a complete schema-v2 snapshot with no source writes.
4. Publish only after the preview validates.
5. Run GitHub with `dry_run=true`.
6. Confirm one private body-only draft, no SMTP call, one recipient, no attachments, no machine JSON, and a readable verified-signal matrix.
7. Only then run live once.
8. Confirm Gmail accepts one email for `amit.ayre@dialpad.com`.
9. Re-run live and confirm `duplicate_skipped`.

Fixtures prove structure only. They never prove real customer facts.
