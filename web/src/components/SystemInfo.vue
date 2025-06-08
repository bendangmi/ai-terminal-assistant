<!-- SystemInfo.vue -->
<template>
  <div class="system-info">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="8">
        <el-card class="info-card glass-effect" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><Monitor /></el-icon>
              <span>CPU 使用率</span>
            </div>
          </template>
          <div class="metric">
            <div class="metric-main">
              <div class="progress-wrapper">
                <el-progress
                  type="dashboard"
                  :percentage="cpuUsage"
                  :color="getProgressColor(cpuUsage)"
                  :stroke-width="6"
                  :width="90"
                />
              </div>
              <div class="metric-details">
                <div class="metric-value">{{ cpuUsage }}%</div>
                <div class="metric-label">已使用</div>
              </div>
            </div>
            <div class="metric-info">
              <div class="info-item">
                <el-icon><Cpu /></el-icon>
                <span>核心数：{{ systemInfo.cpu.cores }}</span>
              </div>
              <div class="info-item">
                <el-icon><Timer /></el-icon>
                <span>频率：{{ systemInfo.cpu.frequency }} GHz</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="24" :md="8">
        <el-card class="info-card glass-effect" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><Cpu /></el-icon>
              <span>内存使用率</span>
            </div>
          </template>
          <div class="metric">
            <div class="metric-main">
              <div class="progress-wrapper">
                <el-progress
                  type="dashboard"
                  :percentage="memoryUsage"
                  :color="getProgressColor(memoryUsage)"
                  :stroke-width="6"
                  :width="90"
                />
              </div>
              <div class="metric-details">
                <div class="metric-value">{{ memoryUsage }}%</div>
                <div class="metric-label">已使用</div>
              </div>
            </div>
            <div class="metric-info">
              <div class="info-item">
                <el-icon><Box /></el-icon>
                <span>总内存：{{ systemInfo.memory.total }}</span>
              </div>
              <div class="info-item">
                <el-icon><Check /></el-icon>
                <span>可用：{{ systemInfo.memory.available }}</span>
              </div>
              <div class="info-item">
                <el-icon><Loading /></el-icon>
                <span>已用：{{ systemInfo.memory.used }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="24" :md="8">
        <el-card class="info-card glass-effect" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><FolderOpened /></el-icon>
              <span>磁盘使用率</span>
            </div>
          </template>
          <div class="metric">
            <div class="metric-main">
              <div class="progress-wrapper">
                <el-progress
                  type="dashboard"
                  :percentage="diskUsage"
                  :color="getProgressColor(diskUsage)"
                  :stroke-width="6"
                  :width="90"
                />
              </div>
              <div class="metric-details">
                <div class="metric-value">{{ diskUsage }}%</div>
                <div class="metric-label">已使用</div>
              </div>
            </div>
            <div class="metric-info">
              <div class="info-item">
                <el-icon><Files /></el-icon>
                <span>总容量：{{ systemInfo.disk.total }}</span>
              </div>
              <div class="info-item">
                <el-icon><Document /></el-icon>
                <span>已用：{{ systemInfo.disk.used }}</span>
              </div>
              <div class="info-item">
                <el-icon><Folder /></el-icon>
                <span>可用：{{ systemInfo.disk.free }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card class="info-card system-details glass-effect" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><InfoFilled /></el-icon>
              <span>系统信息</span>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="操作系统">
              <el-tag size="small" type="info" class="system-tag">{{ systemInfo.os }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="平台">
              <el-tag size="small" type="success" class="system-tag">{{ systemInfo.platform }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="Python版本">
              <el-tag size="small" type="warning" class="system-tag">{{ systemInfo.python_version }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="CPU核心数">
              <el-tag size="small" type="danger" class="system-tag">{{ systemInfo.cpu_count }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="工作目录" :span="2">
              <el-tag size="small" type="info" class="workspace-tag system-tag">
                {{ systemInfo.working_directory }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <!-- 错误提示 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      closable
      class="error-alert"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  Monitor,
  Cpu,
  FolderOpened,
  InfoFilled,
  Timer,
  Box,
  Check,
  Loading,
  Files,
  Document,
  Folder
} from '@element-plus/icons-vue'
import axios from 'axios'
import { API_ENDPOINTS } from '../config/api'

const cpuUsage = ref(0)
const memoryUsage = ref(0)
const diskUsage = ref(0)
const systemInfo = ref({
  cpu: {
    cores: 0,
    frequency: 0
  },
  memory: {
    total: 0,
    available: 0,
    used: 0
  },
  disk: {
    total: 0,
    used: 0,
    free: 0
  }
})
const loading = ref(false)
const error = ref(null)
const retryCount = ref(0)
const maxRetries = 3
let timer = null

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

const fetchSystemInfo = async (retryCount = 0) => {
  try {
    const response = await axios.get(API_ENDPOINTS.SYSTEM.INFO, {
      timeout: 10000 // 10秒超时
    })
    systemInfo.value = response.data
    error.value = null
    retryCount = 0 // 重置重试计数
  } catch (err) {
    console.error('获取系统信息失败:', err)
    // 设置错误消息
    error.value = err.message || '获取系统信息失败'
    
    // 如果是超时错误且重试次数小于3，则进行重试
    if (err.code === 'ECONNABORTED' && retryCount < 3) {
      const delay = Math.min(1000 * Math.pow(2, retryCount), 4000)
      console.log(`将在 ${delay}ms 后进行第 ${retryCount + 1} 次重试`)
      await new Promise(resolve => setTimeout(resolve, delay))
      return fetchSystemInfo(retryCount + 1)
    }
  }
}

const getProgressColor = (percentage) => {
  if (percentage < 60) return [{
    color: '#67C23A',
    percentage: 60
  }, {
    color: '#E6A23C',
    percentage: 80
  }, {
    color: '#F56C6C',
    percentage: 100
  }]
  if (percentage < 80) return '#E6A23C'
  return '#F56C6C'
}

onMounted(() => {
  fetchSystemInfo()
  // 降低轮询频率到15秒
  timer = setInterval(fetchSystemInfo, 15000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
})
</script>

<style>
.system-info {
  padding: var(--spacing-4);
  background: var(--bg-color-secondary);
  min-height: 100%;
}

.info-card {
  height: 100%;
  transition: var(--transition-all);
  background: var(--bg-color-primary);
  border: 1px solid var(--border-color-base);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-base);
  overflow: hidden;
  position: relative;
}

.info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--primary-gradient);
  opacity: 0;
  transition: var(--transition-opacity);
}

.info-card:hover {
  transform: translateY(-4px);
  border-color: var(--primary-color);
  box-shadow: var(--shadow-medium), var(--shadow-glow);
}

.info-card:hover::before {
  opacity: 1;
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text-color-primary);
  padding: var(--spacing-4);
  border-bottom: 1px solid var(--border-color-light);
  background: var(--bg-color-secondary);
}

.header-icon {
  font-size: var(--font-size-lg);
  color: var(--primary-color);
  filter: drop-shadow(0 0 8px var(--primary-color));
}

.metric {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  padding: var(--spacing-4);
  position: relative;
}

.metric-main {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: var(--spacing-6);
  padding: var(--spacing-4);
  background: var(--bg-color-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color-light);
}

.progress-wrapper {
  position: relative;
}

.metric-details {
  text-align: center;
  padding: var(--spacing-3);
  background: var(--bg-color-float);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color-light);
}

.metric-value {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-color-primary);
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-1);
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.metric-label {
  font-size: var(--font-size-sm);
  color: var(--text-color-secondary);
  font-weight: var(--font-weight-medium);
}

.metric-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
  padding: var(--spacing-3);
  background: var(--bg-color-float);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color-light);
}

.info-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  color: var(--text-color-regular);
  font-size: var(--font-size-sm);
  padding: var(--spacing-2) var(--spacing-3);
  border-radius: var(--radius-md);
  transition: var(--transition-all);
  background: var(--bg-color-secondary);
  border: 1px solid transparent;
}

.info-item:hover {
  background: var(--bg-color-tertiary);
  border-color: var(--border-color-base);
  transform: translateX(4px);
  color: var(--text-color-primary);
}

.info-item .el-icon {
  color: var(--primary-color);
  font-size: var(--font-size-md);
  filter: drop-shadow(0 0 5px var(--primary-color));
}

.system-details {
  margin-top: var(--spacing-6);
}

.system-details :deep(.el-descriptions__cell) {
  padding: var(--spacing-3) var(--spacing-4);
}

.system-details :deep(.el-descriptions__label) {
  color: var(--text-color-regular);
  font-weight: var(--font-weight-medium);
  background: var(--bg-color-secondary);
}

.system-tag {
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: var(--spacing-2) var(--spacing-3);
}

.mt-20 {
  margin-top: var(--spacing-5);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .system-info {
    padding: var(--spacing-2);
  }
  
  .el-col {
    margin-bottom: var(--spacing-4);
  }
  
  .metric {
    padding: var(--spacing-3);
  }
  
  .metric-main {
    flex-direction: column;
    gap: var(--spacing-3);
    padding: var(--spacing-3);
  }
  
  .metric-info {
    padding: var(--spacing-2);
  }
  
  .system-details :deep(.el-descriptions__cell) {
    padding: var(--spacing-2);
  }
  
  .card-header {
    padding: var(--spacing-2) var(--spacing-3);
  }
  
  .info-item {
    padding: var(--spacing-2);
  }
}
</style> 