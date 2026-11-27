# Customer Integrations Pulse operations

This is a separate, owner-only product telemetry report. It does not change the Weekly Agentic Customer Review or its recipient list. The first edition is a measured call-logging pulse; it is not yet a census of every integration or a failure-monitoring system.

## Reader and cadence

- Recipient: Amit only, at `amit.ayre@dialpad.com`.
- A Codex scheduled task runs at 09:00 Asia/Kolkata. Monday compares the latest seven complete days with the preceding seven days. Tuesday through Sunday compare yesterday with the same weekday one week earlier.
- The task uses Amit's connected read-only BigQuery and Gmail apps. It retrieves every BigQuery result page and checks Gmail Sent for the dated subject before sending. If the source or connection is unavailable, it does not send a normal report and instead reports the blocker in the Codex chat.
- This is a local scheduled task, so the computer must be on and the Codex desktop app running at the scheduled time. Connected-app access may need reauthorization. The GitHub workflow in this repository validates the code on pull requests; it does not send email or run on a schedule.

## Source and claim boundaries

The query reads `uv_entities.Call`, `CallInfo`, and `Company` from Firespotter analytics in BigQuery. It counts calls with saved Salesforce activity IDs or saved Slack, Zendesk, or HubSpot external IDs. It separates integrations and counts companies with a saved result. A call with two saved IDs counts in two provider rows; provider totals are not a unique-call denominator. The email leads with a short interpretation of material provider changes, customer-level shifts, and saved manual disposition use before the tables.

Saved external IDs establish a confirmed artifact. They do not establish attempted volume, failure rate, retry state, or time to log. DialApp and other integrations are absent. The Salesforce client split joins the saved root call to its user-facing call leg and groups evidence for the embedded Salesforce client, native desktop, web, mobile, mixed, and unclassified calls. Do not interpret the root `dialpad` device value as the Dialpad app: production code assigns it to operator call legs. Do not infer Dialpad Everywhere from these categories. Do not label Salesforce the most used integration overall using this report.

`Call.dispositions` measures saved manual dispositions on those confirmed calls. It does not count AI outcomes, which are stored separately. The current `AiRecap` table is not partitioned by date; a date-filtered join estimates a large scan, so do not add it to the daily query until a cheaper verified source is found. Do not substitute an Amplitude UI-action count for a call-level disposition count without labeling its different denominator.

The optional `--jira-signals` input can add reviewed, current Jira issues as investigation context. Each entry must have `key`, `provider`, `status`, and a concise factual `summary`. The report always states that a related issue does not prove the cause of a measured volume change. If Jira was not checked, say so; do not silently imply there were no issues. Keep issue content concise and do not copy customer conversations or personal data into the email.

Customer shifts compare confirmed call volume and pass a minimum baseline of 100 calls, a difference of at least 25 calls, and a difference of at least 30%. They are leads for investigation, not diagnoses. The email does not quote customer content, call content, record IDs, or individual caller data.

## Review and recovery

The first live BigQuery read and owner-only Gmail delivery were completed manually through the connected apps. Review the email's counts, source link, customer shifts, and coverage note before changing the report. Check the Codex scheduled-task run history after the first automated run. If a run fails or sends an unexpected claim, pause the scheduled task and inspect the source query and result pagination before resuming.

The Python generator and tests in this repository are the calculation reference and can also produce a no-send report from a JSON snapshot. Runtime report files belong under `reports/customer_integrations_pulse/`, which is ignored by Git. Never commit customer-level snapshots or upload them as public GitHub Actions artifacts.

## Future hosted runner

The GitHub runner does not have BigQuery access. A hosted email schedule would require a dedicated read-only identity and restricted trust setup; Amit's current Google Cloud account can query BigQuery but cannot grant those IAM permissions. Do not turn the GitHub check into a scheduled email job without that separate access review.

## Next sources

The broader customer pulse still needs source contracts for DialApp call outcomes, Amplitude adoption events, AI outcomes, support signals, and a distinct Dialpad Everywhere measurement. The public Secoda documentation describes a catalog and glossary, but it is not Dialpad's internal workspace; catalog definitions remain unverified until that workspace is accessible. Glean and Confluence may provide useful definitions and customer context, but they are not automatically covered by this query. Add each as an independently validated section with its own denominator, source link, and coverage note. Until then, describe this as an enriched confirmed call-logging edition, not a full census of integration health.
