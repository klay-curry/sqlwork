import request from '@/utils/request'

// 获取商家商品列表
export const getProducts = (params) => {
  return request.get('/api/merchant/products', { params })
}

// 创建商品
export const createProduct = (data) => {
  return request.post('/api/merchant/products', data)
}

// 更新商品
export const updateProduct = (id, data) => {
  return request.put(`/api/merchant/products/${id}`, data)
}

// 删除商品
export const deleteProduct = (id) => {
  return request.delete(`/api/merchant/products/${id}`)
}

// 获取商家订单列表
export const getOrders = (params) => {
  return request.get('/api/merchant/orders', { params })
}

// 获取销售趋势
export const getSalesTrend = (params) => {
  return request.get('/api/merchant/sales/trend', { params })
}

// 获取Top商品
export const getTopProducts = (params) => {
  return request.get('/api/merchant/products/top', { params })
}

// 获取类目分布
export const getCategoryDistribution = () => {
  return request.get('/api/merchant/category/distribution')
}

// 获取AI建议
export const getAISuggestions = () => {
  return request.get('/api/merchant/ai/suggestions')
}
