// 防抖指令
const debounce = {
  mounted(el, binding) {
    if (typeof binding.value !== 'function') {
      console.error('v-debounce value must be a function')
      return
    }
    let timer = null
    el.handler = () => {
      if (timer) {
        clearTimeout(timer)
      }
      timer = setTimeout(() => {
        binding.value()
      }, binding.arg || 300)
    }
    el.addEventListener('click', el.handler)
  },
  unmounted(el) {
    el.removeEventListener('click', el.handler)
  }
}

// 长按指令
const longpress = {
  mounted(el, binding) {
    if (typeof binding.value !== 'function') {
      console.error('v-longpress value must be a function')
      return
    }
    let pressTimer = null
    const start = (e) => {
      if (e.button) {
        if (e.type === 'click' && e.button !== 0) {
          return
        }
      }
      if (pressTimer === null) {
        pressTimer = setTimeout(() => {
          binding.value(e)
        }, binding.arg || 1000)
      }
    }
    const cancel = () => {
      if (pressTimer !== null) {
        clearTimeout(pressTimer)
        pressTimer = null
      }
    }
    el.addEventListener('mousedown', start)
    el.addEventListener('touchstart', start)
    el.addEventListener('click', cancel)
    el.addEventListener('mouseout', cancel)
    el.addEventListener('touchend', cancel)
    el.addEventListener('touchcancel', cancel)
  }
}

// 复制指令
const copy = {
  mounted(el, binding) {
    el.copyData = binding.value
    el.addEventListener('click', () => {
      const textarea = document.createElement('textarea')
      textarea.value = el.copyData.toString()
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('Copy')
      document.body.removeChild(textarea)
      ElMessage.success('复制成功')
    })
  },
  updated(el, binding) {
    el.copyData = binding.value
  }
}

// 权限指令
const permission = {
  mounted(el, binding) {
    const { value } = binding
    const roles = useUserStore().roles
    if (value && value instanceof Array && value.length > 0) {
      const permissionRoles = value
      const hasPermission = roles.some(role => permissionRoles.includes(role))
      if (!hasPermission) {
        el.parentNode && el.parentNode.removeChild(el)
      }
    } else {
      throw new Error('need roles! Like v-permission="[\'admin\',\'editor\']"')
    }
  }
}

// 拖拽指令
const drag = {
  mounted(el, binding) {
    el.style.cursor = 'move'
    el.style.position = 'absolute'
    el.onmousedown = (e) => {
      const disX = e.clientX - el.offsetLeft
      const disY = e.clientY - el.offsetTop
      document.onmousemove = (e) => {
        let left = e.clientX - disX
        let top = e.clientY - disY
        // 防止拖出边界
        const maxLeft = document.body.clientWidth - el.offsetWidth
        const maxTop = document.body.clientHeight - el.offsetHeight
        if (left < 0) left = 0
        if (top < 0) top = 0
        if (left > maxLeft) left = maxLeft
        if (top > maxTop) top = maxTop
        el.style.left = left + 'px'
        el.style.top = top + 'px'
      }
      document.onmouseup = () => {
        document.onmousemove = document.onmouseup = null
      }
      return false
    }
  }
}

// 水波纹指令
const ripple = {
  mounted(el, binding) {
    el.style.position = 'relative'
    el.style.overflow = 'hidden'
    el.addEventListener('click', (e) => {
      const ripple = document.createElement('span')
      ripple.className = 'ripple'
      ripple.style.position = 'absolute'
      ripple.style.left = `${e.offsetX}px`
      ripple.style.top = `${e.offsetY}px`
      ripple.style.transform = 'translate(-50%, -50%)'
      ripple.style.width = '0'
      ripple.style.height = '0'
      ripple.style.borderRadius = '50%'
      ripple.style.backgroundColor = 'rgba(255, 255, 255, 0.35)'
      ripple.style.transition = 'all 0.4s ease-out'
      el.appendChild(ripple)
      setTimeout(() => {
        ripple.style.width = '200px'
        ripple.style.height = '200px'
        ripple.style.opacity = '0'
      }, 0)
      setTimeout(() => {
        ripple.remove()
      }, 400)
    })
  }
}

// 图片懒加载指令
const lazyLoad = {
  mounted(el, binding) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          el.src = binding.value
          observer.unobserve(el)
        }
      })
    })
    observer.observe(el)
  }
}

// 无限滚动指令
const infiniteScroll = {
  mounted(el, binding) {
    const load = binding.value
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        load()
      }
    })
    const target = el.querySelector('.infinite-scroll-bottom')
    if (target) {
      observer.observe(target)
    }
  }
}

export default {
  debounce,
  longpress,
  copy,
  permission,
  drag,
  ripple,
  lazyLoad,
  infiniteScroll
} 