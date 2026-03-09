# Session 2: Pair build

**Format:** You work on a real task together. Both of you thinking throughout. One at the keyboard at a time.

**Duration:** 60 min

You're coming in with a breadboard from Session 1. This session is the build. Your facilitator takes the first ticket, you take the next one.

## Part 1: Facilitator builds the first ticket (20 min)

Your facilitator picks up the first ticket from the breadboard and runs `/feature-dev`. You're not watching. You're in it: calling things out, questioning decisions, catching what looks off.

Watch specifically for:
- How they describe what they want to Claude. Plain language, not technical spec.
- How they evaluate the result in the browser. Spacing, alignment, hover states, edge cases.
- How they react when something is wrong. They describe it, not debug it.
- How they check accessibility before moving on: *"Check this for keyboard navigation, contrast, and focus states."*

## Part 2: You drive (35-40 min)

You take the next ticket. Your facilitator navigates.

- **Describe** what you want to Claude in plain language
- **Look** at the result in the browser
- **React** honestly: "the spacing is wrong", "that's not the right component", "what about the hover state?"
- **Tell Claude** to fix it
- **Check** the result again

Repeat until it's right. Then check accessibility before you move on.

When you're done: run `/pr-create` to get a preview link and send it in Dialpad. That's the full loop.

**If you're not sure where to start:**
- Ask Claude what the ticket needs. It has the breadboard context.
- Add a missing state (loading, empty, error)
- Ask Claude to search Dialtone for the right component or icon

## Part 3: Reflection (5 min)

What felt natural? What felt scary? What do you want more practice with?

## Before next session

- Try one thing on your own. Open Claude Code in any project and ask it a question. Just a question, not a build. Something like: "What Dialtone components would work for a settings panel?" See what comes back.
- If you want more: pick one small thing from what we built today and make a change to it on your own.

## Reference

- [The process](/process) for the workflow we followed
- [The toolkit](/toolkit) for command reference
- [Getting started](/cheat-sheet) for prompts to try
