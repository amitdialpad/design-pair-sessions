# Build a prototype

Bring the problem, the source material, and the decisions you want to test. `prototype-builder` helps turn them into a plan and a working prototype. Your job is to decide whether the result helps you learn what you need to learn.

## Start a build

Open your agent in the Design repo root and state whether you want Studio or Beacon. Use `/prototype-builder` in Claude Code or `$prototype-builder` in Codex. For Beacon, run `project-start` first for a ticket and branch. For Studio, the builder handles setup after plan approval.

If you are still choosing a target or setting up access, use [Start here](/start-here). You can return to any part of this guide as your question changes.

## Give it a useful starting prompt

```text
$prototype-builder Build this in Studio.

Purpose: Help us evaluate how people compare two plan options.
Inputs: [PRD link], [Figma frame link], and the attached research notes.
Focus: Comparison layout, selecting a plan, and the confirmation state.
Fidelity: Recommend a stage that fits this question before building.

Settings I want:
- Switch between two plans and five plans.
- Toggle monthly and annual billing.
- Show normal, empty, and error states.

Variants: A compact table and a card layout using the same data.
Do not add other settings or variants without proposing them in the plan.

Use supported Dialtone components and tokens. Explain any verified gaps,
separating the prototype UI from the settings controls.
Show me the plan before building.
```

In Claude, change the first line to `/prototype-builder`. For Beacon, run `project-start` first, say where the experience belongs, and point to the closest existing screen to follow.

Give the agent as much relevant context as you can: PRDs, research notes, screenshots, Figma or FigJam links, and Google Docs, Sheets, or Slides. If it cannot read a source, resolve access or provide its contents before treating the plan as source-grounded. Josh found connector authorization easiest in the desktop apps; the CLI can then pick up the configured access.

Be explicit about what settings should help you test. Extra knobs are not automatically useful. Name their defaults, the states they reveal, and the comparisons you want to make.

## Review the plan, then build

1. The skill reads your inputs and settles the target, fidelity, focus, and open decisions.
2. It writes a plan and shows you what it intends to build. Correct missing states, unhelpful settings, or assumptions here.
3. After approval, it sets up the prototype and builds from that plan. Studio's creation workflow uses scripts for scaffolding and validation rather than asking the LLM to hand-copy the template.
4. It checks the result, including Dialtone usage, the app's required checks, and a browser walkthrough of the planned interactions.
5. Its handoff gives you the location, how to run it, what was built, assumptions, validation results, and anything still unverified.

Open the prototype yourself. Try every requested state and variant. Evaluate hierarchy, copy, keyboard use, motion, and the edges. Josh's first-shot example was useful after roughly 30 minutes with one starting prompt, but that is an example, not a time estimate or a substitute for your review.

## Dialtone and verified gaps

Beacon's upgrade to **Dialtone 10.5.1** merged in [Design PR #185](https://github.com/dialpad/design/pull/185). Each Studio prototype owns its dependency versions, so check the installed version rather than assuming it matches Beacon.

The agent should reuse existing app components and Dialtone before custom UI. If something appears missing, have it verify the installed components, tokens, and documentation. Some apparent gaps are source-design mismatches, such as typography sizes in Figma that do not match the current Dialtone ladder.

Include the final report's verified gaps in your PR description. Separate them into:

- **Prototype UI:** capabilities needed by the experience you are testing.
- **Settings controls:** capabilities needed by the controls used to explore it.

For each gap, explain the need, the closest supported building block, what is missing, and the workaround. This helps Francis and Josh distinguish component work from documentation improvements.

## Use controls that help you test

In Studio, the shared shell provides settings, appearance controls, and About information. Specify which controls your experiment needs. See [Studio controls and releases](/studio) for the current shell, versioning, and announced additions.

When you need another skill, use `skill-search`. [Skills](/skills) explains the workflows available to your agent.
