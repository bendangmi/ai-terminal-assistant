<!-- 连接测试组件 -->
<template>
  <div class="connection-test">
    <el-tabs v-model="activeTab">
      <!-- 服务器连接测试 -->
      <el-tab-pane label="服务器连接测试" name="server">
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
            <el-button
              type="primary"
              @click="testServerConnection"
              :loading="serverTesting"
            >
              测试连接
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 大模型配置测试 -->
      <el-tab-pane label="大模型配置测试" name="llm">
        <el-form
          ref="llmForm"
          :model="llmConfig"
          :rules="llmRules"
          label-width="120px"
        >
          <el-form-item label="API Key" prop="api_key">
            <el-input
              v-model="llmConfig.api_key"
              type="password"
              show-password
              placeholder="输入您的API Key"
            />
          </el-form-item>
          
          <el-form-item label="模型名称" prop="model_name">
            <el-input
              v-model="llmConfig.model_name"
              placeholder="例如: gpt-4"
            />
          </el-form-item>
          
          <el-form-item label="API Base URL">
            <el-input
              v-model="llmConfig.api_base"
              placeholder="可选，默认为OpenAI官方API"
            />
          </el-form-item>
          
          <el-form-item label="组织ID">
            <el-input
              v-model="llmConfig.organization"
              placeholder="可选，用于多组织账户"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              @click="testLLMConfig"
              :loading="llmTesting"
            >
              测试配置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'ConnectionTest',
  setup() {
    const activeTab = ref('server')
    const serverTesting = ref(false)
    const llmTesting = ref(false)

    const serverConfig = reactive({
      host: '',
      port: 8000,
      protocol: 'http',
      username: '',
      password: ''
    })

    const llmConfig = reactive({
      api_key: '',
      model_name: 'gpt-4',
      api_base: '',
      organization: ''
    })

    const serverRules = {
      host: [
        { required: true, message: '请输入服务器地址', trigger: 'blur' }
      ],
      port: [
        { required: true, message: '请输入端口号', trigger: 'blur' },
        { type: 'number', message: '端口号必须为数字', trigger: 'blur' }
      ]
    }

    const llmRules = {
      api_key: [
        { required: true, message: '请输入API Key', trigger: 'blur' }
      ],
      model_name: [
        { required: true, message: '请输入模型名称', trigger: 'blur' }
      ]
    }

    const testServerConnection = async () => {
      try {
        serverTesting.value = true
        const response = await axios.post('/api/test-server-connection', serverConfig)
        ElMessage.success(response.data.message)
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '连接测试失败')
      } finally {
        serverTesting.value = false
      }
    }

    const testLLMConfig = async () => {
      try {
        llmTesting.value = true
        const response = await axios.post('/api/test-llm-config', llmConfig)
        ElMessage.success(response.data.message)
      } catch (error) {
        ElMessage.error(error.response?.data?.detail || '配置测试失败')
      } finally {
        llmTesting.value = false
      }
    }

    return {
      activeTab,
      serverConfig,
      llmConfig,
      serverRules,
      llmRules,
      serverTesting,
      llmTesting,
      testServerConnection,
      testLLMConfig
    }
  }
}
</script>

<style scoped>
.connection-test {
  padding: 20px;
}

.el-form {
  max-width: 600px;
  margin: 0 auto;
}
</style> 