# Evaluate and iterate

An agent saying “done” is your cue to use the prototype. Walk through the experience as the person it is designed for, starting from where they would actually enter.

## Check the question you started with

Can you now evaluate the layout, interaction, or flow you wanted to test? Look for assumptions the agent made and behavior that was left as a placeholder. A polished screen can still miss the purpose of the prototype.

## Try the experience and its edges

| Check | What to try |
|---|---|
| Flow and clarity | Can someone understand the purpose and find the next action? |
| Visual hierarchy | Do type, spacing, grouping, and emphasis support the decision? |
| Interaction | Click through, go back, cancel, retry, and change your mind. |
| States and data | Try empty, loading, error, long text, and large data sets where relevant. |
| Accessibility | Use the keyboard, check focus, and review labels and contrast. |
| Appearance and size | Try a smaller viewport and the modes and density settings the prototype supports. |
| Dialtone | Ask the agent to verify component and token choices against the installed version. |

In Beacon, also check the relevant roles, permissions, and feature-flag states. In Studio, test every setting and variant you requested: the controls should change the experience in a useful way.

## Give feedback the agent can act on

Describe what you did, what happened, what you expected, and why it matters.

```text
When I switch to five plans, the primary action disappears below the fold.
People should be able to compare the options and continue without hunting.
Keep the current comparison data and adjust the layout. Show me the result
at a narrow viewport too.
```

Fixes can also reveal a design decision. If the agent proposes a different interaction, evaluate that choice before letting it spread across the prototype.

## Make decisions easier to review

When there are several options, ask the agent for a reviewable artifact: a side-by-side comparison, a list with toggles, or a plan with a place to comment. Use it to make specific decisions, then have the agent record those decisions in the source plan so they survive the session.

## Repeat the loop

Describe → inspect → give feedback → revise → inspect again.

Ask “How do I test this?” for a checklist based on what was built. Report passes and failures, then recheck the affected flow after a fix. Keep the plan or notes aligned with decisions you make during iteration.

When the prototype answers the question well enough for someone else to evaluate it, [share your work](/share). Directional feedback can happen before every detail is polished.
