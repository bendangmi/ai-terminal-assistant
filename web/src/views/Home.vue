<template>
  <div class="home">
    <div class="home__hero">
      <h1 class="home__title">AI 终端助手</h1>
      <p class="home__subtitle">智能化的终端操作与系统监控工具</p>
      <div class="home__actions">
        <el-button type="primary" size="large" @click="$router.push('/terminal')">
          <el-icon><Tools /></el-icon>
          开始使用终端
        </el-button>
        <el-button size="large" @click="$router.push('/monitor')">
          <el-icon><Monitor /></el-icon>
          查看系统状态
        </el-button>
      </div>
    </div>

    <div class="home__features">
      <h2 class="home__section-title">主要功能</h2>
      <div class="home__feature-grid">
        <div class="feature-card" v-for="feature in features" :key="feature.title">
          <el-icon class="feature-card__icon">
            <component :is="feature.icon" />
          </el-icon>
          <h3 class="feature-card__title">{{ feature.title }}</h3>
          <p class="feature-card__desc">{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Tools, Monitor, ChatLineRound, Setting } from '@element-plus/icons-vue'

const features = [
  {
    icon: 'Tools',
    title: '智能终端',
    description: '支持自然语言交互的智能终端，让命令行操作更简单'
  },
  {
    icon: 'Monitor',
    title: '系统监控',
    description: '实时监控系统资源使用情况，包括 CPU、内存、磁盘等'
  },
  {
    icon: 'ChatLineRound',
    title: '智能对话',
    description: '基于 AI 的智能对话系统，帮助解决各种系统操作问题'
  },
  {
    icon: 'Setting',
    title: '可定制化',
    description: '支持主题切换、终端配置等个性化设置'
  }
]
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-6);
}

.home__hero {
  text-align: center;
  margin-bottom: var(--spacing-8);
  padding: var(--spacing-8) 0;
}

.home__title {
  font-size: 3.5rem;
  font-weight: 800;
  color: var(--text-color);
  margin-bottom: var(--spacing-4);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 10px rgba(0, 180, 216, 0.2);
}

.home__subtitle {
  font-size: var(--font-size-xl);
  color: var(--text-color-secondary);
  margin-bottom: var(--spacing-8);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.home__actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-4);
  margin-bottom: var(--spacing-8);
}

.home__actions .el-button {
  padding: 12px 24px;
  font-size: var(--font-size-md);
}

.home__section-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: var(--spacing-8);
  text-align: center;
}

.home__feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-6);
}

.feature-card {
  padding: var(--spacing-6);
  border-radius: var(--radius-lg);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop-filter);
  -webkit-backdrop-filter: var(--glass-backdrop-filter);
  border: 1px solid var(--glass-border);
  text-align: center;
  transition: var(--transition-all);
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-color);
}

.feature-card__icon {
  width: 48px;
  height: 48px;
  font-size: 48px;
  margin-bottom: var(--spacing-4);
  color: var(--primary-color);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.feature-card__title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: var(--spacing-3);
}

.feature-card__desc {
  color: var(--text-color-secondary);
  line-height: 1.6;
  font-size: var(--font-size-base);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .home {
    padding: var(--spacing-4);
  }

  .home__title {
    font-size: 2rem;
  }

  .home__subtitle {
    font-size: var(--font-size-md);
  }

  .home__actions {
    flex-direction: column;
  }

  .home__feature-grid {
    grid-template-columns: 1fr;
  }
}
</style> 