<template>
  <div class="user-center-container">
    <div class="cloud-decoration"></div>

    <div class="content-layout">
      <aside class="side-scroll">
        <div class="scroll-handle top"></div>
        <nav class="nav-list">
          <div class="nav-item" :class="{ active: activeTab === 'profile' }" @click="activeTab = 'profile'">我的名帖</div>
          <div class="nav-item" :class="{ active: activeTab === 'collection' }">传世收藏</div>
          <div class="nav-item" :class="{ active: activeTab === 'footprint' }">光影足迹</div>
          <!-- 新增API用量导航项 -->
          <div class="nav-item" :class="{ active: activeTab === 'apiUsage' }" @click="activeTab = 'apiUsage'">API用量监控</div>
          <div class="nav-item" @click="handleLogout">退出归隐</div>
        </nav>
        <div class="scroll-handle bottom"></div>
      </aside>

      <main class="main-paper">
        <!-- 原有个人资料面板 -->
        <div v-if="activeTab === 'profile'">
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
        </div>

        <!-- 新增API用量监控面板 -->
        <div v-if="activeTab === 'apiUsage'">
          <section class="profile-header">
            <h2 class="user-name">API用量监控 <span class="badge">Token统计</span></h2>
          </section>

          <!-- 用量概览 -->
          <section class="stats-grid api-stats">
            <div class="stat-box">
              <span class="label">今日使用Token</span>
              <span class="value">{{ apiUsage.todayToken }}</span>
            </div>
            <div class="stat-box">
              <span class="label">本周使用Token</span>
              <span class="value">{{ apiUsage.weekToken }}</span>
            </div>
            <div class="stat-box">
              <span class="label">本月使用Token</span>
              <span class="value">{{ apiUsage.monthToken }}</span>
            </div>
          </section>

          <!-- 用量趋势图表 -->
          <section class="api-chart">
            <h3 class="section-title">近7天Token使用趋势</h3>
            <div class="chart-container">
              <div class="chart-bar" v-for="(item, index) in apiTrend" :key="index">
                <div class="bar" :style="{ height: `${(item.value / maxTrendValue) * 100}%`, background: '#b30000' }"></div>
                <div class="chart-label">{{ item.date }}</div>
              </div>
            </div>
          </section>

          <!-- 模型明细 -->
          <section class="api-detail">
            <h3 class="section-title">各模型使用明细</h3>
            <table class="api-table">
              <thead>
                <tr>
                  <th>模型名称</th>
                  <th>调用次数</th>
                  <th>消耗Token</th>
                  <th>平均Token/次</th>
                  <th>最后调用时间</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(model, index) in modelDetail" :key="index">
                  <td>{{ model.name }}</td>
                  <td>{{ model.callCount }}</td>
                  <td>{{ model.tokenUsed }}</td>
                  <td>{{ model.averageToken }}</td>
                  <td>{{ model.lastCallTime }}</td>
                </tr>
              </tbody>
            </table>
          </section>

          <!-- 用量预警设置 -->
          <section class="api-alert">
            <h3 class="section-title">用量预警设置</h3>
            <div class="form-row">
              <label>月用量预警阈值 (Token)</label>
              <input v-model="alertThreshold" type="number" placeholder="设置阈值，超过则提醒" />
            </div>
            <button class="save-btn" @click="saveAlertThreshold">保存预警设置</button>
          </section>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const user = ref({});
// 新增标签页控制
const activeTab = ref('profile');

// 模拟API用量数据（实际项目中替换为真实接口请求）
const apiUsage = ref({
  todayToken: 0,
  weekToken: 0,
  monthToken: 0
});

// 近7天使用趋势
const apiTrend = ref([
  { date: '7天前', value: 0 },
  { date: '6天前', value: 0 },
  { date: '5天前', value: 0 },
  { date: '4天前', value: 0 },
  { date: '3天前', value: 0 },
  { date: '2天前', value: 0 },
  { date: '昨日', value: 0 },
  { date: '今日', value: 0 }
]);

// 最大趋势值（用于图表高度计算）
const maxTrendValue = computed(() => {
  const values = apiTrend.value.map(item => item.value);
  return Math.max(...values, 1); // 避免除以0
});

// 模型使用明细
const modelDetail = ref([
  { name: 'GPT-3.5 Turbo', callCount: 0, tokenUsed: 0, averageToken: 0, lastCallTime: '无' },
  { name: 'GPT-4', callCount: 0, tokenUsed: 0, averageToken: 0, lastCallTime: '无' },
  { name: '文心一言', callCount: 0, tokenUsed: 0, averageToken: 0, lastCallTime: '无' },
  { name: '通义千问', callCount: 0, tokenUsed: 0, averageToken: 0, lastCallTime: '无' }
]);

// 预警阈值
const alertThreshold = ref(10000);

onMounted(() => {
  // 读取用户信息
  const savedUser = localStorage.getItem('user') || sessionStorage.getItem('user');
  if (savedUser) {
    user.value = JSON.parse(savedUser);
    // 加载API用量数据（实际项目中替换为真实接口）
    loadApiUsageData();
    // 加载预警阈值
    const savedThreshold = localStorage.getItem('api_alert_threshold');
    if (savedThreshold) alertThreshold.value = Number(savedThreshold);
  } else {
    router.push('/login');
  }
});

// 加载API用量数据（核心：对接真实接口）
const loadApiUsageData = () => {
  // **************************
  // 实际项目中替换为你的后端接口
  // 示例：
  // fetch('/api/v1/user/api-usage', {
  //   headers: {
  //     'Authorization': `Bearer ${localStorage.getItem('token')}`
  //   }
  // })
  // .then(res => res.json())
  // .then(data => {
  //   apiUsage.value = data.summary;
  //   apiTrend.value = data.trend;
  //   modelDetail.value = data.modelDetail;
  // })
  // **************************

  // 模拟数据（测试用，实际删除）
  apiUsage.value = {
    todayToken: 1258,
    weekToken: 8965,
    monthToken: 35872
  };
  apiTrend.value = [
    { date: '7天前', value: 980 },
    { date: '6天前', value: 1250 },
    { date: '5天前', value: 870 },
    { date: '4天前', value: 1560 },
    { date: '3天前', value: 920 },
    { date: '2天前', value: 1890 },
    { date: '昨日', value: 1495 },
    { date: '今日', value: 1258 }
  ];
  modelDetail.value = [
    { name: 'GPT-3.5 Turbo', callCount: 42, tokenUsed: 28950, averageToken: 689, lastCallTime: '2024-05-20 14:35:22' },
    { name: 'GPT-4', callCount: 8, tokenUsed: 6922, averageToken: 865, lastCallTime: '2024-05-20 10:12:45' },
    { name: '文心一言', callCount: 15, tokenUsed: 1250, averageToken: 83, lastCallTime: '2024-05-19 18:45:11' },
    { name: '通义千问', callCount: 9, tokenUsed: 750, averageToken: 83, lastCallTime: '2024-05-19 16:22:33' }
  ];
};

// 保存预警阈值
const saveAlertThreshold = () => {
  localStorage.setItem('api_alert_threshold', alertThreshold.value);
  alert('预警阈值保存成功！');
};

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('user');
  sessionStorage.removeItem('user');
  localStorage.removeItem('token');
  sessionStorage.removeItem('token');
  router.push('/login');
};
</script>

<style scoped>
.user-center-container {
  min-height: 100vh;
  background: #121212 url('../asset/img/opacity-b25.png');
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
  background: #f4f1ea;
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

/* 新增API用量样式 */
.api-stats {
  margin-top: 20px;
}

.chart-container {
  display: flex;
  align-items: flex-end;
  gap: 15px;
  height: 200px;
  padding: 20px;
  border: 1px solid #ddd;
  margin-bottom: 40px;
}

.chart-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
}

.bar {
  width: 80%;
  border-radius: 5px 5px 0 0;
  transition: height 0.5s ease;
}

.chart-label {
  margin-top: 10px;
  font-size: 0.8rem;
  color: #666;
}

.api-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 40px;
}

.api-table th, .api-table td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

.api-table th {
  background: rgba(179, 0, 0, 0.1);
  color: #8e0000;
  font-family: 'Noto Serif SC', serif;
}

.api-table td {
  color: #333;
}

.api-alert {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #ddd;
}
</style>