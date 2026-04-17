# Design with Beacon

A living guide to building with AI at Dialpad. The workflow, the toolkit, and what's changing each week.

New here? Start with [The process](/process), then explore the [Beacon toolkit](/toolkit). The [Pair sessions](/sessions/session-1) are there when you're ready to work through it with someone.

## What's new in Beacon

Auto-synced from [beacon-app releases](https://github.com/dialpad/beacon-app/releases). Toolkit page reflects these changes.

<!-- BEACON_RELEASES_START -->

**AI Assistant feature flags consolidated in devtools**

Feature flag controls for AI Assistant are now unified in a single devtools panel instead of scattered across multiple locations. This makes it easier to toggle AI preferences and test different feature combinations without hunting through settings.

<span class="release-meta">[v2026.4.40](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.40) · 16 April 2026</span>

---

**Canvas AI conversation repository and Dialpad integration**

Beacon now connects canvas conversations to Dialpad's AI service, enabling designers to view and interact with AI-assisted conversations directly within the canvas workspace. New hooks and components support conversation persistence and panel management. Reach out to Josh if you're exploring how to surface AI insights in your designs.

<span class="release-meta">[v2026.4.38](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.38) · 15 April 2026</span>

---

**Inbox adopts conversation index pipeline**

The inbox views and data handling now use the conversation index pipeline for more consistent message retrieval and filtering across InboxList, InboxDetailFeed, and InboxMessageDetails. This refactor improves how inbox content is loaded and paginated behind the scenes. If you notice any changes in how messages appear or load, let Josh know.

<span class="release-meta">[v2026.4.37](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.37) · 15 April 2026</span>

---

**Power Dialer campaign context added to callbar**

The callbar now displays Power Dialer campaign information during active calls, giving you immediate context about which campaign a call belongs to. Check the ActiveCallOverlay and CallbarOverlays components to see the new campaign details in action.

<span class="release-meta">[v2026.4.35](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.35) · 14 April 2026</span>

---

**Star icon removed from system sidebar channel groups**

The favorite star that was incorrectly appearing next to channels in system sidebar groups has been fixed. This cleans up the visual hierarchy in your left sidebar when browsing channel organization.

<span class="release-meta">[v2026.4.28](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.28) · 12 April 2026</span>

---

**AI summary pill gains morphing states and share action**

The SummarizePill component in the message feed now supports animated state transitions and includes a share action. This gives designers a new interactive pattern for displaying AI-generated summaries in conversations.

<span class="release-meta">[v2026.4.27](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.27) · 11 April 2026</span>

---

**Inbox thread replies display and panel opening fixed**

The inbox detail feed now correctly shows reply indicators on threads and properly opens the thread panel when selected. This fixes the interaction behavior designers will see when working with inbox message threads in Beacon.

<span class="release-meta">[v2026.4.24](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.24) · 9 April 2026</span>

---

**Contact Center views navigation scaffold launches**

The left sidebar now supports Contact Center list navigation with new CcList and CcListRow components, alongside updates to sidebar data handling, favorites, groups, and item movement logic. This scaffold enables designers to preview and interact with Contact Center organization in the sidebar. Reach out to Josh if you need details on the feature flag behavior or placeholder states.

<span class="release-meta">[v2026.4.22](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.22) · 9 April 2026</span>

---

:::details View older releases

**Credits and usage billing page redesigned**

The billing section now features a completely rebuilt interface with new components for displaying plan usage, transaction history, wallet management, and credit balances. Designers will see updated layouts, data tables, and modals throughout the billing area. Reach out to Josh if you need details on the new billing component APIs.

<span class="release-meta">[v2026.4.18](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.18) · 7 April 2026</span>

---

**User hovercard phone numbers fixed**

Phone numbers now display correctly in user hovercards. The underlying phone formatting and display logic has been refactored for consistency across the hovercard component.

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
**[Best practices for using Claude Opus 4.7 with Claude Code](https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code)**<br><small>Apr 16, 2026 · Claude Code</small>

Learn how to use recalibrated effort levels, adaptive thinking, and new defaults to optimize your Claude Code setup with Opus 4.7.

---

**[Using Claude Code: session management and 1M context](https://claude.com/blog/using-claude-code-session-management-and-1m-context)**<br><small>Apr 15, 2026 · Claude Code</small>

Learn how to manage context in Claude Code—when to continue, rewind, compact, or clear a session, and how subagents keep parent context clean.

---

**[Introducing routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code)**<br><small>Apr 14, 2026 · Product announcements</small>

Define repeatable routines that work your backlog, review your PRs, and respond to events in the cloud.

---

**[Redesigning Claude Code on desktop for parallel agents](https://claude.com/blog/claude-code-desktop-redesign)**<br><small>Apr 14, 2026</small>

Today, we're releasing a redesign of the Claude Code desktop app, built to help you run more Claude Code tasks at once.

:::details View past updates

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

---

**[The advisor strategy: Give agents an intelligence boost](https://claude.com/blog/the-advisor-strategy)**<br><small>Apr 9, 2026 · Product announcements</small>

Pair Opus as an advisor with Sonnet or Haiku as an executor, and get Opus-level intelligence in your agents at a fraction of the cost.

:::

*Updated April 17, 2026*
<!-- CLAUDE_FEED_END -->
