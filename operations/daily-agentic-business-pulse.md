# Weekly Agentic Customer Review operations

Workflow: Daily Agentic Business Pulse (existing repository/workflow name retained). Human email: Weekly Agentic Customer Review — YYYY-MM-DD. The active producer contract is [schema 7](../skills/daily-agentic-business-pulse/SKILL.md); schema-1 through schema-6 compatibility is for existing readers only.

## Purpose and evidence boundary

The review supports business awareness, anticipation, and product judgment. Explain changed selling/fulfillment/support model, source-backed business constraints, and customer consequences rather than producing a delivery evidence ledger or a list of proof-gathering tasks. Retain the full admitted portfolio and qualify service, direction, approval, milestone, accountability, and blocker independently. Missing documentation is not automatically a customer decision or failure.

Company-source access stays read-only. Research runs inside private Glean Agent 8f3fd6d966c64916b11b505a580ff64f. Source order is written leadership decisions, current migration/fulfillment inventory, PM/customer workbooks and communications, exact Salesforce admission/commercial identity, then Jira supporting evidence. Generated reports and agent recaps are discovery only; re-read primary evidence. Query or document modification time never replaces substantive claim date.

Salesforce, Jira, and Glean must be healthy, linked, fresh, and recorded with access_mode: read_only. Receipts use actual successful read/query times, at most 12 hours old and at most 10 minutes future-dated. Optional code context needs a receipt when used and never proves acceptance. Inaccessible individual documents become precise claim gaps when the source family is healthy; they never excuse skipping the audit.

No source writes, repository changes, customer outreach, grants/configuration, permission bypass, or customer-system exports during report generation. The research agent's only write is approved Gmail Create Draft for the source envelope. Protected relay Gmail persistence/delivery is separate. No BigQuery, Pinot, Agentic Analytics, inferred usage/outcome telemetry, raw conversations, transcripts, prompts, tool arguments, customer payloads, credentials, or secrets belong in the review.

## Schedule and date rules

The private Glean Agent runs Monday 08:00 Asia/Kolkata; protected delivery is Monday 09:00. Unchanged GitHub Monday fallback times: 04:07, 04:47, 05:53, 07:07, and 09:07 IST. UTC cron expressions: 37 22 * * 0; 17 23 * * 0; 23 0 * * 1; 37 1 * * 1; 37 3 * * 1. A cron event is not a guaranteed start time.

The first released scheduled runner waits until 09:00 IST, then polls Gmail every 30 seconds for up to 1,800 seconds. Runs are serialized with concurrency group daily-agentic-business-pulse, cancel-in-progress: false, and 345-minute job timeout. Later runs check accepted-send idempotency and skip duplicates. A fallback relay does not rerun research.

Scheduled report_date is actual Monday IST; comparison window is preceding Monday through Sunday. Manual workflow_dispatch dry_run and protected test_send never wait until 09:00. Only explicitly requested test_send permits another current IST date; its window starts seven days before latest Monday and ends yesterday. Tests do not change cadence or permit stale/backdated evidence.

## Schema 7 operating checks

Read the full active contract before changing the private agent:

- Retain every admitted customer. Reconcile prior delivered roster, exact aliases/identities, primary delivery entry, and additional inventory candidates. Broader inventory is not admission. Explain supported additions, explicit exits, and alias corrections; unresolved differences require partial coverage, not a forced count.
- Carry forward pending commitments/checkpoints: did proof arrive, slip, or remain unresolved? Missing evidence alone does not establish a missed commitment.
- Require base customer fields and transition.route; six claims current_service, direction, decision, next_milestone, accountability, blocker; reciprocal priority tags; attention fields. Every claim independently has text/status/substantive date/primary links. Known service survives missing decision evidence.
- Non-unconfirmed claims need substantive date <= report date and primary links. Unconfirmed claims may have explicit null date and empty links but identify precise missing proof. Proposed migration is not approved migration, target is not commitment, migration work is not accepted completion, and coordinator is not automatically accountable.
- Milestone date_status none pairs with null target_date. Proposed/committed require ISO target date; committed also requires verified primary support from the appropriate party. Proposed dates stay visibly proposed.
- Priority reported counts and exact matched names are separate. Unique cohort keys/memberships must reciprocate row tags. Different cohorts can overlap. Show unmatched remainder; never add priority counts or assume every priority customer is live.
- Summary derives exactly from rows. customers_without_current_data means current_service.status is not verified, not whole-customer ignorance. Continuing holds are no_change; failing requires a newly changed blocking dependency. Recommendations, tags, or newly discovered old records alone are not weekly movement.
- Attempt and privately record every source-to-conclusion row/claim audit. Never promote a recap to evidence, a closed ticket to acceptance, or a contractual/access gate to inferred technical cause.
- Jira counters retain schema-6 nullable semantics: both fields present; null only with specific row note and visible gap; validated keys retained. Cited-key length and updated time do not prove full counts or material changes. Never substitute zero. Jira source health/freshness stays mandatory.

Render order is Executive signal; What changed this week; Priority context; Customer transition; Decisions needing attention; Company revenue and sales; Full roster and evidence gaps. Main highlights/attention preserve producer order by consequence and credible deadline; full canonical roster is alphabetical. Routine appointments do not outrank more consequential commitments. Each customer has one full record; highlights refer to it.

Keep purpose/systems, dated position/direction, actual decision, qualified milestone, accountable role/coordinator, blocker, and Agentic contract ACV visible. Avoid duplicate stories, six generic unknown columns, ticket-count tables, and a fixed word cap that drops customers. An optional one- or two-item Product and design implications section uses grounded unique insights, never repeats next_watch or assigns PS work to Amit. Strategy updates may include source-backed money constraints with precise label and owner; they are not automatically earned revenue/bookings/forecast.

## Company measures

Optional company_context carries at most eight individually qualified claims about Ada, the combined company, financial evidence gaps, or a supported outlook. Keep entity, period and source quality explicit. Historical/pro forma/publicly reported values are not fresh certified results and cannot be added to the Dialpad-only operational snapshot. Apply normal claim validation; no invented profit, cash, valuation or three-month forecast.

Revenue fields/validation remain unchanged. The schema-7 compact helper presents numbers first with real periods, scoped interpretation, and specific unavailable notes. It does not fetch data, certify estimates, redefine measures, or infer broad company strengthening from one ARR metric. Profit, cash, valuation, and outlook stay unproven unless separately sourced.

The mandatory fresh Salesforce snapshot is annual recurring contract value from Dialpad's own Salesforce Account records, not a customer's CRM, earned revenue, or the Finance-certified ARR bridge. Preserve positive quarter-start cohort, its current ARR, positive ARR without opening snapshot, and all arithmetic. Label paid_licenses licenses on paying accounts: sum Total_Dialpad_License__c where Customer__c is true and ARR__c positive. Opening-cohort change is not churn/retention; the entire new/unsnapshotted bucket is not new growth.

Prior-report comparisons require stored like-for-like fields, cohort and currency, not rounded human email. Otherwise prior date/changes stay null with specific baseline note. Finance ARR retains actual reporting grain or explicit latest_arr_period null plus latest_arr_note; never substitute old bridges, zeros, or operational estimates.

Available bookings need governed common company/Agentic scope, dates, stages, exclusions/subtypes, and currency conversion. Opportunity.Agent_AI_ACV__c is the dedicated amount; Product Interest does not classify whole-opportunity ACV as Agentic. Broad won totals alone are not governed bookings. Never clip adjustments, count fulfillment/migration as a new sale, or combine Ada/Dialpad ARR without reconciled entity/currency/cohort.

When scope cannot be verified, explicit weekly_sales null plus weekly_sales_note, and/or quarter null plus quarter_note, preserve safe customer review without substitute metrics/shares. Notes are nonempty <=320 characters; missing keys fail. Available objects keep every numeric/arithmetic gate and no unavailable note. Either null bookings object requires fresh current-report-date Salesforce snapshot and correct fiscal-quarter label.

Q1 is February–April, Q2 May–July, Q3 August–October, Q4 November–January. Missing only the official Finance/RevOps target retains quarter actuals/available forecasts with target, attainment, gap, and required pace null plus target_note. Never infer company targets from sample dashboards, incomplete quotas, or subset plans. Leadership ambition remains a target. Full technical methods/receipts remain private; human presentation stays concise.

## Private source draft and protected delivery

After all gates pass, create exactly one source draft:

- Subject: [INTERNAL RELAY — DO NOT SEND] Weekly Agentic Customer Review — YYYY-MM-DD
- To: amit.ayre@dialpad.com; no Cc, Bcc, or attachments.
- Human preview then one schema-7 JSON envelope between ---BEGIN PULSE MACHINE JSON--- and ---END PULSE MACHINE JSON---.

Never send the internal draft manually. The relay ignores narrative, validates snapshot, deterministically renders final body, and persists the protected body-only Gmail delivery draft before SMTP. Final email has no attachments or machine JSON.

Final recipients come only from protected PULSE_RECIPIENTS: Amit's single approved address, Bcc only. To is exactly undisclosed-recipients:;, Cc absent; SMTP strips Bcc. Missing/additional/duplicate/different/visible final recipients fail before SMTP. Source-draft permission never authorizes a different recipient.

Live Message-ID is <daily-agentic-business-pulse-YYYY-MM-DD@dialpad.com>; dry-run/test paths have separate keys and protected test subject. Gmail Sent is checked before delivery. Prior accepted send returns duplicate_skipped. A prepared draft with no confirmed Sent record blocks an ambiguous retry rather than risking a second send. Never clear idempotency or bypass persistence to force delivery.

## Runtime privacy

Validation/preparation files exist only on the ephemeral runner, mode 0600:

- reports/agentic_business_pulse/YYYY-MM-DD.md
- reports/agentic_business_pulse/YYYY-MM-DD.json
- reports/agentic_business_pulse/YYYY-MM-DD.run.json

This repository is public. Never upload bodies, snapshots, source drafts, audit excerpts, or evidence as Actions artifacts, logs, summaries, or repository files. The workflow has no artifact-upload step. Public results/logs contain sanitized operational metadata only, never private values/evidence. Private audit/source persistence stays in private Glean runs and approved Gmail drafts/delivered mail; runtime files disappear with the runner. Do not introduce new storage or export destinations.

## Failures and operator interpretation

Fail closed for unhealthy/missing/stale/writable required sources; unsafe/unverifiable admission/identity; skipped audits; unsupported verified claims; invalid dates/window/schema/summaries/links/values; privacy violations; or failed recipient/persistence/idempotency gates. Empty admitted roster is invalid.

No newly verified movement is not itself failure. Safely audited partial coverage, last-known/proposed/unconfirmed claims, incomplete named priority cohorts, nullable Jira counts, and explicit unavailable optional measures remain visible gaps. Complete means safe procedure, not universal certainty.

Expected failures use once-per-IST-date alert with Message-ID <daily-agentic-business-pulse-failure-YYYY-MM-DD@design-pair-sessions.github>. Sent/already-sent alert yields handled failure and can leave Actions green; green does not prove report delivery. Notifier failure leaves process failed so GitHub is final alert path. Inspect sanitized outcome and Gmail Sent state, never print private source responses or exception payloads.

## Release verification

1. Check active contract against relay/helper and run repository tests/live PR validation with synthetic fixtures.
2. Update private Glean instructions in draft; preserve read-only access, source envelope, protected recipient, Monday 08:00/09:00 schedule.
3. Preview current authorized sources. Independently audit roster/admission/aliases, primary support/dates, carried commitments, real movement, cohort reciprocity/remainder, summaries, company scopes/currency/nulls, editorial consequence, and privacy. Generated preview prose is not evidence.
4. Confirm safe complete schema-7 snapshot. Audited uncertain claims and partial coverage are valid; all required source/admission/audit/schema/privacy gates remain mandatory. Publish only after validation.
5. Run protected no-send dry_run. Confirm readable body-only private delivery draft, one canonical record per customer, no machine JSON/attachments/public artifacts, approved Bcc only.
6. Only when explicitly authorized, perform one protected test_send or live send as requested; verify Gmail accepted correct rendered body/recipient without exposing address. Preview alone is not send authorization.
7. Verify separate test/live idempotency: a repeated authorized delivery with same key must duplicate_skip, not send again.

Fixtures prove structure/arithmetic/rendering only, never real customer facts or freshness.
