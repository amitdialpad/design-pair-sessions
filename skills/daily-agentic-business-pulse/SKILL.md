---
name: daily-agentic-business-pulse
description: Produce a daily, source-linked operating report that connects Dialpad Agentic commercial performance, customer reality, delivery risk, and production implementation evidence. Use only when fresh approved company sources are available.
---

# Daily Agentic Business Pulse

Produce a decision-ready daily operating report for an Agentic built-process designer. Connect commercial reality to product and design execution. Do not produce a Jira digest or a speculative narrative.

## Hard boundary

Use fresh evidence from all four required source classes:

1. Salesforce: bookings, targets, opportunities, forecast categories, Agentic-specific ACV, total bundled opportunity amount, close dates, accounts, owners, onboarding, and expansion.
2. Jira: Agentic customer issues, blockers, aging work, launch readiness, and ownership.
3. Glean/company search and document reading: EAPs, customer feedback, meetings, product plans, decisions, and the linked operating-model documents.
4. Production-code search: implementation ground truth, tests, feature flags, telemetry, schemas, deployment evidence, and runtime behavior.

If any required source is unavailable, stale, or unauthorized, stop normal report generation. Do not silently reuse prior values. Return a machine-readable failure that names each failed source. A report may be labeled `Data incomplete` only when the caller explicitly allows incomplete sends.

Never invent company facts, source links, account names, bookings, pipeline, targets, ownership, dates, or implementation status. The prior snapshot is comparison context, not current evidence.

## Reporting clock

- Resolve the reporting date and current time in `Asia/Kolkata`.
- Use the IST calendar date as the report date and idempotency key.
- State the exact comparison window in the report and snapshot.
- Compare against the most recent successful prior snapshot when available.
- GitHub-hosted schedules can start late; do not change the intended report date merely because execution starts several minutes after 09:00 IST.

## Evidence discipline

Label material statements with one of these classifications:

- `[Verified fact]`: directly supported by a linked authoritative source.
- `[Signal]`: an observed change or pattern that is meaningful but not conclusive.
- `[Inference]`: a reasoned interpretation built from named facts or signals.
- `[Unknown]`: information needed for a decision that could not be verified.

Link material claims to their source. Prefer the specific Salesforce record, Jira ticket or filter, company document section, pull request, commit, code path, test, feature flag, dashboard, or deployment record over a generic home page.

Keep source attribution compact in the narrative and provide a complete source register in `Sources and confidence`.

## Commercial definitions

Keep these concepts structurally and linguistically separate:

- Booked revenue is closed business. Never describe open pipeline as booked revenue.
- Open pipeline is not revenue. Qualify it by forecast category and close window.
- Agentic-specific ACV is the amount attributable to Agentic products.
- Total bundled opportunity amount can include non-Agentic products. Never substitute it for Agentic-specific ACV.
- Target attainment equals booked Agentic ACV divided by the applicable Agentic target.
- Gap equals target minus booked Agentic ACV, with over-target performance represented explicitly.
- Pace states the time basis and method used.
- Qualified pipeline coverage equals qualified open Agentic ACV divided by the remaining Agentic target gap. State how `qualified` was selected.

Show unknown or unavailable values as unknown. Do not turn missing amounts into zero.

## Customer and EAP reality

Trace outcomes across pre-sales, onboarding, deployment, and Customer Success. Surface:

- customer goal and agreed success criteria;
- current phase and recent movement;
- onboarding, adoption, expansion, or churn risk;
- named owner when permitted;
- blockers and dependencies;
- evidence from customer feedback, meetings, decisions, Jira, telemetry, or implementation.

Use only permitted account names. Otherwise use a stable redacted label. Do not persist contacts, email addresses, phone numbers, transcript excerpts, raw customer payloads, or unnecessary personal data.

## Jira and delivery risk

Use Jira as one evidence stream, not the report's organizing model. Prioritize work that materially affects a customer outcome, commercial commitment, EAP result, launch condition, reliability, or unblock decision.

For material delivery risks, capture:

- ticket and source link;
- customer or commercial consequence;
- owner and next decision when permitted;
- age or due-date movement;
- acceptance criteria;
- dependencies and rollback expectation;
- whether the work changed since the prior snapshot.

Do not equate `Done` or `Closed` with deployed or customer-exposed behavior.

## Implementation reality

For each material product claim, distinguish the strongest verified state:

1. `code_exists`
2. `tested`
3. `flagged`
4. `instrumented`
5. `deployed`
6. `customer_exposed`

These states are cumulative only when evidence proves each one. Link the implementation evidence. Name the relevant production API, schema, feature flag, test, telemetry event/dashboard, deployment record, or customer exposure evidence when available.

Prototype, mock, demo, sandbox, fixture, and test data are not deployed production behavior. Never label them `deployed` or `customer_exposed`.

## Daily analysis

Determine what materially changed since the prior successful snapshot:

- booked Agentic ACV and target attainment;
- target gap, pace, and qualified pipeline coverage;
- forecast-category, close-date, ownership, and expansion movement;
- onboarding progress or regression;
- EAP success, adoption, and blocker movement;
- newly aging or resolved delivery risks;
- implementation-state changes;
- newly verified telemetry, rollback, dependency, or reviewer evidence.

Explain why a change matters to product/design execution. Prefer a few consequential changes over a long activity list.

## Required report

The Markdown report must start with the exact title:

`# Daily Agentic Business Pulse — YYYY-MM-DD`

Immediately state:

- reporting time and timezone;
- comparison window;
- overall data status.

Use these exact level-two sections in this order:

1. `## Executive readout`
2. `## Revenue scoreboard`
3. `## Customer and EAP reality`
4. `## Jira and delivery risk`
5. `## Implementation reality`
6. `## Working / not working`
7. `## Decisions and actions`
8. `## Sources and confidence`

### Executive readout

Lead with the business outcome, the most material change, the largest risk, and the decision that deserves attention today. Keep the distinction between fact, signal, inference, and unknown visible.

### Revenue scoreboard

Show booked Agentic ACV, total booked bundled amount, applicable Agentic target, attainment, gap, pace, qualified open Agentic pipeline, total bundled open opportunity amount, and pipeline coverage. State currency, qualification rules, and comparison basis. Do not mix bookings and pipeline in one number.

### Customer and EAP reality

Show meaningful customer/EAP movement, success criteria, onboarding/adoption state, expansion signals, blockers, ownership, and what changed.

### Jira and delivery risk

Show only delivery items with a material business or customer consequence. Include source links, age/change, owner where permitted, dependencies, acceptance criteria, and next action.

### Implementation reality

For each material claim, state the verified implementation level: code exists, tested, flagged, instrumented, deployed, or customer-exposed. Identify unknown gaps explicitly.

### Working / not working

Separate demonstrated positive outcomes from friction, regressions, or unsupported assumptions. Do not treat volume alone as success.

### Decisions and actions

Give a short prioritized list. Each action needs a decision or outcome, owner where permitted, timing, dependency, and source rationale. Preserve named reviewer requirements found in source material.

### Sources and confidence

List each required source class, query time/freshness, status, linked records, and confidence limitations. Include the workflow run URL and report date for troubleshooting. State `[Unknown] None identified` only when evidence genuinely supports that claim.

## Structured snapshot

Return a JSON snapshot alongside the report. Store only aggregate metrics, source links, ticket IDs, permitted account names, short redacted summaries, implementation claims, and run metadata.

The snapshot must include:

- `schema_version`
- `report_date`
- `generated_at`
- `comparison_window` with `start`, `end`, and `label`
- `metrics.revenue` with separate booked Agentic ACV, booked bundled amount, target, gap, attainment, and pace
- `metrics.pipeline` with separate qualified Agentic ACV, bundled opportunity amount, and coverage
- aggregate `metrics.onboarding` and `metrics.eap`
- `source_status` entries for `salesforce`, `jira`, `glean`, and `production_code`, each with status, query time, and links
- `customers` containing only permitted/redacted names, short summaries, and links
- `jira_items` containing ticket IDs, short summaries, status/age, and links
- `implementation_claims` containing claim, evidence origin, verified statuses, fixture marker, and links
- `decisions`
- `changes_since_previous`
- `unknowns`

Do not include raw source responses, query/tool arguments, credentials, tokens, transcripts, contacts, or customer payloads.

## Output contract

Return one JSON object with:

- `report_markdown`: the complete source-linked report;
- `snapshot`: the structured snapshot;
- `agent_request_id`: a non-sensitive runtime request identifier;
- `data_status`: `complete` or `incomplete`;
- `failures`: a list of missing or failed sources.

Return JSON only. Do not wrap it in Markdown fences.

## Source context

Use the three approved document links supplied by the runtime through `source_context`. They correspond to:

- Agentic Connectors Q3 Production Plan;
- B2B Customer Journey Agentic AI;
- Agentic Impact Report PRD.

The direct internal document identifiers belong in the automation's encrypted `PULSE_SOURCE_CONTEXT_JSON` secret, not in a public repository. Read the documents through approved company search/document reading. Do not assume their contents from their titles.

Preserve the operating model across customer outcomes, feature flags, production APIs, acceptance criteria, telemetry, rollback, dependencies, named reviewers, and success criteria from pre-sales through deployment and Customer Success.
