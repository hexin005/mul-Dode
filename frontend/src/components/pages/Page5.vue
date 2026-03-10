<template>
  <div class="heritage-page">
    <div class="container">
      <!-- 第一个卡片：文博网（无悬停效果） -->
      <div class="card first-card">
        <div class="content">
          <div class="title">文</div>
          <div class="title">博</div>
          <div class="title">网</div>
          <div class="description">识准点</div>
        </div>
      </div>

      <!-- 其他卡片 -->
      <div 
        v-for="(card, index) in cards" 
        :key="index" 
        class="card" 
        :class="`card-${index+2}`"
      >
        <div class="content">
          <div class="icon">{{ card.icon }}</div>
          <div class="sub-title">{{ card.title }}</div>
          <div class="description">{{ card.shortDescription }}</div>
          <button class="view-more" @click="showModal(index)">查看更多</button>
        </div>
      </div>
    </div>

    <!-- 弹窗 -->
    <div class="modal-overlay" :class="{ active: showModalFlag }" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-image">
          <div class="carousel-container">
            <div 
              v-for="(color, index) in currentCard.colors" 
              :key="index"
              class="carousel-slide" 
              :class="{ 
                active: currentSlide === index,
                prev: currentSlide > index,
                next: currentSlide < index
              }"
              :style="{ background: `linear-gradient(135deg, ${color} 0%, ${darkenColor(color, 20)} 100%)` }"
            ></div>
          </div>
          <div class="carousel-controls">
            <div 
              v-for="(color, index) in currentCard.colors" 
              :key="index"
              class="carousel-dot" 
              :class="{ active: currentSlide === index }"
              @click="goToSlide(index)"
            ></div>
          </div>
        </div>
        <div class="modal-text">
          <h2 class="modal-title">{{ currentCard.title }}</h2>
          <p class="modal-description">{{ currentCard.fullDescription }}</p>
        </div>
        <button class="close-btn" @click="closeModal">×</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'

// 卡片数据
const cards = reactive([
  {
    icon: '📜📜',
    title: '宣纸传统制作技艺',
    shortDescription: '宣纸制作技艺是中国传统手工造纸技艺的重要代表，已有1000多年历史，以其质地绵韧、不蛀不腐等特点闻名。',
    fullDescription: '宣纸制作技艺是中国传统手工造纸技艺的重要代表，已有1000多年历史。宣纸制作过程复杂，包括选料、浸泡、蒸煮、漂白、打浆、抄纸、压榨、烘干等多道工序。宣纸以其质地绵韧、洁白稠密、光而不滑、不蛀不腐等特点闻名，被誉为"纸寿千年"。宣纸主要产自安徽泾县，是中国书画艺术的重要载体，也是研究中国古代造纸技术的重要实物资料。2006年，宣纸传统制作技艺被列入国家级非物质文化遗产名录。',
    colors: ['#f5e6d3', '#e8d5b9', '#d9c4a3', '#c9b38d', '#b9a277']
  },
  {
    icon: '🌱🌱',
    title: '二十四节气',
    shortDescription: '二十四节气是中国古代订立的一种用来指导农事的补充历法，是中华民族劳动人民长期经验的积累和智慧的结晶。',
    fullDescription: '二十四节气是中国古代订立的一种用来指导农事的补充历法，是中华民族劳动人民长期经验的积累和智慧的结晶。二十四节气根据太阳在黄道上的位置划分，每个节气约15天，反映了一年四季的气候变化规律。二十四节气包括：立春、雨水、惊蛰、春分、清明、谷雨、立夏、小满、芒种、夏至、小暑、大暑、立秋、处暑、白露、秋分、寒露、霜降、立冬、小雪、大雪、冬至、小寒、大寒。2016年，二十四节气被列入联合国教科文组织人类非物质文化遗产代表作名录。',
    colors: ['#5c3d2e', '#7a5240', '#9a6b52', '#b98464', '#d99d76']
  },
  {
    icon: '☯☯️',
    title: '太极拳',
    shortDescription: '太极拳是以中国传统儒、道哲学中的太极、阴阳辩证理念为核心思想，集颐养性情、强身健体等多种功能为一体的传统拳术。',
    fullDescription: '太极拳是以中国传统儒、道哲学中的太极、阴阳辩证理念为核心思想，集颐养性情、强身健体、技击对抗等多种功能为一体的传统拳术。太极拳动作柔和缓慢，强调"以柔克刚"、"以静制动"，注重内外兼修，形神兼备。太极拳有多种流派，如陈式、杨式、吴式、武式、孙式等。练习太极拳可以改善身体平衡能力，增强心肺功能，缓解压力，提高身体协调性。2020年，太极拳被列入联合国教科文组织人类非物质文化遗产代表作名录。',
    colors: ['#4a2c2a', '#6a403c', '#8a544e', '#aa6860', '#ca7c72']
  },
  {
    icon: '🌍🌍',
    title: '文化和自然遗产日',
    shortDescription: '每年6月的第二个星期六是中国的"文化和自然遗产日"，旨在营造保护文化遗产的良好氛围，提高人民群众对文化遗产保护重要性的认识。',
    fullDescription: '每年6月的第二个星期六是中国的"文化和自然遗产日"，旨在营造保护文化遗产的良好氛围，提高人民群众对文化遗产保护重要性的认识。文化和自然遗产日设立于2006年，原为"文化遗产日"，2017年调整为"文化和自然遗产日"。在这一天，全国各地会举办各种形式的宣传活动，如免费开放文物保护单位、举办文化遗产展览、开展非物质文化遗产展示等。这些活动有助于增强公众的文化遗产保护意识，促进文化遗产的传承与发展。',
    colors: ['#8b2323', '#b02e2e', '#d53939', '#f54444', '#ff5555']
  },
  {
    icon: '📷📷',
    title: '摄影',
    shortDescription: '通过影像和声音感受文化遗产的魅力',
    fullDescription: '通过影像和声音感受文化遗产的魅力。摄影作为一种记录和传播手段，在文化遗产保护中发挥着重要作用。通过摄影，我们可以记录下文化遗产的现状，展示其独特魅力，唤起公众的保护意识。文化遗产摄影不仅包括对文物古迹的记录，还包括对非物质文化遗产的影像呈现，如传统节庆、民俗活动、手工技艺等。优秀的文化遗产摄影作品能够跨越时空，让观者感受到历史的厚重和文化的魅力，促进文化遗产的传承与传播。',
    colors: ['#1a365d', '#2a4a7a', '#3a5e97', '#4a72b4', '#5a86d1']
  }
])

// 响应式数据
const showModalFlag = ref(false)
const currentSlide = ref(0)
const currentCard = reactive({
  title: '',
  fullDescription: '',
  colors: []
})
let slideInterval = null

// 方法
const showModal = (index) => {
  currentCard.title = cards[index].title
  currentCard.fullDescription = cards[index].fullDescription
  currentCard.colors = [...cards[index].colors]
  showModalFlag.value = true
  startAutoSlide()
}

const closeModal = () => {
  showModalFlag.value = false
  stopAutoSlide()
}

const darkenColor = (color, percent) => {
  const num = parseInt(color.slice(1), 16)
  const amt = Math.round(2.55 * percent)
  const R = (num >> 16) - amt
  const G = ((num >> 8) & 0x00FF) - amt
  const B = (num & 0x0000FF) - amt
  return "#" + (0x1000000 + (R < 0 ? 0 : R) * 0x10000 + (G < 0 ? 0 : G) * 0x100 + (B < 0 ? 0 : B)).toString(16).slice(1)
}

const goToSlide = (slideIndex) => {
  currentSlide.value = slideIndex
}

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % currentCard.colors.length
}

const startAutoSlide = () => {
  stopAutoSlide()
  slideInterval = setInterval(nextSlide, 2000)
}

const stopAutoSlide = () => {
  if (slideInterval) {
    clearInterval(slideInterval)
    slideInterval = null
  }
}

const ensureFullWidth = () => {
  const container = document.querySelector('.container')
  if (container) {
    container.style.width = window.innerWidth + 'px'
  }
}

// 生命周期
onMounted(() => {
  window.addEventListener('resize', ensureFullWidth)
  ensureFullWidth()
})

onUnmounted(() => {
  window.removeEventListener('resize', ensureFullWidth)
  stopAutoSlide()
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.heritage-page {
  font-family: 'Microsoft Yahei', Arial, sans-serif;
  background-color: #0a3d31;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
}

.container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* 所有卡片等宽 */
.card {
  position: relative;
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  cursor: pointer;
  overflow: hidden;
  flex-shrink: 0;
}

/* 根据图片准确的颜色设置卡片背景 */
.first-card {
  background: linear-gradient(135deg, #0a3d31 0%, #1a5a48 100%);
  cursor: default;
}

.card-2 {
  background: linear-gradient(135deg, #f5e6d3 0%, #e8d5b9 100%);
}

.card-3 {
  background: linear-gradient(135deg, #5c3d2e 0%, #7a5240 100%);
}

.card-4 {
  background: linear-gradient(135deg, #4a2c2a 0%, #6a403c 100%);
}

.card-5 {
  background: linear-gradient(135deg, #8b2323 0%, #b02e2e 100%);
}

.card-6 {
  background: linear-gradient(135deg, #1a365d 0%, #2a4a7a 100%);
}

/* 文字颜色 - 根据图片准确设置 */
.first-card,
.card-3,
.card-4,
.card-5,
.card-6 {
  color: white;
}

.card-2 {
  color: #333;
}

/* 内容区域 */
.content {
  padding: 20px;
  text-align: center;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 2;
}

/* 图标样式 */
.icon {
  font-size: 40px;
  margin-bottom: 20px;
}

/* 标题样式 */
.title {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 5px;
}

.sub-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
  line-height: 1.3;
}

/* 描述文本 */
.description {
  font-size: 16px;
  line-height: 1.6;
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  transition: all 0.5s ease;
  margin-top: 10px;
}

/* 查看更多按钮 - 初始状态隐藏 */
.view-more {
  margin-top: 20px;
  font-size: 14px;
  padding: 8px 20px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  color: inherit;
  color: rgba(255, 255, 255, 0.9);
  opacity: 0;
  transform: translateY(10px);
  position: relative;
  z-index: 10;
}

.card-2 .view-more {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

/* 第一个卡片（文博网）特殊样式 - 完全无悬停效果 */
.first-card {
  flex: 1 !important;
  transform: none !important;
  box-shadow: none !important;
  z-index: 1 !important;
}

.first-card:hover {
  flex: 1 !important;
  transform: none !important;
  box-shadow: none !important;
  z-index: 1 !important;
}

.first-card .content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.first-card .title {
  font-size: 36px;
  margin: 8px 0;
  line-height: 1;
}

.first-card .description {
  font-size: 16px;
  max-height: 60px;
  opacity: 1;
  margin-top: 20px;
  color: rgba(255, 255, 255, 0.9);
}

/* 第一个卡片没有查看更多按钮 */
.first-card .view-more {
  display: none;
}

/* 悬停效果 - 只应用于第2-6个卡片 */
.card-2:hover,
.card-3:hover,
.card-4:hover,
.card-5:hover,
.card-6:hover {
  flex: 2.2;
  z-index: 10;
  box-shadow: 0 0 25px rgba(0, 0, 0, 0.3);
}

/* 当有卡片悬停时，其他卡片（除了第一个和当前悬停的）等宽缩小 */
.container:hover .card-2:not(:hover),
.container:hover .card-3:not(:hover),
.container:hover .card-4:not(:hover),
.container:hover .card-5:not(:hover),
.container:hover .card-6:not(:hover) {
  flex: 0.8;
  opacity: 0.85;
}

/* 第一个卡片在任何情况下都不受影响 */
.container:hover .first-card {
  flex: 1 !important;
  opacity: 1 !important;
}

/* 悬停时显示描述和查看更多按钮 */
.card-2:hover .description,
.card-3:hover .description,
.card-4:hover .description,
.card-5:hover .description,
.card-6:hover .description {
  max-height: 120px;
  opacity: 1;
  margin-top: 15px;
}

.card-2:hover .view-more,
.card-3:hover .view-more,
.card-4:hover .view-more,
.card-5:hover .view-more,
.card-6:hover .view-more {
  opacity: 1;
  transform: translateY(0);
  background: rgba(255, 255, 255, 0.25);
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.modal-content {
  width: 80%;
  max-width: 900px;
  height: 70%;
  background-color: white;
  border-radius: 10px;
  display: flex;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  transform: scale(0.8);
  transition: transform 0.3s ease;
  position: relative;
}

.modal-overlay.active .modal-content {
  transform: scale(1);
}

.modal-image {
  width: 40%;
  position: relative;
  overflow: hidden;
}

.carousel-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.carousel-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  background-size: cover;
  background-position: center;
  transform: translateX(100%);
}

.carousel-slide.active {
  opacity: 1;
  transform: translateX(0);
  z-index: 2;
}

.carousel-slide.prev {
  transform: translateX(-100%);
  opacity: 0;
  z-index: 1;
}

.carousel-slide.next {
  transform: translateX(100%);
  opacity: 0;
  z-index: 1;
}

.carousel-controls {
  position: absolute;
  bottom: 20px;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 10px;
  z-index: 10;
}

.carousel-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.carousel-dot.active {
  background-color: white;
  transform: scale(1.2);
}

.modal-text {
  width: 60%;
  padding: 40px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.modal-title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.modal-description {
  font-size: 18px;
  line-height: 1.8;
  color: #555;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 30px;
  color: #fff;
  background: none;
  border: none;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s;
  z-index: 1001;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>