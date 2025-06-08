import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'
import { formatFileSize } from '@/utils'

export const useSystemStore = defineStore('system', () => {
  // 状态
  const cpuUsage = ref(0)
  const memoryUsage = ref(0)
  const diskUsage = ref([])
  const systemInfo = ref({
    os: '',
    platform: '',
    python_version: '',
    cpu_count: 0,
    working_directory: ''
  })
  const cpuInfo = ref({
    cores: 0,
    frequency: 0
  })
  const memoryInfo = ref({
    total: 0,
    used: 0,
    available: 0
  })

  // 历史数据
  const maxHistoryPoints = 60
  const cpuHistory = ref([])
  const memoryHistory = ref([])
  const timeLabels = ref([])

  // 监控间隔
  let monitorInterval = null
  const updateInterval = ref(2000) // 2秒

  // 获取系统信息
  const fetchSystemInfo = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.SYSTEM.INFO)
      const data = response.data

      systemInfo.value = {
        os: data.os,
        platform: data.platform,
        python_version: data.python_version,
        cpu_count: data.cpu_count,
        working_directory: data.working_directory
      }

      cpuInfo.value = {
        cores: data.cpu.cores,
        frequency: data.cpu.frequency
      }

      memoryInfo.value = {
        total: data.memory.total,
        used: data.memory.used,
        available: data.memory.available
      }

      // 更新使用率
      cpuUsage.value = data.cpu.usage
      memoryUsage.value = data.memory.percent

      // 更新历史数据
      updateHistoryData()
    } catch (error) {
      console.error('获取系统信息失败:', error)
    }
  }

  // 更新历史数据
  const updateHistoryData = () => {
    const now = new Date()
    const timeLabel = now.toLocaleTimeString()

    // 更新CPU历史
    if (cpuHistory.value.length >= maxHistoryPoints) {
      cpuHistory.value.shift()
      timeLabels.value.shift()
    }
    cpuHistory.value.push(cpuUsage.value)
    timeLabels.value.push(timeLabel)

    // 更新内存历史
    if (memoryHistory.value.length >= maxHistoryPoints) {
      memoryHistory.value.shift()
    }
    memoryHistory.value.push(memoryUsage.value)
  }

  // 开始监控
  const startMonitoring = () => {
    fetchSystemInfo()
    monitorInterval = setInterval(fetchSystemInfo, updateInterval.value)
  }

  // 停止监控
  const stopMonitoring = () => {
    if (monitorInterval) {
      clearInterval(monitorInterval)
      monitorInterval = null
    }
  }

  // 设置更新间隔
  const setUpdateInterval = (interval) => {
    updateInterval.value = interval
    if (monitorInterval) {
      stopMonitoring()
      startMonitoring()
    }
  }

  // 清空历史数据
  const clearHistory = () => {
    cpuHistory.value = []
    memoryHistory.value = []
    timeLabels.value = []
  }

  return {
    // 状态
    cpuUsage,
    memoryUsage,
    diskUsage,
    systemInfo,
    cpuInfo,
    memoryInfo,
    cpuHistory,
    memoryHistory,
    timeLabels,
    updateInterval,

    // 方法
    startMonitoring,
    stopMonitoring,
    setUpdateInterval,
    clearHistory
  }
})