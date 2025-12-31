<template>
  <el-container class="layout-container">
    <el-header class="layout-header">
      <div class="header-content">
        <h2>网上商城 - 买家端</h2>
        <div class="header-actions">
          <span class="username">欢迎您</span>
          <el-button type="danger" size="small" @click="handleLogout">退出登录</el-button>
        </div>
      </div>
    </el-header>
    
    <el-container>
      <el-aside width="200px" class="layout-aside">
        <el-menu
          :default-active="activeMenu"
          router
          class="menu"
        >
          <el-menu-item index="/user/products">
            <el-icon><ShoppingCart /></el-icon>
            <span>商品列表</span>
          </el-menu-item>
          <el-menu-item index="/user/recommendations">
            <el-icon><Star /></el-icon>
            <span>为你推荐</span>
          </el-menu-item>
          <el-menu-item index="/user/orders">
            <el-icon><List /></el-icon>
            <span>我的订单</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ShoppingCart, Star, List } from '@element-plus/icons-vue'

const route = useRoute()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)

const handleLogout = () => {
  authStore.logout()
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.layout-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.username {
  font-size: 14px;
}

.layout-aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e4e7ed;
}

.menu {
  border: none;
  background-color: transparent;
}

.layout-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
