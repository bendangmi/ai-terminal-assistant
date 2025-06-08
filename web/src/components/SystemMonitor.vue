<!-- SystemMonitor.vue -->
<template>
  <div class="system-monitor">
    <!-- CPU使用率 -->
    <div class="monitor-card">
      <div class="monitor-card__header">
        <div class="monitor-card__title">
          <el-icon class="card-icon"><Cpu /></el-icon>
          <span>CPU使用率</span>
        </div>
        <el-tag :type="getCpuStatus" effect="dark" class="usage-tag">{{ cpuUsage }}%</el-tag>
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
          <span class="metric-value">{{ formatFrequency(cpuInfo.frequency) }}</span>
        </div>
      </div>
    </div>

    <!-- 内存使用率 -->
    <div class="monitor-card">
      <div class="monitor-card__header">
        <div class="monitor-card__title">
          <el-icon class="card-icon"><Monitor /></el-icon>
          <span>内存使用率</span>
        </div>
        <el-tag :type="getMemoryStatus" effect="dark" class="usage-tag">{{ memoryUsage }}%</el-tag>
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
          <span class="metric-value">{{ formatSize(memoryInfo.total) }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">已用</span>
          <span class="metric-value">{{ formatSize(memoryInfo.used) }}</span>
        </div>
        <div class="metric-item">
          <span class="metric-label">可用</span>
          <span class="metric-value">{{ formatSize(memoryInfo.available) }}</span>
        </div>
      </div>
    </div>

    <!-- 磁盘使用率 -->
    <div class="monitor-card">
      <div class="monitor-card__header">
        <div class="monitor-card__title">
          <el-icon class="card-icon"><Files /></el-icon>
          <span>磁盘使用率</span>
        </div>
      </div>
      <div class="disk-list">
        <div v-for="disk in diskUsage" :key="disk.mount" class="disk-item">
          <div class="disk-info">
            <span class="disk-mount">{{ disk.mount }}</span>
            <el-tag :type="getDiskStatus(disk.usage)" size="small" class="usage-tag">
              {{ disk.usage }}%
            </el-tag>
          </div>
          <el-progress
            :percentage="disk.usage"
            :status="getDiskStatus(disk.usage)"
            :stroke-width="6"
            class="disk-progress"
          />
          <div class="disk-details">
            <div class="detail-item">
              <span class="detail-label">总容量:</span>
              <span class="detail-value">{{ formatSize(disk.total) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">已用:</span>
              <span class="detail-value">{{ formatSize(disk.used) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">可用:</span>
              <span class="detail-value">{{ formatSize(disk.free) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 系统信息 -->
    <div class="monitor-card">
      <div class="monitor-card__header">
        <div class="monitor-card__title">
          <el-icon class="card-icon"><InfoFilled /></el-icon>
          <span>系统信息</span>
        </div>
      </div>
      <div class="system-info">
        <div class="info-item">
          <span class="info-label">操作系统</span>
          <span class="info-value">{{ systemInfo.os }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">平台</span>
          <span class="info-value">{{ systemInfo.platform }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Python版本</span>
          <span class="info-value">{{ systemInfo.python_version }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">工作目录</span>
          <span class="info-value truncate">{{ systemInfo.working_directory }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useSystemStore } from '../stores/system'
import { Cpu, Monitor, Files, InfoFilled } from '@element-plus/icons-vue'
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

// 注册Chart.js组件
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

// Store
const systemStore = useSystemStore()

// 计算属性
const cpuUsage = computed(() => systemStore.cpuUsage)
const memoryUsage = computed(() => systemStore.memoryUsage)
const diskUsage = computed(() => systemStore.diskUsage)
const systemInfo = computed(() => systemStore.systemInfo)
const cpuInfo = computed(() => systemStore.cpuInfo)
const memoryInfo = computed(() => systemStore.memoryInfo)

// 状态指示器
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
  if (usage > 90) return 'danger'
  if (usage > 70) return 'warning'
  return 'success'
}

// 图表数据
const cpuChartData = computed(() => ({
  labels: systemStore.timeLabels,
  datasets: [
    {
      label: 'CPU使用率',
      data: systemStore.cpuHistory,
      borderColor: '#409EFF',
      backgroundColor: 'rgba(64, 158, 255, 0.1)',
      fill: true,
      tension: 0.4
    }
  ]
}))

const memoryChartData = computed(() => ({
  labels: systemStore.timeLabels,
  datasets: [
    {
      label: '内存使用率',
      data: systemStore.memoryHistory,
      borderColor: '#67C23A',
      backgroundColor: 'rgba(103, 194, 58, 0.1)',
      fill: true,
      tension: 0.4
    }
  ]
}))

// 图表配置
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 300
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      ticks: {
        callback: value => `${value}%`
      }
    }
  },
  plugins: {
    legend: {
      display: false
    }
  }
}

const cpuChartOptions = {
  ...chartOptions,
  plugins: {
    ...chartOptions.plugins,
    title: {
      display: false
    }
  }
}

const memoryChartOptions = {
  ...chartOptions,
  plugins: {
    ...chartOptions.plugins,
    title: {
      display: false
    }
  }
}

// 格式化函数
const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}

const formatFrequency = (mhz) => {
  if (mhz >= 1000) {
    return `${(mhz / 1000).toFixed(2)} GHz`
  }
  return `${mhz.toFixed(2)} MHz`
}

// 生命周期钩子
onMounted(() => {
  systemStore.startMonitoring()
})

onUnmounted(() => {
  systemStore.stopMonitoring()
})
</script>

<style scoped>
.system-monitor {
  padding: var(--spacing-6);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-6);
  background: var(--neutral-100);
  min-height: 100vh;
}

.monitor-card {
  background: var(--neutral-50);
  border-radius: var(--radius-xl);
  padding: var(--spacing-6);
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
  transition: var(--transition-all);
}

.monitor-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.monitor-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.monitor-card__title {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--neutral-800);
}

.card-icon {
  font-size: var(--font-size-xl);
  color: var(--primary-500);
}

.usage-tag {
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-full);
}

.monitor-card__chart {
  height: 200px;
  position: relative;
}

.monitor-card__footer {
  display: flex;
  justify-content: space-around;
  padding-top: var(--spacing-4);
  border-top: 1px solid var(--neutral-200);
}

.metric-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-2);
}

.metric-label {
  font-size: var(--font-size-sm);
  color: var(--neutral-600);
}

.metric-value {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  color: var(--neutral-800);
}

.disk-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.disk-item {
  padding: var(--spacing-4);
  background: var(--neutral-100);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-3);
}

.disk-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.disk-mount {
  font-weight: var(--font-weight-medium);
  color: var(--neutral-700);
}

.disk-progress {
  margin: var(--spacing-2) 0;
}

.disk-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-3);
  font-size: var(--font-size-sm);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-1);
}

.detail-label {
  color: var(--neutral-600);
}

.detail-value {
  font-weight: var(--font-weight-medium);
  color: var(--neutral-800);
}

.system-info {
  display: grid;
  gap: var(--spacing-4);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-3);
  background: var(--neutral-100);
  border-radius: var(--radius-lg);
}

.info-label {
  color: var(--neutral-600);
}

.info-value {
  font-weight: var(--font-weight-medium);
  color: var(--neutral-800);
}

.truncate {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 768px) {
  .system-monitor {
    padding: var(--spacing-4);
    gap: var(--spacing-4);
  }

  .monitor-card {
    padding: var(--spacing-4);
    gap: var(--spacing-4);
  }

  .disk-details {
    grid-template-columns: 1fr;
    gap: var(--spacing-2);
  }
}
</style> 