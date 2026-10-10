<script setup lang="ts">
import { computed } from 'vue'
import { useData, withBase } from 'vitepress'
import { steps } from './guideSteps'

const { page } = useData()
const index = computed(() => steps.findIndex(step => step.file === page.value.relativePath))
const continuation = computed(() => {
  if (page.value.relativePath === 'index.md') return { step: steps[0], text: 'Start with the question you want your prototype to answer.', action: 'Start here' }
  if (index.value < 0) return null
  if (index.value === 3) return { step: steps[2], text: 'Bring the feedback back into your prototype and try the experience again.', action: 'Keep iterating' }
  const text = [
    'You have a target and a question. Turn them into a prompt and a plan.',
    'Your prototype is ready to try. Walk through it and decide what needs to change.',
    'Ready for another perspective? Share the prototype with a clear question.',
  ][index.value]
  return { step: steps[index.value + 1], text, action: `Continue: ${steps[index.value + 1].label}` }
})
</script>

<template>
  <nav v-if="continuation" class="guide-continuation" aria-label="Continue the guide">
    <p>{{ continuation.text }}</p>
    <a :href="withBase(continuation.step.href)">{{ continuation.action }} <span aria-hidden="true">→</span></a>
  </nav>
</template>
