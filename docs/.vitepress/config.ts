import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/design-pair-sessions/',
  appearance: 'dark',
  title: 'Designing with AI',
  description: 'Build and test prototypes with Studio and Beacon at Dialpad',
  transformPageData(pageData) {
    pageData.frontmatter.navbar = false
  },
  themeConfig: {
    nav: [],
    docFooter: { prev: false, next: false },
    sidebar: [
      {
        text: '',
        items: [
          { text: 'Designing with AI', link: '/' },
          { text: '1. Start here', link: '/start-here' },
          { text: '2. Build a prototype', link: '/prototyping' },
          { text: '3. Evaluate and iterate', link: '/evaluate' },
          { text: '4. Share your work', link: '/share' },
          { text: 'Skills', link: '/skills' },
          { text: 'Tools', link: '/tools' },
        ],
      },
      {
        text: 'Resources',
        collapsed: true,
        items: [
          { text: 'Quick reference', link: '/cheat-sheet' },
          { text: 'Design judgment and process', link: '/process' },
          { text: 'Reference links', link: '/resources' },
          { text: 'Studio controls and releases', link: '/studio' },
        ],
      },
      {
        text: 'Updates',
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
