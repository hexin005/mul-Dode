<template>
  <div class="auth-container" @click="handleGlobalClick">
    <div class="stage-panel">
      <div class="stage-overlay"></div>
      
      <div class="lottie-wrapper" ref="lottieContainer"></div>

      <div class="stage-text">
        <h2>光影流传</h2>
        <p>方寸戏台上，指尖舞乾坤</p>
      </div>
    </div>

    <div class="form-panel">
      <div class="auth-card">
        <div class="seal">雅鉴</div>
        
        <div class="auth-header">
          <h1 class="title">{{ isLogin ? '识得旧友' : '初识雅鉴' }}</h1>
          <p class="subtitle">{{ isLogin ? '输入名帖，重返皮影之境' : '登记名册，开启传承之旅' }}</p>
        </div>

        <div class="auth-form">
          <div class="input-group">
            <label>君之名号</label>
            <input 
              v-model="form.username" 
              type="text" 
              placeholder="请输入用户名" 
              required 
              @click.stop="showUsernameHistory = true"
            />
            <div v-if="showUsernameHistory && usernameHistory.length" class="history-list">
              <div 
                class="history-item" 
                v-for="(item, index) in usernameHistory" 
                :key="index"
                @click.stop="fillUsername(item)"
              >
                {{ item }}
              </div>
            </div>
          </div>
          
          <div class="input-group">
            <label>通关秘钥</label>
            <input 
              v-model="form.password" 
              type="password" 
              placeholder="请输入密码" 
              required 
              @focus="isPasswordFocused = true"
              @blur="isPasswordFocused = false"
            />
          </div>

          <div v-if="isLogin" class="remember-me">
            <label class="remember-label">
              <input type="checkbox" v-model="form.remember" />
              <span class="label-text">铭记此缘 (保持登录状态)</span>
            </label>
          </div>

          <transition name="fade">
            <div v-if="!isLogin" class="register-fields">
              <div class="input-group">
                <label>联络信鸽</label>
                <div class="email-flex">
                  <input 
                    v-model="form.email" 
                    type="email" 
                    placeholder="请输入邮箱" 
                    @click.stop="showEmailHistory = true"
                  />
                  <button @click.prevent="handleSendCode" :disabled="timer > 0" class="code-btn">
                    {{ timer > 0 ? timer + 's' : '获取验证码' }}
                  </button>
                </div>
                <div v-if="showEmailHistory && emailHistory.length" class="history-list">
                  <div 
                    class="history-item" 
                    v-for="(item, index) in emailHistory" 
                    :key="index"
                    @click.stop="fillEmail(item)"
                  >
                    {{ item }}
                  </div>
                </div>
              </div>

              <div class="input-group">
                <label>飞鸽传书</label>
                <input v-model="form.code" type="text" placeholder="六位验证码" />
              </div>

              <div class="input-group">
                <label>再书秘钥</label>
                <input 
                  v-model="form.confirmPassword" 
                  type="password" 
                  placeholder="确认密码" 
                  required 
                  @focus="isPasswordFocused = true"
                  @blur="isPasswordFocused = false"
                />
              </div>
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
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { sendCode, userRegister, userLogin } from '@/services/userApi';
import lottie from 'lottie-web';
// 引入下载的 JSON 文件 (根据你的目录结构，向上退两级回到 src/asset)
import animationData from '@/asset/puppet-anim.json';

const router = useRouter();
const isLogin = ref(true);
const timer = ref(0);
const showUsernameHistory = ref(false);
const showEmailHistory = ref(false);
const timerInterval = ref(null);

// === 核心状态：是否正在输入密码 ===
const isPasswordFocused = ref(false);

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  code: '',
  remember: false
});

// === Lottie 动画控制逻辑 ===
const lottieContainer = ref(null);
let animInstance = null;

onMounted(() => {
  initForm();
  
  // 初始化 Lottie
  animInstance = lottie.loadAnimation({
    container: lottieContainer.value, 
    renderer: 'svg',                  
    loop: true,                       
    autoplay: true,                   
    animationData: animationData      
  });
});

onUnmounted(() => {
  if (timerInterval.value) clearInterval(timerInterval.value);
  // 销毁 Lottie 实例，防止内存泄漏
  if (animInstance) {
    animInstance.destroy();
  }
});

// 聚焦密码框时的行为
const playHideEyes = () => {
  if (!animInstance) return;
  try {
    // 尝试播放特定帧片段。如果这个动画没有遮眼动作，建议把这行改成 animInstance.pause(); (即输入密码时暂停动画)
    // animInstance.playSegments([60, 90], true); 
    
    // 如果想要更稳妥的做法（在不确定具体帧数的情况下），可以加快播放速度来给予反馈
    animInstance.setSpeed(2); 
  } catch (e) {
    console.warn("Lottie 帧控制调整失败", e);
  }
};

// 离开密码框时的行为
const resetAnim = () => {
  if (!animInstance) return;
  try {
    // 恢复正常速度和播放
    animInstance.setSpeed(1);
    animInstance.play();
  } catch (e) {}
};


// === 原有的业务逻辑 ===
const getHistory = (key) => {
  const history = localStorage.getItem(key) || '[]';
  const list = JSON.parse(history);
  return Array.from(new Set(list)).slice(0, 5);
};
const usernameHistory = computed(() => getHistory('usernameHistory'));
const emailHistory = computed(() => getHistory('emailHistory'));
const saveHistory = (key, value) => {
  if (!value) return;
  const history = getHistory(key);
  history.unshift(value);
  localStorage.setItem(key, JSON.stringify(history));
};
const fillUsername = (username) => {
  form.username = username;
  showUsernameHistory.value = false;
};
const fillEmail = (email) => {
  form.email = email;
  showEmailHistory.value = false;
};
const initForm = () => {
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    const user = JSON.parse(savedUser);
    form.username = user.username || '';
    form.remember = true;
    if (user.username) saveHistory('usernameHistory', user.username);
  }
};
const handleSendCode = async () => {
  // 1. 基础前端校验
  if (!form.email) return alert("请先填写信鸽地址（邮箱）");
  const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailReg.test(form.email)) return alert("邮箱格式不正确");
  
  if (timer.value > 0) return;

  try {
    // 2. 发起请求 (参数传递正确，无需修改)
    const res = await sendCode(form.email); 

    // 3. 处理业务逻辑成功 (假设你的后端成功时返回 code: 200)
    if (res.code === 200) {
      alert("验证码已飞鸽传书，请查收");
      
      saveHistory('emailHistory', form.email); // 成功后再保存名册
      
      timer.value = 60;
      if (timerInterval.value) clearInterval(timerInterval.value);
      
      timerInterval.value = setInterval(() => {
        timer.value--;
        if (timer.value <= 0) {
          clearInterval(timerInterval.value);
          timerInterval.value = null;
        }
      }, 1000);
    } else {
      // 处理后端返回了 200 HTTP 状态码，但业务逻辑失败的情况（例如：邮箱已被注册）
      alert(res.msg || "发送失败，请检查邮箱状态");
    }
  } catch (e) {
    // 4. 这里的 error 已经被 userApi.js 的拦截器 alert 过了，所以这里只做控制台打印，防止双重弹窗
    console.error("发送验证码失败:", e);
  }
};

// 卸载时清除定时器
onUnmounted(() => {
  document.removeEventListener('click', handleGlobalClick);
  if (timerInterval.value) clearInterval(timerInterval.value);
});

const toggleMode = () => {
  isLogin.value = !isLogin.value;
  Object.keys(form).forEach(key => form[key] = '');
  timer.value = 0;
  showUsernameHistory.value = false;
  showEmailHistory.value = false;
};

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

const handleGlobalClick = () => {
  showUsernameHistory.value = false;
  showEmailHistory.value = false;
};

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');

/* 保持你原有的 CSS 样式，只需确保 lottie-wrapper 大小合适 */
.lottie-wrapper {
  width: 100%;
  max-width: 400px;
  height: 400px;
  z-index: 2;
  position: relative;
  /* 如果你的动画原背景不是透明的，可以用 mix-blend-mode 融进背景里 */
  /* mix-blend-mode: multiply; */ 
}

/* 全局布局 */
.auth-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: #f5f0e6; 
}

/* 左侧戏台 */
.stage-panel {
  flex: 1.2;
  position: relative;
  background: #1a1a1a url('../asset/img/opacity-b25.png') center/cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #d4af37;
  overflow: hidden;
  box-shadow: inset -10px 0 20px rgba(0,0,0,0.3);
}

.stage-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.8) 100%);
  z-index: 1;
}

.puppet-wrapper {
  width: 100%;
  height: 400px;
  z-index: 2;
  position: relative;
}

.stage-text {
  z-index: 2;
  text-align: center;
  margin-top: 20px;
  font-family: 'Ma Shan Zheng', cursive;
}

.stage-text h2 {
  font-size: 3rem;
  letter-spacing: 0.2em;
  margin-bottom: 10px;
  text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
}

.stage-text p {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.2rem;
  color: #ccc;
}

/* 右侧表单 */
.form-panel {
  flex: 1;
  min-width: 450px;
  background: #fdfbf7;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.auth-card {
  width: 80%;
  max-width: 400px;
  position: relative;
}

.seal {
  position: absolute;
  top: -30px;
  right: 0;
  width: 45px;
  height: 45px;
  border: 2px solid #b30000;
  color: #b30000;
  font-family: 'Ma Shan Zheng', cursive;
  font-weight: bold;
  padding: 4px;
  line-height: 18px;
  font-size: 16px;
  text-align: center;
  transform: rotate(15deg);
  opacity: 0.8;
  border-radius: 4px;
}

.auth-header {
  margin-bottom: 40px;
}

.title {
  font-family: 'Ma Shan Zheng', cursive;
  color: #1a1a1a;
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.subtitle {
  font-family: 'Noto Serif SC', serif;
  color: #666;
  font-size: 0.95rem;
}

.input-group {
  margin-bottom: 24px;
  position: relative;
}

.input-group label {
  display: block;
  font-family: 'Noto Serif SC', serif;
  font-size: 0.9rem;
  color: #333;
  margin-bottom: 8px;
  font-weight: bold;
}

.input-group input {
  width: 100%;
  padding: 12px 0;
  background: transparent;
  border: none;
  border-bottom: 2px solid #ddd;
  color: #1a1a1a;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s;
}

.input-group input:focus {
  border-bottom-color: #b30000;
}

.email-flex {
  display: flex;
  gap: 15px;
  align-items: flex-end;
}

.code-btn {
  padding: 0 20px;
  height: 40px;
  background: transparent;
  border: 1px solid #b30000;
  color: #b30000;
  border-radius: 20px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s;
}

.code-btn:hover:not(:disabled) {
  background: #b30000;
  color: #fff;
}

.code-btn:disabled {
  border-color: #ccc;
  color: #ccc;
  cursor: not-allowed;
}

.remember-me {
  margin-bottom: 30px;
}

.remember-label {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  color: #666;
  font-size: 0.9rem;
}

.remember-label input {
  margin-right: 8px;
  accent-color: #b30000;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: #b30000;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-family: 'Noto Serif SC', serif;
  font-size: 1.1rem;
  font-weight: bold;
  letter-spacing: 4px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(179, 0, 0, 0.2);
}

.submit-btn:hover {
  background: #8e0000;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(179, 0, 0, 0.3);
}

.auth-footer {
  margin-top: 30px;
  text-align: center;
  color: #666;
  font-size: 0.9rem;
}

.auth-footer span {
  cursor: pointer;
  border-bottom: 1px solid transparent;
  transition: all 0.3s;
}

.auth-footer span:hover {
  color: #b30000;
  border-bottom-color: #b30000;
}

/* 历史列表样式 */
.history-list {
  position: absolute;
  z-index: 10;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  top: calc(100% + 5px);
  left: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.history-item {
  padding: 10px 15px;
  color: #333;
  cursor: pointer;
  transition: background 0.2s;
}

.history-item:hover {
  background: #f5f0e6;
  color: #b30000;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>