// src/services/userApi.js
import axios from 'axios';

// 创建用户请求专属axios实例，配置跨域携带Cookie
const userAxios = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000,
  withCredentials: true, // 核心：允许跨域携带Cookie
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
});

// 请求拦截器（可选，统一处理请求头）
userAxios.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器（统一处理错误）
userAxios.interceptors.response.use(
  (response) => {
    return response.data; // 直接返回响应体，简化前端处理
  },
  (error) => {
    const msg = error.response?.data?.msg || '网络错误，请稍后重试';
    alert(msg);
    return Promise.reject(error);
  }
);

// 发送验证码
export const sendCode = (email) => {
  return userAxios.post('/user/send-code', { email });
};

// 用户注册
export const userRegister = (data) => {
  return userAxios.post('/user/register', data);
};

// 用户登录
export const userLogin = (data) => {
  return userAxios.post('/user/login', data);
};