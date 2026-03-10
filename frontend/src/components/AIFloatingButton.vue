<template>
  <div class="ai-assistant-root">
    <!-- 1. 遮罩层：点击关闭，并阻止滚轮事件传递 -->
    <transition name="fade">
      <div 
        v-if="isOpen" 
        class="modal-overlay" 
        @click="closePanel"
        @wheel.prevent
        @touchmove.prevent
      ></div>
    </transition>

    <!-- 2. 悬浮球：收起时显示 -->
    <transition name="scale-fade">
      <div 
        v-show="!isOpen"
        class="floating-ball"
        ref="ballRef"
        :style="ballStyle"
        @mousedown="startDrag"
        @touchstart.passive="startDrag"
        @click="openPanel"
      >
        <div class="ball-content">
          <span class="icon">🤖</span>
        </div>
        <!-- 未读/待机呼吸灯 -->
        <div class="pulse-ring"></div>
      </div>
    </transition>

    <!-- 3. 中央主面板 -->
    <transition name="modal-pop">
      <div 
        v-if="isOpen" 
        class="main-panel"
        @wheel.stop
      >
        <!-- 顶部导航栏 -->
        <div class="panel-header">
          <div class="header-left">
            <span class="logo">🧠</span>
            <span class="title">皮影 AI 助手</span>
            <span class="status-badge" :class="{ online: isBackendOnline }">
              {{ isBackendOnline ? '已连接' : '离线' }}
            </span>
          </div>
          
          <div class="tab-center">
            <button 
              :class="['tab-btn', { active: activeTab === 'chat' }]"
              @click="activeTab = 'chat'"
            >💬 对话</button>
            <button 
              :class="['tab-btn', { active: activeTab === 'image' }]"
              @click="activeTab = 'image'"
            >🖼️ 绘画</button>
          </div>

          <button class="close-btn" @click="closePanel" title="关闭">×</button>
        </div>

        <!-- 内容区域 -->
        <div class="panel-body">
          
          <!-- === TAB 1: 聊天 === -->
          <div v-show="activeTab === 'chat'" class="tab-content chat-mode">
            <div class="messages-area" ref="msgContainer">
              <div v-if="messages.length === 0" class="empty-placeholder">
                <div class="welcome-icon">👋</div>
                <p>你好！我是你的智能皮影传承助手。<br>关于皮影的历史、制作工艺都可以问我。</p>
              </div>

              <div 
                v-for="(msg, index) in messages" 
                :key="index" 
                :class="['message-row', msg.role]"
              >
                <!-- <div class="avatar">{{ msg.role === 'user' ? '' : '🤖' }}</div> -->
                 <div v-if="msg.role !== 'user'" class="avatar">🤖</div>
                <!-- Markdown 渲染 -->
                <div class="bubble markdown-body" v-html="renderContent(msg.content)"></div>
              </div>

              <div v-if="isLoading" class="message-row assistant">
                <div class="avatar">🤖</div>
                <div class="bubble loading-bubble">
                  <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                </div>
              </div>
            </div>

            <div 
              class="quick-questions" 
              ref="quickQScroll" 
              @wheel.prevent="handleHorizontalScroll"
            >
              <button 
                v-for="(q, index) in suggestionQuestions" 
                :key="index"
                class="quick-chip"
                @click="handleQuickAsk(q)"
              >
                {{ q }}
              </button>
            </div>

            <div class="input-bar">
              <input 
                v-model="chatInput" 
                @keyup.enter="handleSendMessage"
                :disabled="isLoading"
                placeholder="输入您的问题..."
                type="text"
                autocomplete="off"
              >
              <button 
                class="send-btn" 
                @click="handleSendMessage"
                :disabled="!chatInput.trim() || isLoading"
              >➤</button>
            </div>
          </div>

          <!-- === TAB 2: 绘画 === -->
          <div v-show="activeTab === 'image'" class="tab-content image-mode">
            <div class="image-scroll-area">
              <div class="section-label">✨ 灵感推荐</div>
              <div class="preset-scroll">
                <span 
                  v-for="tag in presets" 
                  :key="tag" 
                  class="preset-chip"
                  @click="imagePrompt = tag"
                >{{ tag }}</span>
              </div>

              <div class="section-label" style="margin-top: 20px;">📐 选择尺寸</div>
              <div class="size-grid">
                <div 
                  v-for="size in sizeOptions" 
                  :key="size.val" 
                  :class="['size-card', { active: imageSize === size.val }]"
                  @click="imageSize = size.val"
                >
                  <span class="size-name">{{ size.name }}</span>
                  <span class="size-detail">{{ size.res }}</span>
                </div>
              </div>

              <div class="result-display">
                <div v-if="generatedImage" class="image-wrapper">
                  <img :src="generatedImage" alt="Generated">
                  <div class="img-actions">
                    <button @click="handleDownload">💾 下载原图</button>
                  </div>
                </div>
                <div v-else-if="isImageGenerating" class="generating-state">
                  <div class="spinner"></div>
                  <p>正在绘制皮影风格图像...</p>
                </div>
                <div v-else class="empty-state">
                  图像将在这里预览
                </div>
                <p v-if="imageError" class="error-text">❌ {{ imageError }}</p>
              </div>
            </div>

            <div class="input-bar image-input-bar">
              <textarea 
                v-model="imagePrompt" 
                placeholder="描述你想生成的皮影画面..."
                rows="1"
              ></textarea>
              <button 
                class="magic-btn" 
                @click="handleGenerateImage"
                :disabled="isImageGenerating || !imagePrompt.trim()"
              >🎨 生成</button>
            </div>
          </div>

        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue';
import { marked } from 'marked';
import { sendMessage, generateImage, checkBackendStatus } from '../services/api';

// --- 状态管理 ---
const isOpen = ref(false);
const activeTab = ref('chat');
const isBackendOnline = ref(false);

// --- 拖拽逻辑 ---
const ballRef = ref(null);
const ballPos = ref({ x: 0, y: 0 }); 
const isDragging = ref(false);
let startPos = { x: 0, y: 0 };
let initialBallPos = { x: 0, y: 0 };
let moveHandler = null;
let upHandler = null;

const ballStyle = computed(() => ({
  transform: `translate3d(${ballPos.value.x}px, ${ballPos.value.y}px, 0)`
}));

// --- 核心功能 ---
// 打开面板
const openPanel = () => {
  if (isDragging.value) return;
  isOpen.value = true;
  // 锁定背景滚动
  document.body.classList.add('lock-scroll');
  document.documentElement.classList.add('lock-scroll');
};

// 关闭面板
const closePanel = () => {
  isOpen.value = false;
  // 恢复背景滚动
  document.body.classList.remove('lock-scroll');
  document.documentElement.classList.remove('lock-scroll');
};

// --- 聊天数据 ---
const chatInput = ref('');
const messages = ref([]);
const isLoading = ref(false);
const msgContainer = ref(null);
// ✅ 新增：皮影主题快捷提问列表
const suggestionQuestions = [
  "🏮 皮影戏起源于哪个朝代？",
  "✂️ 皮影是如何制作的？",
  "🎭 著名的皮影流派有哪些？",
  "🎬 推荐几部经典的皮影戏？",
  // "🤔 皮影戏与现代科技如何结合？"
];
const quickQScroll = ref(null); // ✅ 新增：获取快捷语容器的引用

// --- 绘画数据 ---
const imagePrompt = ref('');
const imageSize = ref('2K');
const generatedImage = ref('');
const isImageGenerating = ref(false);
const imageError = ref('');
const presets = [
    '皮影孙悟空，大圣归来姿态，红金配色，背景为白色', 
    '中国传统皮影，驴皮雕刻，古代武将，复古韵味，背景为白色', 
    '皮影风格的现代城市，背景为白色',
    '上古神兽皮影形态，祥云环绕，神秘东方风格，背景为白色',
];
const sizeOptions = [
  { name: '1K 方形', res: '1024x1024', val: '1K' },
  { name: '2K 横屏', res: '1792x1024', val: '2K' },
  { name: '4K 超清', res: '2048x2048', val: '4K' }
];

// --- 生命周期 ---
onMounted(async () => {
  // 初始位置：右下角
  ballPos.value = { 
    x: window.innerWidth - 90, 
    y: window.innerHeight - 120 
  };
  isBackendOnline.value = await checkBackendStatus();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  // 防止组件卸载时页面还没解锁
  document.body.classList.remove('lock-scroll');
  document.documentElement.classList.remove('lock-scroll');
  // 移除可能存在的事件监听器
  if (moveHandler && upHandler) {
    document.removeEventListener('mousemove', moveHandler);
    document.removeEventListener('mouseup', upHandler);
    document.removeEventListener('touchmove', moveHandler);
    document.removeEventListener('touchend', upHandler);
  }
});

// --- 拖拽交互 ---
const startDrag = (e) => {
  // 1. 如果是鼠标按下，阻止默认行为（核心修复：防止选中文字）
  if (e.type === 'mousedown') {
    e.preventDefault(); 
    if (e.button !== 0) return; // 只允许左键拖拽
  }
  
  isDragging.value = false;
  
  // 2. 暂时禁止页面文字被选中（双重保险）
  document.body.style.userSelect = 'none'; 
  
  const clientX = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
  const clientY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;
  
  startPos = { x: clientX, y: clientY };
  initialBallPos = { ...ballPos.value };
  
  // 定义移动处理函数
  moveHandler = (ev) => {
    isDragging.value = true;
    const cx = ev.type.startsWith('touch') ? ev.touches[0].clientX : ev.clientX;
    const cy = ev.type.startsWith('touch') ? ev.touches[0].clientY : ev.clientY;
    
    let newX = initialBallPos.x + (cx - startPos.x);
    let newY = initialBallPos.y + (cy - startPos.y);
    
    // 边界限制
    newX = Math.min(Math.max(0, newX), window.innerWidth - 60);
    newY = Math.min(Math.max(0, newY), window.innerHeight - 60);
    
    ballPos.value = { x: newX, y: newY };
  };

  // 定义释放处理函数
  upHandler = () => {
    document.removeEventListener('mousemove', moveHandler);
    document.removeEventListener('mouseup', upHandler);
    document.removeEventListener('touchmove', moveHandler);
    document.removeEventListener('touchend', upHandler);
    
    // 3. 拖拽结束，恢复页面文字可选中状态
    document.body.style.userSelect = ''; 
    
    if (isDragging.value) {
      snapToEdge();
      setTimeout(() => isDragging.value = false, 100);
    }
  };

  // 添加事件监听器
  document.addEventListener('mousemove', moveHandler);
  document.addEventListener('mouseup', upHandler);
  document.addEventListener('touchmove', moveHandler, { passive: false });
  document.addEventListener('touchend', upHandler);
};

const snapToEdge = () => {
  const midX = window.innerWidth / 2;
  const targetX = ballPos.value.x < midX ? 20 : window.innerWidth - 80;
  ballPos.value = { x: targetX, y: ballPos.value.y };
};

const handleResize = () => { snapToEdge(); };
const renderContent = (text) => { return marked.parse(text || ''); };

// --- 业务逻辑 ---
const handleSendMessage = async () => {
  const text = chatInput.value.trim();
  if (!text) return;
  chatInput.value = '';
  messages.value.push({ role: 'user', content: text });
  isLoading.value = true;
  scrollToBottom();

  try {
    const res = await sendMessage(text);
    if (res && (res.success || res.answer || res.content)) {
      messages.value.push({ role: 'assistant', content: res.answer || res.content || '暂无内容' });
    } else {
      messages.value.push({ role: 'assistant', content: `❌ 错误: ${res.error || '服务器未响应'}` });
    }
  } catch (err) {
    messages.value.push({ role: 'assistant', content: '❌ 网络连接异常' });
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
};

// ✅ 新增：点击快捷问题直接发送
const handleQuickAsk = (text) => {
  chatInput.value = text;
  handleSendMessage();
};

// ✅ 新增：处理鼠标滚轮横向滚动
const handleHorizontalScroll = (e) => {
  if (quickQScroll.value) {
    // 将鼠标滚轮的垂直滚动量 (deltaY) 施加到水平滚动位置 (scrollLeft)
    // 这里的 += 决定了方向，e.deltaY 通常向下滚是正数，向右滚
    quickQScroll.value.scrollLeft += e.deltaY;
  }
};

const scrollToBottom = () => {
  nextTick(() => {
    if (msgContainer.value) msgContainer.value.scrollTop = msgContainer.value.scrollHeight;
  });
};

const handleGenerateImage = async () => {
  if (!imagePrompt.value) return;
  isImageGenerating.value = true;
  imageError.value = '';
  generatedImage.value = '';

  try {
    const res = await generateImage(imagePrompt.value, imageSize.value);
    if (res && res.image_url) {
      generatedImage.value = res.image_url;
    } else {
      imageError.value = res.error || '生成失败';
    }
  } catch (e) {
    imageError.value = '请求异常';
  } finally {
    isImageGenerating.value = false;
  }
};

const handleDownload = () => {
  if (!generatedImage.value) return;
  const link = document.createElement('a');
  link.href = generatedImage.value;
  link.download = `shadow-puppet-${Date.now()}.png`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
</script>

<style>
/* --- 全局样式 (必须非 scoped) --- */
/* 这是锁住页面滚动的关键类 */
.lock-scroll {
  overflow: hidden !important;
  height: 100vh !important;
}
</style>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

.ai-assistant-root {
  position: fixed; top: 0; left: 0; width: 0; height: 0;
  z-index: 99999;
  font-family: 'Noto Sans SC', sans-serif;
}

/* 1. 遮罩层 */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  z-index: 10000;
}

/* 2. 悬浮球 */
.floating-ball {
  position: fixed; width: 64px; height: 64px;
  cursor: pointer; pointer-events: auto; touch-action: none;
  z-index: 10001; left: 0; top: 0;
  transition: transform 0.1s linear;
  user-select: none;
}
.ball-content {
  width: 100%; height: 100%; border-radius: 50%;
  background: linear-gradient(135deg, #FF9966, #FF5E62);
  box-shadow: 0 8px 25px rgba(255, 94, 98, 0.5);
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 32px;
}
.pulse-ring {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  border-radius: 50%; border: 2px solid rgba(255, 94, 98, 0.6);
  animation: pulse 2s infinite; pointer-events: none;
}
@keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 100% { transform: scale(1.6); opacity: 0; } }

/* 3. 主面板 (居中加大) */
.main-panel {
  position: fixed;
  top: 50%; left: 50%; transform: translate(-50%, -50%); /* 绝对居中 */
  
  width: 900px; height: 720px; /* 大尺寸，更像应用 */
  max-width: 92vw; max-height: 90vh;
  
  background: #ffffff; border-radius: 24px;
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.3);
  display: flex; flex-direction: column; overflow: hidden;
  z-index: 10002;
}

/* 头部 */
.panel-header {
  padding: 0 24px; height: 70px;
  background: #fff; border-bottom: 1px solid #f0f0f0;
  display: flex; align-items: center; justify-content: space-between;
}
.header-left { display: flex; align-items: center; gap: 12px; flex: 1; }
.header-left .title { font-size: 18px; font-weight: 700; color: #1f2937; }
.status-badge { 
  font-size: 12px; padding: 4px 10px; border-radius: 12px; 
  background: #fee2e2; color: #ef4444; font-weight: 500;
}
.status-badge.online { background: #dcfce7; color: #166534; }

.tab-center {
  background: #f3f4f6; padding: 4px; border-radius: 24px; display: flex;
}
.tab-btn {
  padding: 8px 20px; border: none; background: transparent;
  border-radius: 20px; font-size: 15px; color: #6b7280; cursor: pointer;
  transition: all 0.2s; font-weight: 500;
}
.tab-btn.active { background: white; color: #FF5E62; font-weight: 700; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }

.close-btn {
  width: 36px; height: 36px; border: none; background: #f9fafb;
  border-radius: 50%; font-size: 24px; color: #9ca3af; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}
.close-btn:hover { background: #fee2e2; color: #ef4444; }

/* 内容区 */
.panel-body { 
  flex: 1; overflow: hidden; position: relative; background: #f9fafb;
}
.tab-content { height: 100%; display: flex; flex-direction: column; }

/* 聊天 */
/* 确保消息区域高度自适应，不要被挤没了 */
.messages-area {
  flex: 1; 
  overflow-y: auto; 
  padding: 30px; 
  display: flex; 
  flex-direction: column; 
  gap: 24px;
  /* 确保底部留出空间，不会被快捷栏挡住 */
  padding-bottom: 10px; 
}
.empty-placeholder { text-align: center; color: #9ca3af; margin-top: 80px; }
.welcome-icon { font-size: 60px; margin-bottom: 20px; }

.message-row { display: flex; gap: 16px; max-width: 80%; }
.message-row.user { align-self: flex-end; flex-direction: row-reverse; }

.avatar {
  width: 42px; height: 42px; border-radius: 12px; background: #e5e7eb;
  display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0;
}
/* .user .avatar { background: #FF5E62; } */

.bubble {
  padding: 16px 20px; border-radius: 20px; font-size: 16px; line-height: 1.6;
  background: white; border: 1px solid #e5e7eb; color: #374151;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.user .bubble {
  background: #FF5E62; color: white; border: none;
  border-bottom-right-radius: 4px; box-shadow: 0 4px 10px rgba(255, 94, 98, 0.3);
}
.assistant .bubble { border-bottom-left-radius: 4px; }

/* === 新增：快捷提问栏样式 === */
/* 修改 .quick-questions 样式 */
.quick-questions {
  padding: 10px 24px; /* 上下给点呼吸空间 */
  display: flex;
  gap: 10px;
  overflow-x: auto; 
  white-space: nowrap;
  background: #f9fafb; /* 与背景色一致，或者设为 transparent */
  border-top: 1px solid #f3f4f6; /* 可选：加个顶部分割线区分历史消息 */
  flex-shrink: 0; /* 防止被压缩 */
  
  /* 隐藏滚动条 */
  scrollbar-width: none; 
  -ms-overflow-style: none; 
}

.quick-questions::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

.quick-chip {
  background: #fff;
  border: 1px solid #e5e7eb;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 6px rgba(0,0,0,0.02);
  flex-shrink: 0; /* 防止挤压 */
  display: flex;
  align-items: center;
}

.quick-chip:hover {
  border-color: #FF5E62;
  color: #FF5E62;
  background: #fff1f2;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 94, 98, 0.15);
}

/* 微调：输入框上边框去掉，让视觉更连贯（可选） */
.input-bar {
  border-top: none; 
  padding-top: 10px; /* 稍微减少顶部内边距 */
  background: linear-gradient(to bottom, rgba(255,255,255,0), #fff 20%); /* 渐变遮罩效果 */
}

/* 输入区 */
.input-bar {
  padding: 24px; background: white; border-top: 1px solid #f0f0f0;
  display: flex; gap: 16px; align-items: flex-end;
}
.input-bar input {
  flex: 1; border: 2px solid #f3f4f6; border-radius: 28px; padding: 14px 24px;
  outline: none; transition: border 0.2s; font-size: 16px;
}
.input-bar input:focus { border-color: #FF5E62; }
.send-btn {
  width: 52px; height: 52px; border-radius: 50%; background: #FF5E62;
  color: white; border: none; cursor: pointer; flex-shrink: 0;
  font-size: 20px; transition: transform 0.1s;
}
.send-btn:active { transform: scale(0.95); }
.send-btn:disabled { background: #d1d5db; }

/* 绘画 */
/* === 绘画模式布局优化 === */

/* 1. 滚动区域容器 */
.image-scroll-area { 
  flex: 1; 
  overflow-y: auto; 
  padding: 24px 30px; /* 调整内边距 */
  overscroll-behavior: contain;
}

/* 2. 标题样式微调 */
.section-label { 
  font-size: 15px; 
  font-weight: 700; 
  color: #1f2937; 
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 3. 灵感推荐 - 核心修改：改为自动换行布局 */
.preset-scroll { 
  display: flex; 
  flex-wrap: wrap;       /* 允许换行 */
  gap: 10px;             /* 标签之间的间距 */
  margin-bottom: 24px;   /* 底部留白 */
  padding-bottom: 0;     /* 移除之前的底部padding */
  overflow-x: visible;   /* 移除横向滚动 */
}

/* 4. 标签样式优化 */
.preset-chip {
  background: #f3f4f6; 
  border: 1px solid transparent; 
  padding: 8px 16px; 
  border-radius: 12px;   /* 稍微减小圆角，显得更现代 */
  font-size: 13px; 
  color: #4b5563; 
  cursor: pointer; 
  line-height: 1.5;
  transition: all 0.2s ease;
  
  /* 文本处理：太长的自动省略，防止破坏布局，或者你可以去掉这三行让它完全展示 */
  max-width: 100%;
  text-align: left;
  white-space: normal;   /* 允许标签内文字换行 */
}

.preset-chip:hover { 
  border-color: #FF5E62; 
  color: #FF5E62; 
  background: #fff1f2; 
  transform: translateY(-1px); /* 悬浮微动效 */
  box-shadow: 0 2px 6px rgba(255, 94, 98, 0.15);
}

/* 5. 尺寸选择 - 保持网格但更紧凑 */
.size-grid { 
  display: grid; 
  grid-template-columns: repeat(3, 1fr); 
  gap: 12px; 
  margin-bottom: 24px; 
}

.size-card {
  border: 1px solid #e5e7eb; /* 边框变细 */
  padding: 12px;             /* 减小内边距 */
  border-radius: 12px; 
  text-align: center; 
  cursor: pointer; 
  background: white; 
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.size-card:hover {
  border-color: #ff9966;
}

.size-card.active { 
  border-color: #FF5E62; 
  background: #fff1f2; 
  color: #b91c1c; 
  box-shadow: inset 0 0 0 1px #FF5E62; /* 选中时加粗边框效果 */
}

.size-name { 
  font-weight: 700; 
  font-size: 14px; 
  display: block; 
  margin-bottom: 4px;
}
.size-detail {
  font-size: 12px;
  color: #9ca3af;
}
.size-card.active .size-detail {
  color: #ef4444;
}

/* 6. 结果展示区优化 */
.result-display {
  background: #f9fafb; /* 稍微深一点的背景区分 */
  border-radius: 16px; 
  min-height: 260px;
  display: flex; 
  align-items: center; 
  justify-content: center;
  border: 2px dashed #e5e7eb; 
  position: relative;
  margin-bottom: 10px;
}
.image-wrapper img { max-width: 100%; max-height: 350px; border-radius: 12px; }
.img-actions button {
  background: rgba(255,255,255,0.9); color: #333; border: none; padding: 10px 20px;
  border-radius: 24px; cursor: pointer; font-weight: 600; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.image-input-bar textarea {
  flex: 1; border: 2px solid #f3f4f6; border-radius: 20px; padding: 16px;
  resize: none; outline: none; font-size: 15px; font-family: inherit;
}
.image-input-bar textarea:focus { border-color: #FF5E62; }
.magic-btn {
  background: linear-gradient(135deg, #FF9966, #FF5E62); color: white;
  border: none; border-radius: 28px; padding: 0 32px; font-weight: 600; cursor: pointer; height: 56px;
}

/* 动画 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.modal-pop-enter-active { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.modal-pop-leave-active { transition: all 0.2s ease-in; }
.modal-pop-enter-from { opacity: 0; transform: translate(-50%, -45%) scale(0.95); }
.scale-fade-enter-active, .scale-fade-leave-active { transition: all 0.3s; }
.scale-fade-enter-from, .scale-fade-leave-to { opacity: 0; transform: scale(0); }

/* Markdown & Loading */
:deep(.markdown-body p) { margin: 0 0 10px 0; }
:deep(.markdown-body pre) { background: #2d2d2d; padding: 16px; border-radius: 12px; color: #fff; }
.loading-bubble .dot {
  display: inline-block; width: 6px; height: 6px; background: #9ca3af;
  border-radius: 50%; margin: 0 3px; animation: bounce 1.4s infinite ease-in-out both;
}
.loading-bubble .dot:nth-child(1) { animation-delay: -0.32s; }
.loading-bubble .dot:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
.spinner {
  width: 40px; height: 40px; border: 4px solid #e5e7eb;
  border-top-color: #FF5E62; border-radius: 50%; animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>