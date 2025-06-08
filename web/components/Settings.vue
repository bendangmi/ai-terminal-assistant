<!-- 设置页面组件 -->
<template>
  <div class="settings-container">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 服务器设置 -->
      <el-tab-pane label="服务器设置" name="server">
        <el-form
          ref="serverForm"
          :model="serverConfig"
          :rules="serverRules"
          label-width="120px"
        >
          <el-form-item label="服务器地址" prop="host">
            <el-input v-model="serverConfig.host" placeholder="例如: localhost" />
          </el-form-item>
          
          <el-form-item label="端口" prop="port">
            <el-input-number v-model="serverConfig.port" :min="1" :max="65535" />
          </el-form-item>
          
          <el-form-item label="协议">
            <el-select v-model="serverConfig.protocol">
              <el-option label="HTTP" value="http" />
              <el-option label="HTTPS" value="https" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="用户名">
            <el-input v-model="serverConfig.username" placeholder="可选" />
          </el-form-item>
          
          <el-form-item label="密码">
            <el-input
              v-model="serverConfig.password"
              type="password"
              placeholder="可选"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="testServerConnection">
              测试连接
            </el-button>
            <el-button type="success" @click="saveServerConfig">
              保存配置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- AI设置 -->
      <el-tab-pane label="AI设置" name="ai">
        <el-form
          ref="aiForm"
          :model="aiConfig"
          :rules="aiRules"
          label-width="120px"
        >
          <el-form-item label="AI提供商" prop="provider">
            <el-select v-model="aiConfig.provider" @change="handleProviderChange">
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="OpenAI" value="openai" />
            </el-select>
          </el-form-item>

          <el-form-item label="模型" prop="model">
            <el-select v-model="aiConfig.model">
              <template v-if="aiConfig.provider === 'deepseek'">
                <el-option label="DeepSeek Chat" value="deepseek-chat" />
                <el-option label="DeepSeek Coder" value="deepseek-coder" />
              </template>
              <template v-else>
                <el-option label="GPT-4" value="gpt-4" />
                <el-option label="GPT-4 Turbo" value="gpt-4-turbo" />
                <el-option label="GPT-3.5 Turbo" value="gpt-3.5-turbo" />
              </template>
            </el-select>
          </el-form-item>

          <el-form-item label="API密钥" prop="apiKey">
            <el-input
              v-model="aiConfig.apiKey"
              type="password"
              show-password
              placeholder="输入API密钥"
            />
          </el-form-item>

          <el-form-item label="温度">
            <el-slider
              v-model="aiConfig.temperature"
              :min="0"
              :max="1"
              :step="0.1"
              show-input
            />
          </el-form-item>

          <el-form-item label="最大令牌数">
            <el-input-number
              v-model="aiConfig.maxTokens"
              :min="1"
              :max="4000"
              :step="100"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="testAIConfig">
              测试配置
            </el-button>
            <el-button type="success" @click="saveAIConfig">
              保存配置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 系统设置 -->
      <el-tab-pane label="系统设置" name="system">
        <el-form
          ref="systemForm"
          :model="systemConfig"
          label-width="120px"
        >
          <el-form-item label="调试模式">
            <el-switch v-model="systemConfig.debugMode" />
          </el-form-item>

          <el-form-item label="历史记录大小">
            <el-input-number
              v-model="systemConfig.historySize"
              :min="1"
              :max="100"
              :step="1"
            />
          </el-form-item>

          <el-form-item label="日志级别">
            <el-select v-model="systemConfig.logLevel">
              <el-option label="DEBUG" value="DEBUG" />
              <el-option label="INFO" value="INFO" />
              <el-option label="WARNING" value="WARNING" />
              <el-option label="ERROR" value="ERROR" />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="success" @click="saveSystemConfig">
              保存配置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'Settings',
  setup() {
    const activeTab = ref('server')

    // 服务器配置
    const serverConfig = reactive({
      host: '',
      port: 8000,
      protocol: 'http',
      username: '',
      password: ''
    })

    const serverRules = {
      host: [
        { required: true, message: '请输入服务器地址', trigger: 'blur' }
      ],
      port: [
        { required: true, message: '请输入端口号', trigger: 'blur' }
      ]
    }

    // AI配置
    const aiConfig = reactive({
      provider: 'deepseek',
      model: 'deepseek-coder',
      apiKey: '',
      temperature: 0.7,
      maxTokens: 2000
    })

    const aiRules = {
      provider: [
        { required: true, message: '请选择AI提供商', trigger: 'change' }
      ],
      model: [
        { required: true, message: '请选择模型', trigger: 'change' }
      ],
      apiKey: [
        { required: true, message: '请输入API密钥', trigger: 'blur' }
      ]
    }

    // 系统配置
    const systemConfig = reactive({
      debugMode: false,
      historySize: 20,
      logLevel: 'INFO'
    })

    // 测试服务器连接
    const testServerConnection = async () => {
      try {
        const response = await axios.post('/api/test-server-connection', serverConfig)
        ElMessage.success(response.data.message || '服务器连接成功')
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '服务器连接失败')
      }
    }

    // 测试AI配置
    const testAIConfig = async () => {
      try {
        const response = await axios.post('/api/test-ai-config', {
          provider: aiConfig.provider,
          api_key: aiConfig.apiKey,
          model: aiConfig.model
        })
        ElMessage.success(response.data.message || 'AI配置测试成功')
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || 'AI配置测试失败')
      }
    }

    // 保存配置
    const saveServerConfig = async () => {
      try {
        await axios.post('/api/save-config', {
          section: 'server',
          config: serverConfig
        })
        ElMessage.success('服务器配置已保存')
      } catch (error) {
        ElMessage.error('保存服务器配置失败')
      }
    }

    const saveAIConfig = async () => {
      try {
        await axios.post('/api/save-config', {
          section: 'ai',
          config: aiConfig
        })
        ElMessage.success('AI配置已保存')
      } catch (error) {
        ElMessage.error('保存AI配置失败')
      }
    }

    const saveSystemConfig = async () => {
      try {
        await axios.post('/api/save-config', {
          section: 'system',
          config: systemConfig
        })
        ElMessage.success('系统配置已保存')
      } catch (error) {
        ElMessage.error('保存系统配置失败')
      }
    }

    // 处理AI提供商变更
    const handleProviderChange = (provider) => {
      aiConfig.model = provider === 'deepseek' ? 'deepseek-coder' : 'gpt-4'
    }

    return {
      activeTab,
      serverConfig,
      serverRules,
      aiConfig,
      aiRules,
      systemConfig,
      testServerConnection,
      testAIConfig,
      saveServerConfig,
      saveAIConfig,
      saveSystemConfig,
      handleProviderChange
    }
  }
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.el-form {
  margin-top: 20px;
}

.el-form-item {
  margin-bottom: 22px;
}

.el-button {
  margin-right: 10px;
}
</style> 