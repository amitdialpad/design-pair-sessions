---
name: Daily Agentic Business Pulse
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

Use the current date in the user's preferred timezone. Compare against the most recent successful report and the prior business day or seven-day baseline, depending on the metric. State the comparison window explicitly.

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

Use this structure:

# Daily Agentic Business Pulse — YYYY-MM-DD

## Executive readout

Give a direct green/yellow/red assessment of commercial progress, with one sentence on why.

## Revenue scoreboard

Include current target, booked revenue, attainment, remaining gap, pace required, pipeline by quarter/category, coverage, and the biggest changes since the previous report. Label every number with its date and source.

## Customer and EAP reality

List the strongest customer signals, current onboarding movement, EAP performance, and the top friction themes. Use exact customer language only when the source is verbatim; otherwise paraphrase.

## Jira and delivery risk

List the highest-impact new, aging, resolved, and blocked issues. Include owner and customer/revenue impact.

## Working / not working

Use two short lists. Tie each item to evidence.

## Decisions and actions

Give up to five actions with owner, urgency, and expected business impact. Do not create Jira/Salesforce tasks unless explicitly requested.

## Sources and confidence

Link every material claim to its source. Add a short note for missing data, scope changes, or conflicting metrics.

## Email behavior

Prepare the report for `amit.ayre@dialpad.com` with subject:

`Daily Agentic Business Pulse — YYYY-MM-DD`

The intended recipient is `amit.ayre@dialpad.com`, with subject `Daily Agentic Business Pulse — YYYY-MM-DD`. The intended send time is 09:00 IST daily. This environment currently has no recurring scheduler or outbound email action, so do not claim that a daily email has been configured or delivered. When invoked, generate the source-linked report and a send-ready `.email` artifact. If a future runtime provides an approved scheduler and outbound email action, send only after the report is complete and source-linked; never claim delivery without a successful send result.

## Continuity

Save a dated report and a compact structured snapshot under `/home/user/output/agentic_business_pulse/`. Preserve the previous snapshot so the next run can identify movement. Do not store customer secrets, credentials, raw payloads, or sensitive transcript content. Store links, aggregates, ticket IDs, account names only when permitted, and short redacted summaries.

## Designer-operator layers

These are the additional lenses for an Agentic built-process designer. They should appear in every report when evidence exists, even if revenue is unchanged.

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

### 18. Implementation-aware daily report section

Add this section when code evidence was checked:

## Implementation reality

- What the code confirms.
- What tests confirm.
- What remains behind a flag or gate.
- What is instrumented or uninstrumented.
- What is deployed or customer-exposed versus merely present in a repository.
- The most important code-to-product drift.

If code search returns no authoritative result, say `Code evidence unavailable` and do not infer implementation status from documentation. If search results are only prototypes, mocks, or tests, label them accordingly.

## Quality bar

Be candid and operational. Lead with the answer. Do not pad the report with generic product updates. Do not treat prototypes, pipeline, plans, or anecdotes as shipped revenue. Surface contradictions rather than smoothing them over. If current data cannot answer a question, say exactly what is missing and who owns it.
