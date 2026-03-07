# Project IRL

How a real design project ran from January to March 2026. This was built in Design Studio before Beacon's commands existed. The commands referenced in the annotations show where they would have helped.

This is here so you can see what the full arc looks like: the wrong turns, the pivots, the specific feedback from specific people, and the moments where the design process and engineering tools intersect. Read it once to get the picture.

## Exploring

> **Jan 22** — First prototype lands. 4-tab layout, 3,200 lines, Overview tab already broken. Built with Claude from day 1. Co-authored with Claude Sonnet 4.5.

The project starts from two PRDs and competitive research (49 SaaS billing UIs and the Twilio console). But Amit doesn't start in Figma. He builds to find out what the product should be. The first code is a sketch, not a deliverable.

> **Jan 29–30** — Analytics deep dive. Three commits in two days. Apple-style multi-state widgets, D3 area charts, and a ChatGPT-style AI assistant with conversation management, localStorage persistence, and "pin chart to dashboard" functionality.

Still exploring. Testing whether an analytics dashboard is the right direction. It felt right at the time.

## The pivot

> **Feb 4** — The biggest day of the project. Five commits.

What happened:
- The 4-tab layout gets killed. Single scrollable page.
- The per-service budget model gets killed. The initial design showed services with pre-allocated sub-budgets. The real system uses shared wallet pools with draw-down priority. Building the wrong thing surfaced this.
- Company/office scope switching gets added.
- The analytics dashboard from Jan 30 gets hidden. Not deleted, just hidden.

Four wrong assumptions discovered in one day. All by building and then learning from the result.

**Where commands would have helped:** After this pivot, the problem is finally clear. `/shaping` here would formalize the real requirements (shared wallet pools, company vs. office views, usage history as primary view) so the next round of building has boundaries. `/breadboarding` would map how wallet cards, plan usage, and usage history connect before building them.

## Building with direction

> **Feb 14** — The design doc gets written. 23 days after the first prototype.

Six pages covering problem statement, target users, mental model, 7 design decisions with rationale, 16 usage types with CSR data mapping, component architecture, and success criteria. It includes direct quotes from Cecilia about what CSR data is available and how fax line allotments work.

The design doc captures decisions already made through building. It didn't plan them.

Same day: WalletCard, PlanUsageBalanceTable, WalletSourceBadge, and DeductionPathVisual all ship. PR #233 opens. A deployment bug surfaces (components committed in wrong order).

**Where commands would have helped:** Each component is a vertical slice. `/feature-dev` for the wallet card, then `/feature-dev` for the plan usage table. Each gets its own PR with a demo.

> **Feb 17** — Hierarchical plan usage table with tree-line connectors. Settings tab becomes AddCredits purchase flow (another direction shift mid-build). Three bug fix commits.

> **Feb 19–20** — "Savings" column added. Dennis's feedback: drawdown priority indicators. When services exceed plan limits, child service names turn red with a tooltip showing which wallet is now being charged.

Feedback from a specific person changed a specific interaction. The design doc updates simultaneously.

## The feedback round

> **Feb 26** — The single most information-dense commit in the project. Three reviewers named:

**Ceci** (engineer): Consolidate A2P Outbound SMS into SMS/MMS (single allotment). Flattened the messaging hierarchy from parent/child to a single row.

**Abby**: Replace "Savings" column with "Rate" showing per-unit rates. Replace "Credit Commit Savings" with neutral "Rate Details comparison." Rename "Overflow Safety Net" to "Dialpad Credits." A naming/framing pivot: Abby pushed back on the savings framing (which implies the company is saving money) toward neutral rate transparency.

**Josh**: Infinite scroll with DtSkeleton loading rows instead of pagination. Required generating 150 more transactions.

All three changes implemented in one commit.

**Where commands would have helped:** This is the moment between designing and shipping. `/pr-prep` would run the 6-wave quality check (including the accessibility audit and Dialtone compliance check). `/pr-create` would open the PR with a preview link.

## New sub-problem

> **Feb 27** — Export CSV exploration begins. Five commits in one day.

Transaction data extracted into its own file. Company/office views unified. The Usage by Office matrix removed (it had lived for 23 days). Export CSV goes from a plain button to a DtSplitButton with a full takeover preview modal. AddCredits gets a responsive side-by-side layout.

**Where commands would have helped:** The export flow is a new design problem. `/shaping` again, with different requirements (recipients, recurring reports, custom modals).

> **Mar 2–4** — Josh and Uli feedback on export. Recipients with DtChip (non-removable default email). Recurring report as a separate modal. Multiple Dialtone component gotchas discovered and documented.

The recurring report interaction alone went through three designs: toggle, post-export CTA, text link.

## In parallel: the data question

> **Feb 22 – Mar 5** — Snoopy runs alongside the prototype work.

Amit built a separate tool that cross-referenced Amplitude behavioral data + firespotter source code + Jira tickets to produce design-aware daily reports. It went through 5 phases, ending with a fully automated pipeline that spoke MCP protocol directly to Amplitude.

It got paused because the data was too thin. Billing events were broken or missing. 83% of purchases were completely untracked. The reports faithfully described incomplete data.

The resume trigger was explicitly tied to the prototype: finish the prototype, then define what events to track based on the design (events follow design, not the other way around), then instrument, then Snoopy becomes valuable.

## What the story shows

**Building is designing.** The wallet model, the tab structure, the analytics direction, the savings framing, all discovered through building, not planning.

**The design doc came after, not before.** It captured 23 days of decisions, pivots, and conversations. It was informed by reality, not theory.

**Feedback was specific.** Named people, named opinions, named UI elements. Not "address feedback" but "Abby said replace Savings with Rate because the savings framing implies the company is saving money."

**Nothing was linear.** Analytics built twice. A feature lived 23 days then died. Export went through 4 iterations. The wallet model was fundamentally wrong until the pivot.

**Commands would have helped at specific moments.** Not as a replacement for the messy design process, but as formalization points: writing down what you know after a pivot (`/shaping`), mapping the pieces before building them (`/breadboarding`), quality-checking before sharing (`/pr-prep`).
