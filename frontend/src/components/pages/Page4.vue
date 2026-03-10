<template>
  <section id="make" class="section make">
    <div class="container">
        <h2 class="section-title">探秘皮影制作，邂逅千年匠心</h2>
      <!-- 制作流程主容器 -->
      <div class="make-container">
        <div class="step-name">
          <span>{{ currentStep.name }}</span>
        </div>
        <div class="step-details">
          <div class="step-image-container">
            <img
              :src="currentStep.image"
              :alt="currentStep.name"
              class="step-image"
              @load="onImageLoad"
              @error="onImageError"
            />
          </div>
          <div class="step-description">
            {{ currentStep.description }}
          </div>
        </div>
      </div>
      
      <!-- 时间轴导航 -->
      <div class="timeline">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="timeline-step"
          :class="{ 
            active: index === currentStepIndex,
            completed: index < currentStepIndex
          }"
          @click="goToStep(index)"
          :style="{ '--order': index + 1 }"
        >
          <span class="step-label">{{ step.name }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const currentStepIndex = ref(0)
const imageLoading = ref(false)
const imageError = ref(false)

const steps = reactive([
  {
    name: '选皮',
    image: '/src/asset/img/step_1.png',
    description: '一般选用牛皮、羊皮、驴皮等，比如陇东皮影常选年轻、毛色黑的公牛皮，其厚薄适中，质坚而柔韧，青中透明。优质皮料的选择是制作精美皮影的基础，匠人们通常会亲自挑选，确保皮质均匀、无瑕疵。'
  },
  {
    name: '制皮',
    image: '/src/asset/img/step_2.png',
    description: '将选好的牛皮在洁净凉水里浸泡两、三天，取出用刀刮制，刮去牛毛、肉渣，逐渐刮薄，每刮一次用清水浸泡一次，刮好后撑于木架之上，阴干。这一过程需要极大的耐心和技巧，以确保皮质均匀透亮。'
  },
  {
    name: '画稿',
    image: '/src/asset/img/step_3.png',
    description: '按人物不同身份和个性设计形象，有专门的"样谱"，将创作理念形成初步画面。传统皮影人物造型讲究"五分脸"，即正侧面的形象，这是皮影艺术的独特表现方式。'
  },
  {
    name: '过稿',
    image: '/src/asset/img/step_4.png',
    description: '把刮好的皮分解成块，用湿布潮软，用特制推板加油汁推摩，使皮平展光滑，再用钢针把部件轮廓和图案纹样拷贝、描绘在皮面上。这一步需要精准的手法，以确保图案线条流畅。'
  },
  {
    name: '镂刻',
    image: '/src/asset/img/step_5.png',
    description: '使用宽窄不同的斜口刀、平刀、圆刀等多种刀具，根据不同纹样选择刀具雕刻，如线状纹样用平刀扎，直线条纹样用平刀推。这是最考验匠人功力的环节，一刀失误可能前功尽弃。'
  },
  {
    name: '敷彩',
    image: '/src/asset/img/step_6.png',
    description: '主要使用红、黄、青、绿、黑五种纯色，一般互不调配，通过深浅色区分层次，进行平涂，双面着色，老艺人常自己炮制颜色。传统颜料多来自矿物和植物，色彩鲜艳持久。'
  },
  {
    name: '熨平',
    image: '/src/asset/img/step_7.png',
    description: '目的是使敷彩吃入牛皮内并挥发皮内水分，可用薄木板夹、烙铁烫或土坯砖块搭人字用麦秸烧热压平等方法，过去用"弹指点水"判断温度。这一步骤决定了皮影的平整度和耐久性。'
  },
  {
    name: '缀结',
    image: '/src/asset/img/step_8.png',
    description: '皮影人物通常有头颅、胸、腹等十一个部件，在关节点用牛皮刻成的枢钉或细牛皮条搓成的线缀结合成，再装置三根竹棍作操纵杆。组装后的皮影人物关节灵活，便于表演各种动作。'
  }
])

const currentStep = ref(steps[0])

const goToStep = (index) => {
  currentStepIndex.value = index
  currentStep.value = steps[index]
  imageLoading.value = true
  imageError.value = false
}

const onImageLoad = () => {
  imageLoading.value = false
  imageError.value = false
}

const onImageError = () => {
  imageLoading.value = false
  imageError.value = true
  console.error(`图片加载失败: ${currentStep.value.image}`)
}

onMounted(() => {
  // 初始化第一个步骤
  imageLoading.value = true
})
</script>

<style scoped>
.section{
  padding: 4rem 0;
  background: linear-gradient(135deg, #fffef5 0%, #fffeee 50%, #fffef5 100%);
  min-height: 100vh;
  color: black;
}
.make {
  font-family: "Noto Serif SC", "SimSun", "宋体", serif;
  position: relative;
  overflow: hidden;
}
.container {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* 页面标题样式 */
.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #9E613B; /* 棕色系，与皮影传统色彩相符 */
  text-align: center;
  margin-bottom: 3rem;
  padding: 1rem 0;
  background: linear-gradient(135deg, #9E613B 0%, #D4A76A 50%, #9E613B 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 2px 2px 4px rgba(125, 78, 42, 0.1);
  letter-spacing: 2px;
}

.make-container {
  width: 1100px;
  height: 550px;
  display: flex;
  justify-content: space-between;
  margin-bottom: 3rem;
  background: linear-gradient(145deg, #ffffff, #fffcf8);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 
    0 10px 30px rgba(125, 78, 42, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(201, 168, 124, 0.25);
  position: relative;
}
.make-container:hover {
  transform: translateY(-5px) scale(1.005);
  box-shadow: 
    0 20px 45px rgba(125, 78, 42, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}
.step-name {
  width: 20%;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  background: linear-gradient(135deg, #9E613B, #D4A76A, #9E613B);
  padding: 2.5rem 1.5rem;
  position: relative;
  overflow: hidden;
}
.step-name::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.12), transparent);
  transform: rotate(45deg);
  animation: shimmer 3s infinite linear;
  z-index: 1;
}
@keyframes shimmer {
  0% { transform: rotate(45deg) translateX(-100%); }
  100% { transform: rotate(45deg) translateX(100%); }
}
.step-name span {
  position: relative;
  z-index: 2;
  font-size: 2.4rem;
  font-weight: 700;
  text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.3);
  margin-bottom: 1rem;
  letter-spacing: 2px;
  color: #FFFCF5; 
}
.step-details {
  width: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
}
.step-image-container {
  position: relative;
  width: 480px;
  height: 340px;
  margin-bottom: 2rem;
  perspective: 1200px;
  border-radius: 15px;
  overflow: hidden;
  background: linear-gradient(145deg, #f8f9fa, #e9ecef);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}
.step-image {
  width: 100%;
  height: 100%; 
  border-radius: 10px;
  object-fit: fill; 
  border: 5px solid white;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
  transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-style: preserve-3d;
}
.step-image:hover {
  transform: rotateY(5deg) scale(1.02);
  box-shadow: 5px 10px 30px rgba(0, 0, 0, 0.25);
}
.step-description {
  background: linear-gradient(145deg, #ffffff, #fffcf8);
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  font-size: 1rem;
  line-height: 1.8;
  width: 100%;
  text-align: justify;
  border-left: 6px solid #D4A76A; /* 使用具体颜色值，避免CSS变量 */
  position: relative;
  color: #5C4033; /* 更换为更深一些的棕色，避免重影效果 */
  font-weight: 400;
  text-shadow: none; /* 明确移除文字阴影 */
  text-rendering: optimizeLegibility; /* 优化文字渲染 */
  -webkit-font-smoothing: antialiased; /* 抗锯齿处理 */
  -moz-osx-font-smoothing: grayscale; /* 平滑渲染 */
}
/* 时间轴样式 */
.timeline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 0;
  margin: 3rem 0;
  position: relative;
}

.timeline::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 5%;
  right: 5%;
  height: 4px;
  background: linear-gradient(90deg, 
    #7D4E2A 0%, 
    #C9A87C 50%, 
    #7D4E2A 100%);
  transform: translateY(-50%);
  z-index: 1;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(125, 78, 42, 0.12);
}

.timeline-step {
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 110px;
  padding: 1rem 0;
}

.step-label {
  font-size: 1.3rem;
  font-weight: 600;
  color: #6B4F36; /* 调浅默认文字颜色 */
  transition: all 0.3s ease;
  text-align: center;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(201, 168, 124, 0.2);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
}

.timeline-step.active .step-label {
  color: #7D4E2A;
  background: rgba(201, 168, 124, 0.15);
  font-weight: 700;
  transform: translateY(-3px);
  border-color: #C9A87C;
  box-shadow: 0 6px 20px rgba(125, 78, 42, 0.2);
}

.timeline-step:hover .step-label {
  color: #7D4E2A;
  transform: translateY(-4px);
  background: rgba(201, 168, 124, 0.1);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .step-label {
    font-size: 1.2rem;
    padding: 0.7rem 1.2rem;
  }
}

@media (max-width: 768px) {
  .timeline {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
    padding: 1.5rem 0;
  }
  
  .timeline::before {
    display: none;
  }
  
  .timeline-step {
    min-width: 100px;
    margin: 0.5rem;
  }
  
  .step-label {
    font-size: 1.1rem;
    padding: 0.6rem 1rem;
  }
}

@media (max-width: 480px) {
  .timeline-step {
    min-width: 85px;
  }
  
  .step-label {
    font-size: 1rem;
    padding: 0.5rem 0.8rem;
  }
}
</style>