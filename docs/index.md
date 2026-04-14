# Design with Beacon

A living guide to building with AI at Dialpad. The workflow, the toolkit, and what's changing each week.

New here? Start with [The process](/process), then explore the [Beacon toolkit](/toolkit). The [Pair sessions](/sessions/session-1) are there when you're ready to work through it with someone.

## What's new in Beacon

Auto-synced from [beacon-app releases](https://github.com/dialpad/beacon-app/releases). Toolkit page reflects these changes.

<!-- BEACON_RELEASES_START -->

**[Beacon v2026.4.29](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.29) — 12 April 2026**

Feed area now reclaims space when you collapse the right panel. The layout is more efficient and gives you more room to work with your components when you don't need the side panel open.

---

**[Beacon v2026.4.28](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.28) — 12 April 2026**

Fixed star icon appearing incorrectly on channels within system sidebar groups. The icon now only shows where it should.

---

**[Beacon v2026.4.27](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.27) — 11 April 2026**

Dialpad AI summarize pill now includes morphing state animations and a share action. The pill smoothly transitions between states as it processes, and you can now share summaries directly from the component.

---

**[Beacon v2026.4.26](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.26) — 11 April 2026**

New license and SKU entities in the data layer, plus time-filtered usage queries replacing the old billing plan usage model. The design skill ecosystem has been restructured into advisory skills for better organization. Ask Josh if you're working on billing or licensing features and want the details on the new schema.

<!-- BEACON_RELEASES_END -->

## Beacon Brief

Every Monday. The week's Beacon changes, in plain English.

<!-- BEACON_BRIEF_START -->

### Week of 6–12 Apr 2026

#### What actually changed

The AI summarize pill got morphing states and a share button. It now transitions smoothly between states and lets you send summaries directly to teammates without extra steps.

Billing data got a real overhaul. `billingPlanUsage` is gone. Usage now shows an actual date window instead of a frozen snapshot, so you're looking at real time-filtered data. The Credits & usage billing page redesigned to v3 with better organization.

Contact center views navigation scaffold shipped in v1 and v2. The foundational structure is there for browsing and moving between views. Components are ready. Talk to Josh if you're building on top of this.

Design skill ecosystem got restructured into advisory skills for clearer organization.

#### The bigger shift

Billing and usage tooling is moving toward real-time, scoped data instead of static snapshots. That surfaces better information for decision-making.

#### Where things are still messy

The contact center views scaffold is foundational only. Navigation works. UI is there. But there's still work ahead on what actually lives in those views.

#### What's coming next

The contact center views will start filling in with actual content and workflows. Billing pages will probably see more refinement based on what people actually need to see.

#### Try this

Grab the new summarize pill in v2026.4.27 and test the morphing states. Try sharing a summary to a teammate. It's faster than copy-paste and shows where Claude Code integration is heading.

#### Quick notes

- `billingPlanUsage` is deprecated. Switch to time-filtered usage calls if you have prototypes using the old data.
- Contact center navigation scaffold lives in v2026.4.22. Reach out to Josh before you build on it.
- Design skills ecosystem is reorganized. Check your current advisory skill references if you use them in prototypes.

#### One thing to remember

Real data windows beat snapshots. Push for time-filtered, scoped data in your prototypes instead of static views.

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

**[Preparing your security program for AI-accelerated offense](https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense)**<br><small>Apr 10, 2026</small>

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

**[Harnessing Claude’s intelligence](https://claude.com/blog/harnessing-claudes-intelligence)**<br><small>Apr 2, 2026</small>

Three patterns for building on the Claude Platform that keep pace with Claude's evolving intelligence while balancing latency and cost.

:::

*Updated April 13, 2026*
<!-- CLAUDE_FEED_END -->
