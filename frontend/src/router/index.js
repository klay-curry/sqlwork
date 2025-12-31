import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/user',
    name: 'UserLayout',
    component: () => import('@/views/User/Layout.vue'),
    meta: { requiresAuth: true, role: 'user' },
    redirect: '/user/products',
    children: [
      {
        path: 'products',
        name: 'ProductList',
        component: () => import('@/views/User/ProductList.vue')
      },
      {
        path: 'recommendations',
        name: 'Recommendations',
        component: () => import('@/views/User/Recommendations.vue')
      },
      {
        path: 'orders',
        name: 'MyOrders',
        component: () => import('@/views/User/MyOrders.vue')
      }
    ]
  },
  {
    path: '/merchant',
    name: 'MerchantLayout',
    component: () => import('@/views/Merchant/Layout.vue'),
    meta: { requiresAuth: true, role: 'merchant' },
    redirect: '/merchant/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Merchant/Dashboard.vue')
      },
      {
        path: 'products',
        name: 'ProductManage',
        component: () => import('@/views/Merchant/ProductManage.vue')
      },
      {
        path: 'orders',
        name: 'OrderManage',
        component: () => import('@/views/Merchant/OrderManage.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')
  
  // 需要认证的路由
  if (to.meta.requiresAuth) {
    if (!token) {
      ElMessage.warning('请先登录')
      next('/login')
      return
    }
    
    // 检查角色权限
    if (to.meta.role && to.meta.role !== role) {
      ElMessage.error('没有权限访问该页面')
      next(false)
      return
    }
  }
  
  // 已登录用户访问登录页，重定向到对应首页
  if (to.path === '/login' && token) {
    if (role === 'user') {
      next('/user/products')
    } else if (role === 'merchant') {
      next('/merchant/dashboard')
    } else {
      next()
    }
    return
  }
  
  next()
})

export default router
