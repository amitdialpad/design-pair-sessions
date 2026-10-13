<script setup>
import { withBase } from 'vitepress'
</script>

# Give your agent the guide

Download a short Markdown starter with the practical guidance in this site. Attach it to Claude or Codex, or ask your agent to read the saved file, then describe your project normally.

<a :href="withBase('/downloads/designing-with-ai.md')" download="designing-with-ai.md">Download the Markdown starter →</a>

Version: 12 October 2026. Works as guidance for Claude or Codex; it contains no personal setup or project history.

## Use it on your next project

Open your agent in the intended project and attach the downloaded file, or give it the local file path. Start with:

```text
Read the attached Designing with AI starter and use it for this project.
Find the existing repo skills that fit my request. Ask me for missing
inputs or design decisions, and show the plan before building.
Keep everything local until I approve sharing.

Here is what I want to work on: …
```

The starter tells the agent to use the team's current skills, clarify the prototype's purpose and states, check Dialtone, and bring the result back for your evaluation. You can ask normally; naming a skill is a fallback when the agent misses your intent.

## What it needs

Your agent still needs access to the Design repo, its existing skills, the app's setup, and any source connectors. The starter helps it check what is available and explain what is missing. It does not install those skills or grant access. See [Start here](/start-here) and [Tools](/tools).

Attaching this file gives the current conversation guidance. It does not register an automatically selected skill or ensure future conversations load it. For future work, attach it again or ask your agent to help configure it using your tool's supported project instructions. Keep the repo's existing instructions intact.

## Carry useful lessons forward

The starter asks the agent to investigate observed failures, verify corrections, and reuse relevant lessons. For continuity across sessions, it uses an already-approved notes location or asks where you want to save a short outcome note. The next conversation must read those notes. It does not include Amit's personal logging helper or run anything in the background.

The team repo remains the source of truth. Re-download the starter when this guide changes, and use [Skills](/skills) to find the maintained workflows.
