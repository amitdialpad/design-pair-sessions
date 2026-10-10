# Start here

Step 1 of 4 · [Next: Build a prototype →](/prototyping)

Start with a question about an experience. What do you need to understand by using it? A prototype might help you compare layouts, test a flow, or see whether an idea handles realistic data.

## Choose Studio or Beacon

| Choose Studio when… | Choose Beacon when… |
|---|---|
| You want a standalone experiment | You need the idea inside the existing product |
| You are exploring a layout, interaction, or new flow | Existing navigation, data, roles, or permissions matter |
| You need a blank canvas and controls to compare options | You need to follow an established product pattern |

If you are unsure, describe what you want to learn and ask your agent to recommend a target before building.

## Get set up

You need access to the [Design repo](https://github.com/dialpad/design), Claude Code or Codex, and the sources your prototype depends on. Follow the repo's current setup instructions or ask the team for help. Your agent can help check the app's prerequisites and explain errors.

Open the agent in your local Design repo checkout. Shared skills work from the repo root.

- **Claude Code:** invoke skills with `/`, such as `/prototype-builder`.
- **Codex:** invoke skills with `$`, such as `$prototype-builder`.
- **Beacon:** run `project-start` first to create a ticket and branch.
- **Studio:** `prototype-builder` handles prototype setup after you approve its plan.

Authorize the Figma or Google connectors if your source links need them. Confirm that the agent can read the actual files before it plans from them.

## Bring enough context to make decisions

Give the agent the problem, the people involved, the source material, and the question you want to test. Include an existing product screen when it is the pattern to follow.

Name the important states: normal, empty, loading, error, restricted access, or large amounts of data. Specify the settings and variants that will help you compare ideas, along with their defaults. If you want no extra controls, say so.

You do not need to know every skill or write a technical spec. Describe what the experience should do. Use `skill-search` when you need to find a tool.

## Your first useful outcome

Choose a question you can explore in a short session today. Aim for one reviewable flow that answers it, then show what you learned before expanding it. Move between building, evaluating, and sharing as feedback changes the direction. A working prototype is evidence to learn from; the first version will still need your judgment.

[Build a prototype](/prototyping) has a starting prompt and the plan-to-build workflow.
