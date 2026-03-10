<template>
  <div class="page-indicator">
    <div 
      v-for="index in totalPages" 
      :key="index"
      class="indicator-dot"
      :class="{ active: index - 1 === currentPage }"
      @click="$emit('indicator-click', index - 1)"
    ></div>
  </div>
</template>

<script>
export default {
  name: 'PageIndicator',
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    }
  },
  emits: ['indicator-click']
}
</script>

<style scoped>
.page-indicator {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
}

.indicator-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  margin: 10px 0;
  cursor: pointer;
  transition: all 0.3s;
}

.indicator-dot.active {
  background-color: white;
  transform: scale(1.2);
}
</style>