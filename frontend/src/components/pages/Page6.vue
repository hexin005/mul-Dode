<template>
  <div class="page-content">
    <h1 class="page-title">传统体育</h1>
    <p class="page-desc">传统体育是各民族在长期历史发展中形成的体育活动，既强身健体，又蕴含丰富的文化内涵。</p>
  </div>
</template>

<script>
export default {
  name: 'Page6'
}
</script>

<style scoped>
.page-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding-top: 60px;
  background: linear-gradient(135deg, #1e88e5, #0d47a1);
}

.page-title {
  font-size: 3rem;
  margin-bottom: 20px;
  text-align: center;
}

.page-desc {
  font-size: 1.2rem;
  max-width: 600px;
  line-height: 1.6;
  margin: 0 auto;
  opacity: 0.9;
}
</style>