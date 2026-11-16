---
name: daily-agentic-business-pulse
description: Produces an evidence-based weekly Agentic customer transition review for business awareness, anticipation, and product judgment across the admitted portfolio.
---
# Weekly Agentic Customer Review

## Active contract: schema 7

Produce schema 7. This is the single active producer contract; older-reader compatibility is described separately below. Run private research every Monday at 08:00 Asia/Kolkata for protected relay delivery at 09:00. Review the preceding Monday through Sunday and compare with the prior delivered review.

Help Amit understand the business and anticipate product consequences as a designer-builder. Explain changes in the selling, fulfillment, and support model, their source-backed constraints, and the customer consequences. The report is more than a delivery evidence ledger. Do not turn it into a list of requests to obtain proof or assign PS/delivery work to Amit.

Retain the full admitted customer portfolio. For each customer distinguish what service exists, where it is heading, what is approved versus proposed, the next meaningful checkpoint, and actual accountability. Preserve useful last-known history without asserting present certainty. A missing decision does not erase known service; missing documentation is not automatically an unresolved customer decision.

Keep these distinctions explicit:

- An inventory recommendation is not an approved leadership or customer decision.
- An engineering target is not a customer commitment.
- A migration plan, completed implementation task, and accepted customer completion are different states.
- A priority tag is not an extra customer, an operating stage, or proof of being live.
- Fulfillment or migration of an existing sale is not a new booking.

## Safety and privacy

All company-source access is read-only. Use approved search, read, list, view, code-search, SOQL-query, Jira-search, email-search, and calendar-search operations. Never write, comment, transition, label, configure, grant, export, delete, send, or change permissions in source systems or customer systems. Never bypass a permission boundary.

The research agent's only permitted write is the existing Gmail MCP Create Draft action for the private internal relay envelope, addressed only to amit.ayre@dialpad.com. The separately protected relay performs its established private Gmail persistence and delivery. Source-draft permission does not authorize source changes or outreach.

Never persist raw conversations, transcripts, prompts, tool arguments, customer payloads, credentials, or secrets. Private audit notes contain minimal dated support and reasoning, not raw source dumps. This repository is public: never put private reports, snapshots, drafts, customer evidence, strategy details, or real customer fixtures in repository files, Actions artifacts, logs, or job summaries. Use fictional fixtures. The final email has no attachments or machine JSON.

Do not use BigQuery, Pinot, or Agentic Analytics. Never infer conversations, usage, action success, containment, resolution, CSAT, or other product telemetry. Optional production code is implementation context, never proof of deployment, customer acceptance, or live service. Do not include Amit's personal projects.

## Evidence order and freshness

Research in this order, using each source only for the fact it owns:

1. Approved written leadership decisions and strategy changes.
2. Current migration and fulfillment inventory, including row dates, recommendations, and unresolved ownership.
3. PM/customer workbooks, delivery plans, agreements, communications, and dated decisions.
4. Salesforce for exact identity, admission/commercial records, dedicated Agentic contract value, and governed company measures.
5. Jira as supporting issue/implementation evidence after establishing the actual customer dependency.

Generated reports, agent-written recaps, and search summaries are discovery aids only. Follow their primary links; they never independently corroborate a claim or refresh its evidence date. Document modification, meeting, query, or recap publication time does not replace substantive evidence time.

Salesforce, Jira, and Glean source families must each be healthy, fresh, linked, and read-only. Receipts use actual successful read/query time, not payload assembly time: at most 12 hours old at validation and no more than 10 minutes future-dated. Re-read to refresh; never only change a timestamp. Keep an additional receipt when optional production code is used. A fresh receipt does not make an old customer statement current.

Each source_status receipt contains status: "ok", queried_at (ISO-8601 timestamp with timezone), nonempty direct HTTPS links, and access_mode: "read_only". Required keys are salesforce, jira, and glean.

## Portfolio reconciliation and audit

Retain every known customer admitted to Agentic delivery, including accepted onboarding/build, EAP/pilots, pre-sale builds with assigned delivery resources, deployment, live, and paused engagements. A sales prospect or a name in a broader migration inventory is a candidate until primary evidence establishes delivery entry. A generic template or similar name is insufficient admission evidence.

Reconcile delivery/fulfillment inventory, PM/FDE workbooks, EAP/build roster, exact Salesforce records, and prior delivered roster. The prior review is a retention checklist, not new factual corroboration or an immutable total. Join only by a canonical identifier or exact unambiguous identity. Verify aliases explicitly; never guess from abbreviation, domain, contact, or opportunity title. Reconcile additional names before counting them. Explain supported additions, explicit exits, and alias corrections in changes_since_previous; never silently omit an admitted customer. Unresolved differences require partial coverage, not a forced preferred count.

Carry forward last week's pending commitments and checkpoints. State whether the promised proof arrived, slipped, or remains unresolved, using current primary evidence. Missing proof alone does not establish a missed commitment or customer failure.

Before drafting, attempt and privately record a source-to-conclusion audit for every row and material claim. Re-read primary material, retain its substantive date and minimal support, identify agreement parties, and check that cause, direction, decision, milestone, and accountability follow. A URL alone is not an audit. A known contractual/access gate must not become a technical defect without newer primary support. A coordinator is not automatically the decision owner or accountable delivery role.

One row may contain verified, last-known, proposed, and unconfirmed claims. An inaccessible individual source or unresolved contradiction is a claim-level gap when its source family is healthy and admission/identity is established. Name the precise missing proof and preserve genuine history. Never invent a date, quotation, owner, cause, commitment, or current status. Avoid repeated generic unknown templates.

data_status: "complete" means the required safe procedure completed, not that every claim is current. Audited uncertain claims, incomplete named cohorts, partial coverage, and explicitly unavailable optional measures belong in visible gaps, not failures. Unhealthy required sources, unverifiable admission/identity, skipped audits, unsupported verified claims, schema errors, and privacy violations remain hard failures.

## Snapshot and base customer schema

The private draft contains one outer object with report_markdown (short human preview), agent_request_id (non-sensitive runtime ID), data_status: "complete", failures: [], and snapshot. The relay ignores the preview and deterministically renders snapshot.

Required snapshot fields:

| Field | Contract |
|---|---|
| schema_version | 7 |
| report_date | Real current IST date, YYYY-MM-DD; scheduled delivery is Monday only |
| generated_at | Actual ISO-8601 generation timestamp with timezone |
| comparison_window | start, end, label; scheduled window is preceding Monday through Sunday |
| source_status | Fresh read-only receipts described above |
| coverage | status: reconciled or partial; nonempty note <=600 characters; nonempty primary HTTPS roster links |
| summary | Exact row-derived counts described below |
| customers | Nonempty deduplicated admitted portfolio with canonical names |
| strategy_updates | Dated primary-linked claim objects for material leadership/business changes in the window; [] when none |
| priority_cohorts | Source-reported groups and exact matched canonical names |
| unknowns | Specific material evidence gaps; may be [] |
| changes_since_previous | Supported roster changes and comparison limitations; may be [] |
| executive_read | paragraph; confidence: low, medium, or high; one to four primary HTTPS links |
| business_health | Existing revenue schema and safeguards below |
| company_context | Optional list of up to eight independently qualified financial/context claims; same text/status/evidence_date/links shape as transition claims |

customer_insight is replaced by transition. Legacy commercial_changes may be omitted or empty. insights is optional and limited editorially to one or two unique grounded product/design implications; it is not duplicate customer analysis.

Each customer retains the base schema-5 fields:

| Field | Contract |
|---|---|
| account_name, name_permitted | Canonical safely attributable name; name_permitted: true; no duplicate identities or case variants |
| lifecycle_stage | build, test, validate, publish, live, paused, or unknown; consistent with qualified service evidence, never inferred from sales stage |
| movement | failing, moved, or no_change, as defined below |
| agent_or_use_case | Nonempty known customer purpose, honestly qualified if historical/unresolved |
| links | Nonempty direct primary HTTPS evidence for identity/admission and known context |
| integrations | List of {name,status}; status building, testing, connected, failing, or unknown; never guess readiness |
| change_this_week, next_watch | Each nonempty <=320 characters; actual change or meaningful dated continuity, then specific next proof |
| jira | Both audit counters, validated keys, and specific note when a count is unavailable |
| commercial | Nonempty stage; movement_7d; agentic_acv as verified nonnegative amount or explicit null |
| transition | Route, six independently qualified claims, priority tags, attention fields |

commercial.movement_7d is advanced, slipped, won, lost, value_changed, or no_change. Never substitute total bundled opportunity value for Agentic contract ACV. Label it Agentic contract ACV, not recognized revenue, migration revenue, or a new Ada sale.

jira.new_or_changed_7d and jira.open_customer_bugs must both be present as validated nonnegative numeric counts or explicit null. If either is null, require a specific nonempty jira.note <=320 characters and disclose the limitation in unknowns. Retain validated mapped jira.keys. Key-list length does not prove complete coverage; updated time alone does not prove material change. Never use zero for an incomplete audit. Counts are audit data, not the human report's lead; Jira health/freshness stays mandatory.

## Transition claim contract

transition.route is ada_new, ada_migration, dialpad, undecided, or unknown. It classifies sourced direction, not approval or execution. A migration recommendation can use ada_migration with a proposed direction; approval is a separate decision claim.

Require six claim objects:

- current_service: operating service or last genuinely known state, including supported pause or incomplete deployment.
- direction: sourced platform/fulfillment path, distinguished as recommendation, approved direction, or unresolved choice.
- decision: actual decision or precise decision still required; do not turn silence into approval or a missing record into a known customer dispute.
- next_milestone: next meaningful customer proof/gate, distinct from a suggested implementation plan.
- accountability: actual accountable decision/delivery role and known coordinator, clearly distinguished; no invented assignment.
- blocker: primary supported dependency or exact missing proof; an evidence gap is not automatically a technical blocker.

Each claim contains text, status, evidence_date, and links. text is nonempty and <=320 characters. status is one of:

- verified: accessible dated primary support confirms the stated present fact or actual decision.
- last_known: genuinely dated history, explicitly worded as last known, without asserting it remains true today.
- proposed: sourced recommendation, intended direction, suggested milestone, or target, with no implied approval.
- unconfirmed: exact fact cannot be established; name the precise gap, retaining supported history in other appropriate claims.

Every non-unconfirmed claim requires a substantive YYYY-MM-DD evidence_date <= report_date and nonempty primary HTTPS links. Unconfirmed claims still require both fields but may use explicit null and []; never invent support. Any supplied evidence date must not be future-dated and any supplied link must be HTTPS.

strategy_updates use the same claim structure but always require a date and primary links, even if describing an unresolved written update. Omit unsupported updates rather than create placeholders. Relevant money constraints, such as an open renewal, may appear with precise labeling, actual ownership in text, and primary evidence; they are not earned revenue, bookings, or forecast merely because money is involved.

next_milestone additionally requires target_date (YYYY-MM-DD or null) and date_status: none, proposed, or committed. none pairs exactly with null; proposed/committed require a real ISO target date and a sourced, non-unconfirmed milestone claim. An unconfirmed milestone keeps target_date null and date_status none. Future target dates are allowed, unlike future evidence dates. committed requires a verified claim and primary support for the commitment by the appropriate party. A scheduled review, internal target, or engineering estimate is not a promised go-live. A passed old target is not completion evidence.

transition.priority_cohorts is a list of unique defined cohort keys. transition.attention is boolean; attention_reason is <=320 characters and nonempty when attention is true (may be empty otherwise). Flag real consequential decisions/dependencies, not every documentation gap. Explain customer consequence and next observable checkpoint with the actual accountable role where known.

## Priority context, movement, and summaries

Each priority_cohorts entry has key, label, reported_count (nonnegative integer, never boolean), substantive evidence_date <= report_date, nonempty primary HTTPS links, matched_customers, and note <=600 characters. Keys are unique including case variants. matched_customers contains unique exact canonical row names and must exactly reciprocate row tags. Do not infer a tag because a customer seems important. Different cohorts may overlap.

Keep leadership-reported counts separate from matched records. Matched count cannot exceed reported count. Show reported, matched, and unassigned remainder. An incomplete named roster stays visible. VIP is a nonexclusive priority tag, not an additional customer count or live-stage assertion. Never add overlapping cohort counts or publish a completion percentage without a reconciled denominator and accepted completion evidence.

Calculate summary from canonical rows:

- active_customer_count: all rows, including quiet and paused retained engagements.
- movers_7d: movement is moved or failing, preserving the existing summary definition.
- customers_with_changed_blockers_7d: movement is failing.
- customers_without_current_data: transition.current_service.status is not verified; this does not make the whole customer unknown.
- commercial_moves_7d: commercial.movement_7d is not no_change.

Optional reported_deployment_count is only a directly sourced comparable umbrella total, cannot be smaller than retained rows, and never replaces roster reconciliation. Smaller priority counts belong in priority_cohorts.

failing means a newly changed blocking dependency. moved means an actual material customer/operating/delivery/commercial change during the window. no_change includes continuing holds, unchanged positions, and stale/unconfirmed current status. Discovering an old record, recommending migration, missing fresh evidence, or adding a priority tag does not itself prove weekly movement. No new event is required to retain a customer.

## Reader presentation and editorial judgment

Render in this order:

1. Executive signal: one authored thesis about the strongest consequential change, including changed selling/fulfillment/support model and sourced business constraints when material.
2. What changed this week: dated leadership/business changes, true customer movement, and reconciled roster changes; carry forward pending commitments and report the resulting proof.
3. Priority context: reported groups, matched names, visible unmatched remainder; no additive total.
4. Customer transition: material highlights referring to canonical full-roster records, not duplicate full stories.
5. Decisions needing attention: actual consequential decisions/dependencies, qualified checkpoints, and supported accountability.
6. Company revenue and sales: compact numbers-first company helper with real periods and explicit unavailable measures.
7. Full roster and evidence gaps: one canonical record per admitted customer, specific portfolio gaps, direct evidence.

An optional small Product and design implications section may contain one or two insights when a unique grounded interpretation or explicitly proposed product/design lever helps Amit anticipate a decision. Each insight retains account_name, text <=320 characters, and nonempty primary HTTPS links. Do not repeat next_watch, give routine delivery instructions, or assign PS follow-up to Amit. Omit when no useful distinct implication is supported.

Order main highlights and attention by business/customer consequence and credible deadline, preserving that editorial input order. A routine review appointment should not displace a more consequential commitment. Keep the canonical full roster alphabetical. Each record includes purpose/systems, dated service/direction, actual decision, qualified milestone/date, accountable role versus coordinator, blocker or precise gap, and Agentic contract ACV when verified. Avoid six repetitive unknown columns. Scale length with the roster; never drop customers for an old word cap. Do not render duplicate Analysis or Jira count tables.

executive_read.paragraph is one nonempty paragraph, <=900 characters and 140 words, confidence low/medium/high, with one to four primary HTTPS links. Strategy/restructuring claims require approved written company evidence. Private conversation may guide research, never become report evidence. Current public primary evidence may inform material interpretation, never prove a private fact. Stable history/ambition is not weekly change. When no new signal supports a stronger thesis, say so; never manufacture novelty.

## Company revenue and sales: unchanged measure contract

Use company_context for material Ada or combined-company financial evidence, strengths, and a supported outlook that the existing numeric objects do not represent. Label the entity, measure, actual period, and source quality in each concise claim. Keep historical/latest-available context here, not under this week's changes. A press-reported pro forma unaudited figure is not a current certified total; never compare or add it to a different-date Dialpad-only Salesforce estimate. Current profitability, cash, valuation or three-month forecasts require their own evidence; state a precise access/evidence gap once when unavailable. Outlook may identify explicitly proposed, source-grounded watchpoints, never invent a valuation or financial forecast from a leadership ambition. Claims use the same independent date/status/link validation; do not supply old growth figures as current performance. Omit empty context rather than add generic filler.

Keep the existing business_health schema and every numeric, null, arithmetic, target, currency, and cohort safeguard. The compact helper changes presentation only. verdict remains strengthening/stable/weakening for compatibility; verdict_reason is nonempty <=320 characters and a short scoped interpretation of available measures. One operational ARR measure does not justify a broad company-strengthening conclusion. Profit, cash, valuation, and outlook remain missing proof unless independently supported; do not derive them from ARR.

Salesforce here means Dialpad's own Salesforce Account records, not a customer's CRM integration. Its operational ARR estimate is annual recurring contract value, not earned/recognized revenue or the Finance-certified ARR bridge. Never add Ada and Dialpad ARR without reconciled entities, currency, and cohort. Fulfillment/migration of an existing contract is not a new booking.

weekly_sales contains total_bookings, core_bookings, agentic_bookings, and agentic_share_pct. Available values are finite/nonnegative; core plus Agentic equals total, with share on the same total and period (zero total has zero share). Verify common governed cohort, won stages, dates, revenue/subtype/exclusion rules, and currency conversion. Opportunity.Agent_AI_ACV__c is the dedicated Agentic amount; Product Interest Opportunity_Type__c does not make whole-opportunity ACV Agentic. A broad won ACV_New_USD__c sum is not automatically company bookings. Never clip signed adjustments or redefine the metric to pass validation.

When that basis cannot be verified, use explicit weekly_sales: null plus specific nonempty weekly_sales_note <=320 characters, and/or quarter: null plus quarter_note under the same rule. Missing keys fail; unavailable figures are never zeros/estimates. Available objects must not carry an unavailable note. Either null bookings object still requires the fresh current-report-date Salesforce snapshot and correct fiscal-quarter label. These explicit gaps do not populate failures.

salesforce_operational_snapshot is mandatory, using current read-only Account aggregates:

| Field | Basis |
|---|---|
| as_of_date, quarter_label | Actual report-date query and Dialpad fiscal quarter |
| quarter_start_arr | Sum First_Day_FQ_ARR__c where that field is positive |
| opening_cohort_current_arr | Sum ARR__c for exactly the same positive quarter-start cohort |
| new_or_unsnapshotted_arr | Sum positive ARR__c where quarter-start ARR is null/zero; may be new, reactivated, or previously unsnapshotted |
| current_arr | Opening-cohort current ARR plus new/unsnapshotted bucket |
| net_arr_change, net_arr_change_pct | Current minus quarter-start ARR; percentage denominator quarter-start ARR; zero denominator yields zero |
| opening_cohort_change | Opening-cohort current ARR minus quarter-start ARR; never call it churn/retention |
| paying_accounts, paid_licenses | Account count and sum Total_Dialpad_License__c where Customer__c is true and ARR__c is positive |
| method_note | Nonempty <=320 characters; Salesforce operational estimate, not Finance-certified ARR bridge |
| comparison | Prior safe like-for-like stored snapshot, or explicit null baseline date/changes with specific note |

Counts are nonnegative integers. Base ARR amounts are finite/nonnegative; actual net, percentage, cohort, and comparison changes may be signed. All cohort arithmetic must reconcile. Human label for paid_licenses is licenses on paying accounts, not Finance-certified paid seats. Opening-cohort movement mixes expansion, contraction, churn, reactivation, and corrections; do not invent a driver split or call the entire new/unsnapshotted bucket new growth.

comparison contains previous_snapshot_date, arr_change_since_previous, paying_account_change, paid_license_change, and comparison_note. Retrieve the prior Monday's stored snapshot and compare only identical fields/scope/currency. Previous date precedes current. A rounded human email or missing field definition is not comparability proof. Without it, date and all change values stay null with nonempty comparison_note <=320 characters; never invent the baseline.

latest_arr_period is a current authorized Finance/RevOps bridge with actual period label, signed net_arr_change, new_plus_expansion, churn_plus_contraction, integer net_customers and paid_license_change; or explicit null with specific nonempty latest_arr_note <=320 characters. Keep monthly data monthly. Do not substitute old bridges, operational estimates, zeros, or inferred telemetry.

Available quarter retains label, actual_bookings, agentic_bookings, agentic_share_pct, target_status, target_bookings, attainment_pct, gap_to_target, required_weekly_pace, commit_forecast, best_case_forecast, previous_quarter_bookings, and target_note when needed. Q1 is February–April, Q2 May–July, Q3 August–October, Q4 November–January; the fiscal year ends the following January. Label actuals, forecasts, targets, and prior periods separately.

target_status is verified/unverified/unavailable. A verified company target requires authoritative Finance/RevOps planning evidence, a positive amount, and reconciled attainment/target-minus-actual gap. Required pace uses the correct remaining period; do not invent it. Missing only the official target retains verified actuals/available forecasts in the quarter object while target, attainment, gap, and required pace are null with specific target_note. Never use sample dashboards, incomplete quotas, or subset targets as the company target. Optional forecasts/prior-quarter bookings may be null; available amounts remain finite/nonnegative except the signed gap.

Keep full query definitions, receipts, currency/cohort checks, and minimal audit support private. The human section presents concise readable amounts, real dates, comparisons, and scoped interpretation, with specific gaps instead of technical dumps.

## Failure, dates, and private relay

Fail closed with data_status: "incomplete" and a concise failure entry for unhealthy/missing/stale/writable required sources, unsafe/unverifiable admission or identity, skipped audits, unsupported verified claims, invalid dates/window/schema/counts/links/values, privacy violations, or required permission/configuration changes. Empty admitted roster is invalid. A quiet week without new verified movement is valid when the roster and safe procedure are preserved. Never reuse a prior review as current evidence or zero-fill a gap.

Scheduled reports use real Monday IST date and preceding Monday–Sunday window. Only explicitly requested protected test_send permits another current IST date: window starts seven days before latest Monday and ends yesterday. Label it accurately, distinguish current status from in-window changes, and never backdate evidence or change production cadence.

After every gate passes, create exactly one internal Gmail source draft:

- Subject: [INTERNAL RELAY — DO NOT SEND] Weekly Agentic Customer Review — YYYY-MM-DD
- To: amit.ayre@dialpad.com; no Cc, Bcc, or attachments.
- Short human preview, then one JSON object between ---BEGIN PULSE MACHINE JSON--- and ---END PULSE MACHINE JSON---.

Never manually send the internal source draft. The approved relay validates snapshot, deterministically renders the final email, persists its private body-only delivery draft, and only then sends through the protected path. Final recipients come only from protected configuration: Amit alone in Bcc, To exactly undisclosed-recipients:;, no Cc, Bcc removed from transmitted headers. No attachments, machine JSON, public artifacts, or unredacted recipient address in final content. Recipient validation, deterministic date-based idempotency, ambiguous-send protection, and once-per-date failure alerts remain mandatory. See operations for unchanged schedule and run verification.

## Older-reader compatibility only

The relay retains existing schema-1 through schema-6 reader behavior/safeguards. Schema 6 uses customer_insight and coverage; schema 5 and earlier retain historical requirements/rendering. Old schemas do not acquire transition/cohort rules; nullable Jira counters remain limited to schemas 6 and 7. Do not produce an old schema or apply historical verified-signal-only inclusion, zero-unknown summaries, duplicate Analysis, old render order, or fixed portfolio word cap to schema 7.
