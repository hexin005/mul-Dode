<template>
  <div class="auth-page-wrapper">
    <transition name="toast-fade">
      <div v-if="toast.show" class="toast-wrapper" :class="`toast-${toast.type}`">
        <svg v-if="toast.type === 'error'" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
        <span>{{ toast.message }}</span>
      </div>
    </transition>

    <button class="back-home-btn" @click="goHome">
      <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
      </svg>
      返回首页
    </button>

    <div class="glass-container">
      
      <div class="animation-stage">
        <div class="lottie-wrapper" ref="lottieContainer"></div>
        
        <div class="stage-text">
          <h1 class="main-title">光影流传</h1>
          <p class="sub-title">方寸戏台上，指尖舞乾坤</p>
        </div>
      </div>

      <div class="form-panel">
        <div class="seal">雅鉴</div>
        
        <div class="form-header">
          <h2>{{ isLogin ? '识得旧友' : '初识雅鉴' }}</h2>
          <p>{{ isLogin ? '输入名帖，重返皮影之境' : '登记名册，开启传承之旅' }}</p>
        </div>

        <div class="auth-form">
          <div class="input-group">
            <input 
              v-model="form.username" 
              type="text" 
              placeholder="君之名号" 
              required 
              @click.stop="showUsernameHistory = true"
            />
            <div v-if="showUsernameHistory && usernameHistory.length" class="history-list glass-dropdown">
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
            <input 
              v-model="form.password" 
              :type="showPassword ? 'text' : 'password'" 
              placeholder="通关秘钥" 
              required 
            />
            <span class="eye-icon" @click="togglePassword('password')">
              <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
            </span>
          </div>

          <div v-if="isLogin" class="remember-me">
            <label class="remember-label">
              <input type="checkbox" v-model="form.remember" />
              <span class="label-text">铭记此缘 (保持登录)</span>
            </label>
          </div>

          <transition name="fade-slide">
            <div v-if="!isLogin" class="register-fields">
              <div class="input-group email-group">
                <input 
                  v-model="form.email" 
                  type="email" 
                  placeholder="联络信鸽 (邮箱地址)" 
                  @click.stop="showEmailHistory = true"
                />
                <button @click.prevent="handleSendCode" :disabled="timer > 0" class="code-btn">
                  {{ timer > 0 ? timer + 's' : '获取验证码' }}
                </button>
                <div v-if="showEmailHistory && emailHistory.length" class="history-list glass-dropdown">
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
                <input 
                  v-model="form.code" 
                  type="text" 
                  placeholder="飞鸽传书 (六位验证码)" 
                />
              </div>

              <div class="input-group">
                <input 
                  v-model="form.confirmPassword" 
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  placeholder="再书秘钥" 
                  required 
                />
                <span class="eye-icon" @click="togglePassword('confirm')">
                  <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
                </span>
              </div>
            </div>
          </transition>

          <div class="submit-wrapper">
            <button class="submit-btn" @click="handleSubmit">
              {{ isLogin ? '开启光影' : '录入名册' }}
            </button>
            <transition name="fade-anim">
              <div 
                v-show="isFormReady" 
                class="attention-lottie" 
                ref="attentionLottie"
              ></div>
            </transition>
          </div>

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
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';
// 请确保您的 API 路径正确
import { sendCode, userRegister, userLogin } from '../../services/userApi.js';
import lottie from 'lottie-web';

// 引入三个动画文件
import defaultCatAnim from '@/asset/Totoro Walk.json'; 
import laughingCatAnim from '@/asset/laughing cat.json';
import attentionData from '@/asset/lottieflow-attention-01-000000-easey.json';

const router = useRouter();
const isLogin = ref(true);
const timer = ref(0);
const showUsernameHistory = ref(false);
const showEmailHistory = ref(false);
const timerInterval = ref(null);

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  code: '',
  remember: false
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);

const lottieContainer = ref(null);
const attentionLottie = ref(null); // 新增：引导动画容器
let animInstance = null;
let attentionAnimInstance = null; // 新增：引导动画实例
let errorAnimTimer = null; 

// ==========================================
// 核心逻辑：检测表单是否已填完 (恢复)
// ==========================================
const isFormReady = computed(() => {
  if (isLogin.value) {
    return form.username.trim() !== '' && form.password.trim() !== '';
  } else {
    return (
      form.username.trim() !== '' &&
      form.password.trim() !== '' &&
      form.email.trim() !== '' &&
      form.code.trim() !== '' &&
      form.confirmPassword.trim() !== '' &&
      form.password === form.confirmPassword
    );
  }
});

watch(isFormReady, (ready) => {
  if (ready && attentionAnimInstance) {
    attentionAnimInstance.play();
  } else if (!ready && attentionAnimInstance) {
    attentionAnimInstance.pause();
  }
});

// ==========================================
// 友好的自定义消息提示框 (Toast)
// ==========================================
const toast = ref({
  show: false,
  message: '',
  type: 'error'
});
let toastTimer = null;

const showMessage = (msg, type = 'error') => {
  toast.value = { show: true, message: msg, type };
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.value.show = false;
  }, 3000); 
};

const goHome = () => {
  router.push('/');
};

// ==========================================
// 猫咪动画播放逻辑
// ==========================================
const loadMainAnimation = () => {
  if (animInstance) animInstance.destroy();
  animInstance = lottie.loadAnimation({
    container: lottieContainer.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    animationData: defaultCatAnim
  });
};

const playErrorAnimation = () => {
  if (animInstance) animInstance.destroy();
  if (errorAnimTimer) clearTimeout(errorAnimTimer);

  animInstance = lottie.loadAnimation({
    container: lottieContainer.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    animationData: laughingCatAnim
  });

  errorAnimTimer = setTimeout(() => {
    loadMainAnimation();
  }, 3000);
};

onMounted(() => {
  initForm();
  
  if (lottieContainer.value) {
    loadMainAnimation();
  }

  // 恢复：初始化按钮旁边的引导动画
  if (attentionLottie.value) {
    attentionAnimInstance = lottie.loadAnimation({
      container: attentionLottie.value,
      renderer: 'svg',
      loop: true,
      autoplay: false,
      animationData: attentionData
    });
    if (isFormReady.value) {
      attentionAnimInstance.play();
    }
  }

  document.addEventListener('click', handleGlobalClick);
});

onUnmounted(() => {
  if (timerInterval.value) clearInterval(timerInterval.value);
  if (toastTimer) clearTimeout(toastTimer);
  if (errorAnimTimer) clearTimeout(errorAnimTimer);
  if (animInstance) animInstance.destroy();
  if (attentionAnimInstance) attentionAnimInstance.destroy();
  document.removeEventListener('click', handleGlobalClick);
});

const togglePassword = (type) => {
  if (type === 'password') {
    showPassword.value = !showPassword.value;
  } else if (type === 'confirm') {
    showConfirmPassword.value = !showConfirmPassword.value;
  }
};

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
  }
};

const handleSendCode = async () => {
  if (!form.email) return showMessage("请先填写联络信鸽（邮箱）", "error");
  const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailReg.test(form.email)) return showMessage("邮箱格式不正确", "error");
  if (timer.value > 0) return;

  try {
    const res = await sendCode(form.email); 
    if (res.code === 200) {
      showMessage("验证码已飞鸽传书，请查收", "success");
      saveHistory('emailHistory', form.email); 
      timer.value = 60;
      if (timerInterval.value) clearInterval(timerInterval.value);
      timerInterval.value = setInterval(() => {
        timer.value--;
        if (timer.value <= 0) {
          clearInterval(timerInterval.value);
          timerInterval.value = null;
        }
      }, 1000);
    } else { showMessage(res.msg || "发送失败", "error"); }
  } catch (e) { console.error(e); }
};

const toggleMode = () => {
  isLogin.value = !isLogin.value;
  Object.keys(form).forEach(key => {
    if (key !== 'remember') form[key] = '';
  });
  timer.value = 0;
  showPassword.value = false;
  showConfirmPassword.value = false;
  
  if (errorAnimTimer) {
    clearTimeout(errorAnimTimer);
    loadMainAnimation();
  }
};

const handleSubmit = async () => {
  if (isLogin.value) {
    if (!form.username || !form.password) {
      playErrorAnimation();
      return showMessage("请填写名号和秘钥", "error");
    }
    try {
      const res = await userLogin({
        username: form.username,
        password: form.password,
        remember: form.remember
      });
      if (res.code === 200) {
        showMessage("欢迎归来，旧友", "success");
        saveHistory('usernameHistory', form.username);
        const storage = form.remember ? localStorage : sessionStorage;
        storage.setItem('user', JSON.stringify(res.user));
        if (res.token) storage.setItem('token', res.token);
        
        setTimeout(() => router.push('/user-center'), 800);
      } else { 
        playErrorAnimation();
        showMessage(res.msg || '登录失败', "error");
      }
    } catch (e) { 
        playErrorAnimation();
        showMessage('登录异常，请稍后重试', "error");
    }
    return;
  }

  if (!form.username || !form.password || !form.email || !form.code) {
    playErrorAnimation();
    return showMessage("请填写完整的注册信息", "error");
  }
  if (form.password.length < 6) {
    playErrorAnimation();
    return showMessage("秘钥长度不能少于6位", "error");
  }
  if (form.password !== form.confirmPassword) {
    playErrorAnimation();
    return showMessage("两次秘钥不一致", "error");
  }
  
  try {
    const res = await userRegister({
      username: form.username,
      password: form.password,
      email: form.email,
      code: form.code
    });
    if (res.code === 200) {
      showMessage("名册录入成功，请登录", "success");
      saveHistory('usernameHistory', form.username);
      saveHistory('emailHistory', form.email);
      setTimeout(() => toggleMode(), 800);
    } else { 
      playErrorAnimation();
      showMessage(res.msg || '注册失败', "error");
    }
  } catch (e) { 
      playErrorAnimation();
      showMessage('注册异常，请稍后重试', "error");
  }
};

const handleGlobalClick = () => {
  showUsernameHistory.value = false;
  showEmailHistory.value = false;
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');

.auth-page-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative; 
  background: 
    radial-gradient(circle at 15% 50%, rgba(179, 0, 0, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 85% 30%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
    #121212; 
}

/* Toast 样式 */
.toast-wrapper {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: rgba(20, 20, 20, 0.85);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  border: 1px solid;
  font-family: 'Noto Serif SC', serif;
  font-size: 1.05rem;
  font-weight: 700;
  pointer-events: none;
}
.toast-error {
  border-color: rgba(179, 0, 0, 0.5);
  color: #ff4d4f;
  box-shadow: 0 8px 30px rgba(179, 0, 0, 0.15);
}
.toast-success {
  border-color: rgba(212, 175, 55, 0.5);
  color: #d4af37;
  box-shadow: 0 8px 30px rgba(212, 175, 55, 0.15);
}
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px);
}

/* 返回首页按钮 */
.back-home-btn {
  position: absolute;
  top: 40px;
  left: 40px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
  font-family: 'Noto Serif SC', serif;
  font-size: 1rem;
  padding: 10px 20px;
  border-radius: 30px;
  cursor: pointer;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  z-index: 100;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
.back-home-btn:hover {
  background: rgba(212, 175, 55, 0.15);
  border-color: #d4af37;
  color: #d4af37;
  transform: translateX(-5px);
  box-shadow: 0 4px 20px rgba(212, 175, 55, 0.2);
}

/* 玻璃态面板 */
.glass-container {
  display: flex;
  width: 85vw;           
  height: 80vh;          
  max-width: 1200px;     
  max-height: 800px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(25px) saturate(180%);
  -webkit-backdrop-filter: blur(25px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  overflow: hidden;      
}

.animation-stage {
  flex: 1.3;             
  position: relative;
  background: rgba(0, 0, 0, 0.2); 
  border-right: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
}
.lottie-wrapper {
  width: 100%;
  height: 60%;           
  min-height: 350px;
  position: relative; 
  filter: drop-shadow(0 0 15px rgba(212, 175, 55, 0.2));
}
.stage-text {
  text-align: center;
  margin-top: 20px;
}
.stage-text .main-title {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 4rem;       
  color: #d4af37;
  letter-spacing: 0.2em;
  margin-bottom: 10px;
  text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
}
.stage-text .sub-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 2px;
}

.form-panel {
  flex: 1;
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  min-width: 400px;
}
.form-header {
  margin-bottom: 40px;
}
.form-header h2 {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 2.2rem;
  color: #fff;
  margin-bottom: 8px;
}
.form-header p {
  font-family: 'Noto Serif SC', serif;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 22px;
}
.input-group {
  position: relative;
  width: 100%;
}
.input-group input {
  width: 100%;
  padding: 16px 45px 16px 20px; 
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  color: #fff;
  font-size: 1rem;
  font-family: 'Noto Serif SC', serif;
  outline: none;
  transition: all 0.3s ease;
}
.input-group input:focus {
  border-color: #d4af37;
  background: rgba(0, 0, 0, 0.4);
  box-shadow: 0 0 12px rgba(212, 175, 55, 0.2);
}
.input-group input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.eye-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: color 0.3s ease;
}
.eye-icon:hover { color: #d4af37; }
.email-group { display: flex; gap: 10px; }
.code-btn {
  padding: 0 15px;
  height: 52px;
  background: transparent;
  border: 1px solid rgba(179, 0, 0, 0.5);
  color: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  cursor: pointer;
  white-space: nowrap;
  font-family: 'Noto Serif SC', serif;
  transition: all 0.3s;
}
.code-btn:hover:not(:disabled) {
  background: rgba(179, 0, 0, 0.2);
  border-color: #b30000;
  color: #fff;
}
.code-btn:disabled { border-color: rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.2); cursor: not-allowed; }

.remember-me { margin: -5px 0 5px 5px; }
.remember-label { display: inline-flex; align-items: center; cursor: pointer; color: rgba(255, 255, 255, 0.5); font-size: 0.9rem; }
.remember-label input { margin-right: 8px; accent-color: #d4af37; width: 16px; height: 16px; }

/* 提交按钮及引导动画 */
.submit-wrapper {
  position: relative;
  width: 100%;
  margin-top: 10px;
}
.submit-btn {
  width: 100%; 
  padding: 16px; 
  background: linear-gradient(135deg, #d4af37 0%, #b38627 100%);
  color: #fff; 
  border: none; 
  border-radius: 12px;
  font-family: 'Noto Serif SC', serif; 
  font-size: 1.1rem; 
  font-weight: 700; 
  letter-spacing: 4px;
  cursor: pointer; 
  transition: all 0.3s ease; 
  box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
}
.submit-btn:hover { 
  transform: translateY(-2px); 
  box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4); 
}

/* 恢复：引导箭头动画样式 */
.attention-lottie {
  position: absolute;
  right: -55px;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  pointer-events: none;
  filter: invert(66%) sepia(35%) saturate(855%) hue-rotate(5deg) brightness(94%) contrast(88%);
}
.fade-anim-enter-active,
.fade-anim-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.fade-anim-enter-from,
.fade-anim-leave-to {
  opacity: 0;
  transform: translateY(-50%) translateX(10px);
}

.auth-footer { margin-top: 30px; text-align: center; color: rgba(255, 255, 255, 0.4); font-size: 0.95rem; }
.auth-footer span { cursor: pointer; transition: all 0.3s; position: relative; padding-bottom: 2px; }
.auth-footer span::after { content: ''; position: absolute; width: 0; height: 1px; bottom: 0; left: 50%; background-color: #d4af37; transition: all 0.3s ease; transform: translateX(-50%); }
.auth-footer span:hover { color: #d4af37; }
.auth-footer span:hover::after { width: 100%; }

.seal { position: absolute; top: 30px; right: 30px; width: 45px; height: 45px; border: 1px solid #b30000; color: #b30000; font-family: 'Ma Shan Zheng', cursive; padding: 4px; line-height: 18px; font-size: 16px; text-align: center; transform: rotate(15deg); opacity: 0.5; border-radius: 4px; user-select: none; }

.glass-dropdown { position: absolute; z-index: 100; width: 100%; max-height: 150px; overflow-y: auto; top: calc(100% + 8px); left: 0; background: rgba(20, 20, 20, 0.9); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
.history-item { padding: 12px 20px; color: rgba(255, 255, 255, 0.7); cursor: pointer; transition: background 0.2s; font-size: 0.9rem; }
.history-item:hover { background: rgba(212, 175, 55, 0.2); color: #d4af37; }
.glass-dropdown::-webkit-scrollbar { width: 6px; }
.glass-dropdown::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

.register-fields { display: flex; flex-direction: column; gap: 22px; }
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); max-height: 300px; overflow: hidden; }
.fade-slide-enter-from, .fade-slide-leave-to { opacity: 0; transform: translateY(-10px); max-height: 0; margin-bottom: -22px; }
</style>