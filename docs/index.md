# Design with Beacon

A living guide to building with AI at Dialpad. The workflow, the toolkit, and what's changing each week.

New here? Start with [The process](/process), then explore the [Beacon toolkit](/toolkit). The [Pair sessions](/sessions/session-1) are there when you're ready to work through it with someone.

## What's new in Beacon

Auto-synced from [beacon-app releases](https://github.com/dialpad/beacon-app/releases). Toolkit page reflects these changes.

<!-- BEACON_RELEASES_START -->

**Voicemail content and conversation messaging foundations added**

VoicemailContent.vue now supports voicemail display and playback in the inbox, while new conversation read/write hooks and message gating logic enable upcoming messaging features. Deep linking for conversations and shared messages has also been corrected to use the proper identifiers. Reach out to Josh if you need details on the new voicemail or messaging capabilities.

<span class="release-meta">[v2026.7.4](https://github.com/dialpad/beacon-app/releases/tag/v2026.7.4) · 6 July 2026</span>

---

**Call journey events tracking added to Beacon**

The app now captures and logs call journey events through a new hook in the boot loader seeding layer. This enables better instrumentation of user interactions across call-related workflows. Reach out to Josh if you need details on accessing these events in your designs.

<span class="release-meta">[v2026.7.2](https://github.com/dialpad/beacon-app/releases/tag/v2026.7.2) · 1 July 2026</span>

---

**Release notes modal refinements and event timeline**

The "What's New" modal has been updated based on design feedback. A new shared event timeline feature is now available for collaborative design reviews in Beacon. Reach out to Josh if you have questions about using the timeline in your workflow.

<span class="release-meta">[v2026.7.1](https://github.com/dialpad/beacon-app/releases/tag/v2026.7.1) · 1 July 2026</span>

---

**IVR workflow data model added**

Beacon now supports IVR workflow management with new hooks for workflows and workflow runs. This enables designers to prototype and test interactive voice response experiences with realistic data structures. Reach out to Josh if you need guidance integrating these into your designs.

<span class="release-meta">[v2026.6.33](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.33) · 30 June 2026</span>

---

**Contact history panel scope bug fixed**

The panel in PanelArea now correctly scopes contact history data, preventing information from bleeding across different contact views. This ensures designers see clean, contact-specific history when working in the Inbox and Feed sections.

<span class="release-meta">[v2026.6.24](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.24) · 25 June 2026</span>

---

**Inbox and threads filters unified with new pill component**

The Inbox and Threads sections now use a shared filter pill system that consolidates filtering controls across these areas. Check InboxFilters.vue, ThreadsHeader.vue, and the new useFilterPillBridge.ts if you need to adjust filter behavior or styling. Reach out to Josh if you have questions about how the unified system works.

<span class="release-meta">[v2026.6.22](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.22) · 25 June 2026</span>

---

**Ringtone media key replay bug fixed**

Fixed an issue where stopped ringtones could be replayed using media keys in the hardware sound settings. This prevents unintended audio playback when controlling ringtone behavior.

<span class="release-meta">[v2026.6.21](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.21) · 24 June 2026</span>

---

**Sound preferences and ringtone controls added**

The callbar now includes hardware sound settings and ringtone management through new preference hooks and controls. Incoming call audio behavior can be configured via the Preferences Modal, with underlying sound logic extracted into reusable utilities for consistent behavior across the app.

<span class="release-meta">[v2026.6.19](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.19) · 24 June 2026</span>

---

:::details View older releases

**Artifact publishing and paste-to-send workflow**

Artifacts in the message composer now support direct publishing and a streamlined paste-to-send flow. The panel header, artifact cards, attachment chips, and composer logic have been updated to enable this new capability. Check with Josh if you have questions about how to use the new workflow in your designs.

<span class="release-meta">[v2026.6.18](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.18) · 23 June 2026</span>

---

**AI CSAT scores display one decimal place**

The satisfaction score component now shows ratings with one decimal instead of two, making the metric more readable in dashboards and reports. The mock data rubric has been updated to match, so your preview data will reflect this change consistently.

<span class="release-meta">[v2026.6.14](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.14) · 22 June 2026</span>

---

**Appearance preferences now save as drafts**

The Preferences Modal now stages your appearance changes before saving them. This gives you a chance to review theme and material selections in AppearanceSettings before they're committed. If you hit issues with the new draft behavior, reach out to Josh.

<span class="release-meta">[v2026.6.11](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.11) · 16 June 2026</span>

---

**Resizable panels migrated to Dialtone component library**

The resizable panel system across Beacon's feed, side panels, sidebar menu, and billing layout has been refactored to use Dialtone's DtResizable component. This improves consistency with Dialpad's design system. If you notice any changes to how panels resize or behave, reach out to Josh.

<span class="release-meta">[v2026.6.10](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.10) · 15 June 2026</span>

---

**Contact Center calls surface in conversation index**

Calls from your Contact Center contacts now appear in the conversation index, making it easier to track and reference customer interactions alongside other communication. If you're working with Contact Center data in designs, reach out to Josh for implementation details.

<span class="release-meta">[v2026.6.9](https://github.com/dialpad/beacon-app/releases/tag/v2026.6.9) · 12 June 2026</span>

:::

<!-- BEACON_RELEASES_END -->

## Beacon Brief

Every Monday. The week's Beacon changes, in plain English.

<!-- BEACON_BRIEF_START -->

### Week of 29–5 Jul 2026

This week was mostly refinement work on existing features rather than big new launches. Josh shipped call journey event tracking through the new useCallJourneyEvents hook, which means you can now instrument user interactions across call workflows more precisely. He also added the IVR workflow data model (useWorkflows.ts and useWorkflowRuns.ts hooks) so you can prototype IVR features properly. The "What's New" modal got polished based on design feedback, and there's a new relationship affinity modeling system for visualizing communication patterns and contact interactions. On the bug side, the contact history panel was showing unrelated records instead of filtering to the selected contact, and ringtones were replaying unexpectedly when media keys were pressed—both fixed. The filters across inbox and threads now use a unified pill component, which is cleaner visually and makes the filtering behavior consistent.

#### What actually changed
- **useCallJourneyEvents hook**: Captures call journey event data for better instrumentation of user interactions in call workflows.
- **IVR workflow data model**: useWorkflows.ts and useWorkflowRuns.ts hooks now expose IVR workflow data structures with updated seeding and agent hooks.
- **Relationship affinity modeling**: New topology graphs and communication volume models for visualizing contact and interaction patterns.
- **Unified filter pills**: Inbox detail header, inbox filters, and threads header now use a standardized filter pill component.
- **Contact history panel scope fix**: Now correctly filters to the selected contact instead of showing unrelated records.
- **Ringtone replay fix**: Stopped ringtones no longer replay when media keys are pressed.
- **Whats New modal refinement**: Updated based on recent design review feedback.

#### The bigger shift
The momentum has shifted toward hooking up real data models for complex features (calls, IVR workflows, contact relationships) rather than building foundational UI. This suggests Beacon is moving from generic prototyping toward domain-specific instrumentation. You're getting better scaffolding to mock and test realistic workflows.

#### Where things are still messy
No major blockers this week, but the new data models (IVR workflows, relationship affinity) are still fresh—Josh probably expects design feedback on how useful they actually are for your work.

#### What's coming next
Expect more data model work around contact center and IVR features. The ringtone and audio preferences foundation from last week is probably leading to more sophisticated call audio handling in the design system.

#### Try this
If you're designing an IVR-related feature, pull up the new useWorkflows and useWorkflowRuns hooks and mock out a workflow run. You'll get realistic data shapes instead of guessing at the structure.

#### Quick notes
- The contact history bug was silently wrong for a while—double-check any inbox or contact designs you've been testing.
- Filter pill consistency is now across inbox, threads, and detail headers. If you're building filtering into a new surface, use the same component.
- Sound preferences are now in the Preferences Modal. Test ringtone behavior if you're working on call notifications.

#### One thing to remember
New data models (IVR, relationship affinity, call journey events) shipped this week—reach out to Josh if you need guidance on integrating them into your designs.

---

### Week of 22–28 Jun 2026

This was a solid week of polish and refinement across Beacon. Josh shipped fixes for contact history data isolation, ringtone replay bugs, and appearance preferences that now save as drafts instead of committing immediately. The bigger moves were unifying filter controls across Inbox and Threads with a new pill component and new filter bridge pattern, adding sound preferences and ringtone management to the call experience, and rolling out artifact publishing directly from the composer with a paste-to-send workflow. Resizable panels got migrated to Dialtone's component library for consistency. If you're designing around messaging, filtering, or audio feedback, there's something here that affects how you prototype. The contact history fix also means your test data won't bleed across selections anymore, which matters if you've been seeing weird overlaps in the panel.

#### What actually changed
- Contact history panel now isolates data to the selected contact across panel, feed, and inbox views
- Filter pill component unified Inbox detail, Inbox filters panel, and Threads header under one design and shared `useFilterPillBridge` hook
- Sound preferences and ringtone controls added to Preferences Modal and Callbar with new composables for incoming call timeouts
- Artifacts can now publish directly and send via paste in the message composer with updated attachment chip component
- Ringtone replay bug fixed so stopped ringtones won't restart when media keys are pressed
- Resizable panels migrated from custom implementation to Dialtone's DtResizable component across feed, side panel, sidebar menu, and billing detail
- Appearance preferences now stage changes before saving instead of committing immediately
- AI CSAT scores display one decimal place for more granular feedback metrics

#### The bigger shift
Sound and preferences are getting more integrated into the core call and messaging experience. Josh is also systematically replacing custom components with Dialtone equivalents to reduce maintenance debt.

#### Where things are still messy
The new filter pill bridge is working but Josh flagged it as worth clarifying if you're implementing custom filters. Audio controls are new enough that edge cases around media key interactions are still being ironed out.

#### What's coming next
Expect more Dialtone consolidation across panels and controls. The messaging and artifact publishing flow is becoming more central, so expect refinement there.

#### Try this
Open Preferences and tweak your appearance theme without worrying about breaking your current setup. Change your theme material, preview it, then close without saving. The draft behavior means you can experiment risk-free now.

#### Quick notes
- Check MessageActionMenu.vue if you're designing message interactions—quick emoji reactions are now built in
- Contact Center call surfacing now uses conversation index and membership data instead of the old approach
- Material dimension tokens are available in the theming system if you need spatial relationships in your designs

#### One thing to remember
Contact history data is now properly isolated, so stop second-guessing those panel views.

---

### Week of 15–21 Jun 2026

This week was mostly incremental. Josh shipped draft state management for appearance preferences so you can tweak themes without committing changes immediately, migrated all the resizable panels over to Dialtone components for consistency with the design system, and added a quick emoji reaction strip to the message hover menu. There's also a new What's New modal in the top bar that surfaces release notes directly in Beacon instead of making you hunt for them elsewhere. Contact Center calls now surface properly through conversation membership data, and the theming system gained support for material dimension themes. Nothing here breaks your current work, but if you're designing around call context or working with appearance customization, these changes make things cleaner.

#### What actually changed

- **Appearance preferences now save as drafts.** The Preferences modal stages your changes before you commit them, so you can experiment with theme materials and appearance options without immediately saving.
- **Resizable panels migrated to Dialtone.** The feed, side panel, sidebar menu, navigation panel, and billing layout now use DtResizable instead of custom code. This brings them in line with how Dialpad's design system handles resizable UI.
- **Contact Center calls surface via conversation index.** The bootloader now uses conversation membership data to display call context properly in Beacon's call surfacing components.
- **Message hover bar gained quick emoji reactions.** When you hover over a message, the action menu now includes an emoji reaction strip so you can react faster without opening additional menus.
- **Material dimension theme option added.** The theming system now supports material dimension themes, giving you more flexibility in BrandThemeSettings and ThemeMaterialSelector.
- **What's New modal and release notes interface.** The top bar user menu now shows a new What's New modal that displays release information directly in Beacon instead of requiring you to check external sources.

#### The bigger shift

Beacon is moving toward self-contained workflows. The What's New modal keeps release information inside the tool. Draft state management lets you explore settings without friction. The Dialtone migration aligns Beacon's internals with Dialpad's design system so changes upstream affect both consistently. This is less about new capabilities and more about tightening how things work together.

#### Where things are still messy

The transcript panel and 9-grid button refinements in the active call overlay shipped last month but feel like they're still being iterated on based on how they appeared in the release notes. Reach out to Josh if you're designing around active calls and notice anything off.

#### What's coming next

More of the Account Hub is coming. It already has a construction page. The AI Receptionist wizard got a major redesign last month, so expect that to stabilize or evolve further. The pinned messages panel and AI conversation side panel are both in place, so expect those to get refinement passes as designers use them.

#### Try this

If you're designing appearance customization or theming flows, spin up the Preferences modal and make some changes to your theme materials without saving them. See how the draft state feels. Then save them and verify the material dimension theme option actually applies to your design tokens. This will help you understand what's possible for theme customization work going forward.

#### Quick notes

- Josh is the go-to person for any of these changes if you hit issues or need implementation details.
- The Dialtone migration means panel resizing behavior should feel more consistent across Beacon, but flag anything that feels different from what you expect.
- The What's New modal pulls from ReleaseItem and WhatsNewModal components, so customizing how releases appear is possible if you need it.

#### One thing to remember

Draft state management in preferences and Dialtone component consistency are small changes that make design work smoother.

---

### Week of 8–14 Jun 2026

This was a focused week on call surfaces, quick interactions, and design tokens. Contact Center calls now show up in Beacon's call surfacing system using conversation index data, which matters if you're designing call-related experiences since you'll see more complete activity. Message hover interactions got faster with an emoji quick-react strip on MessageActionMenu. The theming system picked up material dimension token support, giving you another option in Theme settings alongside existing themes. There's also a cleaner What's New modal in the top bar, an inbox persistence fix that stops your panel from disappearing when you navigate away, and updated transcript and button handling in the active call overlay. Nothing revolutionary, but several small improvements that make the tool feel more polished and complete.

#### What actually changed
- Contact Center calls surface via conversation index and membership data in Beacon's call surfacing system
- MessageActionMenu now shows emoji quick-react strip on hover for faster feedback
- Theme settings support material dimension tokens for design token management
- What's New modal redesigned with improved appearance and UX
- Inbox panel state now persists when you navigate away and return
- Active call overlay displays transcript panel with redesigned 9-grid button layout and proper state handling

#### The bigger shift
Beacon is consolidating how it displays real-time information. Calls, messages, and AI responses are all moving toward more integrated views where secondary information (transcripts, reactions, metadata) appears inline rather than in separate panels. This makes the canvas feel less fragmented.

#### Where things are still messy
The transcript panel positioning in the active call overlay is new, so if you notice anything odd with how it aligns or overlaps with controls, Josh wants to know. Material dimension tokens are in but may have edge cases in how they interact with existing theme selections.

#### What's coming next
Expect more work on call interaction surfaces and possibly more refinement of the message composer and AI writing features. The inbox persistence fix suggests stability work is ongoing.

#### Try this
Hover over a message in any thread and use the new emoji strip instead of right-clicking to add reactions. It's faster, especially for repeated reactions.

#### Quick notes
- Reach out to Josh if Contact Center call surfacing affects your current designs
- The What's New modal is in the top bar user menu now, not buried elsewhere
- Material dimension tokens are live in Theme settings if you want to experiment with them

#### One thing to remember
Call and message interactions are getting more streamlined, so test your designs in Beacon before assuming something needs a separate modal or panel.

:::details View June 2026

### Week of 1–7 Jun 2026

This week was quiet on the surface. No major new features shipped to Beacon itself. But the underlying work tells a story: Josh has been reinforcing the foundation that lets designers work with AI-generated content at scale. The transcript panel and button states in the active call overlay give you a more complete picture of call UIs. The canvas now renders AI responses directly in feeds instead of separate panels, which means less switching between views when you're designing around AI features. The omnibox got smarter about showing when concurrent AI requests are competing for resources, so you can spot performance issues during design testing. These are incremental improvements, but they all push in the same direction: making Beacon feel less like a separate tool and more like a natural extension of your design workflow.

#### What actually changed

**Transcript panel and button states added to active call overlay** — You now see the transcript panel and 9-grid button state variations right in the active call overlay, so you get a fuller picture of what the UI looks like during an actual call.

**Canvas renders AI responses as feed rows** — Instead of floating panels, AI-generated content now appears directly in the content feed as it streams in. Check with Josh if this changes how you're structuring your AI-heavy designs.

**Omnibox shows concurrent request contention** — When multiple AI requests are fighting for resources in the global search modal, Beacon now displays signals that help you spot bottlenecks.

**Message composer refactored into sub-components** — The composer got split into smaller, focused pieces. Behavior should be the same, but reach out to Josh if you notice anything off with AI writing controls or recipient selection.

**Omnibox AI classifier routes to canvas** — Search now intelligently figures out which AI requests should flow to the canvas for design work. The plumbing is new, the experience should feel natural.

#### The bigger shift

Every change this week reduces friction between thinking and testing. Beacon is becoming less of a prototype viewer and more of an environment where you can reason about AI behavior in context. The transcript alongside call buttons. The AI responses in feeds instead of modal panels. The contention signals in search. These aren't flashy features. They're about letting you design without constantly hunting for the right view.

#### Where things are still messy

The message composer refactor is fresh. If you're doing heavy work with AI writing controls or share detection, test early and flag anything that feels wrong. The omnibox-to-canvas handoff is new too, so the request routing logic may need adjustment as real workflows shake out.

#### What's coming next

Josh is building toward a tighter loop between conversation context and canvas design. The AI conversation side panel already exists. Expect it to get smarter about surfacing relevant context when you're mid-design. The artifact card system (ArtifactCard, ListCard, SummaryCard, TableCard) is in place but underused. Expect more templates and examples showing how to wire them up.

#### Try this

Load an active call design and look at the transcript panel alongside the 9-grid button states in the new overlay. Then run it through a few button state variations. Notice how much faster it is to see the transcript and buttons in one place instead of toggling between panels. That's the direction Beacon is moving.

#### Quick notes

- The omnibox classifier is working, but Josh recommends checking the request routing if you're using AI search heavily in your designs.
- Message composer behavior should be unchanged, but the internal structure is different now for maintainability.
- The conversation side panel is live but still being tuned for integration. Reach out to Josh if you need custom layouts.

#### One thing to remember

Beacon is shifting from a prototype viewer to a design environment. Every change this week moves you toward fewer clicks and more context.

:::details View May 2026

### Week of 25–31 May 2026

This week was quiet on the surface but adds real capability to how you work with AI outputs in Beacon. The transcript panel now shows up alongside call button states in the active call overlay, giving you the full picture when you're designing call experiences. The canvas started rendering AI responses directly as feed rows instead of in separate panels, which means less switching between views. A few infrastructure updates landed too: the omnibox got smarter about showing when concurrent AI requests are fighting for resources, the message composer got refactored into smaller pieces for better maintainability, and the AI conversation side panel is now fully available alongside your canvas so you can reference conversations without leaving your design work. None of this is flashy, but it all points in the same direction: Beacon is becoming more integrated, less fragmented.

#### What actually changed

The active call overlay now displays the transcript panel with updated button states for the 9-grid. The canvas renders AI responses directly in feed rows as they stream in, instead of in a separate panel. The omnibox now surfaces concurrent stream contention signals so you can see when multiple AI requests are competing. The message composer was refactored into focused sub-components that handle AI writing controls, content state, recipient selection, and share detection separately. The omnibox AI classifier now routes requests directly to the canvas. New card components landed: ArtifactCard, ListCard, SummaryCard, and TableCard for displaying structured AI outputs in feeds. The AI conversation side panel is now collapsible and accessible alongside your canvas.

#### The bigger shift

Beacon is moving away from modal-heavy, panel-based AI interactions toward integrated, stream-aware workflows. Instead of AI outputs appearing in isolation, they now live in the feeds and layouts where designers actually work. This makes prototyping AI-assisted experiences feel less like switching between tools and more like designing in context.

#### Where things are still messy

The message composer refactor is live, but Josh is the person to ask if you notice any behavioral changes. The omnibox-to-canvas routing is new, so edge cases with request classification may still surface. The concurrent stream contention signals are there, but understanding what to do about resource bottlenecks during design work is still being figured out.

#### What's coming next

Expect more refinement around how AI artifacts display in different contexts. The card components are in place, but designers will likely ask for more control over how they render. The conversation panel integration suggests Beacon will keep pulling more Dialpad features directly into the canvas rather than keeping them separate.

#### Try this

Open a design that uses AI features. Check the omnibox and notice the new contention signals when you have multiple requests running. This tells you whether your prototype is going to feel sluggish when AI features pile up. Then look at how AI responses now appear in the feed instead of a side panel—this is closer to how users will actually see them.

#### Quick notes

- The Account Hub now has a construction view, accessible via AccountHubView.vue.
- The message composer refactor shouldn't break your designs, but let Josh know if composer behavior feels off.
- Pinned messages panel is still available in the right sidebar if you use it.

#### One thing to remember

AI outputs belong in the feed now, not in separate panels—design accordingly.

:::details View May 2026

### Week of 18–24 May 2026

This week was all about the active call experience and how AI content streams into your designs. The transcript panel now lives alongside button states in the active call overlay, so you can see the full interaction picture at once. The canvas also started rendering AI responses directly as feed rows instead of floating panels, which means your designs can show what real-time AI content actually looks like in context. On top of that, Josh added new card components (ArtifactCard, ListCard, SummaryCard, TableCard) specifically for displaying structured AI outputs. If you're designing around calls or AI features, this week moved the needle on fidelity.

#### What actually changed

The active call overlay now shows the transcript panel and updated button states together. The canvas renders in-flight AI responses as feed rows instead of separate panels. New artifact card components are available for displaying AI-generated content. The message composer was refactored into smaller sub-components for better maintainability. The omnibox now classifies AI requests and routes them to the canvas. The omnibox also surfaces when multiple concurrent requests are competing for resources so you can see performance bottlenecks. The AI conversation side panel is now collapsible and accessible while you design.

#### The bigger shift

Beacon is tightening the feedback loop between what you design and what actually streams in from AI. Instead of designing in isolation, you're now seeing real response patterns, feed integration, and resource contention as you work. The shift from separate panels to embedded feed rows means designs need to account for how content flows in and reshapes the interface.

#### Where things are still messy

The message composer refactor is new enough that behavior changes may still surface. Josh flagged that if you notice anything off, he wants to know. The omnibox-to-canvas routing and AI classification are solid but worth double-checking if you're relying on specific request behaviors.

#### What's coming next

Expect more card types and ways to customize how artifact content displays. The AI conversation panel will probably get deeper integration with your design canvas. The active call overlay will likely expand to support more complex interaction patterns as the call experience gets richer.

#### Try this

Open the canvas with an AI feature toggled on, and watch a response stream in as a feed row. Then check the omnibox contention signals while it's happening. You'll see exactly where the performance hits if multiple requests fire at once. This is useful if you're designing around AI features that might have competing requests in the real product.

#### Quick notes

- The Account Hub has a new construction view, but it's still minimal.
- AI Receptionist wizard redesign is live with dedicated setup steps and a live preview panel.
- Salesforce account data integration is working, so designs can reference real CRM data now.

#### One thing to remember

When you design around AI content now, it streams in as feed rows, not panels, so layout and spacing need to account for live insertion and reshaping.

:::details View May 2026

### Week of 11–17 May 2026

This was a big week for AI features in Beacon. The omnibox got smarter with AI-powered classification to route your searches correctly, and it now shows you when the system is under load from concurrent streams. The message composer was refactored into smaller pieces for easier maintenance. Four new card components landed (ArtifactCard, ListCard, SummaryCard, TableCard) to display AI-generated content in a feed. The AI conversation side panel is now live alongside your canvas, so you can talk to Claude without leaving your design workspace. The AI Receptionist wizard shipped with a full setup flow and real-time preview. And the pinned messages panel is now accessible from the right sidebar. This is the week Beacon started feeling less like a prototyping tool and more like an AI-first design canvas.

#### What actually changed

The **omnibox AI** now displays contention warnings when multiple concurrent streams compete for resources. It also classifies queries intelligently to route them to the right place, with new hooks managing how omnibox behavior connects to your canvas conversations.

The **message composer** was split into focused sub-components and composables. If you're designing with the composer, this shouldn't break your workflow, but reach out to Josh if you hit anything unexpected.

Four new card components shipped: **ArtifactCard**, **ListCard**, **SummaryCard**, **TableCard**. These power a new read-only feed display via a `useArtifacts` data layer. The feed row was updated to surface these artifacts.

The **AI conversation side panel** (DialpadPanel.vue and DialpadPanelHeader.vue) now appears alongside your canvas. It's resizable, persists your conversation context as you navigate, and integrates with view history and feature flags.

The **AI Receptionist wizard** includes new steps for business info, identity, knowledge, skills, routing, and voice selection. A preview panel lets you see your receptionist configuration in real time.

The **pinned messages panel** is now accessible from the right sidebar in conversation views.

New infrastructure shipped: **Account Hub** construction page, **Salesforce data layer hooks** for account/contact/opportunity data, **agent record extensions** with permission controls, and **AI artifact cards** feeding into the read-only display layer.

#### The bigger shift

The line between Beacon and a conversational AI workspace is blurring. You're no longer just prototyping UI in isolation. You can now have Claude conversations live in your canvas, see AI-generated artifacts rendered as cards, and access a persistent AI panel without switching windows. The omnibox got classification logic to understand what you're asking for. The Receptionist wizard gives you a full setup experience to test. This is moving Beacon toward being the place where you design with AI, not just design for AI.

#### Where things are still messy

The message composer refactor is fresh. Josh should be consulted on any impacts to your specific workflows. The Salesforce data layer is foundation-level right now — it can pull data, but integration patterns into your designs are still being figured out. The AI classifier behavior on omnibox searches is new and worth checking with Josh if you're testing complex search interactions.

#### What's coming next

More card types are likely coming to the artifact feed. The Receptionist experience will probably expand beyond the wizard into management and analytics views. The Salesforce integration will move from data hooks into actual UI patterns that surface CRM info in your designs. Conversation context across panels will get smarter.

#### Try this

Open the AI conversation side panel while you're building a design, and use it to ask Claude about your component structure or UX patterns without leaving the canvas. The panel stays open and remembers context, so it feels like a design partner sitting next to you.

#### Quick notes

- The `useArtifacts` composable is how you access the feed data layer for those new card components.
- Feature flags got consolidated in the devtools panel a few weeks back, so toggling AI features during design is faster now.
- The conversation index

:::details View May 2026

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

:::details View May 2026

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

:::details View April 2026

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

:::details View April 2026

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

:::

:::

:::

:::

:::

:::

:::

:::

<!-- BEACON_BRIEF_END -->

## What's new in Claude

Latest announcements from Anthropic.

<!-- CLAUDE_FEED_START -->
**[Giving admins more visibility and control over Claude spend](https://claude.com/blog/giving-admins-more-visibility-and-control-over-claude-usage-and-spend)**<br><small>Jul 2, 2026 · Product announcements</small>

Richer admin analytics, model-level entitlements, and spend alerts for Claude Enterprise so admins can track adoption, manage cost, and set guardrails that fit their org.

---

**[Getting started with loops](https://claude.com/blog/getting-started-with-loops)**<br><small>Jun 30, 2026 · Claude Code</small>

Practical guidance on progressing from turn-based to goal-based, time-based, and proactive loops.

---

**[Claude in Microsoft Foundry is now generally available](https://claude.com/blog/claude-in-microsoft-foundry)**<br><small>Jun 29, 2026 · Product announcements</small>

Starting today, Claude models are generally available in Microsoft Foundry, hosted on Azure.

---

**[Introducing the Claude apps gateway for Amazon Bedrock and Google Cloud](https://claude.com/blog/introducing-the-claude-apps-gateway)**<br><small>Jun 29, 2026 · Product announcements</small>

Connect Claude Code to Amazon Bedrock and Google Cloud with the new Claude apps gateway: corporate SSO login, centrally enforced policy, role-based access, per-user cost attribution, and spend caps—all from one stateless container on your infrastructure.

:::details View past updates

**[Agent identity in Claude Tag: a new access model for autonomous, team-wide AI](https://claude.com/blog/agent-identity-access-model)**<br><small>Jun 24, 2026 · Claude Code</small>

How Claude Tag’s agent identity access model works, and best practices for configuring it in your team’s workspace.

---

**[Building effective human-agent teams](https://claude.com/blog/building-effective-human-agent-teams)**<br><small>Jun 24, 2026 · Enterprise AI</small>

The way we work with AI is evolving from a single-player to a multiplayer experience, where humans and agents work together as a team to achieve shared goals. We share examples of this new way of working in action.

---

**[The full Claude Desktop experience on AWS, Google Cloud, and Microsoft Foundry](https://claude.com/blog/the-full-claude-desktop-experience-on-aws-google-cloud-and-microsoft-foundry)**<br><small>Jun 22, 2026 · Enterprise AI</small>

Deploy the full Claude desktop experience - chat, Claude Cowork, and Claude Code - using inference on AWS, Google Cloud and Microsoft Foundry. Available today in beta.

---

**[Centrally manage authorization for MCP connectors](https://claude.com/blog/enterprise-managed-auth)**<br><small>Jun 18, 2026 · Enterprise AI</small>

Admins can now provision MCP connectors for their whole organization through their identity provider, starting with Okta. Users get connector access automatically on first login, with authorization configured centrally by their organization.

---

**[Steering Claude Code: CLAUDE.md files, skills, hooks, rules, subagents and more](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)**<br><small>Jun 18, 2026 · Claude Code</small>

Learn about the seven methods for instructing Claude's behavior to understand the context cost and authority of each.

:::

*Updated July 6, 2026*
<!-- CLAUDE_FEED_END -->
