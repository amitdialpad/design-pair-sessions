# What's new in Beacon

Recent updates to Beacon from Josh: features, schema changes, and Claude tool improvements. The toolkit page reflects all of these.

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
**[Product management on the AI exponential](https://claude.com/blog/product-management-on-the-ai-exponential)**<br><small>Mar 19, 2026 · Claude Code</small>

Claude Code’s Head of Product Cat Wu shares how teams should rethink their workflows and roadmaps in the face of rapidly evolving model intelligence.

---

**[Code with Claude comes to San Francisco, London, and Tokyo](https://claude.com/blog/code-with-claude-san-francisco-london-tokyo)**<br><small>Mar 18, 2026 · Claude Code</small>

Technical sessions, live demos of new capabilities, and office hours with Anthropic engineers—watch live or apply to attend.

---

**[1M context is now generally available for Opus 4.6 and Sonnet 4.6](https://claude.com/blog/1m-context-ga)**<br><small>Mar 13, 2026 · Product announcements</small>

Standard pricing now applies across the full 1M window for both models, with no long-context premium. Media limits expand to 600 images or PDF pages.

---

**[Claude now creates interactive charts, diagrams and visualizations](https://claude.com/blog/claude-builds-visuals)**<br><small>Mar 12, 2026</small>

Ask Claude to explain a concept or analyze your data, and it can respond with interactive charts, diagrams, and visualizations — rendered inline as part of the conversation.

:::details View past updates

**[Advancing Claude for Excel and PowerPoint](https://claude.com/blog/claude-excel-powerpoint-updates)**<br><small>Mar 11, 2026 · Enterprise AI</small>

Claude for Excel and PowerPoint now share full context across open files, and skills make any workflow instantly repeatable.

---

**[Bringing Code Review to Claude Code](https://claude.com/blog/code-review)**<br><small>Mar 9, 2026 · Claude Code</small>

Claude Code now dispatches a team of agents on every PR to catch bugs that skims miss. Available in research preview for Team and Enterprise.

---

**[Common workflow patterns for AI agents—and when to use them](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them)**<br><small>Mar 5, 2026 · Agents</small>

Practical guidance on how to structure agent tasks using three common workflow patterns, with tradeoffs and benefits for each.

---

**[Improving skill-creator: Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)**<br><small>Mar 3, 2026 · Claude Code</small>

Skill authors now have tools to verify their skills work, catch regressions, and improve descriptions—no coding required.

---

**[Cowork and plugins for teams across the enterprise](https://claude.com/blog/cowork-plugins-across-enterprise)**<br><small>Feb 24, 2026 · Agents</small>

We're introducing Cowork and plugin updates that let enterprises customize Claude to how you work. Plugins turn Claude into specialized agents for every role and department. Now, you can build private marketplaces to distribute them across your organization.

:::

*Updated March 22, 2026*
<!-- CLAUDE_FEED_END -->
