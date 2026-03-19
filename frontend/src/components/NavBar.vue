<template>
  <div v-if="currentPage === 0" class="nav-container">
    <div class="top-bar">
        <div class="top-left">
          <img src="../asset/img/logo.png" class="logo" alt="皮影数字化传承" />
          <span class="website-name">光影千年·皮影数字化传承</span>
        </div>
        <div class="top-right">
          <div class="date-info">{{ formattedDate }}</div>
          
          <div class="user-avatar" @click="handleAvatarClick" role="button" tabindex="0" @keydown.enter="handleAvatarClick" @keydown.space="handleAvatarClick">
            <img v-if="userInfo?.avatar" :src="userInfo.avatar" class="avatar-img-nav" alt="用户头像" />
            <div v-else-if="userInfo" class="avatar-placeholder-nav">{{ userInfo.username?.charAt(0) || '访' }}</div>
            <div v-else class="avatar-icon">
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
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

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

const router = useRouter();
const route = useRoute();
const userInfo = ref(null);

// 检查登录状态并加载用户信息
const checkUserStatus = () => {
  // 核心修复：同时检查 localStorage 和 sessionStorage
  const savedUser = localStorage.getItem('user') || sessionStorage.getItem('user');
  if (savedUser) {
    userInfo.value = JSON.parse(savedUser);
  } else {
    userInfo.value = null;
  }
};

// 监听路由变化，一旦回到首页就重新检查缓存，确保头像最新
watch(() => route.path, () => {
  checkUserStatus();
});

onMounted(() => {
  checkUserStatus();
});

// 处理头像点击事件
const handleAvatarClick = () => {
  if (userInfo.value) {
    router.push('/user-center');
  } else {
    router.push('/login');
  }
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

.top-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

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

.website-name {
  font-family: 'Ma Shan Zheng', cursive, 'Noto Serif SC', serif;
  font-size: 24px;
  color: #fff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  letter-spacing: 2px;
  font-weight: bold;
}

.top-right {
  display: flex;
  align-items: center;
  gap: 30px;
}

.date-info {
  font-family: 'Noto Serif SC', serif;
  font-size: 16px;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.user-avatar {
  cursor: pointer;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #f56c6c;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  position: relative;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  overflow: hidden;
}

.user-avatar:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  background: rgba(255, 255, 255, 0.3);
}

.user-avatar:active {
  transform: scale(0.95);
}

.avatar-img-nav {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder-nav {
  color: #ffffff;
  font-weight: bold;
  font-size: 1.2rem;
}

.avatar-icon {
  color: #fff;
  width: 24px;
  height: 24px;
  filter: drop-shadow(1px 1px 2px rgba(0, 0, 0, 0.5));
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-bar {
  padding: 10px 0;
  background: none;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

.nav-list {
  display: flex;
  justify-content: center;
  list-style: none;
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
  gap: 10px;
}

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

.nav-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.nav-item.active {
  font-weight: bold;
  position: relative;
  background: none;
}

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
  from { width: 0; left: 50%; }
  to { width: 100%; left: 0; }
}

.nav-item:active {
  transform: translateY(0);
  background: rgba(255, 255, 255, 0.4);
}

@media (max-width: 1200px) {
  .top-bar { padding: 15px 30px; }
  .website-name { font-size: 20px; }
  .nav-item { font-size: 16px; padding: 10px 20px; }
}

@media (max-width: 768px) {
  .top-bar { flex-direction: column; gap: 15px; padding: 15px 20px; }
  .top-left, .top-right { width: 100%; justify-content: center; }
  .website-name { font-size: 18px; }
  .nav-list { flex-direction: column; align-items: center; gap: 5px; }
  .nav-item { width: 100%; text-align: center; border-radius: 0; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.nav-container {
  animation: fadeIn 0.6s ease-out;
}

.nav-container.scrolled {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  background-image: url('../asset/img/opacity-b25.png');
  background-repeat: repeat;
}

.nav-container.scrolled .top-bar { background: none; }
.nav-container.scrolled .nav-bar { background: none; }

.nav-container.dark-bg .website-name,
.nav-container.dark-bg .date-info,
.nav-container.dark-bg .nav-item { color: #fff; }

.nav-container.dark-bg .nav-item.active::after { background: #fff; }

.nav-container.light-bg .website-name,
.nav-container.light-bg .date-info,
.nav-container.light-bg .nav-item {
  color: #333;
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
}

.nav-container.light-bg .top-bar,
.nav-container.light-bg .nav-bar { background: none; }
.nav-container.light-bg .nav-item:hover { background: rgba(0, 0, 0, 0.15); }
.nav-container.light-bg .nav-item.active { background: none; }
.nav-container.light-bg .nav-item.active::after { background: #333; }
.nav-container.light-bg .avatar-icon {
  color: #333;
  filter: drop-shadow(1px 1px 2px rgba(255, 255, 255, 0.8));
}
</style>