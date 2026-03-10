import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import * as api from './services'

const app = createApp(App)



// 使用路由
app.use(router)
// 挂载API服务
app.config.globalProperties.$api = api
// 挂载应用
app.mount('#app')