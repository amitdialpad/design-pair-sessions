# Tools

Tools let the agent do the work: read your source files, inspect Dialtone, run a prototype, and check the result. A [skill](/skills) supplies the workflow for using them.

You describe the outcome and provide access to the relevant sources. The agent should tell you when it cannot read something or when a result has not been verified.

## Where you work

| Tool or environment | What it is for | When you use it |
|---|---|---|
| Claude Code or Codex | Your conversation with an agent that can inspect and change the repo | Describe the problem, review the plan, build, and iterate |
| Studio | Standalone prototypes and experiments | Explore a new layout, flow, or interaction with settings and variants |
| Beacon | Prototypes inside the existing product experience | Test ideas where navigation, data, roles, or permissions matter |
| Browser | Trying the actual experience | Walk through the flow, resize it, use the keyboard, and check the edges |

[Choose Studio or Beacon](/start-here#choose-studio-or-beacon) before building. [Studio controls and releases](/studio) explains the prototype shell.

## What the agent uses

| Tool | What it does | What to ask for |
|---|---|---|
| Dialtone CLI or MCP | Looks up components, tokens, utilities, icons, and documentation | “Verify the available component and its API against the installed Dialtone version.” |
| Figma connector | Reads design context from your source design | “Read this frame and identify the layout, components, and states.” |
| Google Docs, Sheets, or Slides connector | Reads briefs, research, requirements, or structured source data | “Read these sources and flag anything you cannot access before planning.” |
| Jira tooling | Reads ticket context and supports the repo's ticket workflow | “Read the ticket, related work, and acceptance criteria.” |
| Git and GitHub CLI | Manages branches, diffs, pull requests, and review feedback | “Show the diff and review readiness. Keep everything local until I approve a push.” |
| App scripts and checks | Starts the app and runs the checks required for the change | “Give me the exact local URL, what passed, and what remains unverified.” |

The available tools depend on your agent, account access, and project setup. A connector being installed does not establish that it can read a particular file. Ask the agent to confirm access to the sources you supplied.

## Dialtone is the UI source of truth

Use supported components and tokens before creating custom UI. Ask the agent to check the version installed in your prototype; online documentation may describe a different release.

An apparent gap can be a missed component, an unsupported API, or a mismatch in the source design. [Report verified gaps](/prototyping#dialtone-and-verified-gaps), separating prototype UI from settings controls.

## If something is unavailable

Ask the agent to explain what is missing and the smallest setup step needed. Authorize the relevant connector when prompted, or provide the source contents directly. Do not let an unread brief or design silently become an assumption.

[Reference links](/resources) contains official documentation. [Quick reference](/cheat-sheet) has launch commands and common prompts. [Skills](/skills) helps you choose a workflow.
