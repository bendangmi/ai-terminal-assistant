import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 主题模式
  const isDark = ref(false)
  
  // 初始化主题
  const initTheme = () => {
    // 优先使用本地存储的主题设置
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      // 如果没有本地存储，则使用系统主题
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    applyTheme()
  }
  
  // 切换主题
  const toggleTheme = () => {
    isDark.value = !isDark.value
    applyTheme()
  }
  
  // 应用主题
  const applyTheme = () => {
    // 设置 data-theme 属性
    document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
    // 保存到本地存储
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }
  
  return {
    isDark,
    initTheme,
    toggleTheme
  }
}) 