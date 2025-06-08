<!-- 终端组件 -->
<template>
  <div class="terminal-container">
    <!-- 终端输出区域 -->
    <div class="terminal-output" ref="outputRef">
      <div v-for="(item, index) in output" :key="index" class="output-item">
        <div :class="['output-content', item.type]" v-html="item.content"></div>
        <div class="output-time">{{ formatTime(item.timestamp) }}</div>
      </div>
    </div>

    <!-- 命令输入区域 -->
    <div class="terminal-input">
      <el-input
        v-model="command"
        placeholder="输入命令或自然语言描述..."
        @keyup.enter="executeCommand"
        :disabled="executing"
      >
        <template #prefix>
          <span class="prompt">$</span>
        </template>
        <template #append>
          <el-button
            type="primary"
            @click="executeCommand"
            :loading="executing"
          >
            执行
          </el-button>
        </template>
      </el-input>
    </div>

    <!-- 确认对话框 -->
    <el-dialog
      v-model="showConfirmDialog"
      title="危险命令确认"
      width="50%"
    >
      <div class="confirm-content">
        <p>检测到以下潜在危险：</p>
        <ul>
          <li v-for="(warning, index) in warnings" :key="index">
            {{ warning }}
          </li>
        </ul>
        <p>是否确认执行？</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showConfirmDialog = false">取消</el-button>
          <el-button type="danger" @click="confirmExecution">
            确认执行
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'Terminal',
  setup() {
    const command = ref('')
    const output = ref([])
    const executing = ref(false)
    const outputRef = ref(null)
    const showConfirmDialog = ref(false)
    const warnings = ref([])
    const pendingCommand = ref(null)

    // 格式化时间
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString()
    }

    // 滚动到底部
    const scrollToBottom = async () => {
      await nextTick()
      if (outputRef.value) {
        outputRef.value.scrollTop = outputRef.value.scrollHeight
      }
    }

    // 执行命令
    const executeCommand = async (force = false) => {
      if (!command.value.trim() || executing.value) return

      const cmd = command.value.trim()
      executing.value = true

      try {
        const response = await fetch('/api/execute', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            command: cmd,
            force: force
          })
        })

        const data = await response.json()

        if (data.error === '危险命令' && !force) {
          warnings.value = data.warnings
          pendingCommand.value = cmd
          showConfirmDialog.value = true
          executing.value = false
          return
        }

        // 添加命令到输出
        output.value.push({
          type: 'command',
          content: `<span class="prompt">$</span> ${cmd}`,
          timestamp: new Date().toISOString()
        })

        // 添加执行结果到输出
        if (Array.isArray(data.output)) {
          output.value.push(...data.output)
        }

        if (data.error) {
          ElMessage.error(data.error)
        }

        command.value = ''
        await scrollToBottom()
      } catch (error) {
        ElMessage.error('执行命令出错: ' + error.message)
        output.value.push({
          type: 'error',
          content: `执行出错: ${error.message}`,
          timestamp: new Date().toISOString()
        })
      } finally {
        executing.value = false
      }
    }

    // 确认执行危险命令
    const confirmExecution = () => {
      showConfirmDialog.value = false
      if (pendingCommand.value) {
        executeCommand(true)
        pendingCommand.value = null
      }
    }

    onMounted(() => {
      // 添加欢迎信息
      output.value.push({
        type: 'info',
        content: '欢迎使用 AI Terminal Assistant！输入命令或使用自然语言描述你想执行的操作。',
        timestamp: new Date().toISOString()
      })
    })

    return {
      command,
      output,
      executing,
      outputRef,
      showConfirmDialog,
      warnings,
      formatTime,
      executeCommand,
      confirmExecution
    }
  }
}
</script>

<style scoped>
.terminal-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 8px;
}

.terminal-output {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 20px;
  font-family: 'Courier New', Courier, monospace;
  color: #fff;
}

.output-item {
  margin-bottom: 10px;
}

.output-content {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.output-time {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

.output-content.error {
  color: #ff4949;
}

.output-content.info {
  color: #409eff;
}

.output-content.command {
  color: #67c23a;
}

.terminal-input {
  margin-top: auto;
}

.prompt {
  color: #67c23a;
  margin-right: 8px;
}

:deep(.el-input-group__prepend),
:deep(.el-input-group__append) {
  background-color: #2c2c2c;
  border-color: #4c4c4c;
}

:deep(.el-input__wrapper) {
  background-color: #2c2c2c;
}

:deep(.el-input__inner) {
  color: #fff;
}

:deep(.el-input__inner::placeholder) {
  color: #666;
}

.confirm-content {
  color: #666;
}

.confirm-content ul {
  margin: 10px 0;
  padding-left: 20px;
}

.confirm-content li {
  color: #ff4949;
  margin: 5px 0;
}
</style> 