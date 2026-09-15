# Daily Agentic Business Pulse operations

Workflow: `Daily Agentic Business Pulse`

Scheduled execution: every day at `30 3 * * *` UTC, which is 09:00 in `Asia/Kolkata`. GitHub-hosted jobs may start several minutes late. A manual `workflow_dispatch` supports live and dry runs.

## Runtime boundary

The public repository contains orchestration and validation code only. It does not contain company source credentials, internal document identifiers, reports, snapshots, or raw evidence.

The workflow sends one authenticated HTTPS request to an approved company-data agent. That runtime must be able to query Salesforce, Jira, Glean/document reading, and production code, and must apply the complete repository skill at `skills/daily-agentic-business-pulse/SKILL.md`.

Required repository secrets:

- `PULSE_AGENT_URL`: HTTPS endpoint for the approved company-data agent.
- `PULSE_AGENT_TOKEN`: bearer credential for that one agent boundary. Do not add direct Salesforce, Jira, Glean, or code-search credentials here.
- `PULSE_SOURCE_CONTEXT_JSON`: JSON array containing the three approved internal source-context document links.
- `GMAIL_USER`: existing Beacon Brief Gmail sender account.
- `GMAIL_APP_PASSWORD`: existing Beacon Brief Gmail app password with SMTP and IMAP access.

## Company-agent request

The workflow posts JSON containing:

- the current IST report date/time and workflow URL;
- the full skill text and its SHA-256 digest;
- the most recent successful prior snapshot, or `null` on the first run;
- the four required source classes;
- the three source-context links supplied from the encrypted secret;
- the required JSON response shape.

The request payload and bearer credential are never logged.

The agent must return one JSON object:

```json
{
  "report_markdown": "# Daily Agentic Business Pulse — YYYY-MM-DD\n...",
  "snapshot": {},
  "agent_request_id": "non-sensitive-runtime-id",
  "data_status": "complete",
  "failures": []
}
```

The snapshot schema and report rules are defined in the skill and enforced again by `scripts/agentic_business_pulse.py` before persistence or delivery.

## Private persistence and delivery

Reports are written during execution to:

- `reports/agentic_business_pulse/YYYY-MM-DD.md`
- `reports/agentic_business_pulse/YYYY-MM-DD.json`

That directory is gitignored. Before a live send, the exact email with both files attached is persisted as a Gmail draft. After Gmail SMTP accepts the message, the prepared draft is removed and the Sent copy becomes the durable private report/snapshot archive.

Dry runs retain the prepared Gmail draft and do not call SMTP. The draft subject starts with `[DRY RUN]`.

The live message uses a deterministic RFC Message-ID derived from the IST report date. Before generation, the workflow searches Gmail Sent for that ID. A retry therefore exits successfully without calling the agent or sending another report. If a matching prepared draft exists but no Sent copy can be confirmed, the workflow fails closed and asks for inspection instead of risking a duplicate. GitHub Actions concurrency also prevents overlapping pulse jobs.

## Failure behavior

Normal report delivery stops when:

- any required source is missing, failed, or stale;
- the current IST date or comparison window is invalid;
- revenue and pipeline are not structurally separated;
- Agentic ACV and total bundled amounts are not structurally separated;
- required sections, source links, evidence labels, or implementation states are missing;
- prototype/mock/fixture evidence is described as deployed or customer-exposed;
- credentials, raw payloads, tool arguments, transcripts, or unredacted email addresses are detected;
- private Gmail persistence or idempotency checks fail.

The failed Actions run invokes the existing Gmail failure-notification path and links to the workflow run. It does not send a stale or partial normal report.

## Manual verification

1. Configure the approved company agent and all required secrets.
2. Run `Daily Agentic Business Pulse` manually with `dry_run=true`.
3. Confirm the Actions summary reports `dry_run_complete` and `not_sent_draft_persisted`.
4. Inspect the `[DRY RUN]` Gmail draft and both attachments.
5. Run manually with `dry_run=false`.
6. Confirm exactly one report email, the matching attachments, an accepted Gmail result, and source freshness in the Actions summary.
7. Re-run live for the same IST date and confirm `duplicate_skipped` / `already_sent`.

Fixtures are unit-test inputs only. They are never wired into the GitHub workflow and cannot pass validation as deployed or customer-exposed evidence.
