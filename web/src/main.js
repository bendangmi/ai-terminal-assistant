import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { useThemeStore } from './store'

// 导入自定义指令
import directives from './directives'

// 导入自定义样式
import '@/styles/variables.css'
import '@/styles/main.css'
import '@/styles/dark-theme.css'
import '@/styles/element-override.css'
import '@/styles/transitions.css'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

// 注册自定义指令
Object.keys(directives).forEach(key => {
  app.directive(key, directives[key])
})

// 错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue Error:', err)
  console.error('Component:', vm)
  console.error('Error Info:', info)
}

// 初始化主题
const themeStore = useThemeStore()
themeStore.initTheme()

// 设置默认主题
document.documentElement.setAttribute('data-theme', 'dark')

// 挂载应用
app.mount('#app') 