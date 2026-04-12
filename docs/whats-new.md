# What's new in Beacon

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

---

<!-- BEACON_RELEASES_END -->

**March 26, 2026: Shaping skills now based on Ryan Singer's official ShapeUp patterns**

Ryan Singer (creator of the ShapeUp methodology) released his own official shaping skills. Josh incorporated them into Beacon this week while keeping the Beacon-specific additions. The March 23 commands below are the result. One addition not in that entry: `/shaping` now includes upstream/downstream skill references — pointers to adjacent skills that feed in or out of the shaping step.

---

**March 23, 2026: Planning tools overhaul**

`/breadboarding` is now `/breadboard`. The command is significantly enhanced with better chunking, navigation wiring rules, support for multi-system diagrams, and labeled flows.

Two new commands in the planning pipeline: `/framing-doc` (turn raw source material into an evidence-based problem frame before shaping) and `/kickoff-doc` (for collaborative work — creates a territory-based builder reference from a kickoff transcript).

New `/breadboard-reflection` command: two-phase audit that verifies a breadboard against what was actually built. Also runs automatically in `/pr-prep` Wave 5.

`/shaping` updated with a macro fit-check for early-stage work and 🟡 change markers. When you run `/pr-prep`, it now copies your shaping and breadboarding documents into the PR so reviewers can read them.

New `/branch-prune` command: cleans up local branches that were deleted on the server after a PR merged.

All Claude tools in Beacon were rewritten based on updated Anthropic best practices. Things should trigger more reliably.

---

**March 23, 2026: AI writing tools**

Beacon's autocomplete and AI writing tools are updated. You can now preview copy before accepting it and refine further with follow-up prompts. Try it.

---

**March 18, 2026: Claude tool updates**

Expanded `dialpad-design` agents now cover layout, voice & tone, interaction, animation, motion, typography, and color. `/pr-prep` includes a design review check as part of the static analysis wave.

`/shaping` has a new Discovery mode. If your goal is vague, Claude will explore with you before pushing to pick a shape. You don't need it figured out before you start.

New `/debug-trace` command: adds debug logs to the code you point at, outputs runtime state to the console. Use it when you're going in circles on a bug instead of letting Claude keep reading files.

New skills: `feature-flags` (create flags consistently) and `jira-management` (say "update the Jira" or "create a ticket"; Claude handles it without a slash command).

---

**March 18, 2026: Beacon features**

BeaconComposer recipe is live with dedicated content slots and rich text rendering in conversation rows. Storybook for unmigrated Beacon components coming soon.

New Contact Center schema: contact centers, memberships, settings, managed phone numbers, operator skills, operating hour profiles, dispositions, and groups. The data layer is built. UI is next. Ask Josh if you want to start it.

Beacon now runs as an Electron desktop app. To set it up:

```
pnpm install
pnpm approve-builds
```

`approve-builds` is one-time. You'll see a list of builds. Select "electron" and confirm. Then run these in two separate terminal windows:

```
# Terminal 1
pnpm dev

# Terminal 2
pnpm electron:dev
```

The Apple top bar gets a Server menu for switching between your localhost and the main URL. A few things are still rough (DevTools PiP, OS notifications) but it works.

---

**March 17, 2026: Beacon areas to know about**

Beacon has a settings area (gear icon) and an Agents Studio area (1/0 icon in the left sidebar). Agents Studio is not finished yet. Both exist if you need them as a starting point for design work.

Design Studio prototypes can't be ported into Beacon wholesale. Use `/prototype-migrate` to map what carries over and what needs to be rebuilt.

:::details View past updates

**March 13, 2026: Beacon updates**

New [Adding data to Beacon](https://github.com/dialpad/beacon-app/blob/main/docs/development/adding-data-to-beacon.md) guide: schema design, the controller pattern, and the mock data pipeline. Read it before adding any new entity type.

Plan files in `/docs/plans/` are deleted when a branch merges. Move anything worth keeping to Jira before you merge.

`/jira-create` now sets story points automatically.

:::

---

# What's new in Claude

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

**[Harnessing Claude’s intelligence](https://claude.com/blog/harnessing-claudes-intelligence)**<br><small>Apr 2, 2026</small>

Three patterns for building on the Claude Platform that keep pace with Claude's evolving intelligence while balancing latency and cost.

:::

*Updated April 11, 2026*
<!-- CLAUDE_FEED_END -->
