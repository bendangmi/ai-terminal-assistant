<template>
  <div class="monitor-view">
    <el-row :gutter="24">
      <!-- CPU 使用率 -->
      <el-col :xs="24" :sm="12" :md="8">
        <div class="monitor-card">
          <div class="monitor-card__header">
            <div class="monitor-card__title">
              <el-icon><Monitor /></el-icon>
              <span>CPU 使用率</span>
            </div>
            <el-tag :type="getCpuStatus" effect="dark">{{ cpuUsage }}%</el-tag>
          </div>
          <div class="monitor-card__chart">
            <line-chart
              :chart-data="cpuChartData"
              :options="cpuChartOptions"
            />
          </div>
          <div class="monitor-card__footer">
            <div class="metric-item">
              <span class="metric-label">核心数</span>
              <span class="metric-value">{{ cpuInfo.cores }}</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">频率</span>
              <span class="metric-value">{{ cpuInfo.frequency }}GHz</span>
            </div>
          </div>
        </div>
      </el-col>

      <!-- 内存使用率 -->
      <el-col :xs="24" :sm="12" :md="8">
        <div class="monitor-card">
          <div class="monitor-card__header">
            <div class="monitor-card__title">
              <el-icon><Connection /></el-icon>
              <span>内存使用率</span>
            </div>
            <el-tag :type="getMemoryStatus" effect="dark">{{ memoryUsage }}%</el-tag>
          </div>
          <div class="monitor-card__chart">
            <line-chart
              :chart-data="memoryChartData"
              :options="memoryChartOptions"
            />
          </div>
          <div class="monitor-card__footer">
            <div class="metric-item">
              <span class="metric-label">总内存</span>
              <span class="metric-value">{{ formatBytes(memoryInfo.total) }}</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">已用</span>
              <span class="metric-value">{{ formatBytes(memoryInfo.used) }}</span>
            </div>
          </div>
        </div>
      </el-col>

      <!-- 磁盘使用情况 -->
      <el-col :xs="24" :md="8">
        <div class="monitor-card">
          <div class="monitor-card__header">
            <div class="monitor-card__title">
              <el-icon><Document /></el-icon>
              <span>磁盘使用情况</span>
            </div>
          </div>
          <div class="monitor-card__content">
            <el-table 
              :data="diskUsage" 
              stripe 
              style="width: 100%"
              size="small"
              :header-cell-style="{
                background: 'var(--dark-bg-light)',
                color: 'var(--dark-text)',
                borderColor: 'var(--dark-border)'
              }"
            >
              <el-table-column prop="device" label="设备" width="80" />
              <el-table-column prop="mountpoint" label="挂载点" width="100" />
              <el-table-column prop="usage" label="使用率" width="200">
                <template #default="{ row }">
                  <el-progress
                    :percentage="row.usage"
                    :status="getDiskStatus(row.usage)"
                    :stroke-width="8"
                  />
                </template>
              </el-table-column>
              <el-table-column prop="free" label="可用" align="right" />
            </el-table>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  Monitor,
  Connection,
  Document
} from '@element-plus/icons-vue'
import { Line as LineChart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// 注册 Chart.js 组件
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

// 状态
const cpuUsage = ref(0)
const memoryUsage = ref(0)
const diskUsage = ref([])
const cpuInfo = ref({ cores: 0, frequency: 0 })
const memoryInfo = ref({ total: 0, used: 0 })

// 图表数据
const cpuChartData = ref({
  labels: [],
  datasets: [{
    label: 'CPU 使用率',
    data: [],
    borderColor: 'rgb(75, 192, 192)',
    backgroundColor: 'rgba(75, 192, 192, 0.2)',
    fill: true,
    tension: 0.4,
    pointRadius: 0
  }]
})

const memoryChartData = ref({
  labels: [],
  datasets: [{
    label: '内存使用率',
    data: [],
    borderColor: 'rgb(255, 99, 132)',
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    fill: true,
    tension: 0.4,
    pointRadius: 0
  }]
})

// 图表配置
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 0
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      },
      ticks: {
        color: 'rgba(255, 255, 255, 0.7)'
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        color: 'rgba(255, 255, 255, 0.7)',
        maxRotation: 0
      }
    }
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: 'rgba(255, 255, 255, 0.2)',
      borderWidth: 1
    }
  }
}

const cpuChartOptions = { ...chartOptions }
const memoryChartOptions = { ...chartOptions }

// 计算属性
const getCpuStatus = computed(() => {
  if (cpuUsage.value > 90) return 'danger'
  if (cpuUsage.value > 70) return 'warning'
  return 'success'
})

const getMemoryStatus = computed(() => {
  if (memoryUsage.value > 90) return 'danger'
  if (memoryUsage.value > 70) return 'warning'
  return 'success'
})

const getDiskStatus = (usage) => {
  if (usage > 90) return 'exception'
  if (usage > 70) return 'warning'
  return 'success'
}

// 工具函数
const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`
}

// 更新数据
const updateData = () => {
  // 模拟数据更新
  cpuUsage.value = Math.floor(Math.random() * 100)
  memoryUsage.value = Math.floor(Math.random() * 100)
  cpuInfo.value = { cores: 8, frequency: 3.6 }
  memoryInfo.value = { total: 16 * 1024 * 1024 * 1024, used: 8 * 1024 * 1024 * 1024 }

  const now = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  
  // 更新图表数据
  if (cpuChartData.value.labels.length > 10) {
    cpuChartData.value.labels.shift()
    cpuChartData.value.datasets[0].data.shift()
    memoryChartData.value.labels.shift()
    memoryChartData.value.datasets[0].data.shift()
  }
  
  cpuChartData.value.labels.push(now)
  cpuChartData.value.datasets[0].data.push(cpuUsage.value)
  memoryChartData.value.labels.push(now)
  memoryChartData.value.datasets[0].data.push(memoryUsage.value)
}

// 更新磁盘使用情况
const updateDiskUsage = () => {
  diskUsage.value = [
    {
      device: 'C:',
      mountpoint: 'C:',
      total: '256GB',
      used: '180GB',
      free: '76GB',
      usage: 70
    },
    {
      device: 'D:',
      mountpoint: 'D:',
      total: '512GB',
      used: '256GB',
      free: '256GB',
      usage: 50
    }
  ]
}

let updateInterval

onMounted(() => {
  updateData()
  updateDiskUsage()
  updateInterval = setInterval(updateData, 2000)
})

onUnmounted(() => {
  if (updateInterval) {
    clearInterval(updateInterval)
  }
})
</script>

<style>
.monitor-view {
  padding: var(--spacing-base);
}

.monitor-card {
  height: 100%;
  background-color: var(--dark-bg);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--dark-border);
  overflow: hidden;
  transition: all var(--animation-duration-base) var(--animation-timing-base);
}

.monitor-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-card);
}

.monitor-card__header {
  padding: var(--spacing-base);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--dark-bg-light);
  border-bottom: 1px solid var(--dark-border);
}

.monitor-card__title {
  display: flex;
  align-items: center;
  gap: var(--spacing-small);
  color: var(--dark-text);
  font-size: var(--font-size-base);
  font-weight: 500;
}

.monitor-card__title .el-icon {
  font-size: 20px;
  color: var(--primary-color);
}

.monitor-card__chart {
  height: 200px;
  padding: var(--spacing-base);
}

.monitor-card__content {
  padding: var(--spacing-base);
}

.monitor-card__footer {
  padding: var(--spacing-base);
  display: flex;
  justify-content: space-around;
  border-top: 1px solid var(--dark-border);
  background-color: var(--dark-bg-light);
}

.metric-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.metric-label {
  color: var(--dark-text-secondary);
  font-size: var(--font-size-small);
}

.metric-value {
  color: var(--dark-text);
  font-size: var(--font-size-base);
  font-weight: 500;
}

/* Element Plus 表格样式覆盖 */
:deep(.el-table) {
  background-color: transparent;
  color: var(--dark-text);
}

:deep(.el-table tr) {
  background-color: transparent;
}

:deep(.el-table td),
:deep(.el-table th) {
  border-color: var(--dark-border);
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: var(--dark-bg-light);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .monitor-view {
    padding: var(--spacing-small);
  }

  .el-col {
    margin-bottom: var(--spacing-base);
  }

  .monitor-card__chart {
    height: 150px;
  }
}
</style> 