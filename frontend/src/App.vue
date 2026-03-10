<template>
  <div id="app">
    <template v-if="$route.path.startsWith('/school') || 
                   ['/login', '/register', '/user-center'].includes($route.path)">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </template>

    <template v-else>
      <PageContainer />
    </template>
  </div>
</template>


<script>
import PageContainer from './components/PageContainer.vue'

export default {
  name: 'App',
  components: {
    PageContainer
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
}

#app {
  height: 100vh;
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