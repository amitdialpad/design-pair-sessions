# Session 2: Pair build

**Format:** Your facilitator drives first half. You drive second half. Your facilitator navigates.

**Duration:** 60 min

This is the actual pairing session. We pick a small, real task and build it together. The driver controls Claude Code. The navigator watches, asks questions, and catches things the driver misses.

## Part 1: Your facilitator drives (25-30 min)

We start from a real problem. Not a tutorial exercise. Something small enough to finish but real enough to matter.

Your facilitator drives through the full rhythm:

1. **Understand the task.** Pull context from Jira or a PRD. What are we building? What are the constraints?
2. **Explore options.** Maybe check Figma for visual direction. Maybe ask Claude what Dialtone components fit.
3. **Build the first version.** Describe what we want. Claude generates code. Check it in the browser. React to what we see.
4. **Iterate.** Something won't be right. Fix it. Something else won't be right. Fix that too. This is the loop.
5. **Evaluate.** Does it look right? Feel right? Handle edge cases? Follow the design tenets?

**Your job as navigator:**
- Ask "why did you choose that?" when a decision isn't obvious
- Call out things that look off visually (you'll spot things Your facilitator might miss)
- Ask "what happens if...?" for edge cases (no data, too much data, error state)
- Don't hold back. The point of pairing is two sets of eyes, two perspectives.

## Part 2: You drive (25-30 min)

You take over Claude Code. Your facilitator navigates.

You'll make changes to what we just built, or start a new small piece. The thing you're doing:

- **Describe** what you want to Claude in plain language
- **Look** at the result in the browser
- **React** honestly. "The spacing is wrong." "That's not the right component." "What about the hover state?"
- **Tell Claude** to fix what's wrong
- **Check** the result again

Your facilitator is there if you get stuck. But the goal is for you to feel the loop: describe, see, critique, adjust. That's the whole thing.

**Things you might try:**
- Change a color, spacing, or component choice
- Add a missing state (loading, empty, error)
- Ask Claude to explain something in the code you don't understand
- Ask Claude to search Dialtone for a component or icon

## Part 3: Reflection (5 min)

What felt natural? What felt scary? What do you want more practice with?

## Before next session

- Try one thing on your own. Open Claude Code in any project and ask it a question. Just a question, not a build. Something like: "What Dialtone components would work for a settings panel?" See what comes back.
- If you want more: pick one small thing from what we built today and make a change to it on your own.

## Reference

- [The process](/process) for the workflow we followed
- [The toolkit](/toolkit) for command reference
- [Getting started](/cheat-sheet) for prompts to try
