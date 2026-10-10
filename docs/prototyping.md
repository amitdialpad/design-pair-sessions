# Prototyping in Beacon and Studio

Bring the problem, the source material, and the decisions you want to test. `prototype-builder` helps turn them into a plan and a working prototype. Your job is to decide whether the result helps you learn what you need to learn.

This guide combines Josh Hynes's team updates with the Design repo's merged changes, checked on **10 October 2026**. Features described below apply to the current template and tooling; an older prototype may keep its earlier shell and dependencies.

## Choose where to build

| Beacon | Studio |
|---|---|
| An experience inside the existing product | A standalone experiment on a blank canvas |
| Follow the existing screens, data patterns, roles, and permissions | Explore a flow, layout, or interaction without the full product |
| Run `project-start` first for a ticket and branch | `prototype-builder` handles new-prototype setup after plan approval |
| Match Beacon's existing level of fidelity | Agree on the fidelity and focus in the plan |

Shared skills work from the **Design repo root**. You do not need to start inside `apps/beacon` or `apps/studio` to use `prototype-builder`. State the target in your prompt; if it is unclear, the skill asks. App-specific skills such as Studio's `prototype-create` may still need a session inside that app's folder when invoked directly.

Use `/prototype-builder` in Claude Code or `$prototype-builder` in Codex. The same `/` versus `$` convention applies to shared skills such as `project-start`, `skill-search`, `pr-prep`, and `pr-create`.

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

## The current Studio shell

The shared shell merged in [Design PR #190](https://github.com/dialpad/design/pull/190). It keeps the prototype visible while you inspect or adjust it:

- A centered toolbar opens **About** on the left or **Settings** on the right.
- The inspectors use Dialtone's resizable panels and bring the canvas inward. Closing the inspector restores the full-width canvas.
- Only one inspector is open at a time. `Shift+S` toggles Settings outside editable controls; Escape closes the active inspector. `?settings=open` opens Settings when sharing a URL.
- Appearance controls include light, dark, and system mode, text size, density, material, color theme, and high contrast. Use these to stress-test the idea.
- About reads the prototype's title, description, status, purpose, author, Dialtone version, and tags.

Josh's earlier preview described a toolbar that hides or minimizes with pointer position. The merged shell is the reference for current behavior. Existing prototypes do not all acquire it automatically.

**Versioning:** [Design PR #189](https://github.com/dialpad/design/pull/189) added versioned studio-kit releases. New Vue prototypes choose an exact released version, using the latest approved registry release by default. Existing prototypes stay on their pinned version until explicitly upgraded. The shared-shell package still has release and migration checkpoints, so a merged template change does not by itself prove the latest shell is available in every prototype.

## Dialtone and verified gaps

Beacon's upgrade to **Dialtone 10.5.1** merged in [Design PR #185](https://github.com/dialpad/design/pull/185). Each Studio prototype owns its dependency versions, so check the installed version rather than assuming it matches Beacon.

The agent should reuse existing app components and Dialtone before custom UI. If something appears missing, have it verify the installed components, tokens, and documentation. Some apparent gaps are source-design mismatches, such as typography sizes in Figma that do not match the current Dialtone ladder.

Include the final report's verified gaps in your PR description. Separate them into:

- **Prototype UI:** capabilities needed by the experience you are testing.
- **Settings controls:** capabilities needed by the controls used to explore it.

For each gap, explain the need, the closest supported building block, what is missing, and the workaround. This helps Francis and Josh distinguish component work from documentation improvements.

## Find skills and prepare the PR

Use `$skill-search` in Codex or `/skill-search` in Claude to find skills, agents, and rules for a task. The Claude menu now emphasizes entry points; supporting skills remain available to the agent even when hidden from that menu. [Design PR #168](https://github.com/dialpad/design/pull/168) introduced this discovery workflow.

Run `pr-prep` before `pr-create`. PR prep now includes a general adversarial review and focused lenses selected from the changed files, including UI and accessibility, Dialtone adherence, test value, data and state, and security. `skeptic-review` is still available as a separate read-only route. [See the lenses](/toolkit#skeptic-review) and [the merged change](https://github.com/dialpad/design/pull/181).

Use `pr-create` to open the PR with an area-scoped Conventional Commit title: `feat(beacon): ...` for Beacon, or `feat(repo, beacon, design, studio): ...` for shared work. The skill formats this for you. [Design PR #174](https://github.com/dialpad/design/pull/174) introduced the title convention.

## Use interactive artifacts for feedback

Josh also shared a useful pattern for Claude.ai: ask for an interactive artifact when a decision is easier to make visually than line by line. A list of skills with on/off toggles made choosing the user-facing menu quick. A report with comments let him resolve 29 plan changes with the agent as he reviewed.

Try asking for a reviewable artifact with the options, your current choice, and a place to leave specific feedback. Then have the agent apply that feedback to the source plan. Your plan should retain the agreed decisions after the artifact session ends.

## Announced work to watch

These are Josh's announced directions, **not a promise that they are ready to use**:

| Item | Status checked 10 October |
|---|---|
| `design-spec` for evidence-based build plans | Announced; no skill under this name in the current repository inventory |
| Settings in picture-in-picture | The shell has an optional hook, hidden unless a working callback is supplied; general availability is not established |
| A Prompt area for copying a prototype's starting prompt | Announced; not verified in the merged shell |
| Commenting package inspired by Amit's review workflow | Callout API foundations have merged; a usable Studio commenting experience is not established by those changes |
| Reusable settings template library | Announced; not verified as available |

About, resizable inspectors, appearance controls, and versioning have moved beyond that earlier announcement. Use the current repository and `skill-search` to check availability before planning around the remaining items.

Josh credits Josh Everhart's groundwork for enabling these additions. Bring questions and suggestions back to the team with a concrete example of what you wanted to test and what got in the way.
