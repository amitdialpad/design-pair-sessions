# Share your work

[← Evaluate and iterate](/evaluate) · Step 4 of 4

Give people a working experience and a clear question. Share while their feedback can still change the direction. A short exploration shown today can reveal a misunderstanding before it costs the team days.

You can share a recording, a local walkthrough, or your findings while a hosted preview is being prepared. Choose the simplest form that lets people give useful feedback.

## Prepare the preview

Run `pr-prep` before `pr-create`: `/pr-prep` and `/pr-create` in Claude, or `$pr-prep` and `$pr-create` in Codex.

PR prep reviews the changed files, selects the relevant specialist checks, and reports fixes or decisions still needed. Address those before creating the PR. Use `pr-create` to format the title, explain the change, and open the PR. Ask for a draft when the work is still exploratory.

Include the prototype's purpose, the states or variants to try, known limitations, and the validation completed. If Dialtone gaps remain, copy the verified findings from the final report and separate prototype UI gaps from settings-control gaps.

Open the deployed preview yourself before sharing it. Check the exact route, the main flow, and the settings. A successful build does not establish that the shared link works.

## Ask for a specific review

```text
I’m testing whether this comparison helps people choose a plan.
Preview: [exact link]

Try the five-plan variant, switch to annual billing, and select a plan.
Is the difference between the options clear? Does the confirmation give
you enough confidence to continue?

The payment step is a placeholder. I’m looking for feedback on comparison
and selection before refining that step.
```

Tell reviewers what they can change, where to begin, and which decisions are open. Use a short recording when it helps orient them, alongside the interactive preview.

## Make progress visible

With each update, say what you tried, what changed, how much time you spent, and what you need next. Make open questions and blockers easy for someone else to act on. A 20-minute sketch and a two-day prototype invite different expectations; tell people which they are reviewing.

Bring in the people whose perspective could change the decision: your team, relevant partners, leadership, or customers when appropriate. For customer-facing changes or work another team depends on, align with them before committing to it.

## Turn feedback into the next iteration

Bring comments back to the agent with enough context to identify the affected screen or state. Separate bugs from choices that need a design decision. Use `pr-comments` to triage PR feedback.

Ask the agent to apply the agreed changes, [evaluate the result again](/evaluate), and share the updated preview. Keep a short record of decisions so the next session can pick up where you left off.

Merging depends on the app's current review policy and your team's approval. Sharing a draft preview is a useful outcome on its own.

## Keep learning

[Skills and tools](/toolkit) explains the workflows behind these steps. [Design judgment and process](/process) goes deeper into the decisions. The optional [pair sessions](/resources#pair-sessions) are available when learning together would help.
