<template>
  <div class="page-content" :class="{ loaded: pageLoaded }">
    <h2 class="page-title">千年历史，一盏灯影</h2>
    <!-- 自动滚动容器 -->
    <div class="timeline-container">
      <div class="timeline-wrapper" ref="timelineWrapper" @mouseenter="pauseScroll" @mouseleave="resumeScroll">
        <div class="timeline-track" ref="timelineTrack">
          <!-- 渲染数据卡片 -->
          <div v-for="(item, index) in timelineItems" :key="`item-${index}`" class="timeline-card">
            <!-- 卡片内容 - 包含描述和图片 -->
            <div class="card-body">
              <!-- 年代标签 - 顶部左端 -->
              <div class="year-tag">
                {{ item.years }}
              </div>
              <!-- 标题 - 单行显示 -->
              <h3 class="card-title single-line-title">{{ item.title }}</h3>
              <!-- 分割线 -->
              <div class="divider"></div>
              <!-- 描述文本 -->
              <div class="description-container">
                <p class="description-text">
                  {{ item.description }}
                </p>
              </div>
              
              <!-- 图片区域 -->
              <div class="image-section">
                <img :src="item.image" :alt="item.title" class="timeline-image" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';

// 时间轴数据
const timelineItems = [
  {
    years: '公元前140年-公元220年',
    title: '先秦至汉代：起源传说与技艺萌芽',
    description: '《搜神记》载，皮影戏萌芽于汉武帝时。李少翁以剪影慰武帝思李夫人之念，高承据此称影戏始于汉。"弄影" 技艺与皮革加工已为后世奠定基。',
    image: 'src/asset/img/handai.png'
  },
  {
    years: '公元220年-589年',
    title: '魏晋南北朝：宗教催化与形式孕育',
    description: '皮影戏与佛道说唱相关，宗教传播推动 "图像 + 叙事"。剪纸、皮革镂刻助力影偶制作，虽无明确文献，仍为唐代成形。',
    image: 'src/asset/img/weijin.png'
  },
  {
    years: '公元618年-907年',
    title: '唐代：雏形形成与宫廷渗透',
    description: '齐如山《故都百戏图考》称影戏源于唐西安，因西安为古都、玄宗倡美术，文化繁荣，此说有理。汉中现盛行皮影，影偶更大、油绘精、技艺巧于北京。',
    image: 'src/asset/img/tangdai.png'
  },
  {
    years: '公元960年-1279年',
    title: '宋代：市井繁荣与体系成熟',
    description: '宋代皮影戏城市普及，为市民所爱。张耒《明道杂志》首记京师富家子爱看影戏，影人从素纸发展为刻皮设色。杭州有 "绘革社"，艺人分工雕镂彩绘。',
    image: 'src/asset/img/songdai.png'
  },
  {
    years: '公元1206年-1368年',
    title: '元代：跨文化传播与内容革新',
    description: '元明影戏盛行，瞿佑《看灯诗》有载。其吸收戏曲、民歌等精华，形成各异流派，随蒙古西征传入中亚等地，波斯称 "Chāy Khāyāl"。',
    image: 'src/asset/img/yuandai.png'
  },
  {
    years: '公元1368年-1644年',
    title: '明代：流派初现与地域分化',
    description: '明代，皮影戏得到进一步发展。皮影戏逐渐从宫廷走向民间，形成了不同的地域特色。各地艺人根据当地文化和审美习惯，创造了各具特色的皮影艺术风格。',
    image: 'src/asset/img/mingdai.png'
  },
  {
    years: '公元1616年-1911年',
    title: '清代：巅峰鼎盛与流派定型',
    description: '清代皮影鼎盛，王府蓄班藏影。北滦州驴皮影、南海宁羊皮影，唐驴、浙羊、湘牛皮各异，工艺精细，风行南北。',
    image: 'src/asset/img/qingdai.png'
  },
  {
    years: '1912年至今',
    title: '近现代：冲击与传承转型',
    description: '皮影戏为中国古老民间艺术，千年传承。融多技艺，影人精美兼具实用与观赏，当代守传统、为中外文化交流载体。',
    image: 'src/asset/img/jindai.png'
  }
];

// 滚动相关引用和状态
const timelineWrapper = ref(null);
const timelineTrack = ref(null);
const isScrolling = ref(true); // 保留这一个声明
const animationId = ref(null);
const scrollSpeed = ref(1);
const itemsWidth = ref(0);
const itemCount = ref(0);

// 页面加载状态 - 用于页面加载动画
const pageLoaded = ref(false);

// 观察卡片进入视口的函数 - 用于卡片滚动渐入效果
const observeCards = () => {
  if (!timelineWrapper.value) return;
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('card-visible');
        // 只观察一次
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    root: timelineWrapper.value
  });
  
  // 观察所有卡片
  const cards = timelineWrapper.value.querySelectorAll('.timeline-card');
  cards.forEach(card => {
    observer.observe(card);
  });
  
  return observer;
};

// 优化的项目复制函数，确保克隆元素不包含Vue key属性
const duplicateItemsForLoop = () => {
  if (!timelineTrack.value) return;
  
  const originalItems = Array.from(timelineTrack.value.children);
  itemCount.value = originalItems.length;
  
  // 复制两份项目以实现更平滑的无缝循环
  for (let j = 0; j < 2; j++) {
    for (let i = 0; i < itemCount.value; i++) {
      // 创建新的div元素而非直接克隆，避免携带Vue属性
      const clone = document.createElement('div');
      // 设置必要的类和数据属性
      clone.className = 'timeline-card';
      clone.setAttribute('data-original-index', i);
      clone.setAttribute('data-clone-index', j);
      
      // 克隆内容而不是整个元素
      const originalContent = originalItems[i].firstElementChild;
      if (originalContent) {
        const contentClone = originalContent.cloneNode(true);
        clone.appendChild(contentClone);
      }
      
      timelineTrack.value.appendChild(clone);
    }
  }
  
  // 计算项目宽度
  nextTick(() => {
    calculateItemsWidth();
  });
};

// 计算所有原始项目的总宽度
const calculateItemsWidth = () => {
  if (!timelineWrapper.value || itemCount.value === 0) return;
  
  const cards = timelineWrapper.value.querySelectorAll('.timeline-card');
  if (cards.length >= itemCount.value) {
    let totalWidth = 0;
    // 只计算原始项目的宽度
    for (let i = 0; i < itemCount.value; i++) {
      totalWidth += cards[i].offsetWidth;
      // 添加间隙（除了最后一个项目）
      if (i < itemCount.value - 1) {
        totalWidth += 30; // 与CSS中的gap保持一致
      }
    }
    itemsWidth.value = totalWidth;
  }
};

// 优化的滚动函数
const scroll = () => {
  if (!timelineWrapper.value || !isScrolling.value) {
    return;
  }
  
  // 向左滚动
  timelineWrapper.value.scrollLeft += scrollSpeed.value;
  
  // 检查是否需要重置滚动位置以实现循环
  if (timelineWrapper.value.scrollLeft >= itemsWidth.value) {
    // 无缝重置
    timelineWrapper.value.scrollLeft = 0;
  }
  
  animationId.value = requestAnimationFrame(scroll);
};

// 开始自动滚动
const startAutoScroll = () => {
  if (animationId.value) {
    cancelAnimationFrame(animationId.value);
  }
  scroll();
};

// 暂停滚动
const pauseScroll = () => {
  isScrolling.value = false;
  if (animationId.value) {
    cancelAnimationFrame(animationId.value);
    animationId.value = null;
  }
};

// 恢复滚动
const resumeScroll = () => {
  isScrolling.value = true;
  startAutoScroll();
};

// 窗口大小变化处理
const handleResize = () => {
  nextTick(() => {
    calculateItemsWidth();
  });
};

// 组件挂载后初始化
onMounted(() => {
  nextTick(() => {
    // 添加短暂延迟后显示页面内容 - 页面加载动画
    setTimeout(() => {
      pageLoaded.value = true;
    }, 100);
    
    duplicateItemsForLoop();
    startAutoScroll();
    window.addEventListener('resize', handleResize);
    
    // 启动卡片观察器 - 卡片滚动渐入效果
    let observer;
    setTimeout(() => {
      observer = observeCards();
    }, 500);
    
    // 组件卸载时清理观察器
    onUnmounted(() => {
      if (observer) observer.disconnect();
    });
  });
});

// 组件卸载时清理
onUnmounted(() => {
  if (animationId.value) {
    cancelAnimationFrame(animationId.value);
  }
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 页面内容样式 - 温暖米色背景和宣纸纹理 */
.page-content {
  width: 100%;
  min-height: 100vh;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #f9f3e8 0%, #f5e9d8 100%);
  /* 统一使用Page1中的艺术字体 */
  font-family: 'STKaiti', 'KaiTi', 'STZhongsong', 'SimSun', serif;
  color: #5c4d32;
  position: relative;
  overflow: hidden;
  
  /* 页面加载动画 - 初始状态 */
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

/* 页面加载动画 - 加载完成状态 */
.page-content.loaded {
  opacity: 1;
  transform: translateY(0);
}

/* 添加宣纸纹理背景效果 */
.page-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%238a6d3b' fill-opacity='0.03' fill-rule='evenodd'/%3E%3C/svg%3E");
  opacity: 0.7;
  pointer-events: none;
  z-index: 0;
}

/* 页面标题样式 - 采用与Page1一致的艺术字体 */
.page-title {
  text-align: center;
  margin-bottom: 4rem;
  font-weight: bold;
  font-size: 2.8rem;
  /* 艺术字体样式 - 与Page1一致 */
  font-family: 'STKaiti', 'KaiTi', 'STZhongsong', 'SimSun', serif;
  letter-spacing: 3px;
  position: relative;
  z-index: 1;
  
  /* 深褐色文字 */
  color: #8a4a22;
  text-shadow: 1px 1px 3px rgba(138, 74, 34, 0.1);
}

/* 滚动容器 */
.timeline-container {
  width: 100%;
  overflow: hidden;
  position: relative;
  margin-bottom: 2rem;
  z-index: 1;
}

/* 滚动包装器 */
.timeline-wrapper {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  position: relative;
  cursor: grab;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.timeline-wrapper::-webkit-scrollbar {
  display: none; /* Chrome, Safari */
}

.timeline-wrapper:active {
  cursor: grabbing;
}

/* 时间轴轨道 */
.timeline-track {
  display: flex;
  gap: 30px;
  padding: 0 1rem;
  position: relative;
  min-width: 100%;
  width: fit-content;
}

/* 单个卡片 - 添加滚动渐入动画 */
.timeline-card {
  flex: 0 0 auto;
  width: 450px;
  height: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  contain: layout;
  
  /* 卡片滚动渐入动画 - 初始状态 */
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}

/* 卡片滚动渐入动画 - 可见状态 */
.timeline-card.card-visible {
  opacity: 1;
  transform: translateY(0);
}

/* 为不同位置的卡片添加不同的延迟，创建级联效果 */
.timeline-card:nth-child(odd) {
  transition-delay: 0.1s;
}

.timeline-card:nth-child(even) {
  transition-delay: 0.2s;
}

/* 卡片主体 - 米色渐变背景与棕色边框 */
.card-body {
  background: linear-gradient(135deg, #ffffff 0%, #f8f5f0 100%);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 6px 20px rgba(138, 109, 59, 0.1);
  position: relative;
  z-index: 2;
  width: 100%;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  border: 1px solid #d3b88c;
  isolation: isolate;
}

.card-body:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(138, 109, 59, 0.2);
  border-color: #8a4a22;
}

/* 年代标签 - 深褐色背景 - 添加动画效果 */
.year-tag {
  display: inline-block;
  background-color: #8a4a22;
  color: #ffffff;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: left;
  align-self: flex-start;
  height: 36px;
  line-height: 26px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  font-family: 'STKaiti', 'KaiTi', 'STZhongsong', serif;
  letter-spacing: 1px;
  
  /* 年代标签动画 - 添加闪光效果 */
  position: relative;
  overflow: hidden;
}

/* 年代标签闪光动画 */
.year-tag::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  animation: shine 3s infinite;
}

/* 闪光动画关键帧 */
@keyframes shine {
  100% {
    left: 100%;
  }
}

/* 卡片标题 - 艺术字体和深褐色 */
.card-title {
  font-weight: 600;
  line-height: 1.4;
  text-align: left;
  margin-bottom: 1rem;
  font-family: 'STKaiti', 'KaiTi', 'STZhongsong', serif;
  
  /* 深褐色文字 */
  color: #8a4a22;
  letter-spacing: 1px;
}

/* 单行标题样式 */
.single-line-title {
  font-size: 1.4rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  height: auto;
  line-height: 1.6;
}

/* 分割线 - 深褐色渐变 */
.divider {
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #8a4a22, transparent);
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* 描述文本容器 */
.description-container {
  position: relative;
  flex-shrink: 0;
  margin-bottom: 1.5rem;
}

/* 描述文本 - 暖棕色，增加字体粗细使其更清晰 */
.description-text {
  color: #5c4d32;
  line-height: 1.6;
  font-size: 1rem;
  text-align: justify;
  display: -webkit-box;
  -webkit-line-clamp: 5;
  line-clamp: 5;
  -webkit-box-orient: vertical;
  box-orient: vertical;
  overflow: hidden;
  font-family: 'STKaiti', 'KaiTi', serif;
  font-weight: 500;
}

/* 图片区域 - 温暖米色背景 */
.image-section {
  width: 100%;
  min-height: 250px;
  max-height: 300px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: #f9f3e8;
  border-radius: 8px;
  margin-top: auto;
  flex-shrink: 0;
  border: 1px solid #e5d9c5;
  box-shadow: inset 0 0 10px rgba(138, 109, 59, 0.1);
}

/* 图片样式 */
.timeline-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
  border-radius: 4px;
}

.image-section:hover .timeline-image {
  transform: scale(1.05);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .timeline-card {
    width: 400px;
  }
  
  .single-line-title {
    font-size: 1.3rem;
  }
  
  .card-body {
    min-height: 480px;
  }
  
  .image-section {
    min-height: 220px;
    max-height: 280px;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2.2rem;
    margin-bottom: 3rem;
    letter-spacing: 2px;
  }
  
  .timeline-card {
    width: 350px;
  }
  
  .card-body {
    min-height: 450px;
    padding: 1.5rem;
  }
  
  .single-line-title {
    font-size: 1.2rem;
  }
  
  .description-text {
    font-size: 0.95rem;
    -webkit-line-clamp: 4;
    line-clamp: 4;
    font-weight: 500;
  }
  
  .image-section {
    min-height: 200px;
    max-height: 250px;
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: 2rem 1rem;
  }
  
  .page-title {
    font-size: 1.8rem;
    margin-bottom: 2rem;
    letter-spacing: 1px;
  }
  
  .timeline-card {
    width: 300px;
  }
  
  .timeline-track {
    gap: 2rem;
  }
  
  .card-body {
    min-height: 420px;
    padding: 1.2rem;
  }
  
  .single-line-title {
    font-size: 1.1rem;
  }
  
  .description-text {
    font-size: 0.85rem;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    font-weight: 500;
  }
  
  .image-section {
    min-height: 180px;
    max-height: 220px;
  }
}
</style>