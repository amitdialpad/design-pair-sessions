# Resources

References for building and evaluating prototypes in Studio and Beacon. Start with the [four-step guide](/start-here) when you are new.

## Find a reference

- [Skills](/skills): workflows, when to use them, and what they produce.
- [Tools](/tools): apps, connectors, and lookup tools.
- [Quick reference](/cheat-sheet): syntax and common prompts.
- [Studio controls and releases](/studio): the shell, version pins, and announced additions.
- [Design judgment and process](/process): framing, exploration, and evaluation.

## Further reading

| What | Why |
|------|-----|
| [Why AI is Exposing Design's Craft Crisis](https://doc.cc/articles/craft-crisis) | The article behind this whole program. Explains why designers lost strategic influence and how AI provides the way back. |
| [Shape Up, Chapter 4: Find the Elements](https://basecamp.com/shapeup/1.3-chapter-04) | Where breadboarding comes from. Explains how to sketch what a feature should *do* before what it looks like. |
| [Shape Up (full book)](https://basecamp.com/shapeup) | The methodology Josh adapted for Beacon. Shaping, breadboarding, vertical slices, appetite-based planning. Free online. |

## Design process inspiration

| Source | What's useful |
|--------|--------------|
| [Resend Handbook](https://resend.com/handbook) | Concept, implementation, and polish as distinct phases. Share from day one with the entire team. |
| [Rauno Freiberg (Vercel)](https://rauno.me) | Disposable code during exploration. Share tiny videos and demos immediately. Iterate to greatness. |
| [The Craft Crisis](https://doc.cc/articles/craft-crisis) | Strategic literacy. Evaluate AI output. Participate in technical decisions. The philosophical backbone. |

## Design repo documentation

These live in the [Design monorepo](https://github.com/dialpad/design). These links require access to Dialpad’s GitHub organization. Ask your agent to read the current file for your target app; shared workflows and app-specific guidance now live in different places.

| Document | What you'll find |
|----------|-----------------|
| [Root AGENTS.md](https://github.com/dialpad/design/blob/main/AGENTS.md) | Repository conventions and shared tooling |
| [Beacon AGENTS.md](https://github.com/dialpad/design/blob/main/apps/beacon/AGENTS.md) | Beacon's architecture and app-specific guidance |
| [Studio README](https://github.com/dialpad/design/blob/main/apps/studio/README.md) | Prototype creation, settings, local development, and sharing |
| [Shared skills](https://github.com/dialpad/design/tree/main/.agents/skills) | Current skill definitions for Claude and Codex |
| [Studio-kit release policy](https://github.com/dialpad/design/blob/main/packages/studio-kit/RELEASES.md) | Version pins, explicit upgrades, and compatibility |

Use `skill-search` for the live inventory, and [Prototyping in Beacon and Studio](/prototyping) for the designer workflow.

## Tools

| Tool | What it does |
|------|-------------|
| [Claude Code](https://claude.com/claude-code) | AI pair partner. Describe what you want, it builds. Works with the Design repo's shared skills. |
| [Dialtone](https://dialtone.dialpad.com) | Dialpad's design system. Components, tokens, icons, utilities, content guidelines. |
| Dialtone MCP | Search components, icons, and tokens from within Claude. Claude knows the design system. |
| [Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server) | Point Claude at a Figma frame URL, get a code starting point. Bridge between Figma and code. |
| Jira MCP / CLI | Pull ticket context, related tickets, acceptance criteria into Claude. [Jira CLI setup](https://github.com/ankitpokhrel/jira-cli). |
| Amplitude MCP | User behavior data, funnels, drop-offs directly in Claude conversations. |
| [GitHub CLI](https://cli.github.com) | Create PRs, manage branches from the terminal. Used by Beacon's `/pr-create` command. |
| [Skill Creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Anthropic’s skill for creating, testing, and improving skills. See the repository for current setup instructions. |

## Dialtone references

| Resource | Link |
|----------|------|
| Components | [dialtone.dialpad.com/components](https://dialtone.dialpad.com/components/) |
| Utility CSS | [dialtone.dialpad.com/utilities](https://dialtone.dialpad.com/utilities/) |
| Design tokens | [dialtone.dialpad.com/tokens](https://dialtone.dialpad.com/tokens/) |
| Icons | [Icon component and usage](https://dialtone.dialpad.com/components/icon.html) |
| Content guidelines | [dialtone.dialpad.com/guides/content](https://dialtone.dialpad.com/guides/content/) |


## Claude Code guides (Josh Hynes)

| Guide | What's in it |
|-------|-------------|
| [Claude Code: From Zero to Daily Driver](https://gist.github.com/hynes-dialpad/9cd9ca443f7c0e5a6caf8f97d85f563a) | Installation, mental models, session management, CLAUDE.md setup, common failure patterns, daily habits. Written for the Dialpad team. |
| [Skills vs Subagents vs Commands](https://gist.github.com/hynes-dialpad/d38e4408b51c89b500a9dff541cb95ca) | Clears up the most confusing part of Claude Code's extension model. |

Josh also built a [daily workflow system](https://gist.github.com/hynes-dialpad/c92af436741c6beccd5f586edf25c060) — progress tracked automatically, open items surfaced every morning, nothing falling through the cracks. It has three parts:

| Part | What it does |
|------|-------------|
| [Notes system](https://gist.github.com/hynes-dialpad/c92af436741c6beccd5f586edf25c060#file-setup-notes-system-md) | Three hooks that auto-maintain session notes as you work. No manual logging. Survives context compression. |
| [Integrations](https://gist.github.com/hynes-dialpad/c92af436741c6beccd5f586edf25c060#file-setup-integrations-md) | Glean (calendar + email), GitHub CLI, Jira CLI, Dialpad MCP. Feed live data into the daily commands. All optional. |
| [Daily commands](https://gist.github.com/hynes-dialpad/c92af436741c6beccd5f586edf25c060#file-setup-daily-commands-md) | `/day-start` (morning briefing), `/day-wrap` (end of day), `/wrap` (end of session), `/snippet` (weekly update), `/reflect` (extract learnings). |

Install integrations first, then daily commands. The install prompt asks which integrations you have and skips the rest. Start with just the notes system if you want to keep it simple.

## Learning resources

| Resource | What it is |
|----------|-----------|
| [Shape Up](https://basecamp.com/shapeup) | The methodology behind `/shaping` and `/breadboard`. Free book. |
| [Vue 3 + TypeScript Guide](https://vuejs.org/guide/typescript/overview.html) | If you want to understand what Claude is writing. Not required. |
| [Pinia with TypeScript](https://pinia.vuejs.org/core-concepts/#typescript) | State management in Beacon. Again, not required, Claude handles it. |
| [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/) | Accessibility standards. Useful for understanding what `/pr-prep` checks. |

## Pair sessions

The original guided sessions are still here if you want to work through the process with someone. They are optional; you can follow the main guide independently.

- [Session 1: My turn](/sessions/session-1), watch a facilitator frame a real task.
- [Session 2: Pair build](/sessions/session-2), build and evaluate together.
- [Session 3: Your turn](/sessions/session-3), drive while someone helps when needed.

## Internal links

- [The process](/process) for the design workflow
- [The toolkit](/toolkit) for every command explained for designers
- [Quick reference](/cheat-sheet) for skill syntax and common prompts
- [Updates](/updates) for Beacon changes and weekly briefs
- [Toolkit changes](/whats-new) for detected skill and agent changes
- #ai-coding on Dialpad
- Ask the team for help with setup, prototype behavior, or a specific blocker
