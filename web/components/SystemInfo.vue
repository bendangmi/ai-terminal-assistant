<!-- 系统信息组件 -->
<template>
  <div class="system-info">
    <el-collapse v-model="activeNames">
      <!-- 系统资源信息 -->
      <el-collapse-item title="系统资源信息" name="1">
        <div class="resource-info">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>CPU 使用率</span>
                  </div>
                </template>
                <el-progress
                  type="dashboard"
                  :percentage="systemInfo.cpu?.percent || 0"
                  :color="getProgressColor"
                />
                <div class="detail-info">
                  <p>核心数: {{ systemInfo.cpu?.cores }}</p>
                  <p>频率: {{ (systemInfo.cpu?.frequency / 1000).toFixed(2) }} GHz</p>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>内存使用率</span>
                  </div>
                </template>
                <el-progress
                  type="dashboard"
                  :percentage="systemInfo.memory?.percent || 0"
                  :color="getProgressColor"
                />
                <div class="detail-info">
                  <p>总内存: {{ formatBytes(systemInfo.memory?.total) }}</p>
                  <p>可用: {{ formatBytes(systemInfo.memory?.available) }}</p>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>磁盘使用率</span>
                  </div>
                </template>
                <el-progress
                  type="dashboard"
                  :percentage="systemInfo.disk?.percent || 0"
                  :color="getProgressColor"
                />
                <div class="detail-info">
                  <p>总空间: {{ formatBytes(systemInfo.disk?.total) }}</p>
                  <p>可用: {{ formatBytes(systemInfo.disk?.free) }}</p>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-collapse-item>

      <!-- 目录信息 -->
      <el-collapse-item title="目录信息" name="2">
        <div class="directory-info">
          <el-input
            v-model="currentPath"
            placeholder="输入路径"
            class="path-input"
          >
            <template #append>
              <el-button @click="loadDirectoryInfo">刷新</el-button>
            </template>
          </el-input>

          <el-table :data="directoryInfo.files" style="width: 100%">
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="size" label="大小">
              <template #default="scope">
                {{ formatBytes(scope.row.size) }}
              </template>
            </el-table-column>
            <el-table-column prop="modified" label="修改时间">
              <template #default="scope">
                {{ formatDate(scope.row.modified) }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'SystemInfo',
  setup() {
    const activeNames = ref(['1', '2'])
    const systemInfo = ref({})
    const directoryInfo = ref({
      files: [],
      directories: []
    })
    const currentPath = ref('./')

    const loadSystemInfo = async () => {
      try {
        const response = await axios.get('/api/system-info')
        systemInfo.value = response.data
      } catch (error) {
        console.error('加载系统信息失败:', error)
      }
    }

    const loadDirectoryInfo = async () => {
      try {
        const response = await axios.get('/api/directory-info', {
          params: { path: currentPath.value }
        })
        directoryInfo.value = response.data
      } catch (error) {
        console.error('加载目录信息失败:', error)
      }
    }

    const formatBytes = (bytes) => {
      if (!bytes) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
    }

    const formatDate = (timestamp) => {
      return new Date(timestamp * 1000).toLocaleString()
    }

    const getProgressColor = (percentage) => {
      if (percentage < 60) return '#67C23A'
      if (percentage < 80) return '#E6A23C'
      return '#F56C6C'
    }

    // 定时更新系统信息
    onMounted(() => {
      loadSystemInfo()
      loadDirectoryInfo()
      setInterval(loadSystemInfo, 5000)
    })

    return {
      activeNames,
      systemInfo,
      directoryInfo,
      currentPath,
      loadDirectoryInfo,
      formatBytes,
      formatDate,
      getProgressColor
    }
  }
}
</script>

<style scoped>
.system-info {
  padding: 20px;
}

.resource-info {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-info {
  margin-top: 20px;
  text-align: center;
}

.detail-info p {
  margin: 5px 0;
}

.path-input {
  margin-bottom: 20px;
}

.directory-info {
  margin-top: 20px;
}
</style> 