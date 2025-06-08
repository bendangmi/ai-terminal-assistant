<template>
  <div class="settings-view">
    <el-card class="settings-card">
      <template #header>
        <div class="settings-card__header">
          <h2 class="settings-card__title">
            <el-icon><Setting /></el-icon>
            设置
          </h2>
        </div>
      </template>

      <el-form label-position="top">
        <!-- 主题设置 -->
        <el-form-item label="主题">
          <el-select v-model="currentTheme" class="settings-select">
            <el-option
              v-for="theme in themes"
              :key="theme.value"
              :label="theme.label"
              :value="theme.value"
            />
          </el-select>
        </el-form-item>

        <!-- 终端设置 -->
        <el-divider>终端设置</el-divider>
        <el-form-item label="字体大小">
          <el-input-number
            v-model="terminalFontSize"
            :min="12"
            :max="24"
            class="settings-input"
          />
        </el-form-item>

        <el-form-item label="字体">
          <el-select v-model="terminalFont" class="settings-select">
            <el-option label="Consolas" value="Consolas" />
            <el-option label="Monaco" value="Monaco" />
            <el-option label="Courier New" value="Courier New" />
          </el-select>
        </el-form-item>

        <el-form-item label="光标样式">
          <el-select v-model="cursorStyle" class="settings-select">
            <el-option label="块状" value="block" />
            <el-option label="下划线" value="underline" />
            <el-option label="竖线" value="bar" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="cursorBlink">光标闪烁</el-checkbox>
        </el-form-item>

        <!-- 系统设置 -->
        <el-divider>系统设置</el-divider>
        <el-form-item label="数据刷新间隔 (秒)">
          <el-input-number
            v-model="refreshInterval"
            :min="1"
            :max="60"
            class="settings-input"
          />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="enableNotifications">启用系统通知</el-checkbox>
        </el-form-item>

        <!-- 按钮 -->
        <div class="settings-actions">
          <el-button type="primary" @click="saveSettings">保存设置</el-button>
          <el-button @click="resetSettings">重置默认</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Setting } from '@element-plus/icons-vue'
import { useThemeStore } from '@/store'

// 主题相关
const themeStore = useThemeStore()
const currentTheme = ref(themeStore.currentTheme)
const themes = themeStore.themes

// 终端设置
const terminalFontSize = ref(14)
const terminalFont = ref('Consolas')
const cursorStyle = ref('block')
const cursorBlink = ref(true)

// 系统设置
const refreshInterval = ref(2)
const enableNotifications = ref(true)

// 保存设置
const saveSettings = () => {
  // 保存主题
  themeStore.setTheme(currentTheme.value)

  // 保存其他设置
  // TODO: 实现设置保存逻辑

  ElMessage.success('设置已保存')
}

// 重置设置
const resetSettings = () => {
  currentTheme.value = 'light'
  terminalFontSize.value = 14
  terminalFont.value = 'Consolas'
  cursorStyle.value = 'block'
  cursorBlink.value = true
  refreshInterval.value = 2
  enableNotifications.value = true

  ElMessage.info('设置已重置')
}
</script>

<style>
.settings {
  padding: 2rem;
}

.settings-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
}

.settings-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  border-radius: 0.5rem;
  background-color: var(--bg-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
}

.form-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  background-color: white;
}

.btn-save {
  margin-top: 1rem;
}
</style> 