<!-- App.vue -->
<template>
  <el-config-provider :locale="zhCn">
    <router-view v-slot="{ Component }">
      <transition name="fade-transform" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </el-config-provider>
</template>

<script setup>
import { onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const themeStore = useThemeStore()

onMounted(() => {
  // 初始化主题
  themeStore.initTheme()
})
</script>

<style>
/* 全局样式 */
:root {
  color-scheme: light dark;
}

html {
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
  -webkit-text-size-adjust: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

body {
  margin: 0;
  min-height: 100vh;
  color: var(--text-color-primary);
  background: var(--bg-color-primary);
  transition: var(--transition-colors);
}

#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--text-color-placeholder);
  border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-color-secondary);
}

/* Element Plus 主题覆盖 */
:deep(.el-button) {
  --el-button-bg-color: var(--bg-color-float);
  --el-button-border-color: var(--border-color-base);
  --el-button-hover-bg-color: var(--bg-color-secondary);
  --el-button-hover-border-color: var(--primary-color);
  --el-button-active-bg-color: var(--bg-color-tertiary);
  --el-button-active-border-color: var(--primary-dark);
}

:deep(.el-button--primary) {
  --el-button-bg-color: var(--primary-color);
  --el-button-border-color: var(--primary-color);
  --el-button-hover-bg-color: var(--primary-light);
  --el-button-hover-border-color: var(--primary-light);
  --el-button-active-bg-color: var(--primary-dark);
  --el-button-active-border-color: var(--primary-dark);
}

:deep(.el-input__wrapper) {
  background: var(--bg-color-float);
  border: 1px solid var(--border-color-base);
  box-shadow: none !important;
}

:deep(.el-input__wrapper:hover) {
  border-color: var(--primary-color);
}

:deep(.el-input__wrapper.is-focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1) !important;
}

:deep(.el-dialog) {
  --el-dialog-bg-color: var(--bg-color-float);
  --el-dialog-border-radius: var(--radius-lg);
  border: 1px solid var(--border-color-base);
}

:deep(.el-card) {
  --el-card-bg-color: var(--bg-color-float);
  --el-card-border-radius: var(--radius-lg);
  border: 1px solid var(--border-color-base);
}

:deep(.el-menu) {
  --el-menu-bg-color: var(--bg-color-float);
  --el-menu-border-color: var(--border-color-base);
  --el-menu-hover-bg-color: var(--bg-color-secondary);
  --el-menu-active-color: var(--primary-color);
}

:deep(.el-tabs) {
  --el-tabs-header-bg-color: var(--bg-color-float);
  --el-tabs-border-color: var(--border-color-base);
  --el-tabs-active-color: var(--primary-color);
}

/* 暗色主题 */
[data-theme="dark"] {
  color-scheme: dark;
}

[data-theme="dark"] body {
  color: var(--text-color-inverse);
  background: var(--dark-bg-primary);
}

[data-theme="dark"] :deep(.el-button) {
  --el-button-bg-color: var(--dark-bg-tertiary);
  --el-button-border-color: var(--border-color-base);
  --el-button-hover-bg-color: var(--dark-bg-quaternary);
  --el-button-text-color: var(--text-color-inverse);
}

[data-theme="dark"] :deep(.el-input__wrapper) {
  background: var(--dark-bg-tertiary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] :deep(.el-dialog) {
  --el-dialog-bg-color: var(--dark-bg-secondary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] :deep(.el-card) {
  --el-card-bg-color: var(--dark-bg-secondary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] :deep(.el-menu) {
  --el-menu-bg-color: var(--dark-bg-secondary);
  --el-menu-text-color: var(--text-color-inverse);
  --el-menu-hover-bg-color: var(--dark-bg-tertiary);
  --el-menu-border-color: var(--border-color-base);
}

[data-theme="dark"] :deep(.el-tabs) {
  --el-tabs-header-bg-color: var(--dark-bg-secondary);
  --el-tabs-nav-color: var(--text-color-inverse);
  --el-tabs-border-color: var(--border-color-base);
}

/* 响应式设计 */
@media (max-width: 768px) {
  html {
    font-size: 14px;
  }
}

@media (min-width: 769px) and (max-width: 1280px) {
  html {
    font-size: 15px;
  }
}

@media (min-width: 1281px) {
  html {
    font-size: 16px;
  }
}
</style> 