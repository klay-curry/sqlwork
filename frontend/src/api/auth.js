import request from '@/utils/request'

// 用户注册
export const registerUser = (data) => {
  return request.post('/api/auth/register/user', data)
}

// 商家注册
export const registerMerchant = (data) => {
  return request.post('/api/auth/register/merchant', data)
}

// 统一登录
export const login = (data) => {
  return request.post('/api/auth/login', data)
}
