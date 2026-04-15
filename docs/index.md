# Design with Beacon

A living guide to building with AI at Dialpad. The workflow, the toolkit, and what's changing each week.

New here? Start with [The process](/process), then explore the [Beacon toolkit](/toolkit). The [Pair sessions](/sessions/session-1) are there when you're ready to work through it with someone.

## What's new in Beacon

Auto-synced from [beacon-app releases](https://github.com/dialpad/beacon-app/releases). Toolkit page reflects these changes.

<!-- BEACON_RELEASES_START -->

**[Beacon v2026.4.35](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.35) — 14 April 2026**

Power Dialer campaign context now shows in the callbar. You can see which campaign a call belongs to at a glance without digging into other panels.

---

**[Beacon v2026.4.29](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.29) — 12 April 2026**

Feed area now expands to fill available space when you collapse the right panel, giving you more room to see your design work.

---

**[Beacon v2026.4.28](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.28) — 12 April 2026**

Fixed star icon incorrectly appearing next to channels in system sidebar groups. They should only show for favorited items.

<!-- BEACON_RELEASES_END -->

## Beacon Brief

Every Monday. The week's Beacon changes, in plain English.

<!-- BEACON_BRIEF_START -->

### Week of 6–12 Apr 2026 [prev]

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
**[Introducing routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code)**<br><small>Apr 14, 2026 · Product announcements</small>

Define repeatable routines that work your backlog, review your PRs, and respond to events in the cloud.

---

**[Redesigning Claude Code on desktop for parallel agents](https://claude.com/blog/claude-code-desktop-redesign)**<br><small>Apr 14, 2026</small>

Today, we're releasing a redesign of the Claude Code desktop app, built to help you run more Claude Code tasks at once.

---

**[Multi-agent coordination patterns: Five approaches and when to use them](https://claude.com/blog/multi-agent-coordination-patterns)**<br><small>Apr 10, 2026 · Agents</small>

Five multi-agent coordination patterns, their trade-offs, and when to evolve from one to another.

---

**[Seeing like an agent: how we design tools in Claude Code](https://claude.com/blog/seeing-like-an-agent)**<br><small>Apr 10, 2026 · Claude Code</small>

Building Claude Code: How Anthropic designs and refines AI agent tools like AskUserQuestion and Task tool. The key is progressive disclosure and learning to "see like an agent" to maximize effectiveness.

:::details View past updates

**[Preparing your security program for AI-accelerated offense](https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense)**<br><small>Apr 10, 2026</small>

We share our initial set of recommendations to shore up your defenses based on our own findings and security practices.

---

**[Making Claude Cowork ready for enterprise](https://claude.com/blog/cowork-for-enterprise)**<br><small>Apr 9, 2026 · Product announcements</small>

Claude Cowork is now generally available on all paid plans. Within companies, Claude Cowork has become a key part of how teams operate: handling tasks, drafting project deliverables, and keeping teams up to date.

---

**[The advisor strategy: Give agents an intelligence boost](https://claude.com/blog/the-advisor-strategy)**<br><small>Apr 9, 2026 · Product announcements</small>

Pair Opus as an advisor with Sonnet or Haiku as an executor, and get Opus-level intelligence in your agents at a fraction of the cost.

---

**[How Carta Healthcare gets AI to reason like a clinical abstractor](https://claude.com/blog/carta-healthcare-clinical-abstractor)**<br><small>Apr 8, 2026 · Enterprise AI</small>

How Carta Healthcare used Claude and context engineering to build Lighthouse, a clinical abstraction platform reaching 99% accuracy across 22,000 cases a year.

---

**[Claude Managed Agents: get to production 10x faster](https://claude.com/blog/claude-managed-agents)**<br><small>Apr 8, 2026</small>

Introducing Claude Managed Agents, a suite of composable APIs for building and deploying cloud-hosted agents at scale.

:::

*Updated April 15, 2026*
<!-- CLAUDE_FEED_END -->
