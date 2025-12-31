<template>
  <div class="dashboard">
    <!-- 销售趋势 -->
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card v-loading="salesLoading">
          <template #header>
            <div class="card-header">
              <h3>销售趋势</h3>
              <el-select v-model="salesDays" @change="loadSalesTrend" style="width: 120px">
                <el-option label="最近7天" :value="7" />
                <el-option label="最近30天" :value="30" />
                <el-option label="最近90天" :value="90" />
              </el-select>
            </div>
          </template>
          <SalesTrendChart :data="salesTrendData" />
        </el-card>
      </el-col>
    </el-row>

    <!-- Top商品和类目分布 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card v-loading="topProductsLoading">
          <template #header>
            <h3>热销商品Top10</h3>
          </template>
          <TopProductsChart :data="topProductsData" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card v-loading="categoryLoading">
          <template #header>
            <h3>类目销售分布</h3>
          </template>
          <CategoryChart :data="categoryData" />
        </el-card>
      </el-col>
    </el-row>

    <!-- AI经营建议 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card v-loading="suggestionsLoading">
          <template #header>
            <div class="card-header">
              <h3>AI经营建议</h3>
              <el-button size="small" @click="loadSuggestions">刷新建议</el-button>
            </div>
          </template>
          <el-table :data="suggestions" style="width: 100%">
            <el-table-column prop="product_name" label="商品名称" />
            <el-table-column prop="suggestion" label="建议内容" />
            <el-table-column prop="priority" label="优先级" width="120">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)">
                  {{ getPriorityText(row.priority) }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="suggestions.length === 0" description="暂无建议" />
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

const salesLoading = ref(false)
const topProductsLoading = ref(false)
const categoryLoading = ref(false)
const suggestionsLoading = ref(false)

const salesDays = ref(30)
const salesTrendData = ref({ dates: [], sales: [] })
const topProductsData = ref([])
const categoryData = ref([])
const suggestions = ref([])

const loadSalesTrend = async () => {
  salesLoading.value = true
  try {
    const response = await getSalesTrend({ days: salesDays.value })
    salesTrendData.value = response.data || { dates: [], sales: [] }
  } catch (error) {
    console.error('加载销售趋势失败:', error)
  } finally {
    salesLoading.value = false
  }
}

const loadTopProducts = async () => {
  topProductsLoading.value = true
  try {
    const response = await getTopProducts({ limit: 10 })
    topProductsData.value = response.data || []
  } catch (error) {
    console.error('加载Top商品失败:', error)
  } finally {
    topProductsLoading.value = false
  }
}

const loadCategoryDistribution = async () => {
  categoryLoading.value = true
  try {
    const response = await getCategoryDistribution()
    categoryData.value = response.data || []
  } catch (error) {
    console.error('加载类目分布失败:', error)
  } finally {
    categoryLoading.value = false
  }
}

const loadSuggestions = async () => {
  suggestionsLoading.value = true
  try {
    const response = await getAISuggestions()
    suggestions.value = response.data.suggestions || []
  } catch (error) {
    console.error('加载AI建议失败:', error)
  } finally {
    suggestionsLoading.value = false
  }
}

const getPriorityType = (priority) => {
  const map = {
    'high': 'danger',
    'medium': 'warning',
    'low': 'info'
  }
  return map[priority] || 'info'
}

const getPriorityText = (priority) => {
  const map = {
    'high': '高',
    'medium': '中',
    'low': '低'
  }
  return map[priority] || priority
}

const loadAllData = async () => {
  await Promise.all([
    loadSalesTrend(),
    loadTopProducts(),
    loadCategoryDistribution(),
    loadSuggestions()
  ])
}

onMounted(() => {
  loadAllData()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
}
</style>
