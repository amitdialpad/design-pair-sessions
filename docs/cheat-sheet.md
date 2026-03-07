# Getting started

Quick reference. Print it, bookmark it, come back to it.

## Opening Claude Code

1. Open Terminal (Cmd + Space, type "Terminal", Enter)
2. Go to your project: `cd ~/beacon-app`
3. Type `claude` and hit Enter
4. Talk to it like a person

## Opening Beacon

```bash
cd ~/beacon-app
pnpm dev
```

Open http://localhost:3000 in your browser. Dev tools: Ctrl/Cmd + D.

## Five prompts to start with

Nothing scary. Just try one.

```
What Dialtone components are available for showing a list of items?
```

```
Find me a Dialtone icon for a phone call
```

```
Explain what this file does: src/components/conversation/feed/FeedView.vue
```

```
Change the heading text in this component from "Settings" to "Preferences"
```

```
Create a simple card component using DtCard with a title, description,
and a primary action button. Use Dialtone components and tokens.
```

## The commands you'll use most

| You're thinking... | Type this |
|---|---|
| I need a ticket and branch | `/project-start` |
| I know enough to formalize the problem | `/shaping` |
| I've picked a direction, map the pieces | `/breadboarding` |
| This slice is ready to build | `/feature-dev` |
| Clean up what I just built | `/simplify` |
| Is this ready for review? | `/pr-prep` |
| Time to open the PR | `/pr-create` |
| Does the UI follow our design tenets? | Ask the `dialpad-design` agent |
| Lint/type errors need fixing | `/fix-quick` |

Full list on the [toolkit page](/toolkit).

## The feedback loop

1. Get specific feedback from a specific person
2. Paste it into Claude as a prompt
3. Claude makes the change
4. Check the result in the browser
5. Push, share the preview link, get confirmation

## Figma and code

| Do this in Figma | Do this in code |
|---|---|
| Explore visual directions quickly | Test if the design actually works |
| Try 5 layout variants fast | Handle real data, edge cases, interactions |
| Show stakeholders something static | Check loading, error, empty states |
| Update the design file after feedback | Iterate on feedback with Claude in minutes |

**Figma MCP** bridges both directions. Give Claude a Figma URL, get a code starting point. Capture your prototype back into Figma for reviews.

## Translation guide

| They say | It actually is |
|----------|---------------|
| Terminal | Text box where you type commands (like Spotlight) |
| Git | Version history (like Figma's version history) |
| Branch | A safe copy to experiment on (like a Figma page) |
| PR | Sharing your work for review (like a Figma link) |
| Merge | Moving approved work into the main project |
| Commit | Saving a snapshot with a note attached |
| Deploy | Making your work visible to others |
| MCP | A plug that connects Claude to tools (Figma, Dialtone, Jira) |
| TypeScript | The language Beacon uses. Claude writes it. You review the UI. |
| Pinia | Where UI state lives. Claude knows how to use it. |
| IndexedDB | Where data lives. Claude handles it through controllers. |
| Feature flag | A toggle that hides your work until it's ready. Safe experimentation. |

## When you're stuck

1. Tell Claude what's wrong. Describe what you see vs. what you expected.
2. Check the browser console. Right-click, Inspect, Console tab. Errors are in red.
3. Paste the error into Claude. Ask what it means.
4. Start a new conversation. If things get tangled, a fresh context helps.
5. If a commit fails, paste the error into Claude and say "fix it."
6. Ask for help. #ai-coding on Dialpad, or DM your facilitator.

## The mindset

You're not coding. You're describing and critiquing.

First attempts won't be right. That's iteration, not failure.

Your design eye decides when the output is good. Claude writes code. You decide if it works.

Share before it's polished. Direction checks prevent wasted weeks.

Accessibility is part of design, not an add-on. Ask Claude to check. Then verify yourself.

The design doc comes after building, not before. It captures decisions you've already made.

Events follow design. You design the correct user behavior first, then define what to track.
