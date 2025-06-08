<template>
  <div class="terminal-view">
    <div class="terminal-container">
      <div class="terminal-header">
        <div class="terminal-header__title">
          <el-icon><Monitor /></el-icon>
          <span>智能终端</span>
        </div>
        <div class="terminal-header__actions">
          <el-tooltip content="清空终端" placement="top">
            <el-button type="primary" plain @click="clearTerminal">
              <el-icon><Delete /></el-icon>
            </el-button>
          </el-tooltip>
          <el-tooltip content="复制内容" placement="top">
            <el-button type="primary" plain @click="copyToClipboard">
              <el-icon><CopyDocument /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
      </div>
      <div ref="terminalRef" class="terminal-content"></div>
      <div class="terminal-footer">
        <div class="terminal-status">
          <el-tag size="small" type="success">已连接</el-tag>
          <span class="terminal-info">终端就绪</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Terminal as XTerm } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { WebLinksAddon } from 'xterm-addon-web-links'
import { SearchAddon } from 'xterm-addon-search'
import { 
  Monitor,
  Delete,
  CopyDocument
} from '@element-plus/icons-vue'
import 'xterm/css/xterm.css'

const terminalRef = ref(null)
let terminal = null
let fitAddon = null

// 初始化终端
onMounted(() => {
  terminal = new XTerm({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: 'var(--font-family-code)',
    theme: {
      background: 'var(--dark-bg)',
      foreground: 'var(--dark-text)',
      cursor: 'var(--primary-color)',
      selection: 'rgba(255, 255, 255, 0.3)',
      black: '#000000',
      red: 'var(--error-color)',
      green: 'var(--success-color)',
      yellow: 'var(--warning-color)',
      blue: 'var(--primary-color)',
      magenta: '#c678dd',
      cyan: '#56b6c2',
      white: '#ffffff',
      brightBlack: '#5c6370',
      brightRed: '#e06c75',
      brightGreen: '#98c379',
      brightYellow: '#d19a66',
      brightBlue: '#61afef',
      brightMagenta: '#c678dd',
      brightCyan: '#56b6c2',
      brightWhite: '#ffffff'
    }
  })

  fitAddon = new FitAddon()
  terminal.loadAddon(fitAddon)
  terminal.loadAddon(new WebLinksAddon())
  terminal.loadAddon(new SearchAddon())

  terminal.open(terminalRef.value)
  fitAddon.fit()

  window.addEventListener('resize', handleResize)

  // 欢迎信息
  terminal.writeln('\x1b[1;34m欢迎使用 AI 终端助手!\x1b[0m')
  terminal.writeln('\x1b[90m输入命令或使用自然语言描述你想要执行的操作。\x1b[0m')
  terminal.writeln('')
  terminal.write('\x1b[32m$ \x1b[0m')
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (terminal) {
    terminal.dispose()
  }
})

const handleResize = () => {
  if (fitAddon) {
    fitAddon.fit()
  }
}

const clearTerminal = () => {
  if (terminal) {
    terminal.clear()
    terminal.write('\x1b[32m$ \x1b[0m')
  }
}

const copyToClipboard = () => {
  if (terminal) {
    const content = terminal.buffer.active.getLine(0).translateToString()
    navigator.clipboard.writeText(content)
      .then(() => {
        ElMessage.success('已复制到剪贴板')
      })
      .catch(() => {
        ElMessage.error('复制失败')
      })
  }
}
</script>

<style>
.terminal-view {
  height: 100%;
  padding: var(--spacing-base);
}

.terminal-container {
  height: 100%;
  background-color: var(--dark-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--dark-border);
}

.terminal-header {
  height: 48px;
  padding: 0 var(--spacing-base);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--dark-bg-light);
  border-bottom: 1px solid var(--dark-border);
}

.terminal-header__title {
  display: flex;
  align-items: center;
  gap: var(--spacing-small);
  color: var(--dark-text);
  font-size: var(--font-size-base);
  font-weight: 500;
}

.terminal-header__title .el-icon {
  font-size: 20px;
  color: var(--primary-color);
}

.terminal-header__actions {
  display: flex;
  gap: var(--spacing-small);
}

.terminal-content {
  flex: 1;
  padding: var(--spacing-base);
  background-color: var(--dark-bg);
  overflow: hidden;
}

.terminal-footer {
  height: 32px;
  padding: 0 var(--spacing-base);
  display: flex;
  align-items: center;
  background-color: var(--dark-bg-light);
  border-top: 1px solid var(--dark-border);
}

.terminal-status {
  display: flex;
  align-items: center;
  gap: var(--spacing-small);
}

.terminal-info {
  color: var(--dark-text-secondary);
  font-size: var(--font-size-small);
}

/* XTerm 终端样式覆盖 */
:deep(.xterm) {
  padding: 0;
}

:deep(.xterm-viewport) {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--dark-border) transparent;
}

:deep(.xterm-viewport::-webkit-scrollbar) {
  width: 8px;
}

:deep(.xterm-viewport::-webkit-scrollbar-track) {
  background: transparent;
}

:deep(.xterm-viewport::-webkit-scrollbar-thumb) {
  background-color: var(--dark-border);
  border-radius: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .terminal-view {
    padding: var(--spacing-small);
  }

  .terminal-header {
    padding: 0 var(--spacing-small);
  }

  .terminal-content {
    padding: var(--spacing-small);
  }

  .terminal-footer {
    padding: 0 var(--spacing-small);
  }
}
</style> 