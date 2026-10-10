# Skills

Describe what you want to accomplish. Skills give the agent a repeatable way to help you: frame the problem, build a prototype, check the work, or prepare it for review.

**You do not need to learn a command for every task.** In a configured Design repo, the agent can select skills that match your request. Name a skill when you want to start a particular workflow explicitly. You still review design decisions and approve the build plan.

New here? Follow [Start here](/start-here). Looking for a connector or an app? See [Tools](/tools).

## Pick the outcome you need

| When you need to… | Skill | What it gives you |
|---|---|---|
| Find the right help | `skill-search` | Relevant skills, agents, and rules from the current repo |
| Start new Beacon work | `project-start` | A ticket, a branch, and setup checks |
| Turn an idea or design into a prototype | `prototype-builder` | A reviewable plan, a Studio or Beacon prototype, and a validation handoff |
| Create a blank Studio prototype | `prototype-create` | A new prototype or a fork, with scripted setup; use inside Studio |
| Understand the problem in research or conversations | `framing-doc` | A problem frame tied to source evidence |
| Compare approaches before building | `shaping` | Requirements, possible approaches, and a fit check |
| Map a flow to the actual application | `breadboard` | Places, UI, code, data, connections, and demonstrable slices |
| Check whether your branch is ready to share | `pr-prep` | Relevant reviews, fixes within your authorized scope, final checks, and a readiness report |
| Get a focused critical review | `skeptic-review` | Read-only findings from the relevant review lenses |
| Open or update a PR | `pr-create` | A PR with the expected title, description, and evidence |
| Work through PR feedback | `pr-comments` | Triaged comments and the next decisions or fixes |

These are current Design repo workflows, checked on 10 October 2026. They are not all required for every prototype. Use the smallest workflow that answers your question.

## Start with a normal request

**Build:**

```text
Build a Studio prototype from this Figma frame and these research notes.
I want to test comparison and selection. Propose the plan before building.
Use Dialtone and include normal, empty, and error states.
```

**Map an existing flow:**

```text
Show me how this flow connects to the current Beacon screens and data.
Map the existing system before proposing changes.
```

**Prepare for feedback:**

```text
Check whether this prototype is ready for review.
Keep all changes local and tell me what is still unverified.
```

If the agent does not select the intended workflow, ask for it by name. In Claude Code, start your message with `/prototype-builder`; in Codex, use `$prototype-builder`. The same syntax applies to the other skills in the table.

For a new Beacon build, start with `project-start`. For Studio, `prototype-builder` handles setup after you approve the plan. [Build guide and starting prompt](/prototyping).

## What the agent handles in the background

Supporting skills cover Dialtone usage, component work, code quality, testing, Jira, and app-specific behavior. They are building blocks, rather than a checklist for you to invoke.

For example, `prototype-builder` uses `dialtone-usage` to choose supported UI building blocks and reads the target app's setup guidance. PR prep selects reviews based on the actual changes. Ask the agent what it used and what it verified when you need evidence.

**Automatic selection needs setup.** The skills must be available to the agent, and their descriptions must match your request. Importing Dialtone styles or reading a documentation page does not install skills. If a workflow is missing, ask `skill-search` to inspect the current inventory rather than assuming it ran.

## Reviews and your decisions

PR prep can examine interaction and accessibility, Dialtone adherence, state and concurrency, security, compatibility, performance, test value, workflow safety, and unnecessary complexity. It chooses relevant checks for the changed files.

You evaluate the experience in the browser. A readiness report should distinguish verified behavior, remaining issues, and decisions it needs from you. Selecting a skill does not grant permission to push, publish, merge, or send messages.

## Find the current source

The [Design repo skill inventory](https://github.com/dialpad/design/tree/main/.agents/skills) and [designer entry points](https://github.com/dialpad/design/blob/main/.agents/skills/skill-search/references/entry-points.md) are the source of truth. These links require Dialpad GitHub access. App-specific skills may live under the app.

Ask `/skill-search` or `$skill-search` to discover additional workflows, including kickoff documents, checking breadboards, reviewing PRs, and closing out merged work.
