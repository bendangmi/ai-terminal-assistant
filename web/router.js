import { createRouter, createWebHistory } from 'vue-router'
import Terminal from './components/Terminal.vue'
import SystemInfo from './components/SystemInfo.vue'
import Settings from './components/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Terminal',
    component: Terminal
  },
  {
    path: '/system',
    name: 'SystemInfo',
    component: SystemInfo
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 