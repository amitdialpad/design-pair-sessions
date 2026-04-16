# Design with Beacon

A living guide to building with AI at Dialpad. The workflow, the toolkit, and what's changing each week.

New here? Start with [The process](/process), then explore the [Beacon toolkit](/toolkit). The [Pair sessions](/sessions/session-1) are there when you're ready to work through it with someone.

## What's new in Beacon

Auto-synced from [beacon-app releases](https://github.com/dialpad/beacon-app/releases). Toolkit page reflects these changes.

<!-- BEACON_RELEASES_START -->

**Canvas AI connects to @dialpad conversations**

Pull real conversation context directly into your design work while you're building. Useful when you want to reference actual user interactions instead of made-up copy.

<span class="release-meta">[v2026.4.38](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.38) · 15 April 2026</span>

---

**Power Dialer campaign context in the callbar**

You'll see which campaign a call belongs to alongside your call details — no more switching tabs to find out.

<span class="release-meta">[v2026.4.35](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.35) · 14 April 2026</span>

---

**Feed gains space when right panel collapses**

The layout reflows properly when you close the right panel, giving you more room to work instead of leaving a gap.

<span class="release-meta">[v2026.4.29](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.29) · 12 April 2026</span>

---

**Star icon fixed in sidebar channel groups**

It was showing on all channels — now only appears on items you've actually favorited.

<span class="release-meta">[v2026.4.28](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.28) · 12 April 2026</span>

---

**AI summary pill gets animated states and a share action**

The pill morphs smoothly as it processes, and you can share summaries directly from the component without leaving the conversation.

<span class="release-meta">[v2026.4.27](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.27) · 11 April 2026</span>

---

**Design skills reorganized; licensing data layer added**

License and SKU entities are now in the data layer, and billing plan usage supports time-based filtering. Ask Josh if you're working on licensing or billing features.

<span class="release-meta">[v2026.4.26](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.26) · 11 April 2026</span>

---

**Inbox thread replies and panel open behavior fixed**

New reply indicators display correctly, and clicking into a thread opens the panel reliably instead of sometimes doing nothing.

<span class="release-meta">[v2026.4.24](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.24) · 9 April 2026</span>

---

**Contact Center navigation scaffold live**

The foundational nav structure for v1 and v2 Contact Center views is in place. UI work comes next — reach out to Josh if you're planning to work in this area.

<span class="release-meta">[v2026.4.22](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.22) · 9 April 2026</span>

---

:::details View older releases

**Credits & usage billing page redesigned**

Cleaner layout with better visibility into remaining credits, usage breakdown, and spending at a glance.

<span class="release-meta">[v2026.4.18](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.18) · 7 April 2026</span>

---

**Hovercard phone numbers fixed; PR prep improved**

Numbers display correctly in hovercards. The PR prep workflow was also refined to focus on outcomes, making reviews smoother.

<span class="release-meta">[v2026.4.17](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.17) · 7 April 2026</span>

:::

<!-- BEACON_RELEASES_END -->

## Beacon Brief

Every Monday. The week's Beacon changes, in plain English.

<!-- BEACON_BRIEF_START -->

### Week of 6–12 Apr 2026

Josh shipped three releases this week, and they're all about getting you more space and better context while you work. The callbar now shows which Power Dialer campaign a call belongs to, so you don't have to hunt through panels to figure out what you're looking at. The feed area expands when you collapse the right panel, giving you breathing room to actually see your designs. And we fixed a bug where star icons were showing up next to channels they shouldn't have been. None of these are earth-shattering, but together they make Beacon feel a bit less cluttered and a bit more aware of what you're trying to do.

#### What actually changed

Power Dialer campaign context displays in the callbar. Calls now show which campaign they belong to without requiring you to open other panels.

The feed area now expands to fill available horizontal space when you collapse the right panel. You get actual room to work instead of a cramped center column.

Fixed star icons appearing next to channels in system sidebar groups. Only favorited items should show the star now.

#### The bigger shift

The pattern here is removing friction between you and your work. Less clicking to find context. More space to see what you're designing. Fewer visual false positives that make you second-guess what you're seeing.

#### Where things are still messy

Nothing reported as actively broken this week. The docs site had a fix for heading navigation that was causing false skips, but that's backend stuff.

#### What's coming next

Probably more panel and layout refinements. The expansion of the feed area suggests Josh is thinking about how designers actually use the workspace and where their attention needs to go.

#### Try this

Collapse your right panel right now and watch the feed expand. If you're working on anything with a lot of detail, you'll probably notice the difference immediately. It's a small thing that makes a real difference when you're trying to see the whole picture.

#### Quick notes

- v2026.4.35 ships campaign context in callbar
- v2026.4.29 fixes feed area expansion on right panel collapse
- v2026.4.28 removes incorrect star icons from channel lists

#### One thing to remember

Less hunting for context means more time actually designing.

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
