# Resources

Everything referenced across this site, plus useful links for working in Beacon.

## Required reading

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

## Beacon documentation

These live in the [beacon-app repo](https://github.com/dialpad/beacon-app). Claude can read all of them and explain them to you.

| Doc | What's in it |
|-----|-------------|
| [README.md](https://github.com/dialpad/beacon-app/blob/main/README.md) | Getting started, setup, how we work, further reading |
| [CONTRIBUTING.md](https://github.com/dialpad/beacon-app/blob/main/CONTRIBUTING.md) | Branch naming, slash commands, pre-commit hooks, feature flags, troubleshooting |
| [AGENTS.md](https://github.com/dialpad/beacon-app/blob/main/AGENTS.md) | The developer operating manual. 555 lines. Architecture, data layer, TypeScript patterns, components, AI features. |
| [CLAUDE.md](https://github.com/dialpad/beacon-app/blob/main/CLAUDE.md) | Quick reference. Architecture, critical rules, key files, performance targets. |
| [docs/development/getting-started.md](https://github.com/dialpad/beacon-app/blob/main/docs/development/getting-started.md) | Full walkthrough from first ticket to merged PR |
| [docs/development/claude-code-guide.md](https://github.com/dialpad/beacon-app/blob/main/docs/development/claude-code-guide.md) | Complete reference for all commands, agents, skills, rules, and workflows |
| [docs/development/engineering-guide-for-designers.md](https://github.com/dialpad/beacon-app/blob/main/docs/development/engineering-guide-for-designers.md) | How Beacon's codebase is organized and why. Code structure, Vue patterns, data storage, Git, PR hygiene. Read it once. |
| [docs/development/adding-data-to-beacon.md](https://github.com/dialpad/beacon-app/blob/main/docs/development/adding-data-to-beacon.md) | Beacon's data layer: schema design, the controller pattern, mock data pipeline. Read before adding any new entity type. |

Josh wrote this for designers working in Beacon. It covers how the code is organized, why things work the way they do, and what to expect when reviewing Claude's output. Read it once. Keep it open whenever something in the code surprises you.

## Tools

| Tool | What it does |
|------|-------------|
| [Claude Code](https://claude.com/claude-code) | AI pair partner. Describe what you want, it builds. The primary tool for everything. |
| [Dialtone](https://dialtone.dialpad.com) | Dialpad's design system. Components, tokens, icons, utilities, content guidelines. |
| Dialtone MCP | Search components, icons, and tokens from within Claude. Claude knows the design system. |
| [Figma MCP](https://www.figma.com/community/plugin/Claude-MCP) | Point Claude at a Figma frame URL, get a code starting point. Bridge between Figma and code. |
| Jira MCP / CLI | Pull ticket context, related tickets, acceptance criteria into Claude. [Jira CLI setup](https://github.com/ankitpokhrel/jira-cli). |
| Amplitude MCP | User behavior data, funnels, drop-offs directly in Claude conversations. |
| [GitHub CLI](https://cli.github.com) | Create PRs, manage branches from the terminal. Used by Beacon's `/pr-create` command. |
| [Skill Creator](https://claude.com/plugins/skill-creator) | Build, test, and compare Claude skills without code. Install via `/plugin` in Claude, find `skill-creator` under `claude-plugins-official`. |

## Dialtone references

| Resource | Link |
|----------|------|
| Components | [dialtone.dialpad.com/components](https://dialtone.dialpad.com/components/) |
| Utility CSS | [dialtone.dialpad.com/utilities](https://dialtone.dialpad.com/utilities/) |
| Design tokens | [dialtone.dialpad.com/tokens](https://dialtone.dialpad.com/tokens/) |
| Icons | [dialtone.dialpad.com/icons](https://dialtone.dialpad.com/icons/) |
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
| [Shape Up](https://basecamp.com/shapeup) | The methodology behind `/shaping` and `/breadboarding`. Free book. |
| [Vue 3 + TypeScript Guide](https://vuejs.org/guide/typescript/overview.html) | If you want to understand what Claude is writing. Not required. |
| [Pinia with TypeScript](https://pinia.vuejs.org/core-concepts/#typescript) | State management in Beacon. Again, not required, Claude handles it. |
| [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/) | Accessibility standards. Useful for understanding what `/pr-prep` checks. |

## Internal links

- [The process](/process) for the design workflow
- [The toolkit](/toolkit) for every command explained for designers
- [Getting started](/cheat-sheet) for quick reference
- [Project IRL](/story) for the full arc
- [What's new](/) for Beacon toolkit changes
- #ai-coding on Dialpad
- Your facilitator, DM anytime
