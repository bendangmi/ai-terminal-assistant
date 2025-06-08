import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'

export const useSettingsStore = defineStore('settings', () => {
  // 默认配置
  const defaultTerminalConfig = {
    fontSize: 14,
    fontFamily: 'Consolas',
    cursorStyle: 'block',
    cursorBlink: true,
    historySize: 100
  }

  const defaultSystemConfig = {
    updateInterval: 5,
    logLevel: 'info',
    autoStart: false,
    notifications: true
  }

  const defaultAiConfig = {
    provider: 'deepseek',
    apiKey: '',
    model: 'deepseek-coder',
    temperature: 0.7
  }

  const defaultShortcutConfig = {
    execute: 'Enter',
    clear: 'Ctrl + L',
    copy: 'Ctrl + C',
    paste: 'Ctrl + V'
  }

  // 当前配置
  const terminalConfig = ref({ ...defaultTerminalConfig })
  const systemConfig = ref({ ...defaultSystemConfig })
  const aiConfig = ref({ ...defaultAiConfig })
  const shortcutConfig = ref({ ...defaultShortcutConfig })

  // 计算属性
  const currentSettings = computed(() => ({
    terminal: terminalConfig.value,
    system: systemConfig.value,
    ai: aiConfig.value,
    shortcuts: shortcutConfig.value
  }))

  // 加载配置
  const loadSettings = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.SETTINGS)
      const settings = response.data

      // 加载终端配置
      if (settings.terminal) {
        terminalConfig.value = {
          ...defaultTerminalConfig,
          ...settings.terminal
        }
      }

      // 加载系统配置
      if (settings.system) {
        systemConfig.value = {
          ...defaultSystemConfig,
          ...settings.system
        }
      }

      // 加载AI配置
      if (settings.ai) {
        aiConfig.value = {
          ...defaultAiConfig,
          ...settings.ai
        }
      }

      // 加载快捷键配置
      if (settings.shortcuts) {
        shortcutConfig.value = {
          ...defaultShortcutConfig,
          ...settings.shortcuts
        }
      }

      return true
    } catch (error) {
      console.error('加载设置失败:', error)
      return false
    }
  }

  // 保存配置
  const saveSettings = async (settings) => {
    try {
      await axios.post(API_ENDPOINTS.SETTINGS, settings)

      // 更新本地配置
      if (settings.terminal) {
        terminalConfig.value = settings.terminal
      }
      if (settings.system) {
        systemConfig.value = settings.system
      }
      if (settings.ai) {
        aiConfig.value = settings.ai
      }
      if (settings.shortcuts) {
        shortcutConfig.value = settings.shortcuts
      }

      return true
    } catch (error) {
      console.error('保存设置失败:', error)
      throw error
    }
  }

  // 更新配置
  const updateTerminalConfig = (config) => {
    terminalConfig.value = {
      ...terminalConfig.value,
      ...config
    }
  }

  const updateSystemConfig = (config) => {
    systemConfig.value = {
      ...systemConfig.value,
      ...config
    }
  }

  const updateAiConfig = (config) => {
    aiConfig.value = {
      ...aiConfig.value,
      ...config
    }
  }

  const updateShortcutConfig = (config) => {
    shortcutConfig.value = {
      ...shortcutConfig.value,
      ...config
    }
  }

  // 重置配置
  const resetSettings = () => {
    terminalConfig.value = { ...defaultTerminalConfig }
    systemConfig.value = { ...defaultSystemConfig }
    aiConfig.value = { ...defaultAiConfig }
    shortcutConfig.value = { ...defaultShortcutConfig }
  }

  return {
    // 默认配置
    defaultTerminalConfig,
    defaultSystemConfig,
    defaultAiConfig,
    defaultShortcutConfig,

    // 当前配置
    terminalConfig,
    systemConfig,
    aiConfig,
    shortcutConfig,
    currentSettings,

    // 方法
    loadSettings,
    saveSettings,
    updateTerminalConfig,
    updateSystemConfig,
    updateAiConfig,
    updateShortcutConfig,
    resetSettings
  }
}) 