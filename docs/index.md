# Design with Beacon

A living guide to building with AI at Dialpad. The workflow, the toolkit, and what's changing each week.

New here? Start with [The process](/process), then explore the [Beacon toolkit](/toolkit). The [Pair sessions](/sessions/session-1) are there when you're ready to work through it with someone.

## What's new in Beacon

Auto-synced from [beacon-app releases](https://github.com/dialpad/beacon-app/releases). Toolkit page reflects these changes.

<!-- BEACON_RELEASES_START -->

**[Beacon v2026.4.27](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.27) — 11 April 2026**

New Dialpad AI summarize pill with morphing states and share action. The pill now smoothly transitions between states and includes a share button so you can easily pass summaries to teammates.

---

**[Beacon v2026.4.26](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.26) — 11 April 2026**

New licenses/SKU data layer in Beacon. `billingPlanUsage` replaced with time-filtered usage — so usage data now reflects a real date window, not a snapshot.

Design skill ecosystem restructured into advisory skills for better organization and clarity.

---

**[Beacon v2026.4.22](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.22) — 9 April 2026**

New contact center views navigation scaffold (v1 + v2): foundational structure is in place for browsing and navigating between contact center views. UI components are ready for the next phase of development. Reach out to Josh if you're planning to build on top of this.

---

**[Beacon v2026.4.18](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.18) — 7 April 2026**

Credits & usage billing page redesigned. The new v3 layout gives you a clearer view of billing data with improved organization and readability.

<!-- BEACON_RELEASES_END -->

## Beacon Brief

Every Monday. The week's Beacon changes, in plain English.

<!-- BEACON_BRIEF_START -->

### Week of 7–13 Apr 2026

#### What actually changed

`/feature-dev` and `/feature-start` are gone. They've been merged into one: `/feature-team`. Same job, cleaner name. If you've been using either, update your muscle memory. Two new ones also landed quietly: `/jira-done` (marks a ticket done without leaving the terminal) and `/team-cleanup` (tidies up after a build). Also: three new advisory skills: `type-design`, `motion-design`, `interaction-design`. Think of them like asking a specialist to look over your shoulder. Run one after you build something and it'll flag where the craft could be sharper.

#### The bigger shift

Beacon is a prototyping tool. Treat it like one that matters. The data in it should behave like real data. When you catch yourself faking a scenario just to test something, stop. Use a proper scenario instead. If the right one doesn't exist yet, that's a gap worth raising. Get the system design right first, then realistic data, then reusable scenarios, then automation. UI is last. You verify the structure is right through the UI. You don't start there.

#### Where things are still messy

Not every flow has a scenario that covers it yet. The scenario system is there, it's just not complete. So you'll probably hit gaps. The gap itself is useful information. It means something real hasn't been modelled yet.

#### What's coming next

The Contact Center schema shipped: contact centers, memberships, operator skills, operating hour profiles. The data layer is built. The UI layer is next. If any of your upcoming work touches contact center flows, check in before you start designing. The structure is fresh.

#### Try this

Run `type-design`, `motion-design`, or `interaction-design` after your next build. Pick whichever feels most relevant to what you made. It takes 30 seconds and you'll almost always get at least one thing worth acting on.

#### Quick notes

- The homepage now auto-syncs Beacon releases. No need to check GitHub manually
- If you're testing something in Beacon and it only looks right with 10 records, try it with 300. Small and large environments behave differently
- For design principle checks: you can ask Claude to run the `dialpad-design` agent any time, not just at the PR stage

#### One thing to remember

When something in Beacon feels fake or weirdly simple, that's the thing telling you the data model needs fixing. It's not a small thing to clean up later. It's the work.

---

### Week of 6–12 Apr 2026

#### What actually changed
Josh shipped a new AI summarize pill that morphs between states and includes a share button. You can now pass summaries directly to teammates instead of copying them manually.

The billing data layer got a real upgrade. `billingPlanUsage` is gone. Usage now reflects an actual date window instead of just a snapshot, which means the numbers you're looking at actually mean something.

Credits & usage billing page went to v3. The layout is clearer and the data sits better on the page.

Contact center views navigation scaffold landed in v1 and v2 flavors. It's the foundation for browsing between views. If you're planning to build on top of this, talk to Josh first.

Design skill ecosystem got reorganized into advisory skills for better structure.

#### The bigger shift
The pattern here is about making data more honest and navigation more intentional. Snapshots became time windows. Navigation got scaffolding before features got built on top. The summarize pill now invites collaboration instead of just sitting there.

#### Where things are still messy
Contact center views are foundational right now. They're ready for the next phase but that phase hasn't started yet.

#### What's coming next
The contact center navigation scaffold suggests there's more view browsing and switching coming. The billing redesign probably means more focus on how usage data gets presented across the product.

#### Try this
If you're working with usage data in a prototype, switch to the new time-filtered billing layer instead of the old snapshot. You'll see how much clearer it is when the data actually represents a date range.

#### Quick notes
- Summarize pill now has a share action. Test it with your teammates.
- Contact center navigation v1 and v2 are both available. Pick one based on your use case.
- Email delivery for this newsletter just shipped, so you should see it land in your inbox next week.

#### One thing to remember
Data windows beat snapshots. Always know what time period you're actually looking at.

<!-- BEACON_BRIEF_END -->

## What's new in Claude

Latest announcements from Anthropic.

<!-- CLAUDE_FEED_START -->
**[Multi-agent coordination patterns: Five approaches and when to use them](https://claude.com/blog/multi-agent-coordination-patterns)**<br><small>Apr 10, 2026 · Agents</small>

Five multi-agent coordination patterns, their trade-offs, and when to evolve from one to another.

---

**[Seeing like an agent: how we design tools in Claude Code](https://claude.com/blog/seeing-like-an-agent)**<br><small>Apr 10, 2026 · Claude Code</small>

Building Claude Code: How Anthropic designs and refines AI agent tools like AskUserQuestion and Task tool. The key is progressive disclosure and learning to "see like an agent" to maximize effectiveness.

---

**[Preparing your security program for AI-accelerated offense](https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense)**<br><small>Apr 10, 2026 · Agents</small>

We share our initial set of recommendations to shore up your defenses based on our own findings and security practices.

---

**[Making Claude Cowork ready for enterprise](https://claude.com/blog/cowork-for-enterprise)**<br><small>Apr 9, 2026 · Product announcements</small>

Claude Cowork is now generally available on all paid plans. Within companies, Claude Cowork has become a key part of how teams operate: handling tasks, drafting project deliverables, and keeping teams up to date.

:::details View past updates

**[The advisor strategy: Give agents an intelligence boost](https://claude.com/blog/the-advisor-strategy)**<br><small>Apr 9, 2026 · Product announcements</small>

Pair Opus as an advisor with Sonnet or Haiku as an executor, and get Opus-level intelligence in your agents at a fraction of the cost.

---

**[How Carta Healthcare gets AI to reason like a clinical abstractor](https://claude.com/blog/carta-healthcare-clinical-abstractor)**<br><small>Apr 8, 2026 · Enterprise AI</small>

How Carta Healthcare used Claude and context engineering to build Lighthouse, a clinical abstraction platform reaching 99% accuracy across 22,000 cases a year.

---

**[Claude Managed Agents: get to production 10x faster](https://claude.com/blog/claude-managed-agents)**<br><small>Apr 8, 2026</small>

Introducing Claude Managed Agents, a suite of composable APIs for building and deploying cloud-hosted agents at scale.

---

**[How and when to use subagents in Claude Code](https://claude.com/blog/subagents-in-claude-code)**<br><small>Apr 7, 2026 · Claude Code</small>

When to delegate research, parallelize tasks, or get a fresh review with Claude Code subagents—and when to stick with the main session.

---

**[Harnessing Claude's intelligence](https://claude.com/blog/harnessing-claudes-intelligence)**<br><small>Apr 2, 2026</small>

Three patterns for building on the Claude Platform that keep pace with Claude's evolving intelligence while balancing latency and cost.

:::

*Updated April 12, 2026*
<!-- CLAUDE_FEED_END -->
