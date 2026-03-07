import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Design Pair Sessions',
  description: '1:1 training for designers learning to build with AI',
  themeConfig: {
    nav: [],
    sidebar: [
      {
        text: '',
        items: [
          { text: 'Welcome', link: '/' },
          { text: 'The process', link: '/process' },
          { text: 'Project IRL', link: '/story' },
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
        text: 'Beacon',
        items: [
          { text: 'The toolkit', link: '/toolkit' },
          { text: "What's new", link: '/whats-new' },
        ],
      },
      {
        text: 'Reference',
        items: [
          { text: 'Resources', link: '/resources' },
          { text: 'Getting started', link: '/cheat-sheet' },
        ],
      },
    ],
    outline: 'deep',
  },
})
