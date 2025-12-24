# 前端实现指南

## 项目初始化

### 1. 创建Vue3项目
```bash
cd frontend
npm create vite@latest . -- --template vue
npm install
```

### 2. 安装依赖
```bash
npm install vue-router pinia element-plus axios echarts vue-echarts
```

### 3. 项目结构
```
frontend/
├── src/
│   ├── api/              # API调用
│   │   ├── auth.js       # 认证API
│   │   ├── merchant.js   # 商家API
│   │   ├── user.js       # 用户API
│   │   └── common.js     # 通用API
│   ├── components/       # 公共组件
│   │   ├── ProductCard.vue
│   │   ├── OrderList.vue
│   │   └── Charts/
│   │       ├── SalesTrendChart.vue
│   │       ├── TopProductsChart.vue
│   │       └── CategoryChart.vue
│   ├── views/            # 页面
│   │   ├── Login.vue
│   │   ├── User/
│   │   │   ├── ProductList.vue
│   │   │   ├── ProductDetail.vue
│   │   │   └── MyOrders.vue
│   │   └── Merchant/
│   │       ├── Dashboard.vue
│   │       ├── ProductManage.vue
│   │       └── OrderManage.vue
│   ├── router/
│   │   └── index.js      # 路由配置
│   ├── stores/
│   │   ├── auth.js       # 认证状态
│   │   └── cart.js       # 购物车（可选）
│   ├── utils/
│   │   └── request.js    # Axios封装
│   ├── App.vue
│   └── main.js
├── index.html
├── vite.config.js
└── package.json
```

---

## 核心代码示例

### 1. Axios封装 (utils/request.js)
```javascript
import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    ElMessage.error(error.response?.data?.detail || '请求失败')
    return Promise.reject(error)
  }
)

export default request
```

### 2. 路由配置 (router/index.js)
```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('@/views/User/Layout.vue'),
    children: [
      {
        path: 'products',
        component: () => import('@/views/User/ProductList.vue')
      },
      {
        path: 'recommendations',
        component: () => import('@/views/User/Recommendations.vue')
      },
      {
        path: 'orders',
        component: () => import('@/views/User/MyOrders.vue')
      }
    ]
  },
  {
    path: '/merchant',
    name: 'Merchant',
    component: () => import('@/views/Merchant/Layout.vue'),
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/Merchant/Dashboard.vue')
      },
      {
        path: 'products',
        component: () => import('@/views/Merchant/ProductManage.vue')
      },
      {
        path: 'orders',
        component: () => import('@/views/Merchant/OrderManage.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

### 3. 商家数据看板 (views/Merchant/Dashboard.vue)
```vue
<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <h2>销售趋势</h2>
          <SalesTrendChart :data="salesTrendData" />
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <h2>热销商品Top10</h2>
          <TopProductsChart :data="topProductsData" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <h2>类目销售分布</h2>
          <CategoryChart :data="categoryData" />
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <h2>AI经营建议</h2>
          <el-table :data="suggestions" style="width: 100%">
            <el-table-column prop="product_name" label="商品名称" />
            <el-table-column prop="suggestion" label="建议" />
            <el-table-column prop="priority" label="优先级">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)">
                  {{ row.priority }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSalesTrend, getTopProducts, getCategoryDistribution, getAISuggestions } from '@/api/merchant'
import SalesTrendChart from '@/components/Charts/SalesTrendChart.vue'
import TopProductsChart from '@/components/Charts/TopProductsChart.vue'
import CategoryChart from '@/components/Charts/CategoryChart.vue'

const salesTrendData = ref({})
const topProductsData = ref([])
const categoryData = ref([])
const suggestions = ref([])

const loadData = async () => {
  const [trend, top, category, ai] = await Promise.all([
    getSalesTrend(30),
    getTopProducts(10),
    getCategoryDistribution(),
    getAISuggestions()
  ])
  
  salesTrendData.value = trend.data
  topProductsData.value = top.data
  categoryData.value = category.data
  suggestions.value = ai.data.suggestions
}

const getPriorityType = (priority) => {
  const map = { high: 'danger', medium: 'warning', low: 'info' }
  return map[priority] || 'info'
}

onMounted(loadData)
</script>
```

### 4. ECharts折线图组件 (components/Charts/SalesTrendChart.vue)
```vue
<template>
  <v-chart :option="option" style="height: 400px;" />
</template>

<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, TitleComponent])

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const option = computed(() => ({
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: props.data.dates || []
  },
  yAxis: {
    type: 'value'
  },
  series: [{
    data: props.data.sales || [],
    type: 'line',
    smooth: true,
    itemStyle: {
      color: '#5470c6'
    }
  }]
}))
</script>
```

### 5. API调用示例 (api/merchant.js)
```javascript
import request from '@/utils/request'

export const getProducts = (params) => {
  return request.get('/api/merchant/products', { params })
}

export const getSalesTrend = (days) => {
  return request.get('/api/merchant/sales/trend', { params: { days } })
}

export const getTopProducts = (limit) => {
  return request.get('/api/merchant/products/top', { params: { limit } })
}

export const getCategoryDistribution = () => {
  return request.get('/api/merchant/category/distribution')
}

export const getAISuggestions = () => {
  return request.get('/api/merchant/ai/suggestions')
}
```

---

## 启动步骤

1. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

2. **启动开发服务器**
   ```bash
   npm run dev
   ```

3. **访问**
   - http://localhost:5173

4. **构建生产版本**
   ```bash
   npm run build
   ```

---

## 注意事项

1. **CORS配置**：后端已配置允许 `http://localhost:5173`
2. **Token存储**：使用 `localStorage.getItem('token')`
3. **路由守卫**：需要在router中添加认证检查
4. **响应式设计**：使用Element Plus的栅格系统

---

## 完整实现时间估计

- 基础框架搭建：2小时
- 商家数据看板：4小时
- 买家商品页面：3小时
- ECharts集成：2小时
- 测试调试：2小时
- **总计**：约13小时（1-2天）

---

此指南提供了完整的前端实现方案，可直接按照此文档完成前端开发。
# 前端实现指南

## 项目初始化

### 1. 创建Vue3项目
```bash
cd frontend
npm create vite@latest . -- --template vue
npm install
```

### 2. 安装依赖
```bash
npm install vue-router pinia element-plus axios echarts vue-echarts
```

### 3. 项目结构
```
frontend/
├── src/
│   ├── api/              # API调用
│   │   ├── auth.js       # 认证API
│   │   ├── merchant.js   # 商家API
│   │   ├── user.js       # 用户API
│   │   └── common.js     # 通用API
│   ├── components/       # 公共组件
│   │   ├── ProductCard.vue
│   │   ├── OrderList.vue
│   │   └── Charts/
│   │       ├── SalesTrendChart.vue
│   │       ├── TopProductsChart.vue
│   │       └── CategoryChart.vue
│   ├── views/            # 页面
│   │   ├── Login.vue
│   │   ├── User/
│   │   │   ├── ProductList.vue
│   │   │   ├── ProductDetail.vue
│   │   │   └── MyOrders.vue
│   │   └── Merchant/
│   │       ├── Dashboard.vue
│   │       ├── ProductManage.vue
│   │       └── OrderManage.vue
│   ├── router/
│   │   └── index.js      # 路由配置
│   ├── stores/
│   │   ├── auth.js       # 认证状态
│   │   └── cart.js       # 购物车（可选）
│   ├── utils/
│   │   └── request.js    # Axios封装
│   ├── App.vue
│   └── main.js
├── index.html
├── vite.config.js
└── package.json
```

---

## 核心代码示例

### 1. Axios封装 (utils/request.js)
```javascript
import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    ElMessage.error(error.response?.data?.detail || '请求失败')
    return Promise.reject(error)
  }
)

export default request
```

### 2. 路由配置 (router/index.js)
```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('@/views/User/Layout.vue'),
    children: [
      {
        path: 'products',
        component: () => import('@/views/User/ProductList.vue')
      },
      {
        path: 'recommendations',
        component: () => import('@/views/User/Recommendations.vue')
      },
      {
        path: 'orders',
        component: () => import('@/views/User/MyOrders.vue')
      }
    ]
  },
  {
    path: '/merchant',
    name: 'Merchant',
    component: () => import('@/views/Merchant/Layout.vue'),
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/Merchant/Dashboard.vue')
      },
      {
        path: 'products',
        component: () => import('@/views/Merchant/ProductManage.vue')
      },
      {
        path: 'orders',
        component: () => import('@/views/Merchant/OrderManage.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

### 3. 商家数据看板 (views/Merchant/Dashboard.vue)
```vue
<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <h2>销售趋势</h2>
          <SalesTrendChart :data="salesTrendData" />
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <h2>热销商品Top10</h2>
          <TopProductsChart :data="topProductsData" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <h2>类目销售分布</h2>
          <CategoryChart :data="categoryData" />
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <h2>AI经营建议</h2>
          <el-table :data="suggestions" style="width: 100%">
            <el-table-column prop="product_name" label="商品名称" />
            <el-table-column prop="suggestion" label="建议" />
            <el-table-column prop="priority" label="优先级">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)">
                  {{ row.priority }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSalesTrend, getTopProducts, getCategoryDistribution, getAISuggestions } from '@/api/merchant'
import SalesTrendChart from '@/components/Charts/SalesTrendChart.vue'
import TopProductsChart from '@/components/Charts/TopProductsChart.vue'
import CategoryChart from '@/components/Charts/CategoryChart.vue'

const salesTrendData = ref({})
const topProductsData = ref([])
const categoryData = ref([])
const suggestions = ref([])

const loadData = async () => {
  const [trend, top, category, ai] = await Promise.all([
    getSalesTrend(30),
    getTopProducts(10),
    getCategoryDistribution(),
    getAISuggestions()
  ])
  
  salesTrendData.value = trend.data
  topProductsData.value = top.data
  categoryData.value = category.data
  suggestions.value = ai.data.suggestions
}

const getPriorityType = (priority) => {
  const map = { high: 'danger', medium: 'warning', low: 'info' }
  return map[priority] || 'info'
}

onMounted(loadData)
</script>
```

### 4. ECharts折线图组件 (components/Charts/SalesTrendChart.vue)
```vue
<template>
  <v-chart :option="option" style="height: 400px;" />
</template>

<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, TitleComponent])

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const option = computed(() => ({
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: props.data.dates || []
  },
  yAxis: {
    type: 'value'
  },
  series: [{
    data: props.data.sales || [],
    type: 'line',
    smooth: true,
    itemStyle: {
      color: '#5470c6'
    }
  }]
}))
</script>
```

### 5. API调用示例 (api/merchant.js)
```javascript
import request from '@/utils/request'

export const getProducts = (params) => {
  return request.get('/api/merchant/products', { params })
}

export const getSalesTrend = (days) => {
  return request.get('/api/merchant/sales/trend', { params: { days } })
}

export const getTopProducts = (limit) => {
  return request.get('/api/merchant/products/top', { params: { limit } })
}

export const getCategoryDistribution = () => {
  return request.get('/api/merchant/category/distribution')
}

export const getAISuggestions = () => {
  return request.get('/api/merchant/ai/suggestions')
}
```

---

## 启动步骤

1. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

2. **启动开发服务器**
   ```bash
   npm run dev
   ```

3. **访问**
   - http://localhost:5173

4. **构建生产版本**
   ```bash
   npm run build
   ```

---

## 注意事项

1. **CORS配置**：后端已配置允许 `http://localhost:5173`
2. **Token存储**：使用 `localStorage.getItem('token')`
3. **路由守卫**：需要在router中添加认证检查
4. **响应式设计**：使用Element Plus的栅格系统

---

## 完整实现时间估计

- 基础框架搭建：2小时
- 商家数据看板：4小时
- 买家商品页面：3小时
- ECharts集成：2小时
- 测试调试：2小时
- **总计**：约13小时（1-2天）

---

此指南提供了完整的前端实现方案，可直接按照此文档完成前端开发。
