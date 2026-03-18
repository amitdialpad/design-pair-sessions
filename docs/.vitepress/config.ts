import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/design-pair-sessions/',
  title: 'Design Pair Sessions',
  description: '1:1 training for designers learning to build with AI',
  themeConfig: {
    nav: [
      { text: 'Overview', link: '/' },
      { text: 'The process', link: '/process' },
      { text: 'Beacon toolkit', link: '/toolkit' },
      {
        text: 'Pair sessions',
        items: [
          { text: '1. My turn', link: '/sessions/session-1' },
          { text: '2. Pair build', link: '/sessions/session-2' },
          { text: '3. Your turn', link: '/sessions/session-3' },
        ],
      },
      {
        text: 'Reference',
        items: [
          { text: 'Resources', link: '/resources' },
          { text: 'Getting started', link: '/cheat-sheet' },
          { text: 'Project IRL', link: '/story' },
          { text: "What's new", link: '/whats-new' },
        ],
      },
    ],
    sidebar: [
      {
        text: '',
        items: [
          { text: 'Overview', link: '/' },
          { text: 'The process', link: '/process' },
          { text: 'Beacon toolkit', link: '/toolkit' },
        ],
      },
      {
        text: 'Pair sessions',
        items: [
          { text: '1. My turn', link: '/sessions/session-1' },
          { text: '2. Pair build', link: '/sessions/session-2' },
          { text: '3. Your turn', link: '/sessions/session-3' },
        ],
      },
      {
        text: 'Reference',
        items: [
          { text: 'Resources', link: '/resources' },
          { text: 'Getting started', link: '/cheat-sheet' },
          { text: 'Project IRL', link: '/story' },
          { text: "What's new", link: '/whats-new' },
        ],
      },
    ],
    outline: 'deep',
  },
})
