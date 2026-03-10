// AI服务API封装
// 注意：使用localhost而不是127.0.0.1，端口与后端保持一致
const API_BASE_URL = 'http://localhost:5000/api';
const API_TIMEOUT = 60000; // 60秒超时

// 封装fetch请求，添加超时和统一错误处理
async function fetchWithTimeout(url, options, timeout = API_TIMEOUT) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  
  try {
    console.log(`正在请求: ${url}`);
    console.log('请求选项:', options);
    
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    clearTimeout(id);
    
    console.log(`收到响应: ${response.status} ${response.statusText}`);
    
    if (!response.ok) {
      throw new Error(`HTTP错误! 状态码: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('响应数据:', data);
    return data;
  } catch (error) {
    clearTimeout(id);
    console.error('请求错误详情:', error);
    if (error.name === 'AbortError') {
      throw new Error('请求超时，请稍后重试');
    }
    if (error.name === 'TypeError') {
      throw new Error('网络连接失败，请检查服务是否运行');
    }
    throw error;
  }
}

// 生成图像API
export async function generateImage(prompt, size = '2K', model = 'model1') {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/generate_image`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt, size, model_name: model }) // 修复：model -> model_name
    });
    
    return response; // 直接返回完整响应
  } catch (error) {
    console.error('生成图像失败:', error);
    return { 
      success: false, 
      error: error.message || '生成图像失败，请检查网络连接或稍后重试',
      details: error.toString()
    };
  }
}

// 发送文本消息API
// 在api.js中添加后端状态检测
export async function checkBackendStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/models`, {
      method: 'GET',
      timeout: 5000 // 5秒超时
    });
    return response.ok;
  } catch (error) {
    return false;
  }
}

// 修改sendMessage函数，添加后端状态检查
export async function sendMessage(question, model = 'model1') {
  try {
    // 先检查后端状态
    const isBackendRunning = await checkBackendStatus();
    if (!isBackendRunning) {
      throw new Error('后端服务未启动，请先启动后端服务再使用AI功能');
    }
    
    const apiUrl = `${API_BASE_URL}/chat`;
    console.log(`发送消息到 ${apiUrl}`, { question, model });
    
    const response = await fetchWithTimeout(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: question, model_name: model }) // 修复：question -> message，model -> model_name
    });
    
    console.log('收到API响应:', response);
    return response; 
  } catch (error) {
    console.error('发送消息失败:', error);
    return { 
      success: false, 
      error: error.message || '发送消息失败',
      errorType: error.name || 'UnknownError',
      isNetworkError: error.name === 'AbortError' || error.name === 'TypeError',
      details: error.toString()
    };
  }
}

// 获取可用模型列表
export async function getAvailableModels() {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/models`);
    return response;
  } catch (error) {
    console.error('获取模型列表失败:', error);
    return { success: false, error: error.message };
  }
}

// 分析图像API（如果需要）
export async function analyzeImage(imageData) {
  try {
    const formData = new FormData();
    formData.append('image', imageData);
    
    const response = await fetchWithTimeout(`${API_BASE_URL}/analyze_image`, {
      method: 'POST',
      body: formData
    });
    
    return response;
  } catch (error) {
    console.error('分析图像失败:', error);
    return { success: false, error: error.message };
  }
}