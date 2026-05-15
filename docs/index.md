# Design with Beacon

A living guide to building with AI at Dialpad. The workflow, the toolkit, and what's changing each week.

New here? Start with [The process](/process), then explore the [Beacon toolkit](/toolkit). The [Pair sessions](/sessions/session-1) are there when you're ready to work through it with someone.

## What's new in Beacon

Auto-synced from [beacon-app releases](https://github.com/dialpad/beacon-app/releases). Toolkit page reflects these changes.

<!-- BEACON_RELEASES_START -->

**AI conversation side panel added to Dialpad**

A new DialpadPanel component with header now appears alongside your design canvas, giving you quick access to AI-assisted conversations. The panel integrates with floating layer utilities and view history tracking to maintain state as you navigate. Reach out to Josh if you'd like to explore how to use this for design feedback and iteration.

<span class="release-meta">[v2026.5.7](https://github.com/dialpad/beacon-app/releases/tag/v2026.5.7) · 14 May 2026</span>

---

**Account Hub construction page added**

The Account Hub now includes a new construction page view accessible via AccountHubView.vue. Feature flag logic in useFeatureFlags.ts has been updated to support rolling out this section. Reach out to Josh if you need to adjust the rollout strategy.

<span class="release-meta">[v2026.5.6](https://github.com/dialpad/beacon-app/releases/tag/v2026.5.6) · 13 May 2026</span>

---

**AI Receptionist setup wizard and preview panel**

The receptionist configuration flow now includes a multi-step wizard (BusinessStep, IdentityStep, KnowledgeStep, RoutingStep, SkillsStep, VoiceStep, ReviewStep) with supporting widgets for persona and voice selection. A new preview panel (ReceptionistPreviewPanel.vue) lets you see your receptionist in action as you configure it. Reach out to Josh if you need guidance on integrating these into your designs.

<span class="release-meta">[v2026.5.5](https://github.com/dialpad/beacon-app/releases/tag/v2026.5.5) · 12 May 2026</span>

---

**Pinned messages panel added to right sidebar**

The right sidebar now includes a dedicated pinned messages section where you can view and manage saved conversation pins. This complements the existing saved content area and gives you quick access to important message references in your design reviews.

<span class="release-meta">[v2026.5.4](https://github.com/dialpad/beacon-app/releases/tag/v2026.5.4) · 8 May 2026</span>

---

**Agent record extensions and permission foundation**

The Skills Workflows tab and agent-related composables now support extended agent records with permission controls. This lays groundwork for more flexible agent configuration in Agentic Studio. Check with Josh if you need details on the new extension patterns.

<span class="release-meta">[v2026.5.3](https://github.com/dialpad/beacon-app/releases/tag/v2026.5.3) · 6 May 2026</span>

---

**Salesforce account data layer integration**

The Salesforce data hooks (useSalesforceAccount, useSalesforceContact, useSalesforceOpportunity) are now available for use in Beacon. Boot loader seeding has been updated to support this new data layer. If you're building experiences that need Salesforce account, contact, or opportunity data, reach out to Josh for implementation guidance.

<span class="release-meta">[v2026.5.2](https://github.com/dialpad/beacon-app/releases/tag/v2026.5.2) · 5 May 2026</span>

---

**AI writing panel UX polish and refinement**

The Composer AI panel and response cards have been refined for better usability. Improvements include updated interaction patterns in the AI mode hook and inbox data handling. If you notice any edge cases in the AI writing experience, let Josh know.

<span class="release-meta">[v2026.5.1](https://github.com/dialpad/beacon-app/releases/tag/v2026.5.1) · 1 May 2026</span>

---

**Message composer gets AI rewrite presets**

The message composer now includes premade AI rewrite options in a new popover panel. Designers can see how these preset rewrites appear and behave in the composer UI by checking ComposerAIPanel.vue and the new ComposerAIOptionsPopover.vue component.

<span class="release-meta">[v2026.4.50](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.50) · 30 April 2026</span>

---

:::details View older releases

**AI Receptionists navigation and detail views added**

The left sidebar navigation now includes AI Receptionists with a new dedicated section. Designers can explore the receptionists home view and individual receptionist details through the updated navigation panel and composer toolbar. Reach out to Josh if you need clarification on the new feature flags or navigation structure.

<span class="release-meta">[v2026.4.46](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.46) · 23 April 2026</span>

---

**Preferences and segmented controls migrate to Dialtone**

The Preferences Modal and segmented control components have been refactored to use Dialtone primitives, improving consistency across the design system. This affects the appearance settings, theme selection, and other preference controls throughout Beacon.

<span class="release-meta">[v2026.4.45](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.45) · 23 April 2026</span>

---

**AI Assistant feature flags consolidated in devtools**

The AI Assistant controls and feature flags are now managed in one place within the devtools panel. This streamlines toggling AI preferences and feature flags when testing Beacon components.

<span class="release-meta">[v2026.4.40](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.40) · 16 April 2026</span>

---

**Canvas AI conversation interface launches**

The canvas now supports AI-assisted conversations integrated with Dialpad, accessible through the left sidebar and main content area. New conversation management, draft persistence, and mentions handling have been added to support this workflow. Reach out to Josh if you need guidance on using these new capabilities.

<span class="release-meta">[v2026.4.38](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.38) · 15 April 2026</span>

---

**Inbox adopts conversation index pipeline**

The inbox now uses the conversation index pipeline for data handling and enrichment. This refactor affects how messages load, filter, and paginate in the inbox list and detail views. If you notice changes in inbox performance or behavior, reach out to Josh.

<span class="release-meta">[v2026.4.37](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.37) · 15 April 2026</span>

---

**Power Dialer campaign context added to callbar**

The callbar now displays Power Dialer campaign information, giving you immediate context about active campaigns during calls. Check the ActiveCallOverlay and CallbarOverlays components to see how campaign details integrate with your call interface.

<span class="release-meta">[v2026.4.35](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.35) · 14 April 2026</span>

---

**Feed area reclaims space when right panel closes**

The layout engine now properly redistributes space when you collapse the right panel, giving more room to your feed. This affects how resizable groups adjust across the canvas.

<span class="release-meta">[v2026.4.29](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.29) · 12 April 2026</span>

---

**Star icon removed from sidebar channel groups**

Channels nested under system sidebar groups no longer display an incorrect star icon. This fixes a visual inconsistency in the LeftSidebarExpandedMenu component.

<span class="release-meta">[v2026.4.28](https://github.com/dialpad/beacon-app/releases/tag/v2026.4.28) · 12 April 2026</span>

:::

<!-- BEACON_RELEASES_END -->

## Beacon Brief

Every Monday. The week's Beacon changes, in plain English.

<!-- BEACON_BRIEF_START -->

### Week of 4–10 May 2026

This week was about conversation management and AI polish. The pinned messages panel landed in the right sidebar, giving you a dedicated spot to surface and organize saved highlights from conversations. That's the main UX addition. The rest of the week focused on backend groundwork: Salesforce account data is now live in the data layer, which means features that need CRM context can pull it directly. Agent permissions got a foundation too, so downstream features can enforce granular access controls when agents touch external data. The AI writing experience in the Composer got refinements to both the panel layout and how responses render. None of this breaks existing work, but if you're building features that lean on Salesforce data or AI-assisted messaging, the plumbing is fresher now.

#### What actually changed

**Pinned messages panel** now lives in the right sidebar (PanelArea). It lets you access and manage saved conversation highlights without digging through the feed.

**Salesforce account data layer** is integrated and live. The account hub pulls Accounts, Contacts, and Opportunities data through new hooks in the seeding layer. If you're building features that need CRM context, it's there now.

**Agent record extensions and permissions** got foundational setup in the Skills & Workflows tab and Salesforce integrations. This powers granular access controls when agents interact with external data.

**AI writing panel and response cards** were polished for better UX in the Composer section.

#### The bigger shift

The pattern this week is infrastructure maturity. Less visible UI work, more backend readiness. Beacon is getting the plumbing in place to support features that talk to external systems (Salesforce) and enforce permissions at scale. This suggests the next wave of design work will lean harder on CRM integration and agent capability features.

#### Where things are still messy

Reach out to Josh if you need clarity on how the agent permissions system actually affects design workflows. The foundational setup is there, but the design surface area is still being scoped.

#### What's coming next

Expect more Salesforce-powered features to land in the account hub and agent detail views. The permissions foundation suggests role-based controls are coming next. The AI rewrite presets and summary pills from earlier in May are probably getting more refinement too.

#### Try this

Check out the pinned messages panel this week. Add a few pins to a conversation in your prototypes and see how the panel updates in the right sidebar. It's a clean pattern for surfacing saved context without cluttering the main feed.

#### Quick notes

- Dialtone components are now used in Preferences and segmented controls. If you're designing preference or settings panels, reference these.
- Feature flags for AI Assistant functionality are consolidated in devtools now, making it faster to toggle features during design work.
- Feed layout now expands properly when you collapse the right panel. No more wasted space.

#### One thing to remember

The Salesforce data layer is live, so features that need CRM context don't have to fake it anymore.

---

### Week of 27–3 May 2026

This week was light on shipping but solid on refinement. The AI writing panel got a visual polish pass, and the message composer now has preset rewrite options that let you quickly apply common adjustments without typing prompts. That's the kind of thing that matters—less friction in the actual design workflow. The bigger story is that Beacon keeps filling in gaps around AI features: the Canvas now talks directly to Dialpad's AI service, the devtools panel consolidated all those scattered feature flags into one place, and we've got dedicated navigation for AI Receptionists ready to go. Nothing earth-shattering, but the direction is clear. Reach out to Josh if any of these changes affect your current prototypes.

#### What actually changed
- **AI writing panel and response cards** now have refined interactions and visual feedback. Check ComposerAIPanel.vue and ComposerAIResponseCard.vue.
- **Message composer preset rewrites** surface common writing adjustments in a popover without needing you to type prompts. Customizable presets available on request.
- **AI Receptionists navigation** added to the left sidebar with home and detail views.
- **Preferences modal and segmented controls** now use Dialtone components instead of custom builds. May affect keyboard navigation behavior.
- **AI Assistant feature flags** consolidated in devtools. No more hunting through multiple panels.
- **Canvas AI conversation hooks** (useCanvasConversations, useDialpadConversation, useDialpadPanel) connect to Dialpad's AI service. Test AI features without leaving Beacon.
- **Inbox conversation pipeline** refactored for better data handling and performance across feed, list, and detail views.
- **Power Dialer campaign context** now displays in the callbar.

#### The bigger shift
The tool is getting more opinionated about AI workflows. Instead of just supporting them, Beacon is baking in AI patterns as first-class citizens—preset options, dedicated navigation sections, tighter integration with Dialpad's backend. This means the things you prototype in Beacon now have a clearer path to feeling like the real product.

#### Where things are still messy
The Preferences modal migration to Dialtone is new. If keyboard navigation feels off in segmented controls, that's worth flagging to Josh. The AI Receptionists navigation is scaffolding—the actual functionality is still coming.

#### What's coming next
More work around AI features and the Contact Center section. The navigation structure is in place. Expect to see actual interaction patterns and data flows filling in over the next few weeks.

#### Try this
Open the message composer and look for the preset rewrite options. Try applying one to some copy you're working with. It's faster than typing a prompt, and if it doesn't do what you need, you can always follow up with a custom request.

#### Quick notes
- Feed area now expands properly when you close the right panel. More breathing room.
- Fixed a bug where favorite stars were showing up on channel groups. They shouldn't.
- Inbox reply indicators and detail panel threading now work as expected.

#### One thing to remember
Reach out to Josh before assuming behavior has changed in Preferences or Dialtone components—the migration is recent.

---

### Week of 20–26 Apr 2026

This was a solid week of consolidation and expansion. AI Receptionists got a full navigation home view added to the sidebar, which means designers can now prototype the complete receptionist experience end-to-end. The bigger move was collapsing all the AI Assistant feature flags into devtools so you're not hunting across five different panels to toggle things. Canvas conversations now talk directly to Dialpad services through new hooks, the callbar picked up campaign context, and the layout engine got smarter about reclaiming space when you close panels. These are the kinds of changes that make prototyping feel less janky.

#### What actually changed

**AI Receptionists navigation and home view** — Added AgentsLeftSidebar and ReceptionistNavPanel so you can build full receptionist flows with a dedicated home view and detail pages. New useReceptionists hooks support the whole thing.

**AI Assistant feature flags consolidated** — All the toggles for AI-assisted design features now live in a single devtools panel instead of scattered across the app.

**Canvas AI conversations integrated with Dialpad** — useCanvasConversations, useDialpadConversation, and useDialpadPanel hooks let the canvas talk to Dialpad services for real conversation management in the left sidebar and content area.

**Power Dialer campaign context in callbar** — The callbar now shows which campaign an active call belongs to without you having to leave the calling interface.

**Inbox using conversation index pipeline** — The entire Inbox section (detail feed, message list, data hooks) refactored to use the conversation index pipeline for better performance and filtering.

**Preferences and segmented controls moved to Dialtone** — The Preferences modal and segmented controls got refactored to use Dialtone primitives, so appearance settings and theme selection look and behave more consistently.

**Layout space redistribution when right panel collapses** — The feed area no longer leaves dead space when you close the right panel. Available space gets properly redistributed.

**Star icon removed from channel sidebar groups** — Fixed visual noise where favorites stars were showing up next to channels in system sidebar groups. Only individual contacts and conversations should have favorite status.

#### The bigger shift

There's a clear move toward making Beacon itself feel less like a prototyping tool and more like a real application. Adding campaign context to calls, integrating conversations with Dialpad services, and giving receptionist workflows their own navigation suggests the team is building out proper feature verticals instead of just generic UI components. The consolidation of feature flags and the Dialtone migration also signal a focus on making the tool more predictable and less scattered.

#### Where things are still messy

Canvas AI conversations are new enough that integrations may have rough edges. Reach out to Josh if you hit behavioral changes in the Preferences modal or segmented controls after the Dialtone migration.

#### What's coming next

Expect more feature-specific navigation scaffolds like the Contact Center structure that shipped earlier in April. The pattern of moving from generic hooks to domain-specific ones (receptionist, campaign, conversation) is going to keep going.

#### Try this

Go into devtools and toggle the AI Assistant feature flags. They're all in one panel now instead of spread out. If you're testing AI-assisted design, you'll notice it's much faster to flip things on and off for quick iteration.

#### Quick notes

- Power Dialer campaign context is live in the callbar — test it with active calls to see which campaign they belong to.
- Inbox is now using the conversation index pipeline for better data handling — if you notice changes in how messages load or filter, that's why.
- The callbar, inbox feed, and preferences modal all saw real improvements this week. None of these are breaking, but they're worth a quick look if you're working in those areas.

#### One thing to remember

Beacon is getting faster and more predictable. The infrastructure work around conversation pipelines and feature flags consolidation is boring but it means your prototypes will behave more like the real product.

---

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

:::details View April 2026

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

:::

<!-- BEACON_BRIEF_END -->

## What's new in Claude

Latest announcements from Anthropic.

<!-- CLAUDE_FEED_START -->
**[How Claude Code works in large codebases: Best practices and where to start](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start)**<br><small>May 14, 2026 · Enterprise AI</small>

The most successful Claude Code deployments share a set of recognizable patterns across configurations, tooling, and org structure. This article is part of Claude Code at scale, a new series covering best practices for engineering organizations building with Claude Code at enterprise scale.

---

**[The founder's playbook: Building an AI-native startup](https://claude.com/blog/the-founders-playbook)**<br><small>May 14, 2026 · Claude Code</small>

We share how AI-native founders are using Claude at every stage of the startup journey, with practical exercises, frameworks, and prompts.

---

**[Best practices for computer and browser use with Claude](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude)**<br><small>May 13, 2026 · Agents</small>

Practical guidance for developers building computer and browser use integrations with the Claude model family.

---

**[How Anthropic's cybersecurity team built a threat detection platform with Claude Code](https://claude.com/blog/how-anthropic-uses-claude-cybersecurity)**<br><small>May 12, 2026 · Claude Code</small>

Jackie Bow, technical lead for Anthropic's Detection Platform Engineering team, shares how her team uses Claude Code to build tools that automate alert triage, accelerate investigations, and transform how security analysts work.

:::details View past updates

**[Claude for the legal industry](https://claude.com/blog/claude-for-the-legal-industry)**<br><small>May 12, 2026 · Product announcements</small>

We're releasing 20+ new MCP connectors that link Claude to the software that the legal industry runs on and 12 new plugins tailored specific legal work and practice areas.

---

**[Code w/ Claude SF 2026: Building on the AI exponential](https://claude.com/blog/code-w-claude-sf-2026-sf)**<br><small>May 12, 2026</small>

Check out our Code w/ Claude SF sessions on YouTube.

---

**[Introducing the Claude Platform on AWS](https://claude.com/blog/claude-platform-on-aws)**<br><small>May 11, 2026 · Product announcements</small>

The Claude Platform on AWS is now generally available, offering a new way for AWS customers to access the full set of Claude platform features with AWS authentication, billing, and commitment retirement.

---

**[Agent view in Claude Code](https://claude.com/blog/agent-view-in-claude-code)**<br><small>May 11, 2026 · Product announcements</small>

Today we're introducing agent view in Claude Code: one place to manage all your Claude Code sessions.

---

**[Collaborate with Claude across Excel, PowerPoint, Word and Outlook](https://claude.com/blog/collaborate-with-claude-across-excel-powerpoint-word-and-outlook)**<br><small>May 7, 2026 · Product announcements</small>

Claude for Excel, PowerPoint, and Word are generally available, and Claude for Outlook is now in public beta for all paid plans.

:::

*Updated May 15, 2026*
<!-- CLAUDE_FEED_END -->
