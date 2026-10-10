import DefaultTheme from 'vitepress/theme'
import GuideLayout from './components/GuideLayout.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: GuideLayout,
}
