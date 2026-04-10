<template>
  <div class="page-container">
    <!-- 页面容器 -->
    <div class="pages-wrapper">
      <!-- 页面组件 -->
      <component 
        v-for="(page, index) in pages" 
        :key="index"
        :is="page.component"
        :class="getPageClass(index)"
        :style="{ zIndex: getPageZIndex(index) }"
      />
      
      <!-- 子组件 -->
      <NavBar 
        :currentPage="currentPage" 
        :navItems="navItems"
        @nav-click="handleNavClick"
      />
      <PageIndicator 
        :currentPage="currentPage" 
        :totalPages="pages.length"
        @indicator-click="handleIndicatorClick"
      />
      <HomeButton @home-click="goToHome" />
      
      <!-- 使用新的可拖动圆形AI按钮组件 -->
      <AIFloatingButton />
      
      <!-- 页脚组件 - 只在最后一个页面显示 -->
      <Footer v-if="currentPage === pages.length - 1" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// 导入页面组件
import Page1 from './pages/Page1.vue'
import Page2 from './pages/Page2.vue'
import Page3 from './pages/Page3.vue'
import Page4 from './pages/Page4.vue'
import Page5 from './pages/Page5.vue'

// 导入子组件
import NavBar from './NavBar.vue'
import PageIndicator from './PageIndicator.vue'
import HomeButton from './HomeButton.vue'
// 导入新的AI浮动按钮组件，移除对AIImageGenerator的直接导入
import AIFloatingButton from './AIFloatingButton.vue'
// 导入页脚组件
import Footer from './Footer.vue'

// ★★★ 核心修改：注册 emits 事件，允许向 App.vue 发送信号 ★★★
const emit = defineEmits(['open-game'])

// 路由实例
const router = useRouter()
const route = useRoute()

// 响应式数据
const currentPage = ref(0)
const prevPage = ref(0)
const isScrolling = ref(false)
// 移除showAIImageGenerator变量，因为现在由AIFloatingButton组件管理
const hintVisible = ref(false)
let hintTimeout = null

// 页面路径映射 - 单独定义避免结构复杂化
const pagePaths = [
  '/page1',
  '/page2', 
  '/page3',
  '/page4',
  '/page5',
]

// 页面配置 - 修复：使用实际导入的组件对象而不是字符串
const pages = reactive([
  { component: Page1 },
  { component: Page2 },
  { component: Page3 },
  { component: Page4 },
  { component: Page5 },
])

// 导航项配置
const navItems = reactive([
  { id: 0, name: '首页', target: 'page1' },
  { id: 1, name: '皮影溯源', target: 'page2' },
  { id: 2, name: '影韵万方', target: 'page3' },
  { id: 3, name: '影魂千年', target: 'page4' },
  { id: 4, name: '匠心工艺', target: 'page5' }
])

// 获取页面类名 - 简化类名逻辑
const getPageClass = (index) => {
  if (index === currentPage.value) {
    return `page active`
  }
  if (index < currentPage.value) return 'page prev'
  return 'page next'
}

// 获取页面z-index - 优化层级管理，确保新页面在上方
const getPageZIndex = (index) => {
  // 当前页层级最高
  if (index === currentPage.value) return 10
  // 下一页层级次之，确保从下方进入时在当前页上方
  if (index === currentPage.value + 1) return 9
  // 上一页层级再次之，确保从上方退出时在当前页下方
  if (index === currentPage.value - 1) return 8
  // 其他页面层级最低
  return 1
}

// 安全的路由更新函数
const updateRoute = (index) => {
  try {
    if (index >= 0 && index < pagePaths.length) {
      // 避免路由重复推送导致的错误
      const currentPath = router.currentRoute.value.path
      if (currentPath !== pagePaths[index]) {
        router.push(pagePaths[index])
      }
    }
  } catch (error) {
    console.warn('路由更新失败:', error)
  }
}

// 导航点击处理
const handleNavClick = (index) => {
  if (!isScrolling.value) {
    prevPage.value = currentPage.value
    currentPage.value = index
    showHint()
    setScrollLock()
    updateRoute(index)
  }
}

// 指示器点击处理
const handleIndicatorClick = (index) => {
  if (!isScrolling.value) {
    prevPage.value = currentPage.value
    currentPage.value = index
    showHint()
    setScrollLock()
    updateRoute(index)
  }
}

// 返回首页
const goToHome = () => {
  if (!isScrolling.value) {
    prevPage.value = currentPage.value
    currentPage.value = 0
    showHint()
    setScrollLock()
    updateRoute(0)
  }
}

// 显示提示
const showHint = () => {
  hintVisible.value = true
  clearTimeout(hintTimeout)
  hintTimeout = setTimeout(() => {
    hintVisible.value = false
  }, 2000)
}

// 设置滚动锁定
const setScrollLock = () => {
  isScrolling.value = true
  setTimeout(() => {
    isScrolling.value = false
  }, 600) // 与过渡时间匹配
}

// 鼠标滚轮事件处理
const handleWheel = (e) => {
  if (isScrolling.value) return
  
  // 检查是否在可滚动元素上滚动
  const target = e.target
  if (target.scrollHeight > target.clientHeight && target !== document.body) {
    // 如果目标元素有滚动条，则不阻止默认行为
    return
  }
  
  // 不在最后一个页面时，阻止默认滚动行为并触发页面切换
  if (currentPage.value < pages.length - 1) {
    e.preventDefault()
    showHint()
    
    if (e.deltaY > 0) {
      // 向下滚动，下一页
      if (currentPage.value < pages.length - 1) {
        prevPage.value = currentPage.value
        currentPage.value++
        setScrollLock()
        updateRoute(currentPage.value)
      }
    } else {
      // 向上滚动，上一页
      if (currentPage.value > 0) {
        prevPage.value = currentPage.value
        currentPage.value--
        setScrollLock()
        updateRoute(currentPage.value)
      }
    }
  } else {
    // 在最后一个页面时，检查页面是否已经滚动到顶部
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop
    
    // 如果页面已经滚动到顶部，且向上滚动，则触发页面切换
    if (scrollTop === 0 && e.deltaY < 0) {
      if (currentPage.value > 0) {
        e.preventDefault()
        showHint()
        prevPage.value = currentPage.value
        currentPage.value--
        setScrollLock()
        updateRoute(currentPage.value)
      }
    }
    // 否则允许默认滚动行为（滚动到页脚或从页脚滚动回页面）
  }
}

// 键盘事件处理
const handleKeydown = (e) => {
  if (e.key === 'ArrowDown' || e.key === 'PageDown') {
    if (currentPage.value < pages.length - 1) {
      prevPage.value = currentPage.value
      currentPage.value++
      showHint()
      setScrollLock()
      updateRoute(currentPage.value)
    }
  } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
    if (currentPage.value > 0) {
      prevPage.value = currentPage.value
      currentPage.value--
      showHint()
      setScrollLock()
      updateRoute(currentPage.value)
    }
  } else if (e.key === 'Home') {
    prevPage.value = currentPage.value
    currentPage.value = 0
    showHint()
    setScrollLock()
    updateRoute(0)
  } else if (e.key === 'End') {
    prevPage.value = currentPage.value
    currentPage.value = pages.length - 1
    showHint()
    setScrollLock()
    updateRoute(currentPage.value)
  }
}

// 触摸事件处理
let touchStartY = 0
let touchStartTime = 0

const handleTouchStart = (e) => {
  touchStartY = e.touches[0].clientY
  touchStartTime = Date.now()
}

const handleTouchEnd = (e) => {
  if (isScrolling.value) return
  
  const touchEndY = e.changedTouches[0].clientY
  const diff = touchStartY - touchEndY
  const touchDuration = Date.now() - touchStartTime
  
  // 只有当滑动距离足够且时间较短时才触发页面切换
  if (Math.abs(diff) > 50 && touchDuration < 500) {
    // 检查是否在可滚动元素上滑动
    const target = e.target
    if (target.scrollHeight > target.clientHeight && target !== document.body) {
      // 如果目标元素有滚动条，则不触发页面切换
      return
    }
    
    // 不在最后一个页面时，触发页面切换
    if (currentPage.value < pages.length - 1) {
      if (diff > 0) {
        // 向下滑动，下一页
        if (currentPage.value < pages.length - 1) {
          prevPage.value = currentPage.value
          currentPage.value++
          showHint()
          setScrollLock()
          updateRoute(currentPage.value)
        }
      } else {
        // 向上滑动，上一页
        if (currentPage.value > 0) {
          prevPage.value = currentPage.value
          currentPage.value--
          showHint()
          setScrollLock()
          updateRoute(currentPage.value)
        }
      }
    } else {
      // 当在最后一个页面时，检查页面是否已经滚动到顶部
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop
      
      // 如果页面已经滚动到顶部，且向上滑动，则触发页面切换
      if (scrollTop === 0 && diff < 0) {
        if (currentPage.value > 0) {
          showHint()
          prevPage.value = currentPage.value
          currentPage.value--
          setScrollLock()
          updateRoute(currentPage.value)
        }
      }
    }
  }
}

// 初始化路由同步
const syncRouteWithPage = () => {
  try {
    const currentPath = router.currentRoute.value.path
    // 找到对应路径的页面索引
    const pageIndex = pagePaths.findIndex(path => path === currentPath)
    if (pageIndex !== -1 && pageIndex !== currentPage.value) {
      prevPage.value = currentPage.value
      currentPage.value = pageIndex
      setScrollLock()
    }
  } catch (error) {
    console.warn('路由同步失败:', error)
  }
}

// 生命周期钩子
onMounted(() => {
  document.addEventListener('wheel', handleWheel, { passive: false })
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('touchstart', handleTouchStart, { passive: true })
  document.addEventListener('touchend', handleTouchEnd, { passive: true })
  
  // 初始化时同步路由和页面
  syncRouteWithPage()
  
  // 添加路由变化监听
  router.afterEach(() => {
    syncRouteWithPage()
  })
})

onUnmounted(() => {
  document.removeEventListener('wheel', handleWheel)
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('touchstart', handleTouchStart)
  document.removeEventListener('touchend', handleTouchEnd)
  clearTimeout(hintTimeout)
})
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  overflow: hidden;
  position: relative;
  /* 隐藏滚动条但保留滚动功能 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

/* 隐藏 WebKit 浏览器的滚动条 */
.page-container::-webkit-scrollbar {
  display: none;
}

.pages-wrapper {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  /* 隐藏滚动条但保留滚动功能 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

/* 隐藏 WebKit 浏览器的滚动条 */
.pages-wrapper::-webkit-scrollbar {
  display: none;
}

.page {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  /* 只保留transform过渡，移除opacity过渡，避免消失动画 */
  transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: transform;
  backface-visibility: hidden;
}

/* 当前活动页面 - 居中显示 */
.page.active {
  transform: translateY(0);
  opacity: 1; /* 始终保持可见 */
  position: relative;
  z-index: 10;
}

/* 上一页 - 完全移出屏幕上方，没有淡出效果 */
.page.prev {
  transform: translateY(-100%);
  opacity: 1; /* 始终保持不透明，避免淡出 */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 9;
}

/* 下一页 - 完全移出屏幕下方，没有淡出效果 */
.page.next {
  transform: translateY(100%);
  opacity: 1; /* 始终保持不透明，避免淡出 */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 9;
}

/* 添加AI功能按钮样式 */
.ai-feature-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #9c27b0;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 100;
  transition: all 0.3s;
}

.ai-feature-btn:hover {
  background-color: #7b1fa2;
  transform: scale(1.05);
}

.ai-generator-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 20px;
}

.close-ai-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-ai-btn:hover {
  background: #d32f2f;
}

/* ★★★ 新增：手势游戏入口按钮样式 ★★★ */
.gesture-game-btn {
  position: fixed;
  bottom: 30px;
  left: 30px; /* 放在左下角，避开右下角的AI按钮 */
  z-index: 100;
  
  display: flex;
  align-items: center;
  gap: 8px;
  
  padding: 12px 24px;
  background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
  color: #1a4d2e;
  border: none;
  border-radius: 50px;
  
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(150, 230, 161, 0.4);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.gesture-game-btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(150, 230, 161, 0.6);
}

.gesture-game-btn .icon {
  font-size: 20px;
}

/* 呼吸灯动画效果 */
.ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  border-radius: 50px;
  border: 2px solid white;
  transform: translate(-50%, -50%) scale(1);
  opacity: 0;
  animation: ripple-anim 2s infinite;
}

@keyframes ripple-anim {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
  100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .gesture-game-btn {
    bottom: 20px;
    left: 20px;
    padding: 10px 16px;
    font-size: 14px;
  }
  .gesture-game-btn .text {
    display: none; /* 手机上只显示图标，节省空间 */
  }
}
</style>