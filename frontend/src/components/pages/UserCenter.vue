<template>
  <div class="user-center-container">
    <div class="cloud-decoration"></div>

    <div class="content-layout">
      <aside class="side-scroll">
        <div class="scroll-handle top"></div>
        <nav class="nav-list">
          <div class="nav-item active">我的名帖</div>
          <div class="nav-item">传世收藏</div>
          <div class="nav-item">光影足迹</div>
          <div class="nav-item" @click="handleLogout">退出归隐</div>
        </nav>
        <div class="scroll-handle bottom"></div>
      </aside>

      <main class="main-paper">
        <section class="profile-header">
          <div class="avatar-wrapper">
            <div class="ink-circle"></div>
            <div class="avatar-text">{{ user.username?.charAt(0) || '访' }}</div>
          </div>
          <div class="user-info">
            <h2 class="user-name">{{ user.username }} <span class="badge">传承者</span></h2>
            <p class="user-bio">“于方寸之间，传光影千年。”</p>
          </div>
        </section>

        <section class="stats-grid">
          <div class="stat-box">
            <span class="label">入阁天数</span>
            <span class="value">12</span>
          </div>
          <div class="stat-box">
            <span class="label">点亮省份</span>
            <span class="value">5</span>
          </div>
          <div class="stat-box">
            <span class="label">收藏皮影</span>
            <span class="value">28</span>
          </div>
        </section>

        <section class="settings-form">
          <h3 class="section-title">详细资料</h3>
          <div class="form-row">
            <label>名号</label>
            <input v-model="user.username" type="text" readonly />
          </div>
          <div class="form-row">
            <label>门派 (职业)</label>
            <input type="text" placeholder="如：全栈画师" />
          </div>
          <div class="form-row">
            <label>联络信鸽 (邮箱)</label>
            <input type="email" placeholder="email@example.com" />
          </div>
          <button class="save-btn">保存更改</button>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const user = ref({});

onMounted(() => {
  // 从本地加载用户信息
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    user.value = JSON.parse(savedUser);
  } else {
    router.push('/login');
  }
});

const handleLogout = () => {
  localStorage.removeItem('user');
  router.push('/page1'); // 返回首页
};
</script>

<style scoped>
.user-center-container {
  min-height: 100vh;
  background: #121212 url('../asset/img/opacity-b25.png'); /* 复用你的底纹 */
  padding: 80px 20px 40px;
  display: flex;
  justify-content: center;
}

.content-layout {
  display: flex;
  gap: 40px;
  max-width: 1100px;
  width: 100%;
}

/* 侧边卷轴样式 */
.side-scroll {
  width: 200px;
  background: #f4f1ea; /* 宣纸色 */
  border-left: 2px solid #d4af37;
  border-right: 2px solid #d4af37;
  position: relative;
  height: fit-content;
}

.scroll-handle {
  height: 20px;
  background: #8e0000;
  width: 110%;
  margin-left: -5%;
  border-radius: 10px;
}

.nav-list {
  padding: 40px 0;
}

.nav-item {
  padding: 15px 30px;
  font-family: 'Noto Serif SC', serif;
  cursor: pointer;
  transition: all 0.3s;
  color: #333;
}

.nav-item.active, .nav-item:hover {
  background: rgba(179, 0, 0, 0.1);
  color: #b30000;
  padding-left: 40px;
}

/* 主体宣纸区域 */
.main-paper {
  flex: 1;
  background: #f4f1ea;
  box-shadow: 10px 10px 30px rgba(0,0,0,0.5);
  padding: 50px;
  position: relative;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 30px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 30px;
  margin-bottom: 30px;
}

.avatar-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ink-circle {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 4px double #b30000;
  border-radius: 50%;
  animation: rotate 10s linear infinite;
}

.avatar-text {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 3rem;
  color: #333;
}

.user-name {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 2.2rem;
  color: #1a1a1a;
}

.badge {
  font-size: 0.9rem;
  background: #b30000;
  color: #fff;
  padding: 2px 8px;
  font-family: 'Noto Serif SC', serif;
  vertical-align: middle;
}

/* 统计数据 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.stat-box {
  border: 1px solid #d4af37;
  padding: 20px;
  text-align: center;
}

.stat-box .label {
  display: block;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 5px;
}

.stat-box .value {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 1.8rem;
  color: #b30000;
}

/* 表单样式 */
.section-title {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #8e0000;
}

.form-row {
  margin-bottom: 20px;
}

.form-row label {
  display: block;
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 5px;
}

.form-row input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  background: transparent;
  font-family: 'Noto Serif SC', serif;
}

.save-btn {
  background: #1a1a1a;
  color: #f4f1ea;
  padding: 12px 30px;
  border: none;
  cursor: pointer;
  float: right;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>