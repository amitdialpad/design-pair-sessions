import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/design-pair-sessions/',
  title: 'Design with AI',
  description: 'Build and test prototypes with Studio and Beacon at Dialpad',
  themeConfig: {
    nav: [
      { text: 'Start here', link: '/start-here' },
      { text: 'Build', link: '/prototyping' },
      { text: 'Evaluate', link: '/evaluate' },
      { text: 'Share', link: '/share' },
      { text: 'Resources', link: '/resources' },
    ],
    sidebar: [
      {
        text: 'Design with AI',
        items: [
          { text: 'Overview', link: '/' },
          { text: '1. Start here', link: '/start-here' },
          { text: '2. Build a prototype', link: '/prototyping' },
          { text: '3. Evaluate and iterate', link: '/evaluate' },
          { text: '4. Share your work', link: '/share' },
        ],
      },
      {
        text: 'Resources',
        collapsed: true,
        items: [
          { text: 'Skills and tools', link: '/toolkit' },
          { text: 'Quick reference', link: '/cheat-sheet' },
          { text: 'Design judgment and process', link: '/process' },
          { text: 'Project IRL', link: '/story' },
          { text: 'Links and pair sessions', link: '/resources' },
        ],
      },
      {
        text: 'Keep up',
        collapsed: true,
        items: [
          { text: 'Updates and Beacon Brief', link: '/updates' },
          { text: 'Toolkit changes', link: '/whats-new' },
        ],
      },
    ],
    outline: { level: [2, 3] },
  },
})
