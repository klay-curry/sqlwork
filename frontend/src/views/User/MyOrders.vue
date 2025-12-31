<template>
  <div class="my-orders">
    <el-card>
      <template #header>
        <h3>我的订单</h3>
      </template>
      
      <el-table :data="orders" v-loading="loading" style="width: 100%">
        <el-table-column prop="order_id" label="订单号" width="80" />
        <el-table-column prop="product_name" label="商品名称" />
        <el-table-column prop="merchant_name" label="商家" width="120" />
        <el-table-column prop="quantity" label="数量" width="80" />
        <el-table-column label="单价" width="100">
          <template #default="{ row }">
            ¥{{ row.unit_price }}
          </template>
        </el-table-column>
        <el-table-column label="总价" width="100">
          <template #default="{ row }">
            ¥{{ row.total_amount }}
          </template>
        </el-table-column>
        <el-table-column prop="order_time" label="下单时间" width="180" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadOrders"
        @current-change="loadOrders"
        style="margin-top: 20px; justify-content: center;"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserOrders } from '@/api/user'

const loading = ref(false)
const orders = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const loadOrders = async () => {
  loading.value = true
  try {
    const response = await getUserOrders({
      page: currentPage.value,
      size: pageSize.value
    })
    orders.value = response.data.items || []
    total.value = response.data.total || 0
  } catch (error) {
    console.error('加载订单失败:', error)
  } finally {
    loading.value = false
  }
}

const getStatusType = (status) => {
  const map = {
    'pending': 'warning',
    'paid': 'success',
    'shipped': 'info',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'pending': '待支付',
    'paid': '已支付',
    'shipped': '已发货',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return map[status] || status
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.my-orders {
  padding: 0;
}
</style>
