<template>
  <div class="page-content">
    <!-- 视频背景 -->
    <div class="video-background">
      <video 
        id="backgroundVideo" 
        ref="videoRef" 
        muted 
        loop 
        playsinline 
        class="background-video" 
        preload="auto"
        autoplay
      >
        <source src="../../asset/video/1.mp4" type="video/mp4">
        您的浏览器不支持视频标签
      </video>
    </div>
    
    <!-- 内容层 -->
    <div class="hero-content">
      <h1 class="hero-title" :class="{ 'animate-in': isVisible }">光影千年</h1>
      <p class="hero-subtitle" :class="{ 'animate-in': isVisible }">皮影数字化传承 · 以数字为幕，续写千年传奇</p>
      <button class="cta-button" :class="{ 'animate-in': isVisible }" @click="goToNextPage">
        步入光影之境
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

// 视频引用
const videoRef = ref(null);
// 控制动画显示状态
const isVisible = ref(false);
// 创建路由实例
const router = useRouter();

// 跳转到下一页
const goToNextPage = () => {
  // 使用路由跳转到page2
  router.push('/page2');
};

// 处理视频加载和播放
const handleVideo = () => {
  const video = videoRef.value;
  if (video) {
    // 确保视频在页面加载后播放
    video.play().catch(error => {
      console.warn('视频自动播放失败，等待用户交互：', error);
      // 添加用户交互监听器来触发播放
      const handleUserInteraction = () => {
        video.play();
        document.removeEventListener('click', handleUserInteraction);
        document.removeEventListener('touchstart', handleUserInteraction);
      };
      document.addEventListener('click', handleUserInteraction);
      document.addEventListener('touchstart', handleUserInteraction);
    });
  }
};

// 监听滚动事件，显示动画
const handleScroll = () => {
  // 可以根据需要调整显示逻辑
  isVisible.value = true;
};

// 生命周期钩子
onMounted(() => {
  handleVideo();
  isVisible.value = true; // 页面加载时显示动画
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
/* 页面容器 */
.page-content {
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #000;
}

/* 视频背景容器 */
.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

/* 背景视频样式 */
.background-video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  transform: translate(-50%, -50%);
  filter: brightness(0.7); /* 稍微调暗视频以提高文字可读性 */
}

/* 内容层样式 */
.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  /* 移除了这里的color:white，让各个元素单独设置颜色 */
  padding: 20px;
  max-width: 800px;
}

/* 标题样式 - 艺术字体效果 */
.hero-title {
  font-size: 4.5rem;
  font-weight: bold;
  margin-bottom: 20px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 1s ease-out;
  /* 艺术字体样式 */
  font-family: 'STKaiti', 'KaiTi', 'STZhongsong', 'SimSun', serif;
  letter-spacing: 5px;
  text-transform: uppercase;
  
  /* 修改为暖金色，增强皮影艺术感 */
  color: #f8d77a;
  text-shadow: 0 0 10px rgba(248, 215, 122, 0.7), 
               0 0 20px rgba(248, 215, 122, 0.5),
               0 0 30px rgba(248, 215, 122, 0.3);
}

/* 副标题样式 */
.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 40px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 1s ease-out 0.3s; /* 延迟0.3秒动画 */
  /* 艺术字体样式 */
  font-family: 'STKaiti', 'KaiTi', 'STZhongsong', serif;
  letter-spacing: 2px;
  
  /* 添加金色到白色的渐变效果 */
  background: linear-gradient(90deg, #f8d77a, #fff, #f8d77a);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: none; /* 移除之前的黑色阴影 */
  
  /* 添加动画效果 */
  animation: shine 3s infinite linear;
}

/* 按钮样式 */
.cta-button {
  display: inline-block;
  padding: 15px 30px;
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
  background-color: rgba(255, 255, 255, 0.2);
  border: 2px solid white;
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(30px);
  transition: all 1s ease-out 0.6s; /* 延迟0.6秒动画 */
  backdrop-filter: blur(5px);
  cursor: pointer;
  /* 艺术字体样式 */
  font-family: 'STKaiti', 'KaiTi', 'STZhongsong', serif;
  letter-spacing: 2px;
  position: relative;
  overflow: hidden;
}

.cta-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: all 0.6s;
}

.cta-button:hover::before {
  left: 100%;
}

.cta-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3), 0 0 15px rgba(248, 215, 122, 0.4);
  
  /* 悬停时变为金色 */
  color: #f8d77a;
  border-color: #f8d77a;
}

.cta-button:active {
  transform: translateY(0) scale(0.98);
}

/* 动画进入效果 */
.animate-in {
  opacity: 1;
  transform: translateY(0);
}

/* 文字渐变动画 */
@keyframes shine {
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 200% center;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.8rem;
    letter-spacing: 3px;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
    letter-spacing: 1px;
  }
  
  .cta-button {
    padding: 12px 24px;
    font-size: 1rem;
    letter-spacing: 1px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2.2rem;
    letter-spacing: 2px;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    letter-spacing: 0.5px;
  }
}
</style>