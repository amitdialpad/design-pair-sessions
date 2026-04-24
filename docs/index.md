# Design with Beacon

A living guide to building with AI at Dialpad. The workflow, the toolkit, and what's changing each week.

New here? Start with [The process](/process), then explore the [Beacon toolkit](/toolkit). The [Pair sessions](/sessions/session-1) are there when you're ready to work through it with someone.

## What's new in Beacon

Auto-synced from [beacon-app releases](https://github.com/dialpad/beacon-app/releases). Toolkit page reflects these changes.

<!-- BEACON_RELEASES_START -->

**AI Receptionists navigation and views added**

The left sidebar and main navigation now include AI Receptionists as a destination, with new home and detail views in the composer toolbar. Designers can explore the new ReceptionistNavPanel, AiReceptionistView, and AiReceptionistsView components. Reach out to Josh if you need details on the feature flag integration or receptor hooks.

<span class="release-meta">[v2026.4.46](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.46) · 23 April 2026</span>

---

**Preferences and controls migrate to Dialtone**

The Preferences Modal and various control components now use Dialtone primitives instead of custom implementations. This includes updates to BillingControls, CallbarControls, VariantPicker, WindowGradientToggle, and related settings panels. If you notice any behavioral changes in how these controls feel or appear, reach out to Josh.

<span class="release-meta">[v2026.4.45](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.45) · 23 April 2026</span>

---

**AI Assistant feature flags consolidated in devtools panel**

Feature flag controls for AI Assistant have been reorganized into a single devtools panel location, making it easier to manage AI behavior settings while designing. Check the AIAssistantControls and FeatureFlags sections if you need to adjust AI preferences during your workflow.

<span class="release-meta">[v2026.4.40](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.40) · 16 April 2026</span>

---

**Canvas AI conversation integration with Dialpad**

The Canvas view now connects to Dialpad's AI service for managing conversations. You'll see new conversation handling across the left sidebar, message composer, and feed area. Reach out to Josh if you need details on how the new conversation persistence and mention features work.

<span class="release-meta">[v2026.4.38](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.38) · 15 April 2026</span>

---

**Inbox adopts conversation index pipeline**

The Inbox view now uses an updated data pipeline for loading and displaying conversations. This affects how messages load and render in InboxDetailFeed, InboxList, and InboxMessageDetails. If you notice any changes in message ordering, filtering, or pagination behavior, reach out to Josh.

<span class="release-meta">[v2026.4.37](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.37) · 15 April 2026</span>

---

**Power Dialer campaign context added to callbar**

The callbar now displays Power Dialer campaign information directly in ActiveCallOverlay and related callbar components, giving you better visibility into campaign context during calls. Check with Josh if you need details on how this integrates with existing callbar controls and overlays.

<span class="release-meta">[v2026.4.35](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.35) · 14 April 2026</span>

---

**Feed area reclaims space when right panel collapses**

The feed now expands to use available horizontal space when you close the right panel. This gives you more room to work with your design content without manual adjustment.

<span class="release-meta">[v2026.4.29](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.29) · 12 April 2026</span>

---

**Star icon removed from system sidebar channel groups**

The favorite star that was incorrectly appearing next to channels in system sidebar groups has been fixed. This cleans up the visual hierarchy in your left navigation when browsing channel organization.

<span class="release-meta">[v2026.4.28](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.28) · 12 April 2026</span>

---

:::details View older releases

**AI summary pill gets animated states and share**

The SummarizePill component in the feed now supports morphing animations between states and includes a share action. Check FeedMessageList and FeedView to see the pill in context, and reach out to Josh if you need details on the animation behavior.

<span class="release-meta">[v2026.4.27](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.27) · 11 April 2026</span>

---

**Inbox thread replies now display correctly**

The inbox detail feed now shows accurate reply indicators and properly opens thread panels when you interact with messages. This fixes display and interaction issues in the InboxDetailFeed component and underlying data handling.

<span class="release-meta">[v2026.4.24](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.24) · 9 April 2026</span>

---

**Contact Center views navigation scaffold added**

The left sidebar now supports Contact Center list views with new CcList and CcListRow components, plus updated sidebar data hooks to handle CC-specific navigation. Designers can now preview and test CC navigation patterns in the left nav and sidebar preview areas. Reach out to Josh if you need details on the v1 and v2 scaffold implementations.

<span class="release-meta">[v2026.4.22](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.22) · 9 April 2026</span>

---

**Credits & usage billing page redesigned**

The billing page in Beacon now reflects the v3 design with updated layouts and information hierarchy. Check the Credits & Usage section to see the refreshed interface.

<span class="release-meta">[v2026.4.18](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.18) · 7 April 2026</span>

:::

<!-- BEACON_RELEASES_END -->

## Beacon Brief

Every Monday. The week's Beacon changes, in plain English.

<!-- BEACON_BRIEF_START -->

### Week of 13–19 Apr 2026

AI features got more organized this week, and the inbox got a real upgrade under the hood. Josh consolidated all the AI Assistant feature flags into one devtools panel, which means you're not hunting through settings anymore when you want to test different AI behavior. The bigger move was connecting canvas conversations directly to Dialpad's AI service — conversations now persist and you can interact with them right in your workspace. Meanwhile, the inbox switched to a new conversation index pipeline for how it retrieves and filters messages, which should make pagination and loading feel snappier. There's also new stuff for Contact Center navigation in the sidebar, Power Dialer campaign context in the call bar, and a few fixes that clean up visual clutter and interaction bugs.

#### What actually changed

- **AI Assistant feature flags in devtools**: All the toggle controls for AI behavior are now in one panel instead of scattered everywhere.
- **Canvas AI conversation integration**: Conversations now connect to Dialpad's service with persistence and panel management. Check out the new hooks if you're surfacing AI insights in your designs.
- **Inbox conversation index pipeline**: InboxList, InboxDetailFeed, and InboxMessageDetails now use a unified pipeline for retrieving and filtering messages.
- **Power Dialer campaign context in callbar**: ActiveCallOverlay and CallbarOverlays now display which campaign a call belongs to.
- **Contact Center sidebar navigation**: New CcList and CcListRow components let designers preview Contact Center organization in the left sidebar.
- **AI summary pill enhancements**: SummarizePill now has animated state transitions and a share action.
- **Inbox thread display fixes**: Reply indicators now show correctly and thread panels open when you click them.
- **Removed star icon from system sidebar channel groups**: Just a visual cleanup in the left sidebar.

#### The bigger shift

There's a clear momentum toward making AI features more discoverable and usable in the canvas. Feature flags are getting consolidated, conversations are persisting, and new components are shipping to surface AI insights directly in your work. At the same time, inbox and sidebar navigation are getting rebuilt with better data pipelines and scaffolding for larger feature sets like Contact Center.

#### Where things are still messy

The Contact Center sidebar navigation is a scaffold right now, so some behavior depends on feature flags. Josh has notes on that if you need them. The inbox refactor is solid, but if you notice any weird message loading or pagination, that's worth reporting.

#### What's coming next

Contact Center views will probably keep expanding beyond the sidebar navigation. The billing redesign that shipped last week suggests more of the UI is being rebuilt for consistency. Expect more conversation-based features to land in the canvas as the AI integration deepens.

#### Try this

Open devtools in Beacon and find the consolidated AI Assistant feature flag panel. Toggle a few settings and watch how the canvas AI conversation behavior changes. It's much faster than clicking through menus now.

#### Quick notes

- v2026.4.40 landed on the 16th and is the most recent stable release.
- If you're designing around inbox threads, test the new reply indicators — they work now.
- Reach out to Josh if you're exploring Contact Center sidebar behavior or the new billing component APIs.

#### One thing to remember

Feature flags, conversations, and inbox data are all getting unified pipelines this month — designs that rely on these should feel faster and more reliable.

---

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
**[Built-in memory for Claude Managed Agents](https://claude.com/blog/claude-managed-agents-memory)**<br><small>Apr 23, 2026</small>

Memory on Claude Managed Agents lets you build agents that learn from every task, user, and session, with no memory infrastructure to maintain.

---

**[New connectors in Claude for everyday life](https://claude.com/blog/connectors-for-everyday-life)**<br><small>Apr 23, 2026</small>

Claude now connects to the apps you use every week, including AllTrails, Instacart, Audible, Booking.com, and TripAdvisor. Ask, and Claude brings in the right app.

---

**[Building agents that reach production systems with MCP](https://claude.com/blog/building-agents-that-reach-production-systems-with-mcp)**<br><small>Apr 22, 2026 · Agents</small>

Patterns for building effective MCP integrations: server design, OAuth with CIMD and vaults, context-efficient clients, and skills. Plus where MCP fits alongside direct API calls and CLIs for connecting agents to your systems.

---

**[Meet the winners of our Built with Opus 4.6 Claude Code hackathon](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon)**<br><small>Apr 20, 2026 · Claude Code</small>

From a cardiologist to an electronic musician, get to the know the winners of our Built with Opus 4.6 hackathon.

:::details View past updates

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

---

**[Multi-agent coordination patterns: Five approaches and when to use them](https://claude.com/blog/multi-agent-coordination-patterns)**<br><small>Apr 10, 2026 · Agents</small>

Five multi-agent coordination patterns, their trade-offs, and when to evolve from one to another.

:::

*Updated April 24, 2026*
<!-- CLAUDE_FEED_END -->
