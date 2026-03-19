<template>
  <div class="user-center-container">
    <div class="content-layout">
      <aside class="sidebar">
        <div class="back-home-wrapper">
          <button class="back-home-btn" @click="goHome">
            <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            返回首页
          </button>
        </div>

        <nav class="nav-list">
          <div class="nav-item" :class="{ active: activeTab === 'profile' }" @click="activeTab = 'profile'">我的名帖</div>
          <div class="nav-item" :class="{ active: activeTab === 'collection' }">传世收藏</div>
          <div class="nav-item" :class="{ active: activeTab === 'footprint' }">光影足迹</div>
          <div class="nav-item" :class="{ active: activeTab === 'apiUsage' }" @click="activeTab = 'apiUsage'">API用量监控</div>
        </nav>
        
        <div class="logout-wrapper">
          <div class="nav-item logout" @click="handleLogout">退出登录</div>
        </div>
      </aside>

      <main class="main-content">
        <div v-if="activeTab === 'profile'" class="fade-in">
          <section class="profile-header">
            <div class="avatar-clickable" @click="triggerUpload">
              <img v-if="user.avatar" :src="user.avatar" class="avatar-img" alt="用户头像" />
              <div v-else class="avatar-placeholder">{{ user.username?.charAt(0) || '访' }}</div>
              <div class="upload-overlay">
                <span>更换头像</span>
              </div>
            </div>

            <div class="user-info">
              <h2 class="user-name">{{ user.username || '神秘访客' }} <span class="badge">传承者</span></h2>
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
              <input v-model="user.username" type="text" readonly class="input-readonly" />
            </div>
            <div class="form-row">
              <label>门派 (职业)</label>
              <input type="text" placeholder="如：全栈画师" class="input-field" />
            </div>
            <div class="form-row">
              <label>联络信鸽 (邮箱)</label>
              <input type="email" placeholder="email@example.com" class="input-field" />
            </div>
            <div class="form-actions">
              <button class="primary-btn">保存更改</button>
            </div>
          </section>
        </div>

        <div v-if="activeTab === 'apiUsage'" class="fade-in">
          <section class="profile-header">
            <h2 class="user-name">API用量监控 <span class="badge blue">Token统计</span></h2>
          </section>

          <section class="stats-grid api-stats">
            <div class="stat-box">
              <span class="label">今日使用Token</span>
              <span class="value text-blue">{{ apiUsage.todayToken }}</span>
            </div>
            <div class="stat-box">
              <span class="label">本周使用Token</span>
              <span class="value text-blue">{{ apiUsage.weekToken }}</span>
            </div>
            <div class="stat-box">
              <span class="label">本月使用Token</span>
              <span class="value text-blue">{{ apiUsage.monthToken }}</span>
            </div>
          </section>

          <section class="api-chart">
            <h3 class="section-title">近7天Token使用趋势</h3>
            <div class="chart-container">
              <div class="chart-bar" v-for="(item, index) in apiTrend" :key="index">
                <div class="bar" :style="{ height: getBarHeight(item) }"></div>
                <div class="chart-label">{{ item.date }}</div>
              </div>
            </div>
          </section>

          <section class="api-detail">
            <h3 class="section-title">各模型使用明细</h3>
            <div class="table-responsive">
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
            </div>
          </section>

          <section class="api-alert">
            <h3 class="section-title">用量预警设置</h3>
            <div class="form-row">
              <label>月用量预警阈值 (Token)</label>
              <input v-model="alertThreshold" type="number" placeholder="设置阈值，超过则提醒" class="input-field" />
            </div>
            <div class="form-actions">
              <button class="primary-btn" @click="saveAlertThreshold">保存预警设置</button>
            </div>
          </section>
        </div>
      </main>
    </div>

    <div v-if="showAvatarModal" class="avatar-modal-overlay" @click.self="closeAvatarModal">
      <div class="avatar-modal fade-in">
        <div class="modal-header">
          <button class="close-btn" @click="closeAvatarModal">×</button>
          <h4 class="modal-title">修改头像</h4>
        </div>
        <div class="modal-content-inner">
          <div class="large-avatar-wrapper">
            <img v-if="user.avatar" :src="user.avatar" class="large-avatar-img" alt="放大头像" />
            <div v-else class="large-avatar-placeholder">{{ user.username?.charAt(0) || '访' }}</div>
            <div v-if="isUploading" class="uploading-loader">
              <div class="spinner"></div>
              <span>上传中...</span>
            </div>
          </div>
          <p class="modal-subtext">请选择新的头像文件</p>
          <div class="upload-options">
            <div class="option-item" @click="openFileInput">
              <div class="option-icon">
                <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <circle cx="8.5" cy="8.5" r="1.5"></circle>
                  <polyline points="21 15 16 10 5 21"></polyline>
                </svg>
              </div>
              <span>修改图片 (从设备上传)</span>
            </div>
            <div class="option-item">
              <div class="option-icon">
                <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
              </div>
              <span>使用插图</span>
            </div>
          </div>
          <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" hidden />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import { uploadAvatar } from '../../services/userApi.js';


const router = useRouter();
const user = ref({
  id: '', 
  username: '',
  avatar: '' 
});
const activeTab = ref('profile');

const goHome = () => {
  router.push('/');
};

// --- 头像上传与弹窗逻辑 ---
const showAvatarModal = ref(false);
const isUploading = ref(false);
const fileInput = ref(null);

const triggerUpload = () => {
  if (isUploading.value) return; 
  showAvatarModal.value = true;
};

const closeAvatarModal = () => {
  showAvatarModal.value = false;
};

const openFileInput = () => {
  fileInput.value.click();
};

//  简化 updateUserStorageAvatar，只更新当前会话即可（删掉模拟DB）
const updateUserStorageAvatar = (newAvatar) => {
  const storageArea = localStorage.getItem('user') ? localStorage : sessionStorage;
  const savedStr = storageArea.getItem('user');
  
  if (savedStr) {
    const savedUser = JSON.parse(savedStr);
    savedUser.avatar = newAvatar;
    storageArea.setItem('user', JSON.stringify(savedUser));
  }
};

//  修改 handleFileUpload 方法
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 本地预览（让用户先看到图片变了）
  const reader = new FileReader();
  reader.onload = (e) => {
    user.value.avatar = e.target.result; 
  };
  reader.readAsDataURL(file);

  // 构造发给后端的 FormData
  const formData = new FormData();
  formData.append('avatar', file); 
  // 👇 核心：把当前的用户名传给后端，后端就知道是哪个用户要换头像了
  formData.append('username', user.value.username); 

  isUploading.value = true;
  
  try {
    // 调用我们刚才在 userApi.js 里写的方法
    const response = await uploadAvatar(formData);

    if (response.code === 200) { 
      // 成功！把后端返回的真实图片 URL 赋给前端
      if (response.data && response.data.avatarUrl) {
        user.value.avatar = response.data.avatarUrl;
        updateUserStorageAvatar(user.value.avatar);
      }
      closeAvatarModal(); 
    } else {
      throw new Error(response.msg || '上传失败');
    }
  } catch (error) {
    console.error('头像上传报错:', error);
    alert('头像上传失败，请检查网络或后端服务');
    closeAvatarModal();
  } finally {
    isUploading.value = false;
    if (fileInput.value) {
      fileInput.value.value = ''; 
    }
  }
};

const apiUsage = ref({ todayToken: 0, weekToken: 0, monthToken: 0 });

const apiTrend = ref([
  { date: '7天前', value: 0 }, { date: '6天前', value: 0 },
  { date: '5天前', value: 0 }, { date: '4天前', value: 0 },
  { date: '3天前', value: 0 }, { date: '2天前', value: 0 },
  { date: '昨日', value: 0 }, { date: '今日', value: 0 }
]);

const maxTrendValue = computed(() => {
  const values = apiTrend.value.map(item => item.value);
  return Math.max(...values, 1);
});

const getBarHeight = (item) => {
  return `${(item.value / maxTrendValue.value) * 100}%`;
};

const modelDetail = ref([]);
const alertThreshold = ref(10000);

//  修改 onMounted 钩子（删掉那些去本地找头像的代码）
onMounted(() => {
  const savedUser = localStorage.getItem('user') || sessionStorage.getItem('user');
  if (savedUser) {
    // 因为后端登录接口现在会返回 avatar 了，直接合并即可！
    user.value = { ...user.value, ...JSON.parse(savedUser) };

    loadApiUsageData();
    const savedThreshold = localStorage.getItem('api_alert_threshold');
    if (savedThreshold) alertThreshold.value = Number(savedThreshold);
  } else {
    router.push('/login');
  }
});

const loadApiUsageData = () => {
  apiUsage.value = { todayToken: 1258, weekToken: 8965, monthToken: 35872 };
  apiTrend.value = [
    { date: '7天前', value: 980 }, { date: '6天前', value: 1250 },
    { date: '5天前', value: 870 }, { date: '4天前', value: 1560 },
    { date: '3天前', value: 920 }, { date: '2天前', value: 1890 },
    { date: '昨日', value: 1495 }, { date: '今日', value: 1258 }
  ];
  modelDetail.value = [
    { name: 'GPT-3.5 Turbo', callCount: 42, tokenUsed: 28950, averageToken: 689, lastCallTime: '2024-05-20 14:35:22' },
    { name: 'GPT-4', callCount: 8, tokenUsed: 6922, averageToken: 865, lastCallTime: '2024-05-20 10:12:45' }
  ];
};

const saveAlertThreshold = () => {
  localStorage.setItem('api_alert_threshold', alertThreshold.value);
  alert('预警阈值保存成功！');
};

const handleLogout = () => {
  // 清空所有本地验证数据，代表退出登录
  localStorage.removeItem('user');
  sessionStorage.removeItem('user');
  localStorage.removeItem('token');
  sessionStorage.removeItem('token');
  
  router.push('/');
};
</script>

<style scoped>
/* 简洁白 Modern Minimalist 风格 */
.user-center-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  box-sizing: border-box;
}

.user-center-container * {
  box-sizing: border-box;
}

.content-layout {
  display: flex;
  gap: 24px;
  max-width: 1200px;
  width: 100%;
}

.sidebar {
  width: 240px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  height: fit-content;
  overflow: hidden;
}

.back-home-wrapper {
  padding: 20px 20px 10px;
  border-bottom: 1px solid #ebeef5;
}

.back-home-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: none;
  border: 1px solid #dcdfe6;
  color: #606266;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s;
  width: 100%;
}

.back-home-btn:hover {
  background: #ecf5ff;
  color: #409EFF;
  border-color: #c6e2ff;
}

.nav-list {
  padding: 16px 0;
  flex: 1;
}

.nav-item {
  padding: 14px 24px;
  font-size: 0.95rem;
  color: #303133;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: #f5f7fa;
}

.nav-item.active {
  background: #ecf5ff;
  color: #409EFF;
  border-left-color: #409EFF;
  font-weight: 500;
}

.logout-wrapper {
  padding: 16px 0;
  border-top: 1px solid #ebeef5;
}

.nav-item.logout {
  color: #F56C6C;
}
.nav-item.logout:hover {
  background: #fef0f0;
}

.main-content {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 40px;
  min-height: 600px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 32px;
  margin-bottom: 32px;
}

.avatar-clickable {
  position: relative;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 2.5rem;
  color: #909399;
  font-weight: bold;
}

.upload-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-clickable:hover .upload-overlay {
  opacity: 1;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 1.8rem;
  color: #303133;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.badge {
  font-size: 0.8rem;
  background: #e1f3d8;
  color: #67C23A;
  padding: 4px 10px;
  border-radius: 20px;
  vertical-align: middle;
  font-weight: normal;
  margin-left: 8px;
}

.badge.blue {
  background: #ecf5ff;
  color: #409EFF;
}

.user-bio {
  color: #909399;
  font-size: 0.9rem;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.stat-box {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  transition: transform 0.2s;
  border: 1px solid transparent;
}

.stat-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border-color: #c6e2ff;
}

.stat-box .label {
  display: block;
  font-size: 0.85rem;
  color: #606266;
  margin-bottom: 8px;
}

.stat-box .value {
  font-size: 1.8rem;
  color: #303133;
  font-weight: bold;
}
.stat-box .value.text-blue {
  color: #409EFF;
}

.section-title {
  font-size: 1.1rem;
  color: #303133;
  margin-bottom: 20px;
  font-weight: 600;
}

.form-row {
  margin-bottom: 20px;
  max-width: 500px;
}

.form-row label {
  display: block;
  font-size: 0.85rem;
  color: #606266;
  margin-bottom: 6px;
}

.input-field, .input-readonly {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #303133;
  transition: border-color 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #409EFF;
}

.input-readonly {
  background-color: #f5f7fa;
  color: #909399;
  cursor: not-allowed;
}

.form-actions {
  margin-top: 30px;
}

.primary-btn {
  background: #409EFF;
  color: #ffffff;
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background 0.3s;
}

.primary-btn:hover {
  background: #66b1ff;
}

.chart-container {
  display: flex;
  align-items: flex-end;
  gap: 20px;
  height: 220px;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 8px;
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
  width: 60%;
  background: #409EFF;
  border-radius: 4px 4px 0 0;
  transition: height 0.8s ease-out;
}

.chart-bar:hover .bar {
  background: #66b1ff;
}

.chart-label {
  margin-top: 12px;
  font-size: 0.75rem;
  color: #909399;
}

.table-responsive {
  overflow-x: auto;
}

.api-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 40px;
}

.api-table th, .api-table td {
  border-bottom: 1px solid #ebeef5;
  padding: 16px;
  text-align: left;
}

.api-table th {
  background: #f8f9fa;
  color: #606266;
  font-weight: 600;
  font-size: 0.85rem;
}

.api-table td {
  color: #303133;
  font-size: 0.9rem;
}

.api-alert {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #ebeef5;
}

/* 模态框样式 */
.avatar-modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.avatar-modal {
  background: #ffffff;
  border-radius: 12px;
  width: 480px;
  max-width: 100%;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  overflow: hidden;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.8rem;
  color: #909399;
  cursor: pointer;
  line-height: 1;
}

.close-btn:hover {
  color: #F56C6C;
}

.modal-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #303133;
}

.modal-content-inner {
  padding: 30px;
  text-align: center;
}

.large-avatar-wrapper {
  position: relative;
  width: 180px;
  height: 180px;
  margin: 0 auto 20px;
  border-radius: 50%;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.large-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.large-avatar-placeholder {
  font-size: 6rem;
  color: #909399;
  font-weight: bold;
}

.uploading-loader {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #409EFF;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 4px solid rgba(64, 158, 255, 0.3);
  border-top-color: #409EFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.modal-subtext {
  font-size: 0.9rem;
  color: #909399;
  margin-bottom: 24px;
}

.upload-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 8px;
  background: #f8f9fa;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.option-item:hover {
  background: #ecf5ff;
}

.option-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(64, 158, 255, 0.1);
  color: #409EFF;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-item span {
  font-size: 0.9rem;
  color: #303133;
}

.fade-in {
  animation: fadeIn 0.4s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>