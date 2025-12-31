import request from '@/utils/request'

// 获取用户订单列表
export const getUserOrders = (params) => {
  return request.get('/api/user/orders', { params })
}

// 创建订单
export const createOrder = (data) => {
  return request.post('/api/user/orders', data)
}

// 搜索商品
export const searchProducts = (data) => {
  return request.post('/api/user/search', data)
}

// 获取个性化推荐
export const getRecommendations = (params) => {
  return request.get('/api/user/recommendations', { params })
}
