import { defineStore } from 'pinia'
import { terminalAPI } from '@/config/api'

export const useTerminalStore = defineStore('terminal', {
  state: () => ({
    terminals: [],
    activeTerminalId: null,
    isConnected: false,
    commandHistory: [],
    historyIndex: -1,
    settings: {
      fontSize: 14,
      fontFamily: 'Consolas, monospace',
      cursorStyle: 'block', // block, underline, bar
      cursorBlink: true,
      theme: {
        background: '#1E1E1E',
        foreground: '#FFFFFF',
        cursor: '#FFFFFF',
        selection: '#264F78',
        black: '#000000',
        red: '#CD3131',
        green: '#0DBC79',
        yellow: '#E5E510',
        blue: '#2472C8',
        magenta: '#BC3FBC',
        cyan: '#11A8CD',
        white: '#E5E5E5',
        brightBlack: '#666666',
        brightRed: '#F14C4C',
        brightGreen: '#23D18B',
        brightYellow: '#F5F543',
        brightBlue: '#3B8EEA',
        brightMagenta: '#D670D6',
        brightCyan: '#29B8DB',
        brightWhite: '#E5E5E5'
      }
    }
  }),

  actions: {
    async createTerminal() {
      try {
        const response = await terminalAPI.create()
        const terminal = {
          id: response.id,
          title: `Terminal ${this.terminals.length + 1}`,
          buffer: '',
          rows: 24,
          cols: 80
        }
        this.terminals.push(terminal)
        this.activeTerminalId = terminal.id
        return terminal.id
      } catch (error) {
        console.error('创建终端失败:', error)
        throw error
      }
    },

    async closeTerminal(terminalId) {
      try {
        await terminalAPI.close(terminalId)
        const index = this.terminals.findIndex(t => t.id === terminalId)
        if (index !== -1) {
          this.terminals.splice(index, 1)
          if (this.activeTerminalId === terminalId) {
            this.activeTerminalId = this.terminals.length > 0 ? this.terminals[0].id : null
          }
        }
      } catch (error) {
        console.error('关闭终端失败:', error)
        throw error
      }
    },

    setActiveTerminal(terminalId) {
      if (this.terminals.some(t => t.id === terminalId)) {
        this.activeTerminalId = terminalId
      }
    },

    async sendCommand(command) {
      if (!this.activeTerminalId || !command) return

      try {
        await terminalAPI.sendCommand(this.activeTerminalId, command)
        this.addToHistory(command)
      } catch (error) {
        console.error('发送命令失败:', error)
        throw error
      }
    },

    updateTerminalBuffer(terminalId, data) {
      const terminal = this.terminals.find(t => t.id === terminalId)
      if (terminal) {
        terminal.buffer += data
      }
    },

    clearTerminalBuffer(terminalId) {
      const terminal = this.terminals.find(t => t.id === terminalId)
      if (terminal) {
        terminal.buffer = ''
      }
    },

    resizeTerminal(terminalId, rows, cols) {
      const terminal = this.terminals.find(t => t.id === terminalId)
      if (terminal) {
        terminal.rows = rows
        terminal.cols = cols
        terminalAPI.resize(terminalId, rows, cols)
      }
    },

    addToHistory(command) {
      this.commandHistory.push(command)
      this.historyIndex = this.commandHistory.length
    },

    getPreviousCommand() {
      if (this.historyIndex > 0) {
        this.historyIndex--
        return this.commandHistory[this.historyIndex]
      }
      return ''
    },

    getNextCommand() {
      if (this.historyIndex < this.commandHistory.length - 1) {
        this.historyIndex++
        return this.commandHistory[this.historyIndex]
      }
      return ''
    },

    updateSettings(newSettings) {
      this.settings = {
        ...this.settings,
        ...newSettings
      }
    },

    setConnectionStatus(status) {
      this.isConnected = status
    }
  },

  getters: {
    activeTerminal: (state) => state.terminals.find(t => t.id === state.activeTerminalId),
    terminalCount: (state) => state.terminals.length,
    hasTerminals: (state) => state.terminals.length > 0,
    currentSettings: (state) => state.settings
  }
}) 