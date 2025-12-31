import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi } from '@/api/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const role = ref(localStorage.getItem('role') || '')
  const userId = ref(localStorage.getItem('userId') || '')
  
  const isLoggedIn = () => {
    return !!token.value
  }
  
  const login = async (username, password, userRole) => {
    try {
      const response = await loginApi({
        username,
        password,
        role: userRole
      })
      
      if (response.access_token) {
        token.value = response.access_token
        role.value = userRole
        
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('role', userRole)
        
        ElMessage.success('登录成功')
        
        // 根据角色跳转
        if (userRole === 'user') {
          router.push('/user/products')
        } else if (userRole === 'merchant') {
          router.push('/merchant/dashboard')
        }
        
        return true
      }
    } catch (error) {
      console.error('登录失败:', error)
      return false
    }
  }
  
  const logout = () => {
    token.value = ''
    role.value = ''
    userId.value = ''
    
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('userId')
    
    ElMessage.success('已退出登录')
    router.push('/login')
  }
  
  return {
    token,
    role,
    userId,
    isLoggedIn,
    login,
    logout
  }
})
