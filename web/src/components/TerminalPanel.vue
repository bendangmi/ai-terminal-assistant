<!-- TerminalPanel.vue -->
<template>
  <div class="terminal-panel">
    <!-- 终端显示区域 -->
    <div class="terminal-display">
      <div class="terminal-header">
        <div class="terminal-header__title">
          <el-icon><Monitor /></el-icon>
          <span>智能终端</span>
        </div>
        <div class="terminal-header__actions">
          <el-tooltip content="清空终端" placement="top">
            <el-button type="primary" text @click="clearTerminal">
              <el-icon><Delete /></el-icon>
            </el-button>
          </el-tooltip>
          <el-tooltip content="复制内容" placement="top">
            <el-button type="primary" text @click="copyToClipboard">
              <el-icon><DocumentCopy /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
      </div>
      <div ref="terminalRef" class="terminal-content"></div>
    </div>

    <!-- 命令输入区域 -->
    <div class="command-input">
      <div class="input-mode-switch">
        <el-radio-group v-model="inputMode" size="small">
          <el-radio-button value="command">命令模式</el-radio-button>
          <el-radio-button value="natural">自然语言</el-radio-button>
        </el-radio-group>
      </div>

      <div class="input-area">
        <el-input
          v-model="commandInput"
          :placeholder="inputMode === 'command' ? '输入命令...' : '使用自然语言描述你想执行的操作...'"
          type="textarea"
          :rows="2"
          :autosize="{ minRows: 2, maxRows: 4 }"
          @keydown.enter.exact.prevent="executeCommand"
          @keydown.ctrl.enter="executeCommand"
        >
          <template #prefix>
            <span class="input-prefix">{{ inputMode === 'command' ? '$' : 'AI' }}</span>
          </template>
        </el-input>
        
        <el-button 
          type="primary" 
          @click="executeCommand"
        >
          <el-icon>
            <component :is="inputMode === 'command' ? 'Terminal' : 'ChatLineRound'" />
          </el-icon>
          {{ inputMode === 'command' ? '执行' : '发送' }}
        </el-button>
      </div>
    </div>

    <!-- 执行结果区域 -->
    <div class="execution-results">
      <div class="results-header">
        <span class="results-title">执行结果</span>
        <el-button-group>
          <el-button text size="small" @click="clearResults">
            <el-icon><Delete /></el-icon>
            清空
          </el-button>
          <el-button text size="small" @click="copyResults">
            <el-icon><DocumentCopy /></el-icon>
            复制
          </el-button>
        </el-button-group>
      </div>
      <div class="results-content" ref="resultsRef">
        <div 
          v-for="(result, index) in executionResults" 
          :key="index"
          :class="['result-item', result.type]"
        >
          <div class="result-timestamp">{{ result.timestamp }}</div>
          <div class="result-content">
            <pre><code>{{ result.content }}</code></pre>
          </div>
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
import { ElMessage } from 'element-plus'
import 'xterm/css/xterm.css'

// 终端相关
const terminalRef = ref(null)
let terminal = null
let fitAddon = null

// 输入模式
const inputMode = ref('command')
const commandInput = ref('')

// 执行结果
const resultsRef = ref(null)
const executionResults = ref([])

// 初始化终端
onMounted(() => {
  initTerminal()
})

onUnmounted(() => {
  if (terminal) {
    terminal.dispose()
  }
})

const initTerminal = () => {
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
  terminal.writeln('\x1b[90m可以使用命令模式或自然语言模式进行操作。\x1b[0m')
  terminal.writeln('')
  terminal.write('\x1b[32m$ \x1b[0m')
}

const handleResize = () => {
  if (fitAddon) {
    fitAddon.fit()
  }
}

// 终端操作
const clearTerminal = () => {
  if (terminal) {
    terminal.clear()
    terminal.write('\x1b[32m$ \x1b[0m')
  }
}

const copyToClipboard = () => {
  if (terminal) {
    const content = terminal.buffer.active.getLine(0).translateToString()
    copyText(content)
  }
}

// 命令执行
const executeCommand = async () => {
  if (!commandInput.value.trim()) return

  const command = commandInput.value
  const timestamp = new Date().toLocaleTimeString()

  // 添加到执行结果
  executionResults.value.push({
    type: 'command',
    timestamp,
    content: `${inputMode.value === 'command' ? '$' : 'AI'} ${command}`
  })

  try {
    // TODO: 实际的命令执行逻辑
    const result = await mockExecuteCommand(command)
    
    executionResults.value.push({
      type: 'output',
      timestamp,
      content: result
    })
  } catch (error) {
    executionResults.value.push({
      type: 'error',
      timestamp,
      content: error.message
    })
  }

  // 清空输入
  commandInput.value = ''
  
  // 滚动到底部
  scrollToBottom()
}

// 模拟命令执行
const mockExecuteCommand = async (command) => {
  await new Promise(resolve => setTimeout(resolve, 500))
  if (inputMode.value === 'command') {
    return `Executed command: ${command}`
  } else {
    return `AI 助手正在处理: ${command}\n分析结果将在这里显示...`
  }
}

// 结果操作
const clearResults = () => {
  executionResults.value = []
}

const copyResults = () => {
  const text = executionResults.value
    .map(result => `[${result.timestamp}] ${result.content}`)
    .join('\n')
  copyText(text)
}

// 工具函数
const copyText = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('已复制到剪贴板')
  } catch (err) {
    ElMessage.error('复制失败')
  }
}

const scrollToBottom = () => {
  if (resultsRef.value) {
    resultsRef.value.scrollTop = resultsRef.value.scrollHeight
  }
}
</script>

<style>
.terminal-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  background: var(--bg-color-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-base);
  overflow: hidden;
  position: relative;
}

.terminal-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--primary-gradient);
  opacity: 0.8;
}

/* 终端显示区域 */
.terminal-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--dark-bg-primary);
  overflow: hidden;
  border: 1px solid var(--border-color-base);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-medium);
}

.terminal-header {
  height: 44px;
  padding: 0 var(--spacing-4);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--dark-bg-secondary);
  border-bottom: 1px solid var(--border-color-base);
}

.terminal-header__title {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  color: var(--text-color-inverse);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
}

.terminal-header__title .el-icon {
  color: var(--primary-color);
  font-size: var(--font-size-lg);
  filter: drop-shadow(0 0 8px var(--primary-color));
}

.terminal-header__actions {
  display: flex;
  gap: var(--spacing-2);
}

.terminal-header__actions .el-button {
  border: 1px solid transparent;
  transition: var(--transition-all);
  color: var(--text-color-inverse);
}

.terminal-header__actions .el-button:hover {
  background: var(--dark-bg-tertiary);
  border-color: var(--border-color-base);
  transform: translateY(-2px);
}

.terminal-content {
  flex: 1;
  padding: var(--spacing-4);
  background: var(--dark-bg-primary);
  font-family: var(--font-family-code);
}

/* 命令输入区域 */
.command-input {
  padding: var(--spacing-4);
  background: var(--bg-color-secondary);
  border-top: 1px solid var(--border-color-base);
}

.input-mode-switch {
  margin-bottom: var(--spacing-4);
  display: flex;
  justify-content: center;
}

.input-mode-switch :deep(.el-radio-group) {
  background: var(--bg-color-float);
  padding: var(--spacing-1);
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color-base);
}

.input-mode-switch :deep(.el-radio-button__inner) {
  background: transparent;
  border: none;
  padding: var(--spacing-2) var(--spacing-4);
  color: var(--text-color-regular);
  transition: var(--transition-all);
}

.input-mode-switch :deep(.el-radio-button__orig-radio:checked + .el-radio-button__inner) {
  background: var(--primary-gradient);
  color: var(--text-color-inverse);
  box-shadow: var(--shadow-glow);
}

.input-area {
  display: flex;
  gap: var(--spacing-3);
}

.input-area :deep(.el-textarea__inner) {
  background: var(--bg-color-float);
  border: 1px solid var(--border-color-base);
  border-radius: var(--radius-lg);
  padding: var(--spacing-3);
  color: var(--text-color-primary);
  font-family: var(--font-family-code);
  resize: none;
  transition: var(--transition-all);
}

.input-area :deep(.el-textarea__inner:focus) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.2);
}

.input-prefix {
  color: var(--primary-color);
  font-weight: var(--font-weight-semibold);
  padding: 0 var(--spacing-2);
  text-shadow: 0 0 10px var(--primary-color);
}

.input-area .el-button {
  height: auto;
  align-self: stretch;
  padding: 0 var(--spacing-4);
  border-radius: var(--radius-lg);
  background: var(--primary-gradient);
  border: none;
  font-weight: var(--font-weight-semibold);
  transition: var(--transition-all);
}

.input-area .el-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.input-area .el-button .el-icon {
  margin-right: var(--spacing-2);
  font-size: var(--font-size-md);
}

/* 执行结果区域 */
.execution-results {
  height: 200px;
  display: flex;
  flex-direction: column;
  background: var(--bg-color-float);
  border: 1px solid var(--border-color-base);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-base);
}

.results-header {
  padding: var(--spacing-3) var(--spacing-4);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-color-secondary);
  border-bottom: 1px solid var(--border-color-base);
}

.results-title {
  font-weight: var(--font-weight-semibold);
  color: var(--text-color-primary);
}

.results-content {
  flex: 1;
  padding: var(--spacing-4);
  overflow-y: auto;
  background: var(--bg-color-float);
}

.result-item {
  margin-bottom: var(--spacing-3);
  padding: var(--spacing-3);
  border-radius: var(--radius-lg);
  background: var(--bg-color-secondary);
  border: 1px solid var(--border-color-light);
  transition: var(--transition-all);
}

.result-item:hover {
  transform: translateX(4px);
  border-color: var(--primary-color);
  background: var(--bg-color-tertiary);
}

.result-item.command {
  border-left: 2px solid var(--primary-color);
}

.result-item.output {
  border-left: 2px solid var(--success-color);
}

.result-item.error {
  border-left: 2px solid var(--danger-color);
}

.result-timestamp {
  font-size: var(--font-size-sm);
  color: var(--text-color-secondary);
  margin-bottom: var(--spacing-2);
}

.result-content {
  font-family: var(--font-family-code);
  white-space: pre-wrap;
  word-break: break-all;
  color: var(--text-color-primary);
}

.result-content pre {
  margin: 0;
  padding: var(--spacing-3);
  background: var(--bg-color-tertiary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color-light);
}

/* 暗色主题适配 */
[data-theme="dark"] .terminal-panel {
  background: var(--dark-bg-primary);
}

[data-theme="dark"] .command-input {
  background: var(--dark-bg-secondary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] .input-mode-switch :deep(.el-radio-group) {
  background: var(--dark-bg-tertiary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] .input-area :deep(.el-textarea__inner) {
  background: var(--dark-bg-tertiary);
  border-color: var(--border-color-base);
  color: var(--text-color-inverse);
}

[data-theme="dark"] .execution-results {
  background: var(--dark-bg-secondary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] .results-header {
  background: var(--dark-bg-tertiary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] .results-content {
  background: var(--dark-bg-secondary);
}

[data-theme="dark"] .result-item {
  background: var(--dark-bg-tertiary);
  border-color: var(--border-color-base);
}

[data-theme="dark"] .result-item:hover {
  background: var(--dark-bg-quaternary);
}

[data-theme="dark"] .result-content pre {
  background: var(--dark-bg-quaternary);
  border-color: var(--border-color-base);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .terminal-panel {
    gap: var(--spacing-3);
  }

  .terminal-header {
    height: 40px;
    padding: 0 var(--spacing-3);
  }

  .command-input {
    padding: var(--spacing-3);
  }

  .input-mode-switch {
    margin-bottom: var(--spacing-3);
  }

  .execution-results {
    height: 150px;
  }

  .results-header {
    padding: var(--spacing-2) var(--spacing-3);
  }

  .results-content {
    padding: var(--spacing-3);
  }

  .result-item {
    padding: var(--spacing-2);
    margin-bottom: var(--spacing-2);
  }
}
</style> 