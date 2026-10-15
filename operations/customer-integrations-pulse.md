# Customer Integrations Pulse operations

This is a separate, owner-only product telemetry report. It does not change the Weekly Agentic Customer Review or its recipient list. The first edition is a measured call-logging pulse; it is not yet a census of every integration or a failure-monitoring system.

## Reader and schedule

- Recipient: Amit only, at the fixed `amit.ayre@dialpad.com` address.
- Scheduled for 09:00 Asia/Kolkata. Monday is a seven-complete-day report compared with the preceding seven days. Tuesday through Sunday compare yesterday with the same weekday in the prior week.
- A manual workflow run defaults to a no-send dry run. Its generated files remain on the ephemeral runner and are not uploaded as artifacts or printed in Actions logs.
- The schedule is inactive until the repository variable `CUSTOMER_INTEGRATIONS_PULSE_ENABLED` is explicitly set to `true`. Set it only after the first dry run and email have been reviewed.

## Source and claim boundaries

The query reads `uv_entities.Call`, `CallInfo`, and `Company` from Firespotter analytics in BigQuery. It counts calls with saved Salesforce activity IDs or saved Slack, Zendesk, or HubSpot external IDs. It separates integrations and counts companies with a saved result. A call with two saved IDs counts in two provider rows; provider totals are not a unique-call denominator.

Saved external IDs establish a confirmed artifact. They do not establish attempted volume, failure rate, retry state, or time to log. DialApp and other integrations are absent. `device_type` is retained in the query output, but CTI, Dialpad app, and Dialpad Everywhere cannot yet be inferred reliably from this field alone. Do not label Salesforce the most used integration overall using this report.

Customer shifts compare confirmed call volume and pass a minimum baseline of 100 calls, a difference of at least 25 calls, and a difference of at least 30%. They are leads for investigation, not diagnoses. The email does not quote customer content, call content, record IDs, or individual caller data.

## Runner access required

The interactive BigQuery connection does not authorize GitHub Actions. Provision a dedicated read-only Google Cloud service account for this workflow, with query-job creation on billing project `uv-beta` and read access to only the three source tables or equivalent authorized views. Configure GitHub OpenID Connect Workload Identity Federation scoped to this repository and its default branch, and set the repository variables `CUSTOMER_PULSE_WIF_PROVIDER` and `CUSTOMER_PULSE_SERVICE_ACCOUNT`. [Google's authentication action recommends federation over a long-lived key](https://github.com/google-github-actions/auth#authenticate-to-google-cloud-from-github-actions). Do not paste a credential into the repository or chat.

The existing Gmail secrets `GMAIL_USER` and `GMAIL_APP_PASSWORD` are used for SMTP and a Sent Mail duplicate check. Delivery always targets the fixed owner address, regardless of other environment values. The Message-ID includes the local report date and cadence, so retries do not intentionally send a second copy.

## Release sequence

1. Review the code and coverage statements in the draft pull request.
2. Provision the runner identity and variables above. Leave the schedule switch off.
3. Run `Customer Integrations Pulse` manually with **send = false**. Confirm the workflow succeeds without logging customer names or uploading report artifacts.
4. Run it once manually with **send = true** and verify the owner-only email, links, counts, and coverage caveats.
5. Re-run the same day and verify `duplicate_skipped`.
6. Set `CUSTOMER_INTEGRATIONS_PULSE_ENABLED=true` when the recurring email is wanted.

## Next sources

The broader customer pulse still needs source contracts for DialApp call outcomes, Amplitude adoption events, Jira customer-impacting issues, and verified surface attribution. Add each as an independently validated section with its own denominator and coverage note. Until then, the report should be described as the initial confirmed call-logging edition.
