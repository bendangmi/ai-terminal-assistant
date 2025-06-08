<!-- Settings.vue -->
<template>
  <div class="settings">
    <el-tabs>
      <!-- AI配置 -->
      <el-tab-pane label="AI配置">
        <el-form :model="aiConfig" label-width="120px">
          <el-form-item label="提供商">
            <el-select v-model="aiConfig.provider" placeholder="请选择提供商">
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="OpenAI" value="openai" />
            </el-select>
          </el-form-item>
          <el-form-item label="API密钥">
            <el-input
              v-model="aiConfig.api_key"
              type="password"
              placeholder="请输入API密钥"
              show-password
            />
          </el-form-item>
          <el-form-item label="模型">
            <el-select v-model="aiConfig.model" placeholder="请选择模型">
              <el-option
                v-for="model in availableModels[aiConfig.provider]"
                :key="model"
                :label="model"
                :value="model"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="温度">
            <el-slider
              v-model="aiConfig.temperature"
              :min="0"
              :max="2"
              :step="0.1"
              show-input
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 系统配置 -->
      <el-tab-pane label="系统配置">
        <el-form :model="systemConfig" label-width="120px">
          <el-form-item label="更新间隔(秒)">
            <el-input-number
              v-model="systemConfig.updateInterval"
              :min="1"
              :max="60"
            />
          </el-form-item>
          <el-form-item label="日志级别">
            <el-select v-model="systemConfig.logLevel" placeholder="请选择日志级别">
              <el-option label="DEBUG" value="debug" />
              <el-option label="INFO" value="info" />
              <el-option label="WARNING" value="warning" />
              <el-option label="ERROR" value="error" />
            </el-select>
          </el-form-item>
          <el-form-item label="自动启动">
            <el-switch v-model="systemConfig.autoStart" />
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 终端配置 -->
      <el-tab-pane label="终端配置">
        <el-form :model="terminalConfig" label-width="120px">
          <el-form-item label="字体大小">
            <el-input-number
              v-model="terminalConfig.fontSize"
              :min="8"
              :max="32"
            />
          </el-form-item>
          <el-form-item label="字体">
            <el-select v-model="terminalConfig.fontFamily" placeholder="请选择字体">
              <el-option label="Consolas" value="Consolas" />
              <el-option label="Monaco" value="Monaco" />
              <el-option label="Menlo" value="Menlo" />
              <el-option label="Source Code Pro" value="Source Code Pro" />
            </el-select>
          </el-form-item>
          <el-form-item label="主题">
            <el-select v-model="terminalConfig.theme" placeholder="请选择主题">
              <el-option label="暗色" value="dark" />
              <el-option label="亮色" value="light" />
            </el-select>
          </el-form-item>
          <el-form-item label="命令历史数">
            <el-input-number
              v-model="terminalConfig.historySize"
              :min="50"
              :max="1000"
              :step="50"
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <!-- 操作按钮 -->
    <div class="settings-actions">
      <el-button type="primary" @click="saveSettings">保存设置</el-button>
      <el-button @click="resetSettings">重置</el-button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { API_ENDPOINTS } from '../config/api'

export default {
  name: 'Settings',
  setup() {
    const aiConfig = ref({
      provider: 'deepseek',
      api_key: '',
      model: 'deepseek-coder',
      temperature: 0.7
    })

    const systemConfig = ref({
      updateInterval: 5,
      logLevel: 'info',
      autoStart: false,
      debugMode: false
    })

    const terminalConfig = ref({
      fontSize: 14,
      fontFamily: 'Consolas',
      theme: 'dark',
      historySize: 100
    })

    const availableModels = {
      deepseek: [
        'deepseek-chat',
        'deepseek-coder'
      ],
      openai: [
        'gpt-4',
        'gpt-4-turbo',
        'gpt-3.5-turbo'
      ]
    }

    // 加载设置
    const loadSettings = async (retryCount = 0) => {
      try {
        const response = await axios.get(API_ENDPOINTS.SETTINGS, {
          timeout: 10000 // 增加超时时间到10秒
        })
        const settings = response.data
        
        // 加载AI配置
        const provider = settings.ai?.provider || 'deepseek'
        const providerConfig = settings.ai?.[provider] || {}
        
        aiConfig.value = {
          provider: provider,
          api_key: providerConfig.api_key || '',
          model: providerConfig.model || availableModels[provider][0],
          temperature: providerConfig.temperature || 0.7
        }
        
        // 加载系统配置
        systemConfig.value = {
          updateInterval: settings.general?.history_size || 5,
          logLevel: settings.logging?.level?.toLowerCase() || 'info',
          autoStart: settings.general?.auto_start || false,
          debugMode: settings.general?.debug_mode || false
        }
        
        // 加载终端配置
        const terminalSettings = settings.ui?.terminal || {}
        terminalConfig.value = {
          fontSize: terminalSettings.font_size || 14,
          fontFamily: terminalSettings.font_family || 'Consolas',
          theme: terminalSettings.theme || 'dark',
          historySize: terminalSettings.history_size || 100
        }
      } catch (error) {
        console.error('加载设置失败:', error)
        
        // 如果是超时错误且重试次数小于3，则进行重试
        if (error.code === 'ECONNABORTED' && retryCount < 3) {
          const delay = Math.min(1000 * Math.pow(2, retryCount), 4000) // 指数退避，最大4秒
          console.log(`将在 ${delay}ms 后重试加载设置`)
          await new Promise(resolve => setTimeout(resolve, delay))
          return loadSettings(retryCount + 1)
        }
        
        ElMessage.error('加载设置失败')
      }
    }

    // 保存设置
    const saveSettings = async () => {
      try {
        // 构建正确的配置格式
        const config = {
          ai: {
            provider: aiConfig.value.provider,
            [aiConfig.value.provider]: {
              model: aiConfig.value.model,
              api_key: aiConfig.value.api_key,
              temperature: aiConfig.value.temperature
            }
          },
          general: {
            history_size: systemConfig.value.updateInterval,
            debug_mode: systemConfig.value.debugMode,
            auto_start: systemConfig.value.autoStart
          },
          logging: {
            level: systemConfig.value.logLevel.toUpperCase()
          },
          ui: {
            terminal: {
              font_size: terminalConfig.value.fontSize,
              font_family: terminalConfig.value.fontFamily,
              theme: terminalConfig.value.theme,
              history_size: terminalConfig.value.historySize
            }
          }
        }

        await axios.post(API_ENDPOINTS.SETTINGS, config)
        ElMessage.success('设置保存成功')
      } catch (error) {
        ElMessage.error('保存设置失败')
        console.error('保存设置失败:', error)
      }
    }

    // 重置设置
    const resetSettings = () => {
      loadSettings()
    }

    onMounted(() => {
      loadSettings()
    })

    return {
      aiConfig,
      systemConfig,
      terminalConfig,
      availableModels,
      saveSettings,
      resetSettings
    }
  }
}
</script>

<style scoped>
.settings {
  padding: 20px;
}

.settings-actions {
  margin-top: 20px;
  text-align: right;
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-slider) {
  width: 300px;
}
</style> 