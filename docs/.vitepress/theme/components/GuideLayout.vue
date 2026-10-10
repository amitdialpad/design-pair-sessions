<script setup lang="ts">
import { onMounted, ref } from 'vue'
import DefaultTheme from 'vitepress/theme'
import GuideNavigation from './GuideNavigation.vue'
import GuideContinuation from './GuideContinuation.vue'
import SidebarAppearance from './SidebarAppearance.vue'

const collapsed = ref(false)
const preferenceKey = 'design-with-ai-sidebar-collapsed'

onMounted(() => {
  try {
    collapsed.value = localStorage.getItem(preferenceKey) === 'true'
  } catch { /* Navigation still works when browser storage is unavailable. */ }
})

function toggleNavigation() {
  collapsed.value = !collapsed.value
  try {
    localStorage.setItem(preferenceKey, String(collapsed.value))
  } catch { /* Keep the choice for this page when storage is unavailable. */ }
}
</script>

<template>
  <DefaultTheme.Layout :class="{ 'navigation-collapsed': collapsed }">
    <template #layout-top>
      <button
        class="sidebar-toggle"
        :aria-expanded="!collapsed"
        aria-controls="VPSidebarNav"
        :aria-label="collapsed ? 'Show navigation' : 'Hide navigation'"
        @click="toggleNavigation"
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <rect x="1.5" y="2.5" width="13" height="11" rx="2" stroke="currentColor" />
          <path d="M6 3v10" stroke="currentColor" />
        </svg>
        <span>{{ collapsed ? 'Menu' : 'Hide menu' }}</span>
      </button>
    </template>
    <template #doc-before><GuideNavigation /></template>
    <template #doc-after><GuideContinuation /></template>
    <template #sidebar-nav-after><SidebarAppearance /></template>
  </DefaultTheme.Layout>
</template>
