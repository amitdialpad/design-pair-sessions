<script setup lang="ts">
import { computed } from 'vue'
import { useData, withBase } from 'vitepress'
import { steps } from './guideSteps'

const { page } = useData()
const index = computed(() => steps.findIndex(step => step.file === page.value.relativePath))
const previous = computed(() => index.value > 0 ? steps[index.value - 1] : { label: 'Designing with AI', href: '/' })
const next = computed(() => steps[index.value + 1])
</script>

<template>
  <nav v-if="index >= 0" class="guide-navigation" aria-label="Guide navigation">
    <a class="guide-previous" :href="withBase(previous.href)">
      <span aria-hidden="true">←</span> {{ previous.label }}
    </a>
    <span class="guide-position">Step {{ index + 1 }} of {{ steps.length }}</span>
    <a v-if="next" class="guide-next" :href="withBase(next.href)">
      {{ next.label }} <span aria-hidden="true">→</span>
    </a>
    <span v-else class="guide-complete">Keep iterating</span>
  </nav>
</template>
