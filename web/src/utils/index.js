// 日期格式化
export const formatDate = (date, format = 'YYYY-MM-DD HH:mm:ss') => {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

// 防抖函数
export const debounce = (fn, delay) => {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

// 节流函数
export const throttle = (fn, delay) => {
  let last = 0
  return function (...args) {
    const now = Date.now()
    if (now - last > delay) {
      fn.apply(this, args)
      last = now
    }
  }
}

// 深拷贝
export const deepClone = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj
  const clone = Array.isArray(obj) ? [] : {}
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      clone[key] = deepClone(obj[key])
    }
  }
  return clone
}

// 文件大小格式化
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

// 终端相关工具函数
export const terminal = {
  // 解析命令行参数
  parseCommand: (commandString) => {
    const args = []
    let current = ''
    let inQuotes = false
    
    for (let i = 0; i < commandString.length; i++) {
      const char = commandString[i]
      
      if (char === '"' || char === "'") {
        inQuotes = !inQuotes
        continue
      }
      
      if (char === ' ' && !inQuotes) {
        if (current) {
          args.push(current)
          current = ''
        }
        continue
      }
      
      current += char
    }
    
    if (current) {
      args.push(current)
    }
    
    return {
      command: args[0] || '',
      args: args.slice(1)
    }
  },

  // 格式化终端输出
  formatOutput: (output) => {
    return output
      .replace(/\n/g, '<br>')
      .replace(/ /g, '&nbsp;')
      .replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;')
  },

  // 生成命令提示符
  generatePrompt: (username, hostname, path) => {
    return `${username}@${hostname}:${path}$`
  }
}

// 系统监控工具函数
export const monitor = {
  // 计算 CPU 使用率
  calculateCPUUsage: (oldStats, newStats) => {
    const oldTotal = oldStats.user + oldStats.nice + oldStats.sys + oldStats.idle
    const newTotal = newStats.user + newStats.nice + newStats.sys + newStats.idle
    const totalDiff = newTotal - oldTotal
    const idleDiff = newStats.idle - oldStats.idle
    return ((1 - idleDiff / totalDiff) * 100).toFixed(1)
  },

  // 格式化内存大小
  formatMemory: (bytes) => formatFileSize(bytes),

  // 计算网络速度
  calculateNetworkSpeed: (oldStats, newStats, interval) => {
    const rxDiff = newStats.rx - oldStats.rx
    const txDiff = newStats.tx - oldStats.tx
    const seconds = interval / 1000

    return {
      download: formatFileSize(rxDiff / seconds) + '/s',
      upload: formatFileSize(txDiff / seconds) + '/s'
    }
  }
}

// 本地存储工具
export const storage = {
  get: (key, defaultValue = null) => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch (error) {
      console.error('Error reading from localStorage:', error)
      return defaultValue
    }
  },

  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error('Error writing to localStorage:', error)
    }
  },

  remove: (key) => {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error('Error removing from localStorage:', error)
    }
  },

  clear: () => {
    try {
      localStorage.clear()
    } catch (error) {
      console.error('Error clearing localStorage:', error)
    }
  }
}

// 验证工具函数
export const validate = {
  isEmail: (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
  },

  isURL: (url) => {
    try {
      new URL(url)
      return true
    } catch {
      return false
    }
  },

  isIPv4: (ip) => {
    return /^(\d{1,3}\.){3}\d{1,3}$/.test(ip)
  }
}

// 错误处理工具
export const errorHandler = {
  // 统一错误处理
  handle: (error) => {
    console.error('Error:', error)
    if (error.response) {
      // API 错误
      return {
        type: 'API_ERROR',
        status: error.response.status,
        message: error.response.data.message || '服务器错误'
      }
    } else if (error.request) {
      // 网络错误
      return {
        type: 'NETWORK_ERROR',
        message: '网络连接失败'
      }
    } else {
      // 其他错误
      return {
        type: 'UNKNOWN_ERROR',
        message: error.message || '未知错误'
      }
    }
  },

  // 格式化错误消息
  formatMessage: (error) => {
    const result = errorHandler.handle(error)
    return `[${result.type}] ${result.message}`
  }
}

// 生成唯一ID
export const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

// 复制到剪贴板
export const copyToClipboard = (text) => {
  return new Promise((resolve, reject) => {
    try {
      const textarea = document.createElement('textarea')
      textarea.value = text
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      resolve(true)
    } catch (err) {
      reject(err)
    }
  })
}

// 获取浏览器信息
export const getBrowserInfo = () => {
  const ua = navigator.userAgent
  const browser = {
    ie: /MSIE/.test(ua),
    ie6: /MSIE 6.0/.test(ua),
    ie7: /MSIE 7.0/.test(ua),
    ie8: /MSIE 8.0/.test(ua),
    ie9: /MSIE 9.0/.test(ua),
    ie10: /MSIE 10.0/.test(ua),
    ie11: /Trident\/7.0/.test(ua),
    edge: /Edge/.test(ua),
    chrome: /Chrome/.test(ua) && !/Edge/.test(ua),
    firefox: /Firefox/.test(ua),
    opera: /Opera/.test(ua),
    safari: /Safari/.test(ua) && !/Chrome/.test(ua),
    weixin: /MicroMessenger/i.test(ua)
  }
  return browser
}

// 获取操作系统信息
export const getOSInfo = () => {
  const ua = navigator.userAgent
  const os = {
    windows: /Windows/.test(ua),
    mac: /Mac OS X/.test(ua),
    linux: /Linux/.test(ua),
    android: /Android/.test(ua),
    ios: /iPhone|iPad|iPod/.test(ua)
  }
  return os
}

// 检查是否是移动设备
export const isMobile = () => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
}

// 检查是否支持 WebGL
export const hasWebGL = () => {
  try {
    const canvas = document.createElement('canvas')
    return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')))
  } catch (e) {
    return false
  }
}

// 检查是否支持某个 CSS 属性
export const supportCSSProperty = (prop) => {
  return prop in document.documentElement.style
}

// 格式化时间间隔
export const formatTimeAgo = (date) => {
  const now = new Date()
  const diff = now - new Date(date)
  const minute = 60 * 1000
  const hour = minute * 60
  const day = hour * 24
  const month = day * 30
  const year = day * 365

  if (diff < minute) {
    return '刚刚'
  } else if (diff < hour) {
    return Math.floor(diff / minute) + '分钟前'
  } else if (diff < day) {
    return Math.floor(diff / hour) + '小时前'
  } else if (diff < month) {
    return Math.floor(diff / day) + '天前'
  } else if (diff < year) {
    return Math.floor(diff / month) + '个月前'
  } else {
    return Math.floor(diff / year) + '年前'
  }
}

// 检查是否为空对象
export const isEmptyObject = (obj) => {
  return Object.keys(obj).length === 0 && obj.constructor === Object
}

// 检查是否为有效的邮箱地址
export const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

// 检查是否为有效的手机号码（中国大陆）
export const isValidPhone = (phone) => {
  return /^1[3-9]\d{9}$/.test(phone)
}

// 格式化金额
export const formatMoney = (number, decimals = 2, dec_point = '.', thousands_sep = ',') => {
  number = (number + '').replace(/[^0-9+-Ee.]/g, '')
  const n = !isFinite(+number) ? 0 : +number
  const prec = !isFinite(+decimals) ? 0 : Math.abs(decimals)
  const sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep
  const dec = (typeof dec_point === 'undefined') ? '.' : dec_point
  let s = ''

  const toFixedFix = function (n, prec) {
    const k = Math.pow(10, prec)
    return '' + Math.round(n * k) / k
  }

  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.')
  const re = /(-?\d+)(\d{3})/
  while (re.test(s[0])) {
    s[0] = s[0].replace(re, '$1' + sep + '$2')
  }

  if ((s[1] || '').length < prec) {
    s[1] = s[1] || ''
    s[1] += new Array(prec - s[1].length + 1).join('0')
  }
  return s.join(dec)
}

// 随机颜色生成
export const randomColor = () => {
  return '#' + Math.floor(Math.random() * 16777215).toString(16)
}

// 随机整数生成
export const randomInt = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1) + min)
}

// 数组乱序
export const shuffleArray = (arr) => {
  const array = [...arr]
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]]
  }
  return array
}

// 获取URL参数
export const getUrlParams = (url = window.location.href) => {
  const params = {}
  const searchParams = new URL(url).searchParams
  for (const [key, value] of searchParams) {
    params[key] = value
  }
  return params
}

// 下载文件
export const downloadFile = (url, filename) => {
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// 检查是否在视口内
export const isInViewport = (element) => {
  const rect = element.getBoundingClientRect()
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  )
}

// 获取滚动位置
export const getScrollPosition = () => ({
  x: window.pageXOffset || document.documentElement.scrollLeft,
  y: window.pageYOffset || document.documentElement.scrollTop
})

// 平滑滚动到顶部
export const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

// 检测暗色模式
export const isDarkMode = () => {
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
}

// 监听暗色模式变化
export const watchDarkMode = (callback) => {
  if (!window.matchMedia) return
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  mediaQuery.addListener(e => callback(e.matches))
  return mediaQuery
}

// 获取设备像素比
export const getDevicePixelRatio = () => {
  return window.devicePixelRatio || 1
}

// 检测是否支持触摸事件
export const isTouchDevice = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0
}

// 检测浏览器是否在线
export const isOnline = () => {
  return navigator.onLine
}

// 监听在线状态变化
export const watchOnlineStatus = (onlineCallback, offlineCallback) => {
  window.addEventListener('online', onlineCallback)
  window.addEventListener('offline', offlineCallback)
  return () => {
    window.removeEventListener('online', onlineCallback)
    window.removeEventListener('offline', offlineCallback)
  }
}

// 格式化代码
export const formatCode = (code) => {
  return code.replace(/^\s+|\s+$/g, '')
           .replace(/([{([])\s+/g, '$1')
           .replace(/\s+([})\]])/g, '$1')
           .replace(/,\s+/g, ', ')
           .replace(/;+\s*/g, '; ')
           .replace(/\s*:\s*/g, ': ')
           .replace(/\s*=\s*/g, ' = ')
}

// 高亮代码
export const highlightCode = (code, language) => {
  // 这里可以集成具体的代码高亮库，如 highlight.js 或 prism.js
  return `<pre><code class="language-${language}">${code}</code></pre>`
}

// 解析终端命令输出的ANSI转义序列
export const parseAnsiOutput = (output) => {
  return output.replace(/\u001b\[\d+m/g, '')
}

// 格式化终端命令
export const formatCommand = (command) => {
  return command.trim().replace(/\s+/g, ' ')
}

// 解析错误堆栈
export const parseErrorStack = (error) => {
  const stack = error.stack || ''
  const lines = stack.split('\n').map(line => line.trim())
  return {
    message: error.message,
    name: error.name,
    stack: lines
  }
}

// 检测是否支持某个终端特性
export const hasTerminalFeature = (feature) => {
  const features = {
    '256color': process.env.TERM && process.env.TERM.includes('256'),
    'truecolor': process.env.COLORTERM === 'truecolor',
    'unicode': process.env.LANG && process.env.LANG.includes('UTF-8')
  }
  return features[feature] || false
}

// 检查命令是否存在
export const commandExists = async (command) => {
  try {
    const response = await fetch(`/api/command-exists?command=${command}`)
    const data = await response.json()
    return data.exists
  } catch {
    return false
  }
} 