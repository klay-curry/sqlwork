<template>
  <div class="product-list">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="searchForm.keyword" placeholder="商品名称或描述" clearable />
        </el-form-item>
        <el-form-item label="类目">
          <el-input v-model="searchForm.category" placeholder="商品类目" clearable />
        </el-form-item>
        <el-form-item label="价格">
          <el-input v-model.number="searchForm.min_price" placeholder="最低价" style="width: 100px" />
          -
          <el-input v-model.number="searchForm.max_price" placeholder="最高价" style="width: 100px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20" v-loading="loading">
      <el-col :span="6" v-for="product in products" :key="product.product_id">
        <el-card class="product-card" shadow="hover">
          <div class="product-info">
            <h3>{{ product.name }}</h3>
            <p class="description">{{ product.description }}</p>
            <div class="price">¥{{ product.price }}</div>
            <p class="merchant">商家: {{ product.merchant_name }}</p>
            <p class="category">类目: {{ product.category }}</p>
            <el-button type="primary" @click="showOrderDialog(product)" style="width: 100%">
              立即购买
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="!loading && products.length === 0" description="暂无商品" />

    <!-- 下单对话框 -->
    <el-dialog v-model="orderDialogVisible" title="下单" width="500px">
      <el-form :model="orderForm" label-width="80px">
        <el-form-item label="商品">
          <el-input v-model="currentProduct.name" disabled />
        </el-form-item>
        <el-form-item label="单价">
          <el-input v-model="currentProduct.price" disabled />
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number v-model="orderForm.quantity" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="总价">
          <el-input :value="totalPrice" disabled />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="orderDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreateOrder" :loading="orderLoading">
          确认下单
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { searchProducts } from '@/api/user'
import { createOrder } from '@/api/user'
import { ElMessage } from 'element-plus'

const loading = ref(false)
const products = ref([])

const searchForm = reactive({
  keyword: '',
  category: '',
  min_price: null,
  max_price: null
})

const orderDialogVisible = ref(false)
const orderLoading = ref(false)
const currentProduct = ref({})
const orderForm = reactive({
  quantity: 1
})

const totalPrice = computed(() => {
  return (currentProduct.value.price * orderForm.quantity).toFixed(2)
})

const loadProducts = async () => {
  loading.value = true
  try {
    const response = await searchProducts({
      keyword: searchForm.keyword || undefined,
      category: searchForm.category || undefined,
      min_price: searchForm.min_price || undefined,
      max_price: searchForm.max_price || undefined
    })
    products.value = response.data || []
  } catch (error) {
    console.error('加载商品失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  loadProducts()
}

const handleReset = () => {
  searchForm.keyword = ''
  searchForm.category = ''
  searchForm.min_price = null
  searchForm.max_price = null
  loadProducts()
}

const showOrderDialog = (product) => {
  currentProduct.value = product
  orderForm.quantity = 1
  orderDialogVisible.value = true
}

const handleCreateOrder = async () => {
  orderLoading.value = true
  try {
    await createOrder({
      product_id: currentProduct.value.product_id,
      quantity: orderForm.quantity
    })
    ElMessage.success('下单成功')
    orderDialogVisible.value = false
  } catch (error) {
    console.error('下单失败:', error)
  } finally {
    orderLoading.value = false
  }
}

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.product-list {
  padding: 0;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
}

.product-card {
  margin-bottom: 20px;
  height: 320px;
}

.product-info h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.description {
  color: #909399;
  font-size: 13px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.price {
  color: #f56c6c;
  font-size: 22px;
  font-weight: bold;
  margin: 10px 0;
}

.merchant, .category {
  font-size: 12px;
  color: #606266;
  margin: 5px 0;
}
</style>
