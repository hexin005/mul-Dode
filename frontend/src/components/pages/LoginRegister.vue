<template>
  <div class="auth-page-wrapper">
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
              @focus="handleFocus('normal')"
              @blur="handleBlur"
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
              @focus="handleFocus('secret')"
              @blur="handleBlur"
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
                  @focus="handleFocus('normal')"
                  @blur="handleBlur"
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
                  @focus="handleFocus('normal')"
                  @blur="handleBlur"
                />
              </div>

              <div class="input-group">
                <input 
                  v-model="form.confirmPassword" 
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  placeholder="再书秘钥" 
                  required 
                  @focus="handleFocus('secret')"
                  @blur="handleBlur"
                />
                <span class="eye-icon" @click="togglePassword('confirm')">
                  <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
                </span>
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
// 请确保您的 API 路径正确
import { sendCode, userRegister, userLogin } from '@/services/userApi';
import lottie from 'lottie-web';

// 引入您的 "No Internet.json" 动画文件
import animationData from '@/asset/No Internet.json'; 

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
let animInstance = null;

// ==========================================
// 核心联动：Lottie 动画状态机配置
// ==========================================
// ⚠️ 同样，请在这里填入你动画文件对应的实际帧数 [起, 止]
const animStates = {
  default: [0, 59], // 正常打开页面时的原样动画（默认状态）
  hide: [60, 90],   // 猫始终在盒子下面的动画段落
  peek: [90, 120]   // 猫从盒子出来的动画段落
};

onMounted(() => {
  initForm();
  
  if (lottieContainer.value) {
    animInstance = lottie.loadAnimation({
      container: lottieContainer.value, 
      renderer: 'svg',                  
      loop: true, // 全局设为循环，让状态保持连续动作
      autoplay: true,                   
      animationData: animationData      
    });
    // 初始播放正常状态
    playAnimState('default', 1);
  }
  document.addEventListener('click', handleGlobalClick);
});

onUnmounted(() => {
  if (timerInterval.value) clearInterval(timerInterval.value);
  if (animInstance) animInstance.destroy();
  document.removeEventListener('click', handleGlobalClick);
});

// ==========================================
// Lottie 播放控制逻辑 (加入速度控制)
// ==========================================
const playAnimState = (stateName, speed = 1) => {
  if (!animInstance || !animStates[stateName]) return;
  try {
    animInstance.setSpeed(speed); // 设置播放速度
    animInstance.loop = true;     // 允许循环，停留在该状态的循环中
    animInstance.playSegments(animStates[stateName], true);
  } catch (e) {
    console.warn("Lottie 播放异常", e);
  }
};

const handleFocus = (inputType) => {
  if (inputType === 'normal') {
    // 1. 焦点在非密码框：猫始终处于盒子里
    playAnimState('hide', 1);
  } else if (inputType === 'secret') {
    // 2. 焦点在密码框
    const isVisible = showPassword.value || showConfirmPassword.value;
    if (isVisible) {
      // 查看密码时（明文）：猫躲在盒子下面
      playAnimState('hide', 0.6);
    } else {
      // 填密码时（密文）：猫从盒子出来 (速度放慢至 0.6 倍速，数字你可以自己微调)
      playAnimState('peek', 0.6);
    }
  }
};

const handleBlur = () => {
  // 3. 没点击输入框时：正常播放动画
  setTimeout(() => {
    if (!document.activeElement || document.activeElement.tagName !== 'INPUT') {
      playAnimState('default', 1);
    }
  }, 150);
};

// ==========================================
// 密码查看/隐藏切换，与动画联动
// ==========================================
const togglePassword = (type) => {
  let isNowVisible = false;
  if (type === 'password') {
    showPassword.value = !showPassword.value;
    isNowVisible = showPassword.value;
  } else if (type === 'confirm') {
    showConfirmPassword.value = !showConfirmPassword.value;
    isNowVisible = showConfirmPassword.value;
  }
  
  // 切换眼睛时，如果光标还在输入框里，立刻改变猫咪状态
  if (document.activeElement && document.activeElement.tagName === 'INPUT') {
      if (isNowVisible) {
        // 变成明文 -> 躲起来
        playAnimState('hide', 1);
      } else {
        // 变成密文 -> 慢速钻出来
        playAnimState('peek', 0.6);
      }
  }
};


// ==========================================
// 表单基础逻辑 (保持不变)
// ==========================================
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
  if (!form.email) return alert("请先填写联络信鸽（邮箱）");
  const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailReg.test(form.email)) return alert("邮箱格式不正确");
  if (timer.value > 0) return;

  try {
    const res = await sendCode(form.email); 
    if (res.code === 200) {
      alert("验证码已飞鸽传书，请查收");
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
    } else { alert(res.msg || "发送失败"); }
  } catch (e) { console.error(e); }
};

const toggleMode = () => {
  isLogin.value = !isLogin.value;
  Object.keys(form).forEach(key => {
    if (key !== 'remember') form[key] = '';
  });
  timer.value = 0;
  
  // 切换模式时重置状态并恢复正常动画
  showPassword.value = false;
  showConfirmPassword.value = false;
  playAnimState('default', 1); 
};

const handleSubmit = async () => {
  if (isLogin.value) {
    if (!form.username || !form.password) {
      return alert("请填写名号和秘钥");
    }
    try {
      const res = await userLogin({
        username: form.username,
        password: form.password,
        remember: form.remember
      });
      if (res.code === 200) {
        saveHistory('usernameHistory', form.username);
        const storage = form.remember ? localStorage : sessionStorage;
        storage.setItem('user', JSON.stringify(res.user));
        if (res.token) storage.setItem('token', res.token);
        await router.push('/user-center');
      } else { 
        alert(res.msg || '登录失败'); 
      }
    } catch (e) { 
        alert('登录异常'); 
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
    return alert("两次秘钥不一致");
  }
  try {
    const res = await userRegister({
      username: form.username,
      password: form.password,
      email: form.email,
      code: form.code
    });
    if (res.code === 200) {
      saveHistory('usernameHistory', form.username);
      saveHistory('emailHistory', form.email);
      toggleMode();
    } else { 
      alert(res.msg || '注册失败'); 
    }
  } catch (e) { 
      alert('注册异常'); 
  }
};

const handleGlobalClick = () => {
  showUsernameHistory.value = false;
  showEmailHistory.value = false;
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');

/* 全局与布局保持上一版的毛玻璃样式 */
.auth-page-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: 
    radial-gradient(circle at 15% 50%, rgba(179, 0, 0, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 85% 30%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
    #121212; 
}

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

.eye-icon:hover {
  color: #d4af37; 
}

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

.submit-btn {
  width: 100%; padding: 16px; margin-top: 10px;
  background: linear-gradient(135deg, #d4af37 0%, #b38627 100%);
  color: #fff; border: none; border-radius: 12px;
  font-family: 'Noto Serif SC', serif; font-size: 1.1rem; font-weight: 700; letter-spacing: 4px;
  cursor: pointer; transition: all 0.3s ease; box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
}
.submit-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4); }

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