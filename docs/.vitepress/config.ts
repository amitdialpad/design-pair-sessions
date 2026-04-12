import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/design-pair-sessions/',
  title: 'Design with Beacon',
  description: 'A living guide to building with AI at Dialpad',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
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
        text: 'More',
        items: [
          { text: 'Getting started', link: '/cheat-sheet' },
          { text: 'Project IRL', link: '/story' },
          { text: 'Resources', link: '/resources' },
        ],
      },
    ],
    sidebar: [
      {
        text: '',
        items: [
          { text: 'Home', link: '/' },
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
          { text: 'Getting started', link: '/cheat-sheet' },
          { text: 'Project IRL', link: '/story' },
          { text: 'Resources', link: '/resources' },
        ],
      },
    ],
    outline: { level: [2, 3] },
  },
})
