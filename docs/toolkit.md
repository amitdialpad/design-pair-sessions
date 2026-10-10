# Skills and tools

The Design repo's shared skills and app-specific tools, explained for designers. Shared definitions live in `.agents/`; Claude has adapters in `.claude/`. Beacon and Studio add their own app-specific guidance.

**Updated 10 October 2026.** Start with [Prototyping in Beacon and Studio](/prototyping). For the live inventory, use `/skill-search` in Claude or `$skill-search` in Codex. The menu shows the workflows people start; the agent loads supporting skills when needed.

You don't need to memorize this. Claude knows all of it. But knowing what exists helps you ask for the right thing at the right time.

> New to this workflow? Start with [Start here](/start-here). Already working? Use [Quick reference](/cheat-sheet).

## Workflows

Examples below use `/skill-name` in Claude Code. In Codex, use `$skill-name`. These are entry points you invoke by name. They trigger specific workflows. Think of them like Figma plugins: you invoke them when you need them.

### Find a tool or build a prototype

#### `/skill-search`

Finds current skills, agents, and rules for your task. With no task, it lists what is available. Shared tools work across the Design repo; app-specific tools carry Beacon or Studio guidance.

Try: `$skill-search do we have a skill for building a settings prototype?`

#### `/prototype-builder`

Turns a brief, PRD, FigJam board, Figma design, or description into a working prototype in Beacon or Studio. It works from the repo root, asks for the target when it is unclear, reads your inputs, and presents a plan before building. After approval, it sets up, builds, and checks the result.

For Beacon, run `project-start` first. For Studio, it calls `prototype-create` for setup. Specify the settings and variants you want rather than leaving them to the agent. [Full guide and prompt](/prototyping).

#### `/prototype-create` (Studio only)

Creates a blank Studio prototype or forks an existing merged one. Start the agent inside `apps/studio` to invoke this app-specific skill directly. It gathers the title, description, purpose, tags, settings, and variants, then uses scripts for setup and validation. You can keep iterating locally before opening a PR.

### Starting a project

#### `/project-start`

Sets you up to begin work. Creates a Jira ticket (or takes an existing one), names your branch, and checks that your tools are configured. If Jira CLI isn't set up, it walks you through the setup step by step.

When it's done, it suggests `/shaping` as the next step but doesn't start it automatically. You decide when you're ready.

**Use when:** You're starting something new and need a ticket and branch.

#### `/framing-doc`

Use this before `/shaping` when you're working from raw source material — transcripts, Slack threads, Jira tickets, research notes. It turns that material into an evidence-based problem frame. Every claim in the Problem and Outcome must trace back to a specific person or moment in the source, or it gets dropped.

**Use when:** You have raw material and need to distill it into a solid problem frame before shaping begins.

#### `/shaping`

Interactive conversation that helps you define the problem and pick a solution approach before building. Not a form to fill out. A back-and-forth with Claude where you work through what you're trying to solve.

**Shaping answers:** what problem are we solving, and what's the right approach?

**Three ways in:**
- **Start from the problem.** Describe what's wrong, what users need, what constraints exist. Requirements emerge from the conversation.
- **Start from a solution.** You already have an idea. Sketch it as Shape A. Claude extracts the implicit requirements from it, then checks what it misses.
- **Start from a vague goal.** You know roughly what you want but can't articulate it yet. Claude runs a Discovery session first, exploring with you before any shaping begins. It won't push you to pick a shape until the problem is clear.

All paths end at the fit check.

**What you end up with:**

**R: Requirements** (R0, R1, R2...): What must be true for any solution to be correct. Not a feature list. Not acceptance criteria. The outcome, not the mechanism. Each R gets a status: *core goal*, *must-have*, *nice-to-have*, or *out*. Max 9 top-level.

**S: Shapes** (A, B, C...): Mutually exclusive solution approaches. Each shape is broken into numbered parts (A1, A2, A3...) describing exactly what you'd build.

Parts are mechanisms, not intentions:

*Intention:* "Handle Power Dialer billing"
*Mechanism:* "New Transaction entries with `type: 'Power Dialer'` and `walletSource: 'Calling Commit'` added to MOCK_TRANSACTIONS in billingMockData.ts"

**Fit check**: Requirements as rows, shapes as columns. Binary pass/fail. If a shape passes everything but still feels wrong, there's a missing requirement. This is what turns a discussion into a decision. For early-stage work where requirements aren't fully defined yet, there's also a macro fit-check: two columns (Addressed? / Answered?) that catch gaps before committing to a shape. 🟡 change markers track what shifted during the session.

**Upstream/downstream skill references**: The shaping document includes pointers to the skills that feed into it (e.g. `/framing-doc`) and the skills it feeds into (e.g. `/breadboard`). Useful orientation for knowing where you are in the pipeline.

**One shape or multiple?** Use multiple shapes when there's a real architectural fork: "do we build a new controller or extend the existing one?" Use a single shape when the solution space is already constrained, the PRD specifies the approach, or there's no meaningful choice to make.

**When to skip shaping:**
- Single-file bug fix
- One obvious approach with no alternatives
- PRD fully specifies the mechanism

**Don't skip shaping when:**
- Multiple valid approaches exist
- Scope is unclear or contested
- You need alignment before building

**Use when:** You have a problem to solve, a solution to test, or even just a vague goal. You don't need it figured out before you start.

#### `/kickoff-doc`

For collaborative work. Takes a kickoff transcript and turns it into a territory-based builder reference document. Design decisions go inline where they matter, not in a grab-bag section at the end. Structured around the work, not the timeline.

**Use when:** You're kicking off a project with others and need a shared reference that captures what was decided and where it applies.

#### `/breadboard`

Takes the selected shape and traces every part of it through the real codebase. You cannot breadboard without a selected shape.

**Breadboarding answers:** where exactly does this approach land in the code, and how does everything wire together?

One rule: every name in a breadboard must point to something real in the code. Not "the database" but `MOCK_TRANSACTIONS`. Not "the filter logic" but `sortedAndFilteredTransactions` in `UsageHistoryTab.vue`. Vague names reveal vague thinking.

**The four tables:**

**P: Places**: Bounded contexts of interaction. Test: can you interact with what's behind this affordance without leaving the current context? No means it's a different Place. A modal is a Place. A dropdown is not.

**U: UI affordances**: What the user sees and acts on. Vue components, Dialtone components, buttons, inputs, rendered rows.

**N: Code affordances**: What makes the UI work. Composables, computed properties, functions, mock data exports.

**S: Data stores**: Where data lives. Mock data exports, Pinia stores, reactive refs, IndexedDB tables.

**Wiring: two columns every row has:**
- **Wires Out**: what this affordance triggers or calls
- **Returns To**: where this affordance's output flows back to

Example:
```
User selects "Power Dialer" from the channel filter (U13)
  Wires Out: N7 — sortedAndFilteredTransactions recomputes
  N7 Returns To: U18 — transaction table re-renders with PD rows only
```

**New affordances** added by the shape get a prefix: UA1 (new UI from Shape A), NA1 (new code from Shape A). Once built, they drop the prefix and become standard U and N.

**Completeness check** before finishing:
1. Every U that displays data has an N feeding it
2. Every N that changes state has a U showing it
3. Every IndexedDB write has a BroadcastChannel notify (Beacon architecture)

A UI affordance with no data source means something is missing. The breadboard catches that before you write a line of code.

**Slicing: how breadboarding ends:**

Affordances group into **vertical implementation slices** (V1, V2...). Each slice cuts through all layers (UI, logic, data) and ends in something you can demo. "See Power Dialer rows in the table, filter to PD only" is a valid slice. "Set up all the mock data" is not. Nothing to show.

Max 9 slices. If you need more, the shape is too large for one cycle. Each slice becomes a PR.

Slices follow a consistent order:
1. Foundation and data layer
2. Core component
3. Required functionality (may be multiple slices)
4. Code extraction for anything the new work displaced
5. Unit tests and documentation

**How slices ship:** One branch per slice, merged directly into main. No parent feature branch. Put the feature behind a Feature Flag until all slices are done. That way each slice ships safely without exposing unfinished work.

**Where the documents go:** Keep working plans in session notes or the target app's `docs/plans/` folder. Planning files must stay out of commits and PR history. PR prep checks this boundary. Preserve the useful decisions in the Jira ticket or another durable reference before removing working plans.

**Use when:** You've picked a direction in `/shaping` and need to plan how to build it.


### Building

#### Building from an approved plan

For a prototype, use `prototype-builder`. For a smaller component or implementation task, describe what you need and let the agent choose supporting skills such as `component-work`. Use `skill-search` when you want to see the available options first. The old `feature-team` and `component-create` names are no longer in the current skill inventory.

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

Prepares your work for review. It captures what changed, runs adversarial and relevant specialist reviews, assesses findings, resolves authorized issues, then runs the final checks for the affected apps. Review happens before the final gate suite, so defects found by reviewers are fixed before validation.

The report distinguishes ready work, fixes still needed, and decisions still needed. It does not create the PR.

**Use when:** You think the work is ready to share.

#### `/skeptic-review`

Runs the read-only adversarial route through PR prep. A general reviewer looks at the diff, then focused reviewers are selected from what changed:

| Lens | What it checks |
|---|---|
| Data, state, and concurrency | Schemas, shared state, races, and delayed updates |
| Test value | Whether generated tests provide useful evidence |
| UI, interaction, and accessibility | Behavior, keyboard access, and regressions |
| Dialtone adherence and gaps | Correct component choices against the installed version; whether a claimed gap is real |
| Security, privacy, and permissions | Access boundaries and exposure |
| Workflow and mutation safety | GitHub Actions, scripts, and safe writes |
| Contracts, validation, and compatibility | APIs, schemas, packages, CLI, and routes |
| Performance and scalability | Costs that grow with data or usage |
| Scope and simplicity | Unnecessary complexity and changes outside the task |

Studio work often needs fewer lenses than Beacon work, but file types and risk decide. A focused skeptic review does not replace the full PR readiness checks.

#### `/pr-create`

Creates or updates the PR after PR prep. Titles now use area-scoped Conventional Commits, for example `feat(beacon): add a new interaction` or `feat(repo, beacon, design, studio): update shared tooling`. The scope identifies the affected areas. Let the skill format the title.

Include the verified Dialtone gaps from the final report in the PR description, separating gaps in the prototype from gaps in its settings controls. Ask for a draft PR when you want an early direction check.

**Use when:** PR prep is complete and you are ready to share.

#### `/pr-complete`

After your PR is merged. Transitions the Jira ticket to Done, wraps session notes, returns you to the main branch. Asks what you want to work on next.

**Use when:** PR is merged. You're closing the loop.

#### `/pr-comments`

Pulls automated review comments from your PR and helps you triage them: which ones matter, which ones to fix, which ones to dismiss.

**Use when:** Your PR has review feedback and you want to work through it systematically.

### Along the way

#### `/breadboard-reflection`

Two-phase audit for verifying a breadboard against the actual code. First phase looks at what's there (SEE). Second phase checks if it's right (REFLECT). Includes a naming test — affordances should use single-verb names — and a design smells catalog. PR prep can also use it when the change has a breadboard.

**Use when:** You want to verify your breadboard reflects what was actually built, not just what was planned.

#### `/branch-prune`

Cleans up local branches that were deleted on the server when a PR was merged or closed. Keeps your local repo tidy without having to remember the git commands.

**Use when:** Your branch list is cluttered with old work.

#### `/bug-hunt`

Systematically searches for bugs in a feature. Doesn't just run tests. Thinks about edge cases, unexpected states, and interactions between components.

**Use when:** After building, when you want to stress-test before sharing.

#### `/perf-check`

Analyzes components for performance issues: unnecessary re-renders, missing memoization, heavy computations in render paths.

**Use when:** Your feature touches rendering or data loading and you want to make sure it's smooth.

#### Jira updates

Ask the agent to create or update a ticket using the shared `jira` skill. `project-start` handles the ticket and branch at the start; `pr-complete` closes the loop after merge.

#### `/debug-trace`

When a bug isn't getting resolved and Claude keeps reading more and more code to find it, stop and use this instead. It adds debug logs to the specific code you point at. Those logs output to the browser console at runtime. Share the console output with Claude to pinpoint the problem. Much faster than letting it read files.

**Use when:** You're going in circles on a bug and need to see actual runtime state, not more code analysis.

#### `/prototype-migrate`

For existing Design Studio work. The `prototype-analyzer` agent reads your prototype, compares it against Beacon's architecture, identifies what already exists in Beacon, what's missing, what conflicts with Beacon's patterns, and estimates complexity.

The output is a gap analysis that feeds directly into `/shaping`. Your prototype isn't wasted. It's a starting point.

One thing to know: Design Studio prototypes can't be dropped into Beacon as-is. They have to come over in pieces. This command maps the gap so you know which pieces, in what order.

**Use when:** You have a Design Studio prototype and want to plan its Beacon version.

### Advanced (you'll find these when you need them)

#### `/data-trace`

Traces how data flows through Beacon's three layers (UI components → controllers → IndexedDB). Useful for debugging when data isn't showing up where you expect it.

#### `/migrate-component`

Migrates old components to current Vue 3 patterns and Beacon conventions. TypeScript improvements, accessibility fixes, composable extraction.

#### `/deps-audit`

Audits project dependencies: security vulnerabilities, available updates, unused packages, bundle sizes.

#### `/batch` (Claude Code built-in)

Orchestrates the same change across many files in parallel. Each unit gets its own isolated copy of the codebase, runs `/simplify` on its changes, and opens a PR. For when you need the same pattern applied across 30+ files.

#### `/loop` (Claude Code built-in)

Runs a prompt on a recurring interval within your session. For watching a deploy or monitoring a process. Session-scoped: exits when you close the terminal.

## Agents and supporting skills

Some skills are entry points you start yourself; others are building blocks the agent loads when the task needs them. A shorter menu does not mean the knowledge disappeared.

`prototype-builder` delegates the approved plan to a prototype implementer and reviews the result. PR prep selects focused reviewers for the changed files. Use `skill-search` to discover current agent profiles rather than relying on an old list.

Supporting skills include `dialtone-usage`, `component-work`, `code-quality`, `unit-testing`, `jira`, and `delegate`. Beacon also has `frontend-patterns`, `feature-flags`, `permission-patterns`, `mock-engine`, and `dialpad-design`. Studio has its own prototype-creation workflow.

**Dialtone:** `dialtone-usage` checks the installed version and the available app components before custom UI. Ask the agent to verify a missing component or token against those sources before calling it a gap. A mismatch in the source Figma file may call for snapping to existing Dialtone typography rather than adding a new component. [How to report gaps](/prototyping#dialtone-and-verified-gaps).

**Design judgment:** ask for a review of hierarchy, interaction, motion, accessibility, and edge states. The agent helps identify problems; you still evaluate the prototype in the browser.

## Rules

Rules auto-load based on what file you're editing. When you're working in `./src/`, Claude automatically follows these.

**Root rules** cover code guidelines, commit messages, Dialtone usage, frontend style, and Vue/TypeScript conventions.

**Dialtone guidance** documents: required props, correct import pattern (`import { DtButton } from "@dialpad/dialtone/vue3"`), usage examples, and what NOT to do. The agent should use supported Dialtone components and tokens before custom equivalents. Check the actual output; a rule is guidance, not a guarantee.

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
