<template>
  <div class="auth-container" ref="authContainerRef">
    <div class="background-overlay"></div>
    
    <div class="auth-card">
      <div class="seal">光影</div>
      
      <div class="auth-header">
        <h1 class="title">{{ isLogin ? '识得旧友' : '初识雅鉴' }}</h1>
        <p class="subtitle">{{ isLogin ? '输入名帖以进入皮影之境' : '登记名册开启数字化传承之旅' }}</p>
      </div>

      <div class="auth-form">
        <!-- 用户名输入框 + 历史列表 -->
        <div class="input-group" ref="usernameInputWrap">
          <input 
            v-model="form.username" 
            type="text" 
            placeholder="君之名号 (用户名)" 
            required 
            @click.stop="showUsernameHistory = true"
          />
          <!-- 用户名历史列表 -->
          <div 
            v-if="showUsernameHistory && usernameHistory.length" 
            class="history-list"
            @click.stop
          >
            <div 
              class="history-item" 
              v-for="(item, index) in usernameHistory" 
              :key="index"
              @click="fillUsername(item)"
            >
              {{ item }}
            </div>
          </div>
        </div>
        
        <!-- 密码输入框 -->
        <div class="input-group">
          <input v-model="form.password" type="password" placeholder="秘钥 (密码)" required />
        </div>

        <!-- 修复：记住我复选框 - 优化label包裹结构，确保点击文字也能勾选 -->
        <div v-if="isLogin" class="remember-me">
          <label class="remember-label" @click.stop>
            <input type="checkbox" v-model="form.remember" id="rem" />
            <span class="label-text">铭记此缘 (记住我)</span>
          </label>
        </div>

        <transition name="fade">
          <div v-if="!isLogin" class="input-group">
            <div v-if="!isLogin" class="input-group email-flex" ref="emailInputWrap">
              <input 
                v-model="form.email" 
                type="email" 
                placeholder="联络信鸽 (邮箱)" 
                @click.stop="showEmailHistory = true"
              />
              <!-- 邮箱历史列表 -->
              <div 
                v-if="showEmailHistory && emailHistory.length" 
                class="history-list email-history"
                @click.stop
              >
                <div 
                  class="history-item" 
                  v-for="(item, index) in emailHistory" 
                  :key="index"
                  @click="fillEmail(item)"
                >
                  {{ item }}
                </div>
              </div>
              <button @click="handleSendCode" :disabled="timer > 0" class="code-btn">
                {{ timer > 0 ? timer + 's' : '获取验证码' }}
              </button>
            </div>
            <div v-if="!isLogin" class="input-group">
              <input v-model="form.code" type="text" placeholder="六位验证码" />
            </div>
            <input v-model="form.confirmPassword" type="password" placeholder="再书秘钥 (确认密码)" required />
          </div>
        </transition>

        <button class="submit-btn" @click="handleSubmit">
          {{ isLogin ? '开启光影' : '录入名册' }}
        </button>
      </div>

      <div class="auth-footer">
        <span @click="toggleMode">
          {{ isLogin ? '尚未识得君？点击登记' : '已有旧友名号？直接登录' }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { sendCode, userRegister, userLogin } from '@/services/userApi';

const router = useRouter();
const isLogin = ref(true);
const timer = ref(0);
// 新增：历史列表显隐控制
const showUsernameHistory = ref(false);
const showEmailHistory = ref(false);
// 新增：获取容器ref，用于全局点击监听
const authContainerRef = ref(null);
// 新增定时器引用
const timerInterval = ref(null);

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  code: '',
  remember: false
});

// 从localStorage读取历史记录（去重、限制条数）
const getHistory = (key) => {
  const history = localStorage.getItem(key) || '[]';
  const list = JSON.parse(history);
  // 去重 + 最多保留5条
  return Array.from(new Set(list)).slice(0, 5);
};

// 计算属性 - 用户名/邮箱历史列表
const usernameHistory = computed(() => getHistory('usernameHistory'));
const emailHistory = computed(() => getHistory('emailHistory'));

// 保存历史记录到localStorage
const saveHistory = (key, value) => {
  if (!value) return; // 空值不保存
  const history = getHistory(key);
  // 把最新值放到最前面
  history.unshift(value);
  localStorage.setItem(key, JSON.stringify(history));
};

// 填充用户名到输入框
const fillUsername = (username) => {
  form.username = username;
  showUsernameHistory.value = false; // 填充后关闭列表
};

// 填充邮箱到输入框
const fillEmail = (email) => {
  form.email = email;
  showEmailHistory.value = false; // 填充后关闭列表
};

// 初始化读取记住的用户信息
const initForm = () => {
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    const user = JSON.parse(savedUser);
    form.username = user.username || '';
    form.remember = true;
    // 初始化时保存用户名到历史（避免首次无记录）
    if (user.username) saveHistory('usernameHistory', user.username);
  }
};

// 发送验证码
const handleSendCode = async () => {
  if (!form.email) return alert("请先填写信鸽地址（邮箱）");
  if (timer.value > 0) return;
  try {
    const res = await sendCode(form.email);
    if (res.code === 200) {
      saveHistory('emailHistory', form.email);
      timer.value = 60;
      // 清除旧定时器
      if (timerInterval.value) clearInterval(timerInterval.value);
      timerInterval.value = setInterval(() => {
        timer.value--;
        if (timer.value <= 0) {
          clearInterval(timerInterval.value);
          timerInterval.value = null;
        }
      }, 1000);
    }
  } catch (e) { /* ... */ }
};

// 卸载时清除定时器
onUnmounted(() => {
  document.removeEventListener('click', handleGlobalClick);
  if (timerInterval.value) clearInterval(timerInterval.value);
});


// 切换登录/注册模式
const toggleMode = () => {
  isLogin.value = !isLogin.value;
  Object.keys(form).forEach(key => form[key] = '');
  timer.value = 0;
  // 切换时关闭历史列表
  showUsernameHistory.value = false;
  showEmailHistory.value = false;
};

// 提交登录/注册
const handleSubmit = async () => {
  // 登录逻辑
  if (isLogin.value) {
    if (!form.username || !form.password) {
      return alert("请填写完整的名号和秘钥");
    }
    try {
      const loginParams = {
        username: form.username,
        password: form.password,
        remember: form.remember
      };
      const res = await userLogin(loginParams);
      
      if (res.code === 200) {
        // 修复：无论是否勾选记住我，都保存用户信息（仅存储位置不同），并强制跳转
        saveHistory('usernameHistory', form.username);
        // 根据remember选择存储方式
        const storage = form.remember ? localStorage : sessionStorage;
        storage.setItem('user', JSON.stringify(res.user));
        if (res.token) {
          storage.setItem('token', res.token);
        }
        // 强制跳转个人中心，不依赖remember状态
        await router.push('/user-center');
      } else {
        // 接口返回非200时提示错误
        alert(res.msg || '登录失败，请检查账号密码');
      }
    } catch (e) {
      console.log("登录失败：", e);
      alert('登录请求异常，请稍后重试');
    }
    return;
  }

  // 注册逻辑
  if (!form.username || !form.password || !form.email || !form.code) {
    return alert("请填写完整的注册信息");
  }
  if (form.password.length < 6) {
    return alert("秘钥长度不能少于6位");
  }
  if (form.password !== form.confirmPassword) {
    return alert("两次输入的秘钥不一致");
  }
  const registerData = {
    username: form.username,
    password: form.password,
    email: form.email,
    code: form.code
  };
  try {
    const res = await userRegister(registerData);
    if (res.code === 200) {
      // 注册成功时保存用户名、邮箱历史
      saveHistory('usernameHistory', form.username);
      saveHistory('emailHistory', form.email);
      toggleMode();
    } else {
      alert(res.msg || '注册失败，请检查信息');
    }
  } catch (e) {
    console.log("注册失败：", e);
    alert('注册请求异常，请稍后重试');
  }
};

// 新增：全局点击隐藏历史列表
const handleGlobalClick = () => {
  showUsernameHistory.value = false;
  showEmailHistory.value = false;
};

// 挂载时添加全局点击监听，卸载时移除（防止内存泄漏）
onMounted(() => {
  initForm();
  document.addEventListener('click', handleGlobalClick);
});
onUnmounted(() => {
  document.removeEventListener('click', handleGlobalClick);
});
</script>

<style scoped>
/* 原有样式全部保留 */
.auth-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #1a1a1a url('../asset/img/opacity-b25.png');
  position: relative;
  overflow: hidden;
}
.auth-card {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
  position: relative;
  text-align: center;
}
.title {
  font-family: 'Ma Shan Zheng', cursive;
  color: #d4af37;
  font-size: 2.5rem;
  margin-bottom: 10px;
}
.subtitle {
  font-family: 'Noto Serif SC', serif;
  color: #ccc;
  font-size: 0.9rem;
  margin-bottom: 30px;
}
.input-group input {
  width: 100%;
  padding: 12px;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-bottom: 1px solid #666;
  color: #fff;
  outline: none;
  transition: border-color 0.3s;
}
.input-group input:focus {
  border-bottom: 1px solid #d4af37;
}
.submit-btn {
  width: 100%;
  padding: 15px;
  background: #b30000;
  color: #fff;
  border: none;
  font-family: 'Noto Serif SC', serif;
  font-weight: bold;
  letter-spacing: 4px;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 20px;
}
.submit-btn:hover {
  background: #8e0000;
  box-shadow: 0 0 15px rgba(179, 0, 0, 0.4);
}
.auth-footer {
  margin-top: 25px;
  color: #999;
  font-size: 0.85rem;
  cursor: pointer;
}
.auth-footer span:hover {
  color: #d4af37;
}
.seal {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border: 2px solid #b30000;
  color: #b30000;
  font-weight: bold;
  padding: 2px;
  line-height: 16px;
  font-size: 14px;
  transform: rotate(15deg);
  opacity: 0.7;
}
.email-flex {
  display: flex;
  gap: 10px;
  position: relative;
}
.code-btn {
  width: 140px;
  height: 42px;
  background: rgba(212, 175, 55, 0.2);
  border: 1px solid #d4af37;
  color: #d4af37;
  cursor: pointer;
  flex-shrink: 0;
}
.code-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
/* 修复：记住我样式 - 优化点击区域和交互 */
.remember-me {
  text-align: left;
  margin-top: -10px;
  margin-bottom: 20px;
  color: #999;
  font-size: 0.8rem;
}
.remember-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}
.remember-label input {
  margin-right: 8px;
  /* 修复复选框样式继承问题 */
  width: auto;
  padding: 0;
  margin-bottom: 0;
  background: none;
  border: none;
}
.label-text:hover {
  color: #d4af37;
  transition: color 0.3s;
}
/* 历史列表样式优化 */
.input-group {
  position: relative;
}
.history-list {
  position: absolute;
  z-index: 10;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid #d4af37;
  border-radius: 4px;
  top: calc(100% - 20px);
  left: 0;
}
/* 邮箱历史列表特殊定位（适配flex布局） */
.email-history {
  width: calc(100% - 150px);
  left: 0;
}
.history-item {
  padding: 8px 12px;
  color: #fff;
  cursor: pointer;
  text-align: left;
}
.history-item:hover {
  background: #d4af37;
  color: #000;
}
/* 滚动条样式优化（可选） */
.history-list::-webkit-scrollbar {
  width: 6px;
}
.history-list::-webkit-scrollbar-thumb {
  background: #d4af37;
  border-radius: 3px;
}
</style>