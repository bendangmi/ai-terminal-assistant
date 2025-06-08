import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const currentTheme = ref('tech-blue')
  const themeNamespace = ref('el')

  const themes = [
    { 
      label: '科技蓝', 
      value: 'tech-blue',
      colors: {
        primary: '#1890ff',
        success: '#52c41a',
        warning: '#faad14',
        error: '#f5222d',
        info: '#1890ff'
      }
    },
    { 
      label: '暗黑', 
      value: 'dark',
      colors: {
        primary: '#177ddc',
        success: '#49aa19',
        warning: '#d89614',
        error: '#d32029',
        info: '#177ddc'
      }
    },
    { 
      label: '极简', 
      value: 'minimal',
      colors: {
        primary: '#000000',
        success: '#4caf50',
        warning: '#ff9800',
        error: '#f44336',
        info: '#2196f3'
      }
    },
    { 
      label: '科幻', 
      value: 'cyberpunk',
      colors: {
        primary: '#00fff1',
        success: '#39ff14',
        warning: '#ff3366',
        error: '#ff0033',
        info: '#00ccff'
      }
    }
  ]

  const setTheme = (theme) => {
    currentTheme.value = theme
    const selectedTheme = themes.find(t => t.value === theme)
    if (selectedTheme) {
      // 更新CSS变量
      document.documentElement.style.setProperty('--primary-color', selectedTheme.colors.primary)
      document.documentElement.style.setProperty('--success-color', selectedTheme.colors.success)
      document.documentElement.style.setProperty('--warning-color', selectedTheme.colors.warning)
      document.documentElement.style.setProperty('--error-color', selectedTheme.colors.error)
      document.documentElement.style.setProperty('--info-color', selectedTheme.colors.info)

      // 保存到本地存储
      localStorage.setItem('theme', theme)
      localStorage.setItem('theme-colors', JSON.stringify(selectedTheme.colors))
    }
  }

  // 初始化主题
  const initTheme = () => {
    const savedTheme = localStorage.getItem('theme')
    const savedColors = localStorage.getItem('theme-colors')

    if (savedTheme && themes.some(t => t.value === savedTheme)) {
      currentTheme.value = savedTheme
      if (savedColors) {
        const colors = JSON.parse(savedColors)
        Object.entries(colors).forEach(([key, value]) => {
          document.documentElement.style.setProperty(`--${key}-color`, value)
        })
      }
    } else {
      // 如果没有保存的主题或主题无效，使用系统主题偏好
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      setTheme(prefersDark ? 'dark' : 'tech-blue')
    }

    // 监听系统主题变化
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'tech-blue')
      }
    })
  }

  return {
    currentTheme,
    themeNamespace,
    themes,
    setTheme,
    initTheme
  }
})

export default {
  useThemeStore
} 