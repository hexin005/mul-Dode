<template>
  <button class="home-btn" title="返回首页" @click="$emit('home-click')">
    ↑
  </button>
</template>

<script>
export default {
  name: 'HomeButton',
  emits: ['home-click']
}
</script>

<style scoped>
.home-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 24px;
  cursor: pointer;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  backdrop-filter: blur(5px);
}

.home-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}
</style>