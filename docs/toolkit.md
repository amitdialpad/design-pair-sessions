# The Beacon toolkit

Everything Josh built into Beacon's `.claude/` directory, explained for designers. This is the same tooling engineers use, but described in terms of what it does for you, not how it works internally.

You don't need to memorize this. Claude knows all of it. But knowing what exists helps you ask for the right thing at the right time.

## Commands

Commands are slash commands you type in Claude Code. They trigger specific workflows. Think of them like Figma plugins: you invoke them when you need them.

### Starting a project

#### `/project-start`

Sets you up to begin work. Creates a Jira ticket (or takes an existing one), names your branch, and checks that your tools are configured. If Jira CLI isn't set up, it walks you through the setup step by step.

When it's done, it suggests `/shaping` as the next step but doesn't start it automatically. You decide when you're ready.

**Use when:** You're starting something new and need a ticket and branch.

#### `/shaping`

Interactive conversation that helps you define the problem and explore solutions before building. Not a form to fill out. A back-and-forth with Claude where you work through what you're trying to solve.

Two ways in:
- **Start from the problem.** Describe what's wrong, what users need, what constraints exist. Requirements emerge from the conversation.
- **Start from a solution.** You already have an idea. Sketch it out and extract the requirements as you go.

What you end up with:
- **Requirements** (R0, R1, R2...): numbered, tracked by status (core goal, must-have, nice-to-have, undecided, out). You negotiate these with Claude. Max 9 top-level.
- **Shapes** (A, B, C...): mutually exclusive solution approaches. Each broken into parts (mechanisms) that describe what you'd actually build.
- **Fit check**: a pass/fail matrix. Requirements as rows, shapes as columns. If a shape passes everything but still feels wrong, there's a missing requirement.

The output is a shaping document that becomes the source of truth for the feature.

**Use when:** You've done enough research to describe the problem. You're formalizing what you know, not discovering it from scratch.

#### `/breadboarding`

Maps a selected shape into concrete pieces. Answers: where do users go, what can they do at each place, and what makes it work?

The output is a set of tables:
- **Places**: bounded contexts of interaction. Simple test: can you interact with what's behind? No = different place. A modal is a place. A dropdown is not.
- **UI affordances**: things users see and act on (buttons, inputs, lists), mapped to Dialtone or Vue components
- **Code affordances**: composables, controllers, services that make the UI work
- **Data stores**: where state lives
- **Wiring**: how everything connects (what triggers what, where data flows)

After breadboarding, the map gets sliced into **vertical increments**. Each slice cuts through all layers (UI, logic, data) and ends in something you can demo. "Open the view, see real data" is a valid first slice. "Set up the database tables" is not, because there's nothing to show. Each slice becomes a PR.

**Use when:** You've picked a direction in `/shaping` and need to plan how to build it.

### Building

#### `/feature-dev`

The main build command. Hands your work to the `feature-team` agent, which orchestrates multiple specialized agents through a pipeline: research, plan, implement, test, pattern review, quality.

It's smart about what you give it:
- **Shaped slice** (has a Jira ticket, demo statement, or breadboard reference): skips research and planning, starts building
- **Vague description**: runs the full pipeline from scratch

You have review gates between every phase. Nothing proceeds without your approval. This isn't autonomous. You're directing the work.

**Use when:** A slice is defined enough to build. You have a clear picture of what the result should be.

#### `/feature-start`

Lighter than `/feature-dev`. Analyzes a feature, plans it, and scaffolds the starting files. Good for when you want to understand the scope before committing to a full build.

**Use when:** You want to explore what building something would involve before actually building it.

#### `/component-create`

Scaffolds a single Vue 3 component with TypeScript and co-located tests. Checks Dialtone first to see if a component already exists that covers what you need (so you don't rebuild something that's already there).

Takes a name and type: `ui`, `feature`, or `layout`. Creates the file structure in the right directory.

**Use when:** You need a new component and want it set up correctly from the start.

#### `/test-create`

Generates tests for a component or composable you've already built. Reads the code, understands what it does, writes tests that cover the key behaviors.

**Use when:** After building something, before shipping it. Or when `/pr-prep` flags missing test coverage.

### Cleaning up

#### `/simplify` (Claude Code built-in)

Reviews your recently changed files with three parallel checks: code reuse (are you duplicating something that exists?), code quality (can this be clearer?), efficiency (can this be faster?). Finds issues and fixes them.

Not Beacon-specific. Works in any project.

**Use when:** After a build session, before `/pr-prep`. Good for cleaning up exploration code that got messy.

#### `/fix-quick`

Fixes lint errors, type errors, import issues, and formatting problems. The mechanical stuff that blocks commits but isn't worth thinking about.

**Use when:** You have a bunch of small errors and just want them gone. Or after a pre-commit hook fails.

### Shipping

#### `/pr-prep`

The quality gate before you open a PR. Runs 6 waves of automated checks:

1. **Mechanical** (parallel): lint, type-check, formatting, build, tests
2. **Gate decision**: stops you if the build or types are broken
3. **Scope analysis**: classifies what changed, cleans up AI attribution in commit messages
4. **Team review** (parallel agents): code reviewer, pattern reviewer, test analyzer, silent failure hunter, comment analyzer, type design analyzer. Each runs independently and reports back.
5. **Static analysis**: accessibility audit (catches clickable divs, missing alt text, broken tab order), documentation audit, Dialtone compliance check
6. **Code simplifier**: optional cleanup if nothing is blocking

Output: a single report telling you what's blocking, what's a warning, what's a suggestion, and what's done well. Does not create the PR.

**Use when:** You think the code is ready. This tells you if it actually is.

#### `/pr-create`

Creates the PR. Writes a human-friendly description (for stakeholders, not just engineers), pushes the code, opens it on GitHub. Picks a contextual GIF because Josh believes PRs should have personality.

Add `skip review` to skip the AI review step (good for docs, skill updates, small changes). Add `new gif` if you want a different GIF. Add `make it a draft PR` to open it as a draft. Useful for early direction checks before it's ready for full review.

**Use when:** `/pr-prep` is clean and you're ready to share. Or use draft mode to share a preview link before the work is finished.

#### `/pr-complete`

After your PR is merged. Transitions the Jira ticket to Done, wraps session notes, returns you to the main branch. Asks what you want to work on next.

**Use when:** PR is merged. You're closing the loop.

#### `/pr-comments`

Pulls automated review comments from your PR and helps you triage them: which ones matter, which ones to fix, which ones to dismiss.

**Use when:** Your PR has review feedback and you want to work through it systematically.

### Along the way

#### `/bug-hunt`

Systematically searches for bugs in a feature. Doesn't just run tests. Thinks about edge cases, unexpected states, and interactions between components.

**Use when:** After building, when you want to stress-test before sharing.

#### `/perf-check`

Analyzes components for performance issues: unnecessary re-renders, missing memoization, heavy computations in render paths.

**Use when:** Your feature touches rendering or data loading and you want to make sure it's smooth.

#### `/jira-create`

Creates Jira tickets for new work or things you discovered while building. Useful when you find a bug or a needed improvement that isn't your current scope.

**Use when:** You found something that needs a ticket but shouldn't derail your current work.

#### `/prototype-migrate`

For existing Design Studio work. The `prototype-analyzer` agent reads your prototype, compares it against Beacon's architecture, identifies what already exists in Beacon, what's missing, what conflicts with Beacon's patterns, and estimates complexity.

The output is a gap analysis that feeds directly into `/shaping`. Your prototype isn't wasted. It's a starting point.

**Use when:** You have a Design Studio prototype and want to plan its Beacon version.

### Advanced (you'll find these when you need them)

#### `/data-trace`

Traces how data flows through Beacon's three layers (UI components → controllers → IndexedDB). Useful for debugging when data isn't showing up where you expect it.

#### `/migrate-component`

Migrates old components to current Vue 3 patterns and Beacon conventions. TypeScript improvements, accessibility fixes, composable extraction.

#### `/deps-audit`

Audits project dependencies: security vulnerabilities, available updates, unused packages, bundle sizes.

#### `/dialtone-typography-migrate`

Migrates old typography CSS classes to the DtText component. Specific to Beacon's ongoing typography cleanup.

#### `/batch` (Claude Code built-in)

Orchestrates the same change across many files in parallel. Each unit gets its own isolated copy of the codebase, runs `/simplify` on its changes, and opens a PR. For when you need the same pattern applied across 30+ files.

#### `/loop` (Claude Code built-in)

Runs a prompt on a recurring interval within your session. For watching a deploy or monitoring a process. Session-scoped: exits when you close the terminal.

## Agents

Agents are specialized workers that commands delegate to. You usually don't invoke them directly. They get called by the commands that need them. But knowing they exist helps you understand what's happening when a command takes a few minutes.

| Agent | What it does | Called by |
|---|---|---|
| `feature-team` | Orchestrates the full build pipeline: research, plan, implement, test, review, quality | `/feature-dev` |
| `prototype-analyzer` | Inventories a prototype and maps it against Beacon | `/prototype-migrate` |
| `codebase-pattern-reviewer` | Reads adjacent code to catch semantic duplication and architectural drift | `/pr-prep` (Wave 3) |
| `dialpad-design` | Reviews UI against Dialpad's 7 Design Tenets | Automatically on UI work, or ask directly |
| `documentation-architect` | Ensures docs exist and are accurate | `/pr-prep` (Wave 4) |
| `error-resolver` | Diagnoses and fixes errors | When something breaks |
| `web-research-specialist` | Researches external libraries and patterns | `/shaping` spikes |
| `dialtone-typography-agent` | Enforces DtText usage | `/pr-prep`, hooks |
| `code-refactor-master` | Handles complex multi-file refactors | When refactoring is needed |
| `refactor-swarm-orchestrator` | Coordinates parallel refactoring agents | Large refactors |
| `webrtc-debugger` | Debugs meeting/call related issues | Meeting feature work |

The **`dialpad-design` agent** is the one designers should know about. It reviews against 7 tenets:

1. **Design systems, not surfaces**: Is the feature available where users need it, or isolated in one place?
2. **Opt into complexity**: Are too many options visible upfront? Are power features in the baseline?
3. **Transparency is non-negotiable**: Are disabled states explained? Is system state clear?
4. **Anticipation over reaction**: Does the user have to hunt for next steps?
5. **Friction is deliberate**: Are destructive actions too easy? Is there unnecessary friction on common actions?
6. **Customize to lock in**: Can users save preferences?
7. **Capability without clarity**: Is the feature's purpose clear?

Ask it: *"Review the UI I just built for the settings feature."* It gives you specific feedback with file/line references and recommendations. It's not a rubber stamp. It pushes back.

## Skills

Skills are knowledge that Claude loads when relevant. You don't invoke them. They activate based on what you're working on. Think of them like design system documentation that Claude has internalized.

| Skill | What Claude knows because of it |
|---|---|
| `shaping` | How to run a shaping session: requirements, shapes, fit checks, documents |
| `breadboarding` | How to map affordances, places, wiring, and slice into vertical increments |
| `accessibility-patterns` | WCAG 2.1 AA compliance: ARIA, keyboard nav, focus management, semantic HTML |
| `frontend-patterns` | Vue 3/TypeScript patterns, MVC architecture, component conventions |
| `data-architecture-enforcer` | Beacon's cache-first controller pattern, IndexedDB, cross-tab sync |
| `dialtone-typography-enforcer` | DtText component usage, typography hierarchy, migration patterns |
| `code-quality` | Max complexity 8, no unused variables, files under 500 lines, no `any` types |
| `permission-patterns` | How to gate features by admin role |
| `mock-data-generator` | How to generate realistic test data |
| `meeting-component-guide` | Meeting UI component hierarchy and patterns |
| `logging-standards` | When and how to add debug logging |
| `project-planning` | How to create standardized plan documents |
| `step-by-step-execution` | How to break complex tasks into incremental changes |
| `swarm-orchestration` | How to coordinate multiple agents in parallel |
| `unit-testing` | Vitest patterns, mock typing, component stubs |
| `workflow-edit` | Safe editing of GitHub Actions workflows |
| `media-device-enforcer` | WebRTC device patterns for meetings |

The ones that matter most for designers: `shaping`, `breadboarding`, `accessibility-patterns`, and `frontend-patterns`. The rest help Claude write better code, which means the code it writes for you is already following the rules.

## Rules

Rules auto-load based on what file you're editing. When you're working in `./src/`, Claude automatically follows these.

**6 root rules** covering code guidelines, commit messages, Dialtone usage, frontend style, and Vue/TypeScript conventions.

**53 Dialtone component rules**, one per component. Each documents: required props, correct import pattern (`import { DtButton } from "@dialpad/dialtone/vue3"`), usage examples, and what NOT to do. Claude won't suggest `<button>` when `<DtButton>` exists. It won't use Tailwind. It won't use inline styles.

You don't need to know what's in these files. Claude reads them automatically. But if Claude suggests a component and you're not sure about it, ask: *"Show me the Dialtone rules for DtModal."* It'll read the rule file and explain the component's proper usage.

## Hooks

Hooks run automatically on every file edit. You never invoke them. They're invisible guardrails.

| Hook | What it does |
|---|---|
| `branch-protection.sh` | Prevents direct edits to protected branches |
| `workflow-security.sh` | Checks for security issues in workflow files |
| `dialtone-linter.sh` | Checks component usage against Dialtone rules |
| `sort-classes-post-edit.sh` | Keeps CSS classes in consistent order |
| `type-check-post-edit.sh` | Runs TypeScript checking after edits |
| `doc-reminder.sh` | Reminds you to update docs when relevant files change |
| `shaping-ripple.sh` | When you change a shaping doc, checks if related docs need updating too |

If a hook blocks something, it tells you why. You can paste the message into Claude and ask it to fix the issue.

## Pre-commit checks

Every git commit runs 6 checks. If any fail, the commit is blocked until fixed.

1. **Schema version**: If you changed the database schema, did you increment the version number?
2. **Field justification**: Schema changes need a brief description of why they exist
3. **Noisy logs**: Catches debug logging that fires too often or adds noise
4. **Comment quality**: Ensures comments describe the system as it is, not as it might be someday
5. **Documentation**: Verifies that `@see` references point to docs that actually exist
6. **Lint + format**: ESLint and Prettier on every commit

If a commit fails: paste the full error into Claude, say "fix it." That's the whole recovery process.
