# The process

You're always designing. Sometimes designing means typing a slash command. Sometimes it means going back to Figma. Sometimes it means pushing a prototype to a PR preview and asking someone "does this feel right?"

## The rhythm

You don't switch between "design mode" and "engineering mode." You move fluidly between tools depending on what the work needs.

Always open Claude Code from inside the Beacon folder: `cd ~/beacon-app` → `claude`. The Beacon commands only work from there. Each project gets its own isolated workspace. `/project-start` handles the ticket, branch, and setup for you.

| What you're doing | Where you are |
|---|---|
| Starting a ticket and branch | `/project-start` |
| Analyzing a PRD, competitive research, checking Amplitude | Claude conversation |
| Exploring layouts, trying visual directions | Sketching, Figma, or Claude in terminal |
| Formalizing requirements after you understand the problem | `/shaping` in Beacon |
| Mapping how all the pieces connect | `/breadboard` in Beacon |
| Slicing the breadboard into Jira tickets | `/jira-create` in Beacon |
| Building each piece of your design into working UI | `/feature-team` in Beacon |
| Checking your UI against Dialpad's design principles | Ask Claude: *"Run the dialpad-design agent"* |
| Getting early directional feedback | Loom, or open a draft PR and share the preview link in Dialpad |
| Checking if the code is ready to share | `/pr-prep` in Beacon |
| Creating the PR and sharing the preview link | `/pr-create` in Beacon → send link in Dialpad |
| Pushing a frame into Figma for refinement | Figma MCP |

Research and exploration are flexible. Go where the work takes you. Once you're in Beacon, the pipeline flows in order: start → shape → breadboard → ticket → build → prep → ship.

## Research (ongoing, not a phase)

Research isn't step 1 that you finish and move on from. It runs alongside everything.

**PRD analysis.** Push the PRD into Claude. Don't read it yourself first. Let Claude study it and ask: what are the user stories? What behaviors does this introduce? What edge cases aren't addressed? You'll catch things buried on page 7 that you'd skim past.

**Jira context.** Not just the current ticket. Past tickets, related work, what's been tried before, what got blocked. Jira MCP or CLI pulls this into your Claude conversation. Understanding history prevents rebuilding what failed before.

**User behavior data.** What are users actually doing today? Amplitude MCP gives you funnels, drop-offs, patterns. Sometimes the research reveals the tracking doesn't exist, which is valuable too: it tells you what you can't measure yet and what needs instrumentation after the design is done.

**Competitive analysis.** Claude can analyze dozens of competitor UIs quickly. Findings go into a doc you reference throughout the project.

**Engineer conversations.** These happen throughout, not just at the start. A single sentence from an engineer about how the system actually works can change how you structure an entire component. Ask engineers how it works. The answer often contradicts what the PRD assumes.

All of this feeds into `/shaping`. The shaping skill has a Frame section (Source, Problem, Outcome) designed to receive this material. The better your research, the sharper your requirements.

## Explore (build to think)

The first code is wrong. That's the point. You build to discover what the right answer is, not to implement a known solution.

You'll build things that get killed. Layouts that don't work. Features that live for weeks before being removed. Mental models that turn out to be fundamentally wrong about how the system actually works. This isn't wasted effort. Every wrong turn teaches you something that makes the next iteration better.

You're not implementing finished Figma mocks. You're using Claude as a co-builder to test whether ideas work. Claude Code is a pair partner with guardrails: one step, manual test, commit. Claude touches only the files for the current step. No autonomous refactoring unless asked. The designer directs, Claude builds, the designer evaluates.

## Structure before variation

Visual exploration gets more valuable when the underlying structure is solid. Build the data and logic layer first, with a clean separation between model, controller, and view. Once that is done, you have real freedom in the view. Try layouts, discard what does not work, keep the structure intact. The view reacts to what the controller says. It does not contain mixed logic.

The inverse is harder. Exploring visually on top of a tangled data model means every visual change risks breaking something structural.

For multiple UI states (error, loading, empty, restricted access), prefer simulated controls over a flag for every condition. A controls panel lets you switch between states and watch the view react. That is more flexible and easier to share.

## Beacon is a production environment, not a demo

This is a mindset shift worth saying directly. Beacon is not a mock UI playground. The data in it should behave like production data. The scenarios should represent real product situations. When something feels fake or oversimplified, that is a signal to fix the data model, not work around it.

In practice, this means:

**Use scenarios, not one-off data.** Beacon has a scenario system for generating realistic mock data: support desk, sales team, onboarding flow. These are reusable. If you find yourself manually creating data to test a flow, stop and use a scenario instead. Designers should not have to "prepare data" to work. If the right scenario doesn't exist, that is a product gap — worth raising, not patching.

**Data is shared across features.** Different parts of the product use the same underlying data. Do not create isolated, feature-specific data just to make one view work. If a billing page and a settings page both need company data, they pull from the same source. Building private data models for individual features is a pattern to avoid.

**The order of priorities matters.** When building, Josh's explicit ordering is: correct system design → realistic data → reusable scenarios → automation → UI comes after. Getting the structure and data right is the work. UI is how you verify the structure is right.

**Size matters for testing.** Beacon supports small, medium, and large environment configurations. Each reflects real behavioral differences: feature availability, usage patterns, system complexity. Test against more than one. An empty-state screen that looks fine with 10 records can fall apart at 10,000.

## Figma and code: when to be where

**Start in Figma when** you need to explore visual directions quickly. Layout options, component choices, spacing, visual hierarchy. Figma is faster than code for purely visual exploration. You can try 5 layout variants in Figma in the time it takes to build one in code.

**Move to code when** you need to test whether the design actually works. Does the interaction feel right? Does it handle real data? What about empty states, loading, errors? What about 3 items vs 300? Code answers questions Figma can't.

**Go back to Figma when** feedback changes the layout or visual direction. When you need to show stakeholders something static and polished. When you need to update the design file for engineering handoff or for your own reference.

**Use Figma MCP** to bridge the two. Point Claude at a Figma frame (just give it the URL) and it reads the design and generates a code starting point. Going the other direction: capture your prototype and bring it back into Figma for reviews.

The prototype is the source of truth for how the design works. Figma is the source of truth for how it looks. They inform each other throughout the project.

## The design doc

The design doc doesn't come first. It captures decisions already made through building, not decisions to be made.

**What goes in it:** Problem statement. Target users. Mental model. Design decisions with rationale (not just "we chose X" but "we chose X because Y, and we considered Z but rejected it because..."). User stories. Component architecture. Success criteria. Quotes from engineers and stakeholders that shaped the direction.

**When to write it:** After you've explored enough to know what you're building. After the big wrong turns have been corrected. After you've talked to enough people that the shape is clear. Not before.

**When to update it:** When feedback changes the direction. When new data comes in. When engineers share constraints you didn't know about. When you pivot. The doc reflects the current state of the design, not the original plan.

## Sharing and feedback

Sharing isn't presenting polished work. It's showing someone specific and asking "does this direction feel right?" Share early: a 30-second screen recording, a message in Dialpad, a PR preview link. The earlier you share, the less you build in the wrong direction.

Push for specifics when you get feedback. Different people catch different things: engineers spot incorrect data models, PMs question scope, your design manager challenges interaction patterns, your team catches visual inconsistencies.

**Turning feedback into action:**

1. Get specific feedback. "Replace Savings with Rate because the savings framing implies the company is saving money" is useful. "Had some thoughts on the table" is not.
2. Paste it into Claude as a prompt. Claude has the context of the codebase.
3. Evaluate the result in the browser. Did it change the right things? Did it break anything else?
4. Push and share the updated preview link.

The loop is tight: feedback, prompt, change, evaluate, share. What used to be a multi-day cycle (get feedback, open Figma, redesign, re-spec, hand to engineer, wait for build, review) compresses into minutes.

When you run `/pr-create`, two independent AI reviewers run automatically on the PR — GPT-4.1 and Claude Sonnet 4.6. They post findings as inline comments on the code. The full review takes around 7-10 minutes. Once it's done, run `/pr-comments` to pull the feedback into Claude and triage what to fix.

## Staying clean while exploring

Exploration creates mess. The mess is fine during exploration. It is not fine when it outlives the decision that created it.

**Dead code.** Remove unused code before merging. AI tools treat dead code as equally important as live code. Anything left behind becomes part of the context future work builds on. Experiments that did not win should not outlive the decision.

**Draft PRs.** A draft PR signals "not ready for review." Use it for work that is exploratory or incomplete. Once it is ready, un-draft it and ask for review. A draft is not just a label. It keeps your work yours until you want input.

**Smaller PRs over stacked chains.** Stacked PRs block downstream work when an early assumption turns out to be wrong. Isolate foundational changes into their own PRs. Each one can be reviewed and merged independently.

**Plan files before complex code.** For anything structurally involved, write a plan file before building. Share it with a collaborator for early feedback. A one-page plan reviewed early prevents a week of rework.

**Explicit blocking.** For foundational PRs that unblock downstream work, say so directly: "I'm blocked on this, I need a fast review." Reviewers cannot prioritize what they do not know is urgent.

## Evaluating what Claude builds

Claude writes code. You decide if it's good. "Good" for a designer means something different than "good" for an engineer.

**Does it look right?** Spacing, alignment, typography hierarchy, visual weight. Your eye catches 12px where it should be 16px. Claude can't see that.

**Does it feel right?** Interactions, transitions, hover states, the rhythm of the interface. Click through it. Claude built what you described, but what you described might not be what you meant.

**Does it work for everyone?** Ask Claude to check accessibility: *"Check this for accessibility: keyboard navigation, contrast, ARIA labels."* Beacon's `/pr-prep` does this too, but checking early is better than checking at the end.

**Does it follow Dialpad's design principles?** The `dialpad-design` agent reviews against Dialpad's design principles. You can ask it directly: *"Review the UI I just built for the settings feature."*

**Does it handle the edges?** New user with no data. Power user with too much data. Slow network. Error during submission. Long text that overflows.

## Testing what you built

After `/feature-team` finishes, before moving to `/pr-prep`, ask:

```
How do I test this?
```

Claude comes back with a checklist based on what was just built. Work through it and report back — pass, fail, or describe what went wrong:

```
1. Pass
2. Pass
3. Fail — the empty state shows even when there is data
```

Claude fixes what's broken. Repeat until everything passes. Then run `/pr-prep`.

## The polish pass

Separate from building and iterating. After the main work is done, a dedicated pass for craft:

- Loading states: what do users see while things load?
- Error states: what happens when something breaks?
- Empty states: new user, no data. Inviting or just blank?
- Transitions: smooth or jarring?
- Alignment: spacing consistent, elements lined up
- Responsive: works at different sizes?
- Accessibility: keyboard nav, contrast, screen reader

This is where the difference shows between "it works" and "it works well." Ask Claude to audit for WCAG issues. Use the `dialpad-design` agent for a design principles check. Then look at it yourself.

## Events follow design

Amplitude event specs get defined based on what the design actually does, not what was planned upfront. You design the correct user behavior first, then define what to track. Instrumentation follows the design, not the other way around.

## When to reach for a command

You don't need to memorize a pipeline. Just recognize the moment.

| You're thinking... | Reach for |
|---|---|
| "I need a ticket and a branch" | `/project-start` |
| "I have raw source material to turn into a problem frame" | `/framing-doc` |
| "I know enough about this problem to write it down" | `/shaping` |
| "I've picked a direction, let me map the pieces" | `/breadboard` |
| "This slice is ready to build properly" | `/feature-team` |
| "I've got my breadboard, time to create tickets" | `/jira-create` |
| "I need a new component scaffolded" | `/component-create` |
| "Let me clean up what I just built" | `/simplify` |
| "Is this ready for review?" | `/pr-prep` |
| "Time to open the PR" | `/pr-create` |
| "I've got PR feedback to triage" | `/pr-comments` |
| "Does this UI follow Dialpad's design principles?" | `dialpad-design` agent |
| "What bugs might be hiding?" | `/bug-hunt` |
| "I have a Design Studio prototype to bring over" | `/prototype-migrate` |
| "Lint/type errors need fixing" | `/fix-quick` |

Between every one of these, you're back to designing.

For what each command, agent, skill, rule, and hook actually does, see [The Beacon toolkit](/toolkit).

## What the commands don't do

`/shaping` can list requirements. It can't tell you which ones matter most to users. `/breadboard` can map affordances. It can't tell you if the flow feels right. `/pr-prep` can catch accessibility violations. It can't tell you if the empty state is inviting or just blank. `/feature-team` can build what you describe. It can't tell you what to describe.

Your eye for spacing, typography, interaction quality, user empathy, edge cases, and the full user journey: that's what makes the output good. The commands make you fast. Your design training makes the result worth shipping.
