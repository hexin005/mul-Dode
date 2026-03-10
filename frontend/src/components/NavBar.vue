<template>
  <div v-if="currentPage === 0" class="nav-container">
    <div class="top-bar">
        <div class="top-left">
          <img src="../asset/img/logo.png" class="logo" alt="皮影数字化传承" />
          <span class="website-name">光影千年·皮影数字化传承</span>
        </div>
        <div class="top-right">
          <!-- 日期信息 -->
          <div class="date-info">{{ formattedDate }}</div>
          <div class="user-avatar" @click="handleLogin" role="button" tabindex="0" @keydown.enter="handleLogin" @keydown.space="handleLogin">
            <div class="avatar-icon">
              
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M12 12C14.7614 12 17 9.76142 17 7C17 4.23858 14.7614 2 12 2C9.23858 2 7 4.23858 7 7C7 9.76142 9.23858 12 12 12Z"
                    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  <path d="M20 21C20 17.134 16.4183 14 12 14C7.58172 14 4 17.134 4 21" stroke="currentColor" 
                    stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              
            </div>
          </div>
        </div>
      </div>
      <div class="nav-bar">
        <ul class="nav-list">
      <li 
        v-for="item in navItems" 
        :key="item.id"
        class="nav-item"
        :class="{ active: item.id === currentPage }"
        @click="$emit('nav-click', item.id)"
      >
        {{ item.name }}
      </li>
    </ul>
      </div>
    
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
// 在 script setup 中引入路由
import { useRouter } from 'vue-router';




// 定义props
const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  navItems: {
    type: Array,
    required: true
  }
});

// 定义emits
const emit = defineEmits(['nav-click']);

// 计算属性 - 格式化日期
const formattedDate = computed(() => {
  const now = new Date();
  return now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });
});

// 处理登录点击事件
const router = useRouter();

const handleLogin = () => {
  // 跳转到登录页面
  // alert('点击成功！'); // 看看有没有弹窗
  router.push('/login');
};
</script>

<style scoped>
/* 导入中文字体 */
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;600;700&display=swap');

/* 全局样式重置 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 导航栏容器 - 修改为使用背景图片 */
.nav-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  background-image: url('../asset/img/opacity-b25.png');
  background-repeat: repeat;
  padding: 0;
  z-index: 1000;
  transition: all 0.3s ease;
}

/* 顶部栏样式 - 移除半透明背景，使用容器的背景图片 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 50px;
  background: none;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

/* 左侧logo和网站名称 */
.top-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

/* Logo样式  */
.logo {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05) rotate(2deg);
}

/* 网站名称样式  */
.website-name {
  font-family: 'Ma Shan Zheng', cursive, 'Noto Serif SC', serif;
  font-size: 24px;
  color: #fff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  letter-spacing: 2px;
  font-weight: bold;
}

/* 右侧信息区域 */
.top-right {
  display: flex;
  align-items: center;
  gap: 30px;
}

/* 日期信息样式 - 移除背景色和阴影 */
.date-info {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

/* 用户头像样式 - 半透明效果 */
.user-avatar {
  cursor: pointer;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: red;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  position: relative;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

.user-avatar:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.3);
}

.user-avatar:active {
  transform: scale(0.95);
}

/* 头像图标样式 - 白色图标增强可见性 */
.avatar-icon {
  color: #fff;
  width: 24px;
  height: 24px;
  filter: drop-shadow(1px 1px 2px rgba(0, 0, 0, 0.5));
}

/* 导航栏主体 - 移除半透明背景，使用容器的背景图片 */
.nav-bar {
  padding: 10px 0;
  background: none;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

/* 导航列表 */
.nav-list {
  display: flex;
  justify-content: center;
  list-style: none;
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
  gap: 10px;
}

/* 导航项样式 - 白色文字增强可读性 */
.nav-item {
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  color: #fff;
  font-weight: 600;
  border-radius: 50px;
  overflow: hidden;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
}

/* 导航项悬停效果 - 半透明背景 */
.nav-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* 导航项激活状态 - 只有下划线，移除背景色 */
.nav-item.active {
  font-weight: bold;
  position: relative;
  background: none;
}

/* 激活状态下的装饰线 - 增强下划线效果 */
.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: #fff;
  border-radius: 2px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    width: 0;
    left: 50%;
  }
  to {
    width: 100%;
    left: 0;
  }
}

/* 导航项点击反馈 */
.nav-item:active {
  transform: translateY(0);
  background: rgba(255, 255, 255, 0.4);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .top-bar {
    padding: 15px 30px;
  }
  
  .website-name {
    font-size: 20px;
  }
  
  .nav-item {
    font-size: 16px;
    padding: 10px 20px;
  }
}

@media (max-width: 768px) {
  .top-bar {
    flex-direction: column;
    gap: 15px;
    padding: 15px 20px;
  }
  
  .top-left,
  .top-right {
    width: 100%;
    justify-content: center;
  }
  
  .website-name {
    font-size: 18px;
  }
  
  .nav-list {
    flex-direction: column;
    align-items: center;
    gap: 5px;
  }
  
  .nav-item {
    width: 100%;
    text-align: center;
    border-radius: 0;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.nav-container {
  animation: fadeIn 0.6s ease-out;
}

/* 滚动时的导航栏样式变化 - 使用背景图片 */
.nav-container.scrolled {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  background-image: url('../asset/img/opacity-b25.png');
  background-repeat: repeat;
}

.nav-container.scrolled .top-bar {
  background: none;
}

.nav-container.scrolled .nav-bar {
  background: none;
}

/* 确保在深色背景上的可读性 */
.nav-container.dark-bg .website-name,
.nav-container.dark-bg .date-info,
.nav-container.dark-bg .nav-item {
  color: #fff;
}

.nav-container.dark-bg .nav-item.active::after {
  background: #fff;
}

/* 确保在浅色背景上的可读性 - 使用背景图片 */
.nav-container.light-bg .website-name,
.nav-container.light-bg .date-info,
.nav-container.light-bg .nav-item {
  color: #333;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.nav-container.light-bg .top-bar,
.nav-container.light-bg .nav-bar {
  background: none;
}

.nav-container.light-bg .nav-item:hover {
  background: rgba(0, 0, 0, 0.15);
}

.nav-container.light-bg .nav-item.active {
  background: none;
}

.nav-container.light-bg .nav-item.active::after {
  background: #333;
}

.nav-container.light-bg .avatar-icon {
  color: #333;
  filter: drop-shadow(1px 1px 2px rgba(255, 255, 255, 0.8));
}
</style>