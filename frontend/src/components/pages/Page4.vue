<template>
  <div class="heritage-page">
    <div class="container">
      <div class="card first-card">
        <div class="content">
          <div class="title">皮</div>
          <div class="title">影</div>
          <div class="title">类</div>
          <div class="title">别</div>
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
          <div class="sub-title" v-html="splitTitle(card.title)"></div>
          <button class="view-more" @click="showModal(index)">查看更多</button>
        </div>
      </div>
    </div>

    <!-- 弹窗 -->
    <div class="modal-overlay" :class="{ active: showModalFlag }" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-image">
          <div class="carousel-container">
            <img 
              v-for="(item, index) in currentCard.images" 
              :key="index"
              :src="item"
              class="carousel-slide-img" 
              :class="{ 
                active: currentSlide === index,
                prev: currentSlide > index,
                next: currentSlide < index
              }"
            />
          </div>
          <div class="carousel-controls">
            <div 
              v-for="(item, index) in currentCard.images" 
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
    title: '头茬',
    fullDescription: '皮影头茬是皮影戏中人物头像的雕刻造型，是用牛皮或驴皮经硝皮、雕刻、上色等工序制成的戏曲道具，堪称皮影戏的"脸谱"。它按角色行当分为生、旦、净、丑等类型，五官造型与色彩均有程式化的象征意义——红色表忠勇、黑色表刚正、白色表奸诈，不同的眉眼鼻型则暗示人物的性格与身份。皮影头茬起源于西汉，鼎盛于明清，全国各地形成了陕西、河北、河南、四川等不同风格流派。2006年入选中国国家级非物质文化遗产，2011年被列入联合国教科文组织人类非物质文化遗产代表作名录。它不仅是表演道具，更是民间雕刻艺术与戏曲艺术的完美结合，浓缩了中国传统美学与民俗信仰于方寸之间，被誉为世界上最早的"动画"艺术。',
    images: ['src/asset/img/tc-01.png', 'src/asset/img/tc-02.png', 'src/asset/img/tc-03.png', 'src/asset/img/tc-04.png', 'src/asset/img/tc-05.png', 'src/asset/img/tc-06.png']
  },
  {
    title: '影身',
    fullDescription: '皮影影身是皮影戏中人物除头部以外的全身造型，包括躯干、上肢、下肢及服饰，通常高约30至40厘米，通过竹签与头茬插接组合使用。影身是皮影艺术中工艺最精湛、装饰最繁复的部分，其服饰上布满龙凤纹、祥云纹、花卉纹等吉祥图案，关节处采用镂空雕刻以实现灵活转动，在幕后灯光照射下投射出独特的半透明光影美学。影身与头茬采用可拆卸组合的演出体制——同一身段可搭配不同头茬饰演不同角色，一物多用，极大丰富了表演的灵活性。影身按服饰等级分为龙袍身、官服身、短打身等多种类型，色彩与纹样也因角色身份和使用场景而异。它不仅是演出道具，更是民间雕刻技艺与服饰美学的集大成者，浓缩了老百姓对各朝代服饰制度的想象及对吉祥美好生活的祈愿。',
     images: ['src/asset/img/ys_01.png', 'src/asset/img/ys_02.png', 'src/asset/img/ys_03.png', 'src/asset/img/ys_04.png', 'src/asset/img/ys_05.png', 'src/asset/img/ys_06.png']
  },
  {
    title: '云朵子',
    fullDescription: '皮影云朵子是皮影戏中为神、佛、妖、怪等超自然角色设计的云彩造型道具，是这类角色腾云驾雾的专属"座驾"。它以云纹为底，将神祇形象与宗教意象巧妙融合，既是民间信仰的视觉化呈现，也是戏剧美学与雕刻艺术的结晶。云朵子的形象渊源可追溯至汉代画像石与历代壁画中的"神案"形象，经明清皮影艺人继承发展，在方寸牛皮上构建出气势恢宏的神话世界，承载着中国人对天界神祇的想象与祈愿，是皮影艺术中文化含量最高、最具浪漫气质的道具门类之一。',
    images: ['src/asset/img/ydz-01.png', 'src/asset/img/ydz-02.png', 'src/asset/img/ydz-03.png', 'src/asset/img/ydz-04.png', 'src/asset/img/ydz-05.png', 'src/asset/img/ydz-06.png']
  },
  {
    title: '桌椅',
    fullDescription: '皮影桌椅是皮影戏中用于装点室内环境、区分社会等级、营造叙事空间的重要道具，分为龙桌龙椅、相桌相椅、绣桌绣墩、佛桌仙桌、福寿桌椅及普通百姓桌椅等多个等级，分别对应皇帝、宰相、闺秀、神仙、寿宴及民间等不同场景。皮影桌椅采用半侧面程式化造型，桌腿、桌面、椅背等处精雕祥云、龙凤、牡丹、莲花等吉祥纹样，在幕后灯光照射下呈现出独特的镂空光影美学。它不仅是演出中的环境道具，更以直观的方式浓缩了中国传统家具制度与礼制秩序的民间想象，是皮影"影中世界"不可或缺的空间叙事元素，寄托着百姓对福禄寿喜的美好祈愿。',
    images: ['src/asset/img/zy-01.png', 'src/asset/img/zy-02.png', 'src/asset/img/zy-03.png', 'src/asset/img/zy-04.png', 'src/asset/img/zy-05.png', 'src/asset/img/zy-06.png']
  },
  {
    title: '衬景',
    fullDescription: '皮影衬景是皮影戏中用于构建戏剧空间、烘托环境氛围的大型布景道具，又称景片，大者可高约一米、宽两米余，需由数块牛皮拼接刻制而成。衬景涵盖宫殿、绣楼、营帐、花园、水晶宫、天宫等建筑与自然景观类型，以及皇帝出巡图、水族仪仗队等宏大场面，是皮影艺术中体量最大、气势最壮、雕刻最繁复的组成部分。其建筑造型严格参照中国古代建筑形制，雕梁画栋、斗拱飞檐一应俱全，同时融入大量吉祥纹样与民间美术元素。衬景充分利用牛皮镂空透光的特性，通过多层景片叠加营造出虚实交错、纵深感极强的舞台空间效果，是皮影"影中世界"时空叙事的关键工具，既承载了中国古代建筑制度的民间记忆，也浓缩了民间艺人惊人的艺术想象力与雕刻技艺的巅峰水准。',
    images: ['src/asset/img/bj-01.png', 'src/asset/img/bj-02.png', 'src/asset/img/bj-03.png', 'src/asset/img/bj-04.png', 'src/asset/img/bj-05.png', 'src/asset/img/bj-06.png']
  }
])

// 响应式数据
const showModalFlag = ref(false)
const currentSlide = ref(0)
const currentCard = reactive({
  title: '',
  fullDescription: '',
  images: []
})
let slideInterval = null

// 方法
const showModal = (index) => {
  currentCard.title = cards[index].title
  currentCard.fullDescription = cards[index].fullDescription
  currentCard.images = [...(cards[index].images || [])] // 如果有images字段则使用，否则为空数组
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
  const length = currentCard.images.length
  currentSlide.value = (currentSlide.value + 1) % length
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

// 拆分标题为单个字符，用于竖排显示
const splitTitle = (title) => {
  return title.split('').map(char => `<span>${char}</span>`).join('');
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
  font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft Yahei', Arial, sans-serif;
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
  align-items: flex-start;
  justify-content: center;
  transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  cursor: pointer;
  overflow: hidden;
  flex-shrink: 0;
}

/* 皮影类别卡片背景改为图片 */
.first-card {
  background-image: url(../../asset/img/fm-0.png);
  background-size: cover;
  background-position: center;
  cursor: default;
}

.card-2 {
  background-image: url(../../asset/img/fm-1.png);
  background-size: cover;
  background-position: left; 
}

.card-2:hover {
  background-position: center; /* 悬停时背景图片居中，展示全部 */
}

.card-3 {
  background-image: url(../../asset/img/fm-2.png);
  background-size: cover;
  background-position: left; 
}
.card-3:hover {
  background-position: center; /* 悬停时背景图片居中，展示全部 */
}

.card-4 {
   background-image: url(../../asset/img/fm-3.png);
  background-size: cover;
  background-position: left; 
}
.card-4:hover {
  background-position: center; /* 悬停时背景图片居中，展示全部 */
}

.card-5 {
  background-image: url(../../asset/img/fm-4.png);
  background-size: cover;
  background-position: left; 
}

.card-6 {
  background-image: url(../../asset/img/fm-5.png);
  background-size: cover;
  background-position: left; 
}

/* 文字颜色优化 */
.first-card,
.card-3,
.card-4,
.card-5,
.card-6 {
  color: #f0f0f0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.card-2 {
  color: #2c3e50;
}

/* 内容区域 */
.content {
  padding: 20px;
  text-align: left;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  position: relative;
  z-index: 2;
}

/* 标题样式 */
.title {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 5px;
  font-family: 'Source Han Serif', 'Songti SC', serif;
  letter-spacing: 2px;
}

.sub-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 30px;
  line-height: 1.8;
  writing-mode: vertical-rl;
  text-orientation: upright;
  text-align: left;
  font-family: 'Source Han Serif', 'Songti SC', serif;
}

.sub-title span {
  display: block;
  margin: 0;
}

/* 查看更多按钮 - 竖排显示 */
.view-more {
  font-size: 14px;
  padding: 10px 5px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  color: inherit;
  writing-mode: vertical-rl;
  text-orientation: upright;
  text-align: left;
  display: inline-block;
  letter-spacing: 2px;
}

.card-2 .view-more {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

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
  text-align: center;
}

.first-card .title {
  font-size: 36px;
  margin: 8px 0;
  line-height: 1;
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

.carousel-slide-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  opacity: 0;
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  transform: translateX(100%);
}

.carousel-slide-img.active {
  opacity: 1;
  transform: translateX(0);
  z-index: 2;
}

.carousel-slide-img.prev {
  transform: translateX(-100%);
  opacity: 0;
  z-index: 1;
}

.carousel-slide-img.next {
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
  color: #2c3e50;
  font-family: 'Source Han Serif', 'Songti SC', serif;
}

.modal-description {
  font-size: 18px;
  line-height: 1.8;
  color: #34495e;
  font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft Yahei', Arial, sans-serif;
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