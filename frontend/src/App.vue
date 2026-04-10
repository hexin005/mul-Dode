<template>
  <div id="app">
    <template v-if="$route.path.startsWith('/school') || 
                   ['/login', '/register', '/user-center'].includes($route.path)">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
      
      <!-- 页脚组件 -->
      <Footer />
    </template>

    <template v-else>
      <PageContainer />
    </template>
  </div>
</template>


<script>
import PageContainer from './components/PageContainer.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    PageContainer,
    Footer
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Microsoft YaHei", sans-serif;
  height: 100vh;
  overflow-x: hidden;
  /* 隐藏滚动条但保留滚动功能 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

/* 隐藏 WebKit 浏览器的滚动条 */
body::-webkit-scrollbar {
  display: none;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

#app > *:not(:last-child) {
  flex: 1;
}

/* 为直接使用 router-view 的页面添加页脚样式 */
#app > template:first-child {
  display: flex;
  flex-direction: column;
}

#app > template:first-child > router-view {
  flex: 1;
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .nav-list {
    flex-direction: column;
    align-items: center;
  }
  
  .nav-item {
    margin: 5px 0;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-desc {
    font-size: 1rem;
    padding: 0 20px;
  }
}
</style>