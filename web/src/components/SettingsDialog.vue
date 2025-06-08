<!-- SettingsDialog.vue -->
<template>
  <el-dialog
    v-model="dialogVisible"
    title="系统设置"
    width="800px"
    :close-on-click-modal="false"
    class="settings-dialog"
    destroy-on-close
  >
    <el-tabs class="settings-tabs">
      <!-- 终端设置 -->
      <el-tab-pane label="终端设置">
        <el-form :model="terminalConfig" label-width="120px" class="settings-form">
          <el-form-item label="字体大小" class="form-item">
            <el-input-number
              v-model="terminalConfig.fontSize"
              :min="8"
              :max="32"
              @change="handleTerminalConfigChange"
              class="custom-number-input"
            />
          </el-form-item>

          <el-form-item label="字体" class="form-item">
            <el-select 
              v-model="terminalConfig.fontFamily" 
              @change="handleTerminalConfigChange"
              class="custom-select"
            >
              <el-option label="Consolas" value="Consolas" />
              <el-option label="Monaco" value="Monaco" />
              <el-option label="Menlo" value="Menlo" />
              <el-option label="Source Code Pro" value="Source Code Pro" />
            </el-select>
          </el-form-item>

          <el-form-item label="光标样式" class="form-item">
            <el-select 
              v-model="terminalConfig.cursorStyle" 
              @change="handleTerminalConfigChange"
              class="custom-select"
            >
              <el-option label="块状" value="block" />
              <el-option label="下划线" value="underline" />
              <el-option label="竖线" value="bar" />
            </el-select>
          </el-form-item>

          <el-form-item class="form-item">
            <el-checkbox 
              v-model="terminalConfig.cursorBlink"
              @change="handleTerminalConfigChange"
              class="custom-checkbox"
            >
              光标闪烁
            </el-checkbox>
          </el-form-item>

          <el-form-item label="命令历史数" class="form-item">
            <el-input-number
              v-model="terminalConfig.historySize"
              :min="50"
              :max="1000"
              :step="50"
              @change="handleTerminalConfigChange"
              class="custom-number-input"
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 系统设置 -->
      <el-tab-pane label="系统设置">
        <el-form :model="systemConfig" label-width="120px" class="settings-form">
          <el-form-item label="更新间隔(秒)" class="form-item">
            <el-input-number
              v-model="systemConfig.updateInterval"
              :min="1"
              :max="60"
              @change="handleSystemConfigChange"
              class="custom-number-input"
            />
          </el-form-item>

          <el-form-item label="日志级别" class="form-item">
            <el-select 
              v-model="systemConfig.logLevel"
              @change="handleSystemConfigChange"
              class="custom-select"
            >
              <el-option label="DEBUG" value="debug" />
              <el-option label="INFO" value="info" />
              <el-option label="WARNING" value="warning" />
              <el-option label="ERROR" value="error" />
            </el-select>
          </el-form-item>

          <el-form-item class="form-item">
            <el-checkbox 
              v-model="systemConfig.autoStart"
              @change="handleSystemConfigChange"
              class="custom-checkbox"
            >
              系统启动时自动运行
            </el-checkbox>
          </el-form-item>

          <el-form-item class="form-item">
            <el-checkbox 
              v-model="systemConfig.notifications"
              @change="handleSystemConfigChange"
              class="custom-checkbox"
            >
              启用系统通知
            </el-checkbox>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- AI配置 -->
      <el-tab-pane label="AI配置">
        <el-form :model="aiConfig" label-width="120px" class="settings-form">
          <el-form-item label="提供商" class="form-item">
            <el-select 
              v-model="aiConfig.provider"
              @change="handleAiConfigChange"
              class="custom-select"
            >
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="OpenAI" value="openai" />
            </el-select>
          </el-form-item>

          <el-form-item label="API密钥" class="form-item">
            <el-input
              v-model="aiConfig.apiKey"
              type="password"
              show-password
              @change="handleAiConfigChange"
              class="custom-input"
            />
          </el-form-item>

          <el-form-item label="模型" class="form-item">
            <el-select 
              v-model="aiConfig.model"
              @change="handleAiConfigChange"
              class="custom-select"
            >
              <el-option
                v-for="model in availableModels[aiConfig.provider]"
                :key="model"
                :label="model"
                :value="model"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="温度" class="form-item">
            <el-slider
              v-model="aiConfig.temperature"
              :min="0"
              :max="2"
              :step="0.1"
              show-input
              @change="handleAiConfigChange"
              class="custom-slider"
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 快捷键设置 -->
      <el-tab-pane label="快捷键">
        <el-form :model="shortcutConfig" label-width="120px" class="settings-form">
          <el-form-item label="执行命令" class="form-item">
            <el-input
              v-model="shortcutConfig.execute"
              placeholder="Enter"
              readonly
              @click="startShortcutCapture('execute')"
              class="custom-input shortcut-input"
            />
          </el-form-item>

          <el-form-item label="清空终端" class="form-item">
            <el-input
              v-model="shortcutConfig.clear"
              placeholder="Ctrl + L"
              readonly
              @click="startShortcutCapture('clear')"
              class="custom-input shortcut-input"
            />
          </el-form-item>

          <el-form-item label="复制内容" class="form-item">
            <el-input
              v-model="shortcutConfig.copy"
              placeholder="Ctrl + C"
              readonly
              @click="startShortcutCapture('copy')"
              class="custom-input shortcut-input"
            />
          </el-form-item>

          <el-form-item label="粘贴内容" class="form-item">
            <el-input
              v-model="shortcutConfig.paste"
              placeholder="Ctrl + V"
              readonly
              @click="startShortcutCapture('paste')"
              class="custom-input shortcut-input"
            />
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveSettings">保存</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useSettingsStore } from '../stores/settings'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const settingsStore = useSettingsStore()

// 对话框显示控制
const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 配置数据
const terminalConfig = ref({
  fontSize: 14,
  fontFamily: 'Consolas',
  cursorStyle: 'block',
  cursorBlink: true,
  historySize: 100
})

const systemConfig = ref({
  updateInterval: 5,
  logLevel: 'info',
  autoStart: false,
  notifications: true
})

const aiConfig = ref({
  provider: 'deepseek',
  apiKey: '',
  model: 'deepseek-coder',
  temperature: 0.7
})

const shortcutConfig = ref({
  execute: 'Enter',
  clear: 'Ctrl + L',
  copy: 'Ctrl + C',
  paste: 'Ctrl + V'
})

// AI模型选项
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

// 配置变更处理
const handleTerminalConfigChange = () => {
  settingsStore.updateTerminalConfig(terminalConfig.value)
}

const handleSystemConfigChange = () => {
  settingsStore.updateSystemConfig(systemConfig.value)
}

const handleAiConfigChange = () => {
  settingsStore.updateAiConfig(aiConfig.value)
}

// 快捷键捕获
const startShortcutCapture = (type) => {
  ElMessage.info('请按下新的快捷键组合')
  // TODO: 实现快捷键捕获逻辑
}

// 保存设置
const saveSettings = async () => {
  try {
    await settingsStore.saveSettings({
      terminal: terminalConfig.value,
      system: systemConfig.value,
      ai: aiConfig.value,
      shortcuts: shortcutConfig.value
    })
    ElMessage.success('设置保存成功')
    dialogVisible.value = false
  } catch (error) {
    ElMessage.error('保存设置失败')
  }
}

// 监听对话框显示
watch(() => dialogVisible.value, (visible) => {
  if (visible) {
    // 加载当前设置
    const settings = settingsStore.currentSettings
    terminalConfig.value = { ...settings.terminal }
    systemConfig.value = { ...settings.system }
    aiConfig.value = { ...settings.ai }
    shortcutConfig.value = { ...settings.shortcuts }
  }
})
</script>

<style scoped>
.settings-dialog {
  --dialog-margin-top: 5vh;
}

.settings-dialog :deep(.el-dialog) {
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  margin-top: var(--dialog-margin-top) !important;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: var(--glass-backdrop-filter);
  -webkit-backdrop-filter: var(--glass-backdrop-filter);
}

.settings-dialog :deep(.el-dialog__header) {
  margin: 0;
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(5px);
}

.settings-dialog :deep(.el-dialog__title) {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-color);
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.settings-dialog :deep(.el-dialog__body) {
  padding: 0;
  background: var(--glass-bg);
}

.settings-dialog :deep(.el-dialog__footer) {
  padding: var(--spacing-4) var(--spacing-6);
  border-top: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(5px);
}

.settings-tabs {
  padding: var(--spacing-6);
}

.settings-tabs :deep(.el-tabs__nav-wrap) {
  padding: 0 var(--spacing-4);
}

.settings-tabs :deep(.el-tabs__item) {
  font-size: var(--font-size-md);
  padding: var(--spacing-3) var(--spacing-4);
  color: var(--text-color-secondary);
  transition: var(--transition-all);
}

.settings-tabs :deep(.el-tabs__item.is-active) {
  color: var(--primary-color);
  font-weight: var(--font-weight-semibold);
  text-shadow: 0 0 10px var(--primary-color);
}

.settings-tabs :deep(.el-tabs__active-bar) {
  height: 3px;
  border-radius: var(--radius-full);
  background: var(--primary-gradient);
  box-shadow: var(--shadow-glow);
}

.settings-form {
  padding: var(--spacing-6) var(--spacing-4);
  background: var(--glass-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--glass-border);
}

.form-item {
  margin-bottom: var(--spacing-6);
}

.form-item :deep(.el-form-item__label) {
  font-size: var(--font-size-sm);
  color: var(--text-color);
  font-weight: var(--font-weight-medium);
  padding-right: var(--spacing-4);
}

.custom-input :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  box-shadow: none !important;
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.02);
  transition: var(--transition-all);
}

.custom-input :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-color);
}

.custom-input :deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.2) !important;
}

.custom-input :deep(.el-input__inner) {
  height: 40px;
  font-size: var(--font-size-md);
  color: var(--text-color);
}

.custom-select :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  box-shadow: none !important;
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.02);
  transition: var(--transition-all);
}

.custom-select :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-color);
}

.custom-select :deep(.el-select__tags) {
  background: transparent;
}

.custom-select :deep(.el-tag) {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: var(--text-color-inverse);
}

.custom-number-input :deep(.el-input__wrapper) {
  border-radius: var(--radius-lg);
  box-shadow: none !important;
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.02);
  transition: var(--transition-all);
}

.custom-number-input :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-color);
}

.custom-number-input :deep(.el-input-number__decrease),
.custom-number-input :deep(.el-input-number__increase) {
  background: transparent;
  border-color: var(--glass-border);
  color: var(--text-color);
}

.custom-number-input :deep(.el-input-number__decrease:hover),
.custom-number-input :deep(.el-input-number__increase:hover) {
  color: var(--primary-color);
}

.custom-checkbox {
  height: 40px;
  display: flex;
  align-items: center;
}

.custom-checkbox :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.custom-checkbox :deep(.el-checkbox__label) {
  color: var(--text-color);
}

.custom-slider :deep(.el-slider__runway) {
  height: 6px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-full);
}

.custom-slider :deep(.el-slider__bar) {
  height: 6px;
  border-radius: var(--radius-full);
  background: var(--primary-gradient);
}

.custom-slider :deep(.el-slider__button) {
  width: 16px;
  height: 16px;
  border: 2px solid var(--primary-color);
  background: var(--bg-color-secondary);
  transition: var(--transition-all);
}

.custom-slider :deep(.el-slider__button:hover) {
  transform: scale(1.2);
}

.shortcut-input {
  cursor: pointer;
}

.shortcut-input :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--glass-border);
}

.shortcut-input :deep(.el-input__inner) {
  cursor: pointer;
  color: var(--text-color);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-3);
}

.dialog-footer .el-button {
  border-radius: var(--radius-lg);
  padding: var(--spacing-2) var(--spacing-6);
  font-weight: var(--font-weight-medium);
  transition: var(--transition-all);
}

.dialog-footer .el-button--default {
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.02);
  color: var(--text-color);
}

.dialog-footer .el-button--default:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  transform: translateY(-2px);
}

.dialog-footer .el-button--primary {
  background: var(--primary-gradient);
  border: none;
}

.dialog-footer .el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

@media (max-width: 768px) {
  .settings-dialog {
    --dialog-margin-top: 2vh;
  }

  .settings-dialog :deep(.el-dialog) {
    width: 95% !important;
    margin: var(--dialog-margin-top) auto !important;
  }

  .settings-form {
    padding: var(--spacing-4) var(--spacing-3);
  }

  .form-item {
    margin-bottom: var(--spacing-4);
  }

  .form-item :deep(.el-form-item__label) {
    padding-right: var(--spacing-3);
  }
}
</style> 