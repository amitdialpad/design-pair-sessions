# Daily Agentic Business Pulse operations

Workflow: `Daily Agentic Business Pulse`

Scheduled execution: every day at `30 3 * * *` UTC, which is 09:00 in `Asia/Kolkata`. GitHub-hosted jobs may start several minutes late. A manual `workflow_dispatch` supports live and dry runs.

Pull requests that change the pulse workflow, skill, scripts, operations guide, or tests run the unit-test validation job without loading any Actions secrets. Scheduled and manually dispatched runs must pass that validation job before the pulse job starts.

## Runtime boundary

The public repository contains orchestration and validation code only. It does not contain company source credentials, internal document identifiers, reports, snapshots, or raw evidence.

Company-data collection runs natively inside private Glean Agent `8f3fd6d966c64916b11b505a580ff64f`. Its daily 09:00 schedule uses the user's existing Glean permissions and the Agent's approved Salesforce, Jira, company-search/document, email/calendar, and production-code tools. This avoids exporting direct company-source credentials or requiring a Glean Platform API token in GitHub.

The Agent must retain the complete Daily Agentic Business Pulse skill, create only one Gmail draft addressed only to `amit.ayre@dialpad.com`, and include the machine-readable relay block described below. The Gmail MCP connection is restricted inside the Agent to `Create Draft`; it has no enabled mailbox-read, label, trash, recovery, Jira-write, or Salesforce-write tools.

At the same `30 3 * * *` UTC schedule, GitHub Actions uses the existing Gmail sender secrets to wait up to 15 minutes for that private draft. It then validates the recipient, report date, sections, source freshness and links, redaction, revenue/pipeline separation, implementation states, and JSON snapshot before sending. A missing, malformed, stale, or duplicate draft fails closed and uses the existing failure-notification path. A clearly labeled `Data incomplete` report may pass only when every required company source was refreshed successfully, unavailable metrics are represented as `null`, and the exact gaps are disclosed; a failed required source still routes to failure notification.

Required repository secrets:

- `GMAIL_USER`: existing Beacon Brief Gmail sender account.
- `GMAIL_APP_PASSWORD`: existing Beacon Brief Gmail app password with SMTP and IMAP access.

No `PULSE_AGENT_TOKEN`, direct Salesforce credential, Jira credential, Glean credential, or code-search credential is required by GitHub Actions.

## Glean draft contract

The Glean Agent creates a draft with the exact subject `Daily Agentic Business Pulse — YYYY-MM-DD`, exactly one `To` recipient (`amit.ayre@dialpad.com`), and no Cc or Bcc. After the human-readable report, the draft includes one JSON object between the exact markers `---BEGIN PULSE MACHINE JSON---` and `---END PULSE MACHINE JSON---`.

The object has this shape:

```json
{
  "report_markdown": "# Daily Agentic Business Pulse — YYYY-MM-DD\n...",
  "snapshot": {},
  "agent_request_id": "non-sensitive-runtime-id",
  "data_status": "complete",
  "failures": []
}
```

The snapshot schema and report rules are defined in the skill and enforced again by `scripts/agentic_business_pulse.py` before persistence or delivery. The relay deterministically normalizes known Glean formatting variants such as `iso_start`/`iso_end`, `evidence_links`, descriptive healthy-source statuses, and implementation status maps; it does not synthesize evidence or turn unknown/deployment-negative states into production claims. GitHub removes the machine block from the delivered report and adds the current workflow URL to the source record.

## Private persistence and delivery

The report recipient is immutable: `amit.ayre@dialpad.com`. Runtime validation rejects any other `To`, `Cc`, or `Bcc` destination before SMTP is called. Failure notifications use the same single-recipient convention.

Reports are written during execution to:

- `reports/agentic_business_pulse/YYYY-MM-DD.md`
- `reports/agentic_business_pulse/YYYY-MM-DD.json`

That directory is gitignored. Before a live send, the exact email with both files attached is persisted as a Gmail draft. After Gmail SMTP accepts the message, the prepared draft is removed and the Sent copy becomes the durable private report/snapshot archive.

Dry runs validate the Glean source draft, retain it, create a private prepared Gmail draft with the Markdown and JSON attachments, and do not call SMTP. The prepared draft subject starts with `[DRY RUN]`.

The live message uses a deterministic RFC Message-ID derived from the IST report date. Before generation, the workflow searches Gmail Sent for that ID. A retry therefore exits successfully without calling the agent or sending another report. If a matching prepared draft exists but no Sent copy can be confirmed, the workflow fails closed and asks for inspection instead of risking a duplicate. GitHub Actions concurrency also prevents overlapping pulse jobs.

## Failure behavior

Normal report delivery stops when:

- any required source is missing, failed, or stale (a missing non-source metric may instead produce a clearly labeled `Data incomplete` report);
- the current IST date or comparison window is invalid;
- revenue and pipeline are not structurally separated;
- Agentic ACV and total bundled amounts are not structurally separated;
- required sections, source links, evidence labels, or implementation states are missing;
- prototype/mock/fixture evidence is described as deployed or customer-exposed;
- credentials, raw payloads, tool arguments, transcripts, or unredacted email addresses are detected;
- private Gmail persistence or idempotency checks fail.

The failed Actions run invokes the existing Gmail failure-notification path and links to the workflow run. It does not send a stale or partial normal report.

## Manual verification

1. Confirm Glean Agent `8f3fd6d966c64916b11b505a580ff64f` is published privately, scheduled daily at 09:00, connected to Gmail MCP, and restricted to `Create Draft` as its only Gmail write tool.
2. Run the Glean Agent once manually and confirm it creates exactly one draft with the report and machine JSON block.
3. Run `Daily Agentic Business Pulse` manually with `dry_run=true`.
4. Confirm the Actions summary reports `dry_run_complete` and `not_sent_draft_persisted`.
5. Inspect the `[DRY RUN]` Gmail draft and both attachments.
6. Run manually with `dry_run=false`.
7. Confirm exactly one report email, the matching attachments, an accepted Gmail result, and source freshness in the Actions summary.
8. Re-run live for the same IST date and confirm `duplicate_skipped` / `already_sent`.

Fixtures are unit-test inputs only. They are never wired into the GitHub workflow and cannot pass validation as deployed or customer-exposed evidence.
