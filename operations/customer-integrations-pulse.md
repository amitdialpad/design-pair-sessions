# Customer Integrations Pulse operations

This is a separate, owner-only product telemetry report. It does not change the Weekly Agentic Customer Review or its recipient list. The first edition is a measured call-logging pulse; it is not yet a census of every integration or a failure-monitoring system.

## Reader and cadence

- Recipient: Amit only, at `amit.ayre@dialpad.com`.
- A Codex scheduled task runs at 09:00 Asia/Kolkata. Monday compares the latest seven complete days with the preceding seven days. Tuesday through Sunday compare yesterday with the same weekday one week earlier.
- The task uses Amit's connected read-only BigQuery and Gmail apps. It retrieves every BigQuery result page and checks Gmail Sent for the dated subject before sending. If the source or connection is unavailable, it does not send a normal report and instead reports the blocker in the Codex chat.
- This is a local scheduled task, so the computer must be on and the Codex desktop app running at the scheduled time. Connected-app access may need reauthorization. The GitHub workflow in this repository validates the code on pull requests; it does not send email or run on a schedule.

## Source and claim boundaries

The query reads `uv_entities.Call`, `CallInfo`, and `Company` from Firespotter analytics in BigQuery. It counts calls with saved Salesforce activity IDs or saved Slack, Zendesk, or HubSpot external IDs. It separates integrations and counts companies with a saved result. A call with two saved IDs counts in two provider rows; provider totals are not a unique-call denominator.

Saved external IDs establish a confirmed artifact. They do not establish attempted volume, failure rate, retry state, or time to log. DialApp and other integrations are absent. `device_type` is retained in the query output, but CTI, Dialpad app, and Dialpad Everywhere cannot yet be inferred reliably from this field alone. Do not label Salesforce the most used integration overall using this report.

Customer shifts compare confirmed call volume and pass a minimum baseline of 100 calls, a difference of at least 25 calls, and a difference of at least 30%. They are leads for investigation, not diagnoses. The email does not quote customer content, call content, record IDs, or individual caller data.

## Review and recovery

The first live BigQuery read and owner-only Gmail delivery were completed manually through the connected apps. Review the email's counts, source link, customer shifts, and coverage note before changing the report. Check the Codex scheduled-task run history after the first automated run. If a run fails or sends an unexpected claim, pause the scheduled task and inspect the source query and result pagination before resuming.

The Python generator and tests in this repository are the calculation reference and can also produce a no-send report from a JSON snapshot. Runtime report files belong under `reports/customer_integrations_pulse/`, which is ignored by Git. Never commit customer-level snapshots or upload them as public GitHub Actions artifacts.

## Future hosted runner

The GitHub runner does not have BigQuery access. A hosted email schedule would require a dedicated read-only identity and restricted trust setup; Amit's current Google Cloud account can query BigQuery but cannot grant those IAM permissions. Do not turn the GitHub check into a scheduled email job without that separate access review.

## Next sources

The broader customer pulse still needs source contracts for DialApp call outcomes, Amplitude adoption events, Jira customer-impacting issues, and verified surface attribution. Add each as an independently validated section with its own denominator and coverage note. Until then, the report should be described as the initial confirmed call-logging edition.
