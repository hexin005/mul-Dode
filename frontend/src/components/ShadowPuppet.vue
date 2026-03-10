<template>
  <div class="container">
    <video ref="video" class="input_video" autoplay playsinline></video>
    <canvas ref="canvas" class="output_canvas" width="640" height="480"></canvas>
    <div v-if="loading" class="loader">AI 模型加载中...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { PoseLandmarker, FilesetResolver } from "@mediapipe/tasks-vision";

const video = ref(null);
const canvas = ref(null);
const loading = ref(true);

let poseLandmarker;

const initAI = async () => {
  const vision = await FilesetResolver.forVisionTasks(
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
  );
  poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath: `https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task`,
      delegate: "GPU"
    },
    runningMode: "VIDEO"
  });
  loading.value = false;
  startCamera();
};

const startCamera = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.value.srcObject = stream;
  video.value.onloadedmetadata = () => {
    renderLoop();
  };
};

const renderLoop = async () => {
  const ctx = canvas.value.getContext('2d');
  
  if (video.value.currentTime !== lastVideoTime) {
    const results = poseLandmarker.detectForVideo(video.value, performance.now());
    
    ctx.clearRect(0, 0, canvas.value.width, canvas.value.height);
    
    if (results.landmarks) {
      drawPuppet(ctx, results.landmarks[0]);
    }
  }
  requestAnimationFrame(renderLoop);
};

// 绘制皮影的关键函数
const drawPuppet = (ctx, landmarks) => {
  if (!landmarks) return;

  // 1. 设置样式（红色皮影风）
  ctx.strokeStyle = "#b30000";
  ctx.lineWidth = 8;
  ctx.lineJoin = "round";

  // 2. 映射关键点 (MediaPipe 坐标是 0-1)
  const getXY = (id) => ({
    x: landmarks[id].x * canvas.value.width,
    y: landmarks[id].y * canvas.value.height
  });

  // 3. 绘制躯干和四肢 (简化版皮影骨架)
  const joints = [
    [11, 12], [11, 23], [12, 24], [23, 24], // 躯干
    [11, 13], [13, 15], // 左臂
    [12, 14], [14, 16], // 右臂
    [23, 25], [25, 27], // 左腿
    [24, 26], [26, 28]  // 右腿
  ];

  joints.forEach(([s, e]) => {
    const start = getXY(s);
    const end = getXY(e);
    ctx.beginPath();
    ctx.moveTo(start.x, start.y);
    ctx.lineTo(end.x, end.y);
    ctx.stroke();
  });

  // 绘制头部 (以鼻子 0 为中心)
  const nose = getXY(0);
  ctx.fillStyle = "#b30000";
  ctx.beginPath();
  ctx.arc(nose.x, nose.y - 20, 30, 0, Math.PI * 2);
  ctx.fill();
};

onMounted(() => {
  initAI();
});
</script>

<style scoped>
.input_video { display: none; } /* 隐藏原始摄像头 */
.output_canvas { border: 2px solid #333; background: #f4f1de; } /* 仿宣纸背景 */
</style>