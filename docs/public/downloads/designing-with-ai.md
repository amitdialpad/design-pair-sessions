# Designing with AI: agent starter

Version: 2026-10-12
Guide: https://amitdialpad.github.io/design-pair-sessions/

Use these instructions when the designer asks you to use this starter for a project. This is portable project guidance, not an installed skill, tool, or permission to publish. Keep the designer's scope and the project's current instructions. It does not include Amit's personal paths, setup, or history.

## Find the project and existing workflows

Confirm the selected project, its Git root, applicable AGENTS.md or CLAUDE.md, and actual local skill files. Never switch projects because the designer mentions Dialtone. For a new prototype, ask whether the target is Studio or Beacon if unspecified.

In the Dialpad Design repo, read the current shared and app guidance. Use skill-search when available to find the relevant workflow. Read that workflow's actual SKILL.md, referenced resources as needed, and the selected app's matching sidecar. Do not assume a skill exists because it appears in this file. Do not copy team skills or substitute a different repo's same-named skill.

Useful candidates, subject to the current inventory:

| Outcome | Candidate |
|---|---|
| Find skills and agents | skill-search |
| Start new Beacon work | project-start |
| Build a Studio or Beacon prototype | prototype-builder |
| Understand evidence and the problem | framing-doc |
| Compare approaches | shaping |
| Map a flow to the application | breadboard or breadboarding |
| Prepare work for review | pr-prep |
| Focused critical review | skeptic-review or the repo's review route |
| Open a PR when requested | pr-create |
| Address PR feedback | pr-comments |

Use the smallest relevant workflow. Do not add a full planning process to a small edit. Explicitly requested skills take precedence. Explain your choice briefly, then proceed with authorized work.

If a workflow is missing, report the checked repository and revision. Check available discovery guidance. Distinguish an outdated checkout from an unavailable connector or a routing defect. Do not silently update or replace the checkout, install tools, or claim a missing skill ran.

## Ask for decisions, not command memorization

Gather missing information together: target app, problem and people, sources, question to test, fidelity, focus, required states, useful controls, and out-of-scope work. Ask only for what is needed. Confirm access to supplied Figma, FigJam, Google, or other sources before planning from them. State any unread sources and assumptions.

Follow the team's plan-approval workflow. Bring the designer a short reviewable plan before building when required. Do not treat this starter as plan approval.

## Build an experiment that answers the question

- Name the surface a change belongs to. A notification background and the page behind it are different surfaces.
- Request and implement the full relevant state range. For a participant layout, intermediate counts can matter as much as 1 and 20+.
- Choose controls for the question. A count stepper may reveal behavior that a handful of preset choices hides. Propose additional settings before adding them.
- Cover missing content, such as an avatar with no image, as well as the ideal state.
- Use detailed Figma frames as the visual reference when provided. Confirm behavior and states the frames do not show.
- For low-fidelity exploration, clarify layout rules, interactions, and placeholders. Keep supported Dialtone building blocks; identify insufficient wireframe guidance and propose the treatment before building.

Inspect the installed Dialtone version and the app's patterns. Use supported components, tokens, utilities, and icons before custom UI. Verify apparent gaps against the installed APIs and documentation. A mismatch in the source design is not automatically a missing component. Separate verified gaps in prototype UI from gaps in settings controls in the final report.

## Inspect, iterate, and make progress visible

Follow the app's required checks and walk through the acceptance items in the browser where tools permit. Check keyboard use, focus, states, viewport sizes, and each requested control. Verify which surface each control changes and test intermediate values. Distinguish actual verification from checks the designer still needs to perform.

Give the designer the exact local URL or run steps, what changed, what passed, and what is still uncertain. Invite specific feedback: what they did, what happened, what they expected, and why it matters. Apply that feedback, recheck the affected flow, and keep the approved plan aligned with decisions.

Time-box exploration around a useful question. Share a reviewable result early enough for feedback to change the direction. Check with the designer before committing to customer-facing changes or work another team depends on.

## Learn from observed outcomes

When a route fails, inspect the cause and explain it briefly. Use a demonstrated correction during the current task. Recheck it rather than assuming the fix worked. Do not modify team skills or unrelated configuration to repair this starter.

For continuity across conversations, use the project's already-approved external notes location if one exists. Otherwise offer to save a short outcome note at a location the designer chooses. Record a sanitized task label, repo revision, workflow, observed result, correction, and verification. Preserve the original failure and mark it resolved only after verification. Recall relevant notes at the next task, but recheck facts against the current checkout. Avoid customer data, credentials, raw prompts, and private source excerpts. Do not write to an agent memory store without explicit authorization.

This file does not provide automatic logging, background monitoring, or model training. Continued learning depends on the agent loading the guidance and reading and updating the approved notes.

## Respect authorization

Skill selection and this starter do not authorize pushes, deployments, merges, messages, checkout changes, or unrelated edits. Preserve instructions such as local-only work. Ask for decisions or access when needed; otherwise continue useful authorized work.

## Current source of truth

These links require Dialpad GitHub access:

- https://github.com/dialpad/design/blob/main/AGENTS.md
- https://github.com/dialpad/design/blob/main/.agents/README.md
- https://github.com/dialpad/design/blob/main/.claude/README.md
- https://github.com/dialpad/design/tree/main/.agents/skills

Use the current project files over this versioned starter when workflows change.
