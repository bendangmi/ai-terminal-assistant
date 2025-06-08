<!-- 主应用组件 -->
<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <h1>AI终端助手</h1>
      <div class="header-actions">
        <el-button type="primary" @click="showSettings = true">
          设置
        </el-button>
      </div>
    </el-header>
    
    <el-main>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="system-monitor">
            <template #header>
              <div class="card-header">
                <span>系统监控</span>
                <el-button
                  type="text"
                  @click="toggleSystemInfo"
                >
                  {{ systemInfoVisible ? '收起' : '展开' }}
                </el-button>
              </div>
            </template>
            <el-collapse-transition>
              <div v-show="systemInfoVisible">
                <SystemInfo />
              </div>
            </el-collapse-transition>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="mt-20">
        <el-col :span="24">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>连接配置</span>
              </div>
            </template>
            <ConnectionTest />
          </el-card>
        </el-col>
      </el-row>
    </el-main>

    <!-- 设置对话框 -->
    <el-dialog
      v-model="showSettings"
      title="系统设置"
      width="80%"
      :close-on-click-modal="false"
    >
      <Settings />
    </el-dialog>
  </el-container>
</template>

<script>
import { ref } from 'vue'
import SystemInfo from './components/SystemInfo.vue'
import ConnectionTest from './components/ConnectionTest.vue'
import Settings from './components/Settings.vue'

export default {
  name: 'App',
  components: {
    SystemInfo,
    ConnectionTest,
    Settings
  },
  setup() {
    const systemInfoVisible = ref(true)
    const showSettings = ref(false)

    const toggleSystemInfo = () => {
      systemInfoVisible.value = !systemInfoVisible.value
    }

    return {
      systemInfoVisible,
      showSettings,
      toggleSystemInfo
    }
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.app-container {
  height: 100%;
}

.app-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.app-header h1 {
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}

.system-monitor {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mt-20 {
  margin-top: 20px;
}

/* 全局样式 */
:deep(.el-dialog__body) {
  padding: 0;
}
</style> 