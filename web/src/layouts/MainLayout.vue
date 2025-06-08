<!-- MainLayout.vue -->
<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="aside">
      <div class="logo" :class="{ 'logo-collapse': isCollapse }">
        <img src="@/assets/logo.svg" alt="logo" />
        <span v-show="!isCollapse">AI Terminal</span>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        :collapse="isCollapse"
        @select="handleSelect"
        router
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <template #title>首页</template>
        </el-menu-item>
        
        <el-menu-item index="/terminal">
          <el-icon><Tools /></el-icon>
          <template #title>终端</template>
        </el-menu-item>
        
        <el-menu-item index="/monitor">
          <el-icon><Monitor /></el-icon>
          <template #title>系统监控</template>
        </el-menu-item>
        
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <template #title>设置</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主要内容区 -->
    <el-container class="main-container">
      <el-header class="header">
        <div class="header-left">
          <el-button
            type="text"
            @click="toggleCollapse"
            class="toggle-button"
          >
            <el-icon>
              <component :is="isCollapse ? 'Expand' : 'Fold'" />
            </el-icon>
          </el-button>
          
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentRoute.meta.title">
              {{ currentRoute.meta.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <el-button
            type="text"
            class="theme-toggle"
            @click="toggleTheme"
          >
            <el-icon>
              <component :is="isDark ? 'Sunny' : 'Moon'" />
            </el-icon>
          </el-button>

          <el-dropdown>
            <el-avatar :size="32" :src="userAvatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleSettings">
                  <el-icon><Setting /></el-icon>设置
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>退出
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/theme'
import {
  HomeFilled,
  Monitor,
  Setting,
  Expand,
  Fold,
  SwitchButton,
  User,
  Moon,
  Sunny,
  Tools
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()

const isCollapse = ref(false)
const userAvatar = ref('')

// 计算当前激活的菜单项
const activeMenu = computed(() => route.path)

// 计算当前路由信息
const currentRoute = computed(() => route)

// 计算是否暗色主题
const isDark = computed(() => themeStore.isDark)

// 切换侧边栏折叠状态
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

// 切换主题
const toggleTheme = () => {
  themeStore.toggleTheme()
}

// 处理菜单选择
const handleSelect = (index) => {
  router.push(index)
}

// 处理设置点击
const handleSettings = () => {
  router.push('/settings')
}

// 处理退出登录
const handleLogout = () => {
  ElMessageBox.confirm('确认退出系统吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('已退出系统')
    // TODO: 实现退出逻辑
  }).catch(() => {})
}
</script>

<style>
.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-color-primary);
  transition: var(--transition-colors);
}

/* 顶部导航栏 */
.navbar {
  height: 60px;
  padding: 0 var(--spacing-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--bg-color-float);
  border-bottom: 1px solid var(--border-color-base);
  box-shadow: var(--shadow-base);
  position: relative;
  z-index: 100;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  text-decoration: none;
}

.brand-logo {
  height: 32px;
  width: auto;
  filter: drop-shadow(0 0 8px var(--primary-color));
}

.brand-text {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-color-primary);
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 10px rgba(22, 119, 255, 0.2);
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
}

.nav-link {
  padding: var(--spacing-2) var(--spacing-4);
  color: var(--text-color-regular);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: var(--transition-all);
}

.nav-link:hover {
  color: var(--primary-color);
  background: var(--bg-color-secondary);
}

.nav-link.active {
  color: var(--primary-color);
  background: var(--primary-bg);
  font-weight: var(--font-weight-semibold);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.theme-switch {
  display: flex;
  align-items: center;
  padding: var(--spacing-2);
  color: var(--text-color-regular);
  background: var(--bg-color-secondary);
  border: 1px solid var(--border-color-base);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: var(--transition-all);
}

.theme-switch:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.theme-switch .el-icon {
  font-size: var(--font-size-lg);
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  padding: var(--spacing-6);
  overflow-y: auto;
  background: var(--bg-color-secondary);
}

.content-container {
  max-width: 1440px;
  margin: 0 auto;
  height: 100%;
}

/* 暗色主题适配 */
[data-theme="dark"] .main-layout {
  background: var(--dark-bg-primary);
}

[data-theme="dark"] .navbar {
  background: var(--dark-bg-secondary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] .brand-text {
  color: var(--text-color-inverse);
}

[data-theme="dark"] .nav-link {
  color: var(--text-color-regular);
}

[data-theme="dark"] .nav-link:hover {
  color: var(--primary-color);
  background: var(--dark-bg-tertiary);
}

[data-theme="dark"] .nav-link.active {
  color: var(--primary-color);
  background: var(--primary-bg);
}

[data-theme="dark"] .theme-switch {
  color: var(--text-color-regular);
  background: var(--dark-bg-tertiary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] .main-content {
  background: var(--dark-bg-primary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar {
    height: 50px;
    padding: 0 var(--spacing-4);
  }

  .brand-logo {
    height: 24px;
  }

  .brand-text {
    font-size: var(--font-size-lg);
  }

  .navbar-menu {
    gap: var(--spacing-2);
  }

  .nav-link {
    padding: var(--spacing-2) var(--spacing-3);
  }

  .main-content {
    padding: var(--spacing-4);
  }
}

@media (max-width: 480px) {
  .navbar-menu {
    display: none;
  }
}
</style> 