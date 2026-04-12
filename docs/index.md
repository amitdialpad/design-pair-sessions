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

### Week of 6–12 Apr 2026

#### What actually changed
The AI summarize pill now morphs between states and has a share button. Pass summaries to teammates without leaving the tool.

Billing data got a real upgrade. `billingPlanUsage` is gone. Usage now reflects an actual date window instead of a frozen snapshot, so you're seeing accurate numbers.

The licenses/SKU data layer is in place and time-filtered. Pull what you need without stale data getting in the way.

Contact center views navigation is scaffolded out in v1 and v2. The foundational structure exists. If you're building on top of this, talk to Josh first.

Credits and usage billing page is redesigned. v3 layout is cleaner and easier to read.

#### The bigger shift
Billing and usage data across Beacon is getting more precise. The shift is away from snapshots and toward actual time windows. This matters for any design that relies on accurate usage reporting.

#### Where things are still messy
Contact center views navigation is still foundational. The components exist but the next phase hasn't started yet.

#### What's coming next
More work on the contact center views navigation likely comes next. The scaffold is ready for it.

#### Try this
If you're building anything with billing or usage data, grab the new time-filtered `billingPlanUsage` layer and test it against a specific date range. You'll see the difference immediately compared to the old snapshot approach.

#### Quick notes
- Email HTML in the docs got fixed for proper table layout
- Design skill ecosystem is reorganized around advisory skills
- The summarize pill now has better visual transitions between states

#### One thing to remember
Billing data now reflects real time windows, not snapshots, so designs that depend on usage reporting are more accurate.

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
