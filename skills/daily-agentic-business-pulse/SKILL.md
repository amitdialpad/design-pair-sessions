---
name: daily-agentic-business-pulse
description: Produces a daily evidence-based view of Dialpad Agentic revenue, pipeline, customer pain, Jira delivery risk, EAP performance, onboarding, and expansion signals, then prepares or sends the report to Amit Ayre.
---
# Daily Agentic Business Pulse

## Mission

Default intended schedule: daily at 09:00 IST. This skill defines the report workflow but does not create a scheduler; an external automation must invoke it at that time. When invoked, track whether Dialpad Agentic is converting into revenue and customer value—not merely whether teams are shipping features.

The report must cover:

- Revenue, bookings, target attainment, remaining gap, pace, and pipeline quality.
- Agentic pipeline by quarter, forecast category, stage, owner, account, and Agentic-specific ACV.
- Customer issues and friction from Jira, support/customer feedback, meetings, docs, and messages.
- What is working and what is failing across Agentic product areas and EAPs.
- EAP cohort performance, customer onboarding, activation, usage, outcomes, and risks.
- Concrete actions, owners, and decisions needed.

## Source priority

Use live company sources first. Prefer the most recent authoritative source for each metric and preserve the source link and date.

1. Salesforce for bookings, opportunities, forecast categories, ACV, close dates, accounts, owners, onboarding/commercial status, and expansion signals.
2. Jira for customer-impacting defects, blockers, aging work, launch readiness, and ownership.
3. Glean search/document reading for EAP updates, customer feedback, product plans, launch notes, strategy, and meeting decisions.
4. Slack, email, and meeting sources for recent customer and field signals when available.
5. Prior daily snapshots only for comparison; never use them as a substitute for a fresh lookup.

## Daily procedure

### 1. Establish the reporting window

Use the current date in the user's preferred timezone. Compare against the most recent successful report and the prior business day or seven-day baseline, depending on the metric. State the comparison window explicitly. If no earlier structured snapshot is available, report current facts without inventing a delta; that continuity gap alone does not make the current report incomplete.

### 2. Refresh revenue and pipeline

Query Salesforce and the latest official revenue/target source. Separate these categories:

- Closed-won/booked revenue.
- Current-quarter target.
- Remaining target gap and attainment percentage.
- Required weekly pace for the remaining selling period.
- Open pipeline by fiscal quarter and forecast category.
- Weighted forecast, if an authoritative probability/forecast field exists.
- Agentic-specific ACV versus total opportunity amount.
- New, advanced, slipped, reduced, stalled, won, and lost opportunities since the prior report.

Never describe open pipeline as revenue. Never combine different target scopes without calling out the change. If the official target changed, show the current target and the previous baseline separately.

Calculate:

- Attainment = booked revenue / current target.
- Remaining gap = current target - booked revenue.
- Pipeline coverage = relevant qualified pipeline / remaining gap.
- Required weekly pace = remaining gap / selling weeks remaining.

Break out Agentic Connectors, Agentic Billing, and other Agentic motions whenever the data supports it. Flag bundled opportunities where total amount materially exceeds Agentic-specific ACV.

### 3. Refresh customer pain and delivery risk

Search Jira and customer-facing sources for the last 24 hours and last 7 days. Prioritize issues that affect:

- Customer onboarding or time to first value.
- Connector setup, authentication, propagation, action execution, testing, publishing, or troubleshooting.
- Agent quality, resolution, latency, safety, analytics, billing, or usage visibility.
- EAP customers, design partners, pilots, or active revenue opportunities.
- Launch blockers, repeated defects, escalations, or support dependency.

For each important issue, capture: customer or cohort if known, symptom, business impact, ticket, status, age, owner, next action, and whether it is recurring.

### 4. Refresh EAP and onboarding performance

Find the latest evidence for each Agentic EAP or design-partner cohort. Track, where available:

- Cohort name, customer count, invited, onboarded, activated, connected, deployed, and active.
- Time from invitation to first value.
- Usage and repeat usage.
- Task completion, resolution, escalation, CSAT, or other outcome measures.
- Feedback themes and representative customer language.
- Accounts blocked, stalled, churned, or converted to paid usage.
- Next onboarding dates and responsible owner.

If a metric is unavailable, write `Not available` rather than estimating it. Distinguish anecdotal feedback from measured performance.

### 5. Synthesize what is working and what needs work

Produce no more than five conclusions. Each conclusion must be tagged as one of:

- `Verified` — supported by a current source or calculated from current records.
- `Signal` — repeated anecdotal evidence or an early directional trend.
- `Inference` — a reasoned interpretation that needs validation.
- `Unknown` — important but not currently measurable.

Prioritize conclusions that affect revenue conversion, customer time to value, EAP continuation, expansion, or launch risk.

### 6. Create the daily report

Write for a design manager and product thinker, not for an operations analyst. The email should feel like a short story told by a smart colleague: what is happening, why it matters, and what Amit can shape. Keep the full evidence taxonomy, issue inventory, calculations, and implementation-status detail in the structured snapshot. In the human report, synthesize those records into a few hard conclusions and link the supporting sources inline.

Use exactly this structure and keep the complete report at 650 words or fewer:

# Daily Agentic Business Pulse — YYYY-MM-DD

_What this covers: DATE–DATE · Compared with: DATE or “first comparable report”_

## TL;DR

Use three to five short sentences to answer: What is happening? Why should Amit care? What should change now? Lead with the human conclusion, not a metric label. Do not open with data availability, methodology, source names, or an evidence label. A reader who stops here should still understand the day.

## The numbers

Show only three or four rounded metrics that change the reader's understanding. Write every item as **plain-English number** — what it means and why it matters. For example:

- **$31K already booked for Agentic** — annual contract value that is won, not a possible deal.
- **$643K still in play** — possible Agentic business, not booked revenue.
- **$2.9M total value of those deals** — the whole bundled deals; only part of this belongs to Agentic.
- **3 early-access customers confirmed active** — the tracker is a month old, so treat this count cautiously.

Normally include booked Agentic annual contract value against target, possible Agentic business, and the strongest customer rollout or value measure. Keep booked revenue and open pipeline visually and verbally separate. Keep Agentic-specific annual contract value separate from total bundled opportunity amount. Put secondary calculations and exact precision in the snapshot.

## The story

Use exactly three `###` conclusion headlines, in this order:

1. `### Money — …`
2. `### Customers — …`
3. `### Product — …`

Each insight gets one short paragraph that tells a mini-story in this order:

- What happened.
- Why it matters to the business or customer.
- What it means for the product or design.

Cluster related Jira tickets, customer reports, and code findings into a pattern; do not list tickets one by one. Cite one or two decisive sources inline with descriptive link text. Mention a specific ticket, customer, feature flag, or code path only when it materially changes a conclusion.

Headlines must state the conclusion in ordinary language. Prefer `Money — interest is not turning into booked business fast enough` over `Funnel quality needs an Agentic-specific operating view`.

## What this means for design

Give Amit no more than three designer-manager moves. Write each as a concrete product/design move followed by `Why:` and the expected business or customer effect. Each must be something he can clarify, frame, review, or make visible as a product/design leader. Do not give him a generic project-management task list or assign work to other people without evidence of ownership.

## What to trust

Use one short paragraph, normally one or two sentences. Say what the reader can rely on and name only the missing evidence that would materially change a conclusion. Do not inventory tools or write `Salesforce, Jira, Glean, email/calendar, and production-code search were refreshed`. Prefer: `Trust the revenue and delivery facts. Treat the customer-value story as early until we have a current measured outcome.`

If every required source family was refreshed and the core booked-revenue, target, gap, attainment, pace, qualified-pipeline, bundled-amount, and coverage metrics are available, set `data_status` to `complete`. Missing prior snapshots, early-access customer counts or outcome baselines, target-owner history, and proof that a change is live for customers are claim-scoped limitations: keep them in `snapshot.unknowns` and narrow the affected conclusion instead of calling the whole report incomplete.

Use `data_status: incomplete` only when a required headline metric is unavailable despite a healthy source refresh. In that case, say `Data incomplete` and explain the consequence in ordinary language, for example: `We cannot tell whether bookings are ahead or behind plan because the current Agentic target was not available.` A missing, failed, or stale required source is a source failure and must follow the failure path rather than producing a normal report. Never use `Data incomplete` as a generic disclaimer or inventory every desirable-but-unavailable field in the email.

### Editorial rules

- Do not display `[Verified fact]`, `[Signal]`, `[Inference]`, or `[Unknown]` labels in the human report. Preserve these distinctions in reasoning and in the structured snapshot.
- Do not create separate human sections for revenue detail, EAP detail, Jira, implementation, working/not working, actions, or source inventories.
- Do not include exhaustive counts, ticket enumerations, workflow mechanics, query descriptions, or raw source lists.
- Round currency for scanning, for example `$429K` and `$4.24M`; use exact values in the snapshot.
- Prefer three strong conclusions over broad coverage. Omit facts that do not alter a conclusion or action.
- Write in direct, calm, conversational language. Use short sentences and concrete verbs. Avoid status-report prose, throat-clearing, repeated caveats, and generic product commentary.
- Translate acronyms on first use: `ACV` becomes `annual contract value`, `EAP` becomes `early-access program`, `GA` becomes `generally available`, and `DTMF` becomes `phone-keypad input`. If the acronym is not needed again, omit it entirely.
- Do not use phrases such as `commercial health`, `conversion-constrained`, `funnel quality`, `operating view`, `evidence chain`, `proof-of-value contract`, `rollout trust`, `customer exposure`, or `production exposure`. Say what happened in everyday words.
- Prefer `simple definition of success` over `proof-of-value contract`, `shared view` over `operating view`, `signals showing what happened` over `telemetry`, `real customers can use it` over `customer exposure`, and `safely undo the rollout` over `rollback state`.
- No sentence may contain more than two unexplained acronyms.
- Every material claim still needs an inline source link. A compact `Sources` link group may appear in `What to trust` when one link supports several claims.
- Include the workflow run link unobtrusively in `What to trust` for troubleshooting.

## Email behavior

Prepare the report for `amit.ayre@dialpad.com` with subject:

`Daily Agentic Business Pulse — YYYY-MM-DD`

The only permitted recipient is `amit.ayre@dialpad.com`, with subject `Daily Agentic Business Pulse — YYYY-MM-DD`. The intended send time is 09:00 IST daily. The approved GitHub relay validates, formats, persists, and sends the report; the Glean agent creates the source-linked draft and machine-readable snapshot. Never add another recipient, send directly around the relay, or claim delivery without a successful provider result.

## Continuity

Save a dated report and a compact structured snapshot under `/home/user/output/agentic_business_pulse/`. Preserve the previous snapshot so the next run can identify movement. Do not store customer secrets, credentials, raw payloads, or sensitive transcript content. Store links, aggregates, ticket IDs, account names only when permitted, and short redacted summaries.

## Designer-operator layers

These are analytical lenses for an Agentic built-process designer. Use them to decide the three most important conclusions; do not turn them into additional email sections or a checklist dump.

### 7. Design-to-production fidelity

For each material Agentic flow in design, development, code review, or rollout, compare the intended experience with production reality. Track:

- Customer-visible promise versus actual supported behavior.
- Production APIs and gates reused versus new assumptions.
- Empty, loading, success, failure, retry, propagation-delay, rollback, and post-create states.
- Telemetry for each meaningful step and whether it avoids credentials, secrets, customer payloads, and raw tool arguments.
- Accessibility, content, localization, and responsive-layout readiness.
- Design source, FE/BE/QA/security reviewers, acceptance criteria, and named owner.
- Whether a prototype, EAP, controlled cohort, or production claim is being overstated.

Flag `Design-ready`, `Build-ready`, `Pilot-ready`, `Production-ready`, and `Evidence-missing` separately. Do not call a flow self-serve if a hidden managed dependency remains.

### 8. Customer journey and handoff integrity

Trace one customer outcome across Sales/SE, Professional Services/SA, FDE, and Customer Success. For active opportunities and EAP accounts, check:

- Original business goal and measurable success criteria.
- Customer IT and business stakeholders engaged.
- Use cases validated on real customer scenarios.
- Architecture, build-versus-configure decisions, dependencies, and known limitations.
- Handoff completeness and whether decisions survived into implementation.
- Scope changes, unresolved assumptions, and risks/decisions/actions/issues.
- Post-launch owner, health signal, value proof, and next expansion candidate.

Call out `handoff breakage` when the next team has to rediscover context or when a customer is handed a status update instead of a usable health and outcome record.

### 9. Agentic activation funnel

Track the funnel for the relevant product or cohort, not just total onboarding:

`Invited → Started → Understood the use case → Connected a system → Created an action/tool → Tested → Published → Executed in an agent → Reused → Expanded`

For each step, capture conversion, time spent, abandonment reason, support/FDE intervention, and the strongest customer evidence. Pay special attention to the first meaningful outcome and repeated use.

For Connector work, separate the technical lifecycle from the business lifecycle. A successful connector publish is not customer value until an agent uses it to complete a meaningful job.

### 10. Outcome and measurement readiness

For every EAP, customer pilot, or major product claim, answer:

- What baseline existed before deployment?
- What exact outcome is being measured?
- Is the definition governed and stable?
- Is instrumentation complete enough to trust the result?
- Can the customer see the evidence?
- Is cost or ROI measured, estimated, or unknown?
- What would cause the customer to continue, expand, or stop?

Track data-coverage gaps, metric-definition conflicts, and manual workarounds as product risks—not analytics footnotes.

### 11. Customer evidence matrix

Organize evidence by persona:

- Business sponsor: value, risk, economic case, executive proof.
- Technical admin: setup clarity, auth, data mapping, debugging, control.
- Agent designer/operator: authoring, testing, observability, iteration.
- End customer or caller: resolution, trust, handoff quality, effort.
- SE/PS/FDE/CS: scoping, implementation, support load, handoff, expansion.

For each recurring issue, record frequency, severity, source, affected persona, affected stage, and the smallest product/process change that could remove it. Distinguish one loud anecdote from a repeated pattern.

### 12. Decision and dependency queue

Maintain a short queue of unresolved decisions that are slowing design or delivery. For each item, capture:

- Decision required.
- Why it matters now.
- Options and trade-offs.
- Decision owner.
- Date needed.
- Downstream teams or customer commitments affected.
- Reversibility if the decision is wrong.

Separate `blocked by decision`, `blocked by dependency`, `blocked by evidence`, and `blocked by capacity`. Do not turn every open question into a Jira ticket.

### 13. Daily design moves for Amit

End the report with up to three recommended designer-led actions for the next working day:

1. One customer or field signal to validate.
2. One product/process decision to force or clarify.
3. One artifact, flow, or handoff to improve.

Each action must name the expected business effect: faster technical win, less FDE effort, higher activation, better agent outcome, lower support risk, stronger proof of value, or expansion readiness.

### 14. Contradiction checks

Actively look for mismatches such as:

- Sales positioning says self-serve while Jira shows repeated FDE intervention.
- A feature is described as shipped while telemetry or customer exposure is absent.
- A connector succeeds technically but no customer workflow uses it.
- A customer reports value while the official metric definition cannot reproduce it.
- A pipeline opportunity is labeled Agentic but has little or no Agentic-specific ACV.
- A design review approves a flow whose production API, failure behavior, or rollback path is unknown.

Surface the contradiction plainly and recommend the smallest evidence-gathering action.

### 15. Weekly synthesis mode

On the final run of each workweek, add:

- What changed materially this week.
- Which leading indicators improved or deteriorated.
- The top three repeated customer problems.
- The biggest design-to-production risk.
- One thing to stop doing.
- One thing to double down on.
- The single most important decision for the following week.

### 16. Production-code ground truth

Use production-code search for implementation questions, decision logic, schemas, feature flags, event names, routing, permissions, and runtime behavior. Do not rely on Jira or design documentation when the question is how the system actually behaves.

For each important flow, trace as far as evidence allows:

`UI state → route/guard → client/API → backend/service → registry/runtime → analytics event → test coverage`

Search for the concrete identifiers named in current work, such as feature flags, canonical IDs, lifecycle states, propagation events, authentication boundaries, action/tool schemas, and billing/usage keys. Prefer implementation and test evidence over comments or mock data.

Report these separately:

- `Implemented in code` — the behavior exists in a real application/service path.
- `Covered by tests` — unit, integration, end-to-end, or contract coverage exists.
- `Flagged or gated` — the behavior is behind the expected feature, route, license, admin, or company gate.
- `Instrumented` — the relevant success, failure, latency, propagation, or usage events are emitted.
- `Deployed` — release, branch, environment, or launch evidence confirms exposure.
- `Customer-exposed` — an EAP, design partner, or production cohort can actually use it.

Never collapse these into a single `shipped` label. Code existence is not proof of deployment, and deployment is not proof of customer exposure.

### 17. Code-to-product drift checks

Compare code evidence with design, Jira, and customer evidence. Flag:

- A documented flow with no matching production route, API, or event.
- A code path that exists only as a prototype, mock, fixture, test helper, or local preview.
- A feature flag or permission that prevents the documented audience from reaching the flow.
- A UI state with no backend behavior, failure handling, rollback, or observability.
- A backend capability that is not discoverable or executable through the intended product surface.
- Tests that validate shape or status code but not the customer outcome.
- Analytics events that omit the identity, propagation time, failure surface, or outcome needed for diagnosis.
- Sensitive credentials, auth codes, headers, tool arguments, raw responses, or customer payloads appearing in logs or analytics.

For each drift finding, identify the smallest next check: inspect a specific file/path, run or locate a test, verify a flag, check a release artifact, or validate an event in telemetry.

### 18. Implementation-aware synthesis

When code evidence materially changes a commercial, customer, or design conclusion, fold it into the relevant `Product` insight under `The story`. State the decisive distinction in plain language, such as “the code exists, but we cannot yet prove that real customers can use it.” Keep the full status breakdown in the structured snapshot.

If code search returns no authoritative result, record `Code evidence unavailable` in the snapshot and do not infer implementation status from documentation. If search results are only prototypes, mocks, or tests, label them accordingly and mention them in the email only when they correct a material misconception.

## Quality bar

Be candid and decisive. Lead with the answer. The human email must be understandable in under three minutes. Do not pad it with generic product updates, evidence labels, source mechanics, or exhaustive issue detail. Do not treat prototypes, pipeline, plans, or anecdotes as shipped revenue. Surface contradictions rather than smoothing them over. Mention a missing item in `What to trust` only when it changes a headline conclusion or decision; otherwise leave it in `snapshot.unknowns`.
