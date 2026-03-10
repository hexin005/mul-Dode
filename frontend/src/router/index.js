import { createRouter, createWebHistory } from 'vue-router'

// 导入一体化组件
const LoginRegister = () => import('../components/pages/LoginRegister.vue')
const UserCenter = () => import('../components/pages/UserCenter.vue')

// 基础页面组件
const Page1 = () => import('../components/pages/Page1.vue')
const Page2 = () => import('../components/pages/Page2.vue')
const Page3 = () => import('../components/pages/Page3.vue')
const Page4 = () => import('../components/pages/Page4.vue')
const Page5 = () => import('../components/pages/Page5.vue')
const Page6 = () => import('../components/pages/Page6.vue')
const ProvinceDetail = () => import('../components/pages/ProvinceDetail.vue')

// 路由配置
const routes = [
  { path: '/', redirect: '/page1' },
  { path: '/page1', name: 'Page1', component: Page1 },
  { path: '/page2', name: 'Page2', component: Page2 },
  { path: '/page3', name: 'Page3', component: Page3 },
  { path: '/page4', name: 'Page4', component: Page4 },
  { path: '/page5', name: 'Page5', component: Page5 },
  { path: '/page6', name: 'Page6', component: Page6 },
  { 
    path: '/school/:schoolName/:provinceName', 
    name: 'ProvinceDetail', 
    component: ProvinceDetail, 
    props: true 
  },
  // 登录/注册复用同一个组件
  { path: '/login', name: 'Login', component: LoginRegister },
  { path: '/register', name: 'Register', component: LoginRegister },
  { path: '/user-center', name: 'UserCenter', component: UserCenter }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router