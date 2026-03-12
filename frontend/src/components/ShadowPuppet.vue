<template>
  <div class="puppet-container">
    <svg viewBox="0 0 200 300" class="puppet-svg">
      <line x1="100" y1="0" x2="100" y2="80" stroke="#ccc" stroke-width="1" stroke-dasharray="4" opacity="0.5" />
      <line x1="70" y1="0" x2="70" y2="130" stroke="#ccc" stroke-width="1" stroke-dasharray="4" opacity="0.5" />

      <g class="body">
        <circle cx="100" cy="80" r="25" fill="#1a1a1a" stroke="#d4af37" stroke-width="2"/>
        <circle cx="110" cy="75" r="3" fill="#d4af37" />
        <path d="M 80 110 L 120 110 L 130 220 L 70 220 Z" fill="#1a1a1a" stroke="#d4af37" stroke-width="2"/>
      </g>

      <g 
        class="arm" 
        :class="{ 'hide-eyes': isHidingEyes }"
      >
        <path d="M 70 110 Q 50 150 40 190 Q 60 190 70 140 Z" fill="#1a1a1a" stroke="#d4af37" stroke-width="2"/>
      </g>
    </svg>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

// 接收外部传来的状态：是否需要遮住眼睛
defineProps({
  isHidingEyes: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
.puppet-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 模拟皮影戏的呼吸感悬浮动画 */
  animation: float 4s ease-in-out infinite;
}

.puppet-svg {
  width: 250px;
  height: 350px;
  filter: drop-shadow(5px 5px 15px rgba(0, 0, 0, 0.9)); /* 皮影的投影效果 */
}

.arm {
  /* 关键：设置旋转中心点在肩膀位置 */
  transform-origin: 70px 110px; 
  /* 动作过渡时间与曲线，模仿戏服袖子的甩动 */
  transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1); 
  transform: rotate(0deg);
}

/* 触发遮眼状态时的 CSS 类 */
.arm.hide-eyes {
  /* 向上旋转 135 度，挡住面部 */
  transform: rotate(135deg); 
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(2deg); }
}
</style>