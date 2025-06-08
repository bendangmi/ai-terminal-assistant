import axios from 'axios'

// API 基础配置
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

// API 端点配置
export const API_ENDPOINTS = {
  // 系统相关
  SYSTEM: {
    INFO: `${BASE_URL}/system/info`,
    CPU: `${BASE_URL}/system/cpu`,
    MEMORY: `${BASE_URL}/system/memory`,
    DISK: `${BASE_URL}/system/disk`,
    NETWORK: `${BASE_URL}/system/network`
  },
  
  // 终端相关
  TERMINAL: {
    CREATE: `${BASE_URL}/terminal/create`,
    CLOSE: `${BASE_URL}/terminal/close`,
    SEND_COMMAND: `${BASE_URL}/terminal/send-command`,
    RESIZE: `${BASE_URL}/terminal/resize`
  },
  
  // 设置相关
  SETTINGS: {
    SAVE: `${BASE_URL}/settings/save`,
    LOAD: `${BASE_URL}/settings/load`
  },
  
  // 更新相关
  UPDATE: {
    CHECK: `${BASE_URL}/update/check`,
    DOWNLOAD: `${BASE_URL}/update/download`,
    INSTALL: `${BASE_URL}/update/install`
  }
}

// API请求配置
export const API_CONFIG = {
  // 请求超时时间（毫秒）
  timeout: 30000,
  
  // 请求头
  headers: {
    'Content-Type': 'application/json'
  },
  
  // 是否携带凭证
  withCredentials: true
}

// 响应状态码
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_ERROR: 500
}

// 错误消息
export const ERROR_MESSAGES = {
  NETWORK_ERROR: '网络连接错误',
  SERVER_ERROR: '服务器内部错误',
  TIMEOUT_ERROR: '请求超时',
  AUTH_ERROR: '认证失败',
  UNKNOWN_ERROR: '未知错误'
}

// API响应处理
export const handleApiResponse = (response) => {
  if (response.status === HTTP_STATUS.OK || response.status === HTTP_STATUS.CREATED) {
    return response.data
  }
  
  throw new Error(response.data.message || ERROR_MESSAGES.UNKNOWN_ERROR)
}

// API错误处理
export const handleApiError = (error) => {
  if (error.response) {
    // 服务器响应错误
    const status = error.response.status
    const message = error.response.data.message

    switch (status) {
      case HTTP_STATUS.BAD_REQUEST:
        return `请求参数错误: ${message}`
      case HTTP_STATUS.UNAUTHORIZED:
        return ERROR_MESSAGES.AUTH_ERROR
      case HTTP_STATUS.FORBIDDEN:
        return '没有权限访问该资源'
      case HTTP_STATUS.NOT_FOUND:
        return '请求的资源不存在'
      case HTTP_STATUS.INTERNAL_ERROR:
        return ERROR_MESSAGES.SERVER_ERROR
      default:
        return ERROR_MESSAGES.UNKNOWN_ERROR
    }
  } else if (error.request) {
    // 请求发送失败
    if (error.code === 'ECONNABORTED') {
      return ERROR_MESSAGES.TIMEOUT_ERROR
    }
    return ERROR_MESSAGES.NETWORK_ERROR
  }
  
  return ERROR_MESSAGES.UNKNOWN_ERROR
}

// 创建axios实例
const apiClient = axios.create({
  baseURL: BASE_URL,
  ...API_CONFIG
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 添加token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => handleApiResponse(response),
  (error) => Promise.reject(handleApiError(error))
)

// API 服务
export const terminalAPI = {
  create: () => apiClient.post(API_ENDPOINTS.TERMINAL.CREATE),
  close: (terminalId) => apiClient.post(API_ENDPOINTS.TERMINAL.CLOSE, { terminalId }),
  sendCommand: (terminalId, command) => apiClient.post(API_ENDPOINTS.TERMINAL.SEND_COMMAND, { terminalId, command }),
  resize: (terminalId, rows, cols) => apiClient.post(API_ENDPOINTS.TERMINAL.RESIZE, { terminalId, rows, cols })
}

export const systemAPI = {
  getSystemInfo: () => apiClient.get(API_ENDPOINTS.SYSTEM.INFO),
  getCPUInfo: () => apiClient.get(API_ENDPOINTS.SYSTEM.CPU),
  getMemoryInfo: () => apiClient.get(API_ENDPOINTS.SYSTEM.MEMORY),
  getDiskInfo: () => apiClient.get(API_ENDPOINTS.SYSTEM.DISK),
  getNetworkInfo: () => apiClient.get(API_ENDPOINTS.SYSTEM.NETWORK)
}

export const settingsAPI = {
  saveSettings: (settings) => apiClient.post(API_ENDPOINTS.SETTINGS.SAVE, settings),
  loadSettings: () => apiClient.get(API_ENDPOINTS.SETTINGS.LOAD)
}

export const updateAPI = {
  checkUpdate: () => apiClient.get(API_ENDPOINTS.UPDATE.CHECK),
  downloadUpdate: () => apiClient.get(API_ENDPOINTS.UPDATE.DOWNLOAD),
  installUpdate: () => apiClient.post(API_ENDPOINTS.UPDATE.INSTALL)
}

export const monitorAPI = {
  getSystemInfo: () => apiClient.get(API_ENDPOINTS.SYSTEM.INFO)
}

export default apiClient 