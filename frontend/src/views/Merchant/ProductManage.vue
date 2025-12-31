<template>
  <div class="product-manage">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>商品管理</h3>
          <el-button type="primary" @click="showAddDialog">新增商品</el-button>
        </div>
      </template>

      <el-table :data="products" v-loading="loading" style="width: 100%">
        <el-table-column prop="product_id" label="ID" width="60" />
        <el-table-column prop="name" label="商品名称" min-width="150" />
        <el-table-column label="价格" width="100">
          <template #default="{ row }">
            ¥{{ row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="80" />
        <el-table-column prop="sales_count" label="销量" width="80" />
        <el-table-column prop="category" label="类目" width="120" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
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
        @size-change="loadProducts"
        @current-change="loadProducts"
        style="margin-top: 20px; justify-content: center;"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="productForm" :rules="rules" ref="productFormRef" label-width="100px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="productForm.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="商品描述" prop="description">
          <el-input 
            v-model="productForm.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入商品描述"
          />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="productForm.price" :min="0" :step="0.01" :precision="2" />
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input-number v-model="productForm.stock" :min="0" />
        </el-form-item>
        <el-form-item label="类目" prop="category">
          <el-input v-model="productForm.category" placeholder="请输入商品类目" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="productForm.status">
            <el-radio :label="1">上架</el-radio>
            <el-radio :label="0">下架</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getProducts, createProduct, updateProduct, deleteProduct } from '@/api/merchant'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const submitLoading = ref(false)
const products = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const dialogVisible = ref(false)
const dialogTitle = ref('新增商品')
const isEdit = ref(false)
const currentProductId = ref(null)

const productFormRef = ref(null)
const productForm = reactive({
  name: '',
  description: '',
  price: 0,
  stock: 0,
  category: '',
  status: 1
})

const rules = {
  name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入商品描述', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  stock: [{ required: true, message: '请输入库存', trigger: 'blur' }],
  category: [{ required: true, message: '请输入类目', trigger: 'blur' }]
}

const loadProducts = async () => {
  loading.value = true
  try {
    const response = await getProducts({
      page: currentPage.value,
      size: pageSize.value
    })
    products.value = response.data.items || []
    total.value = response.data.total || 0
  } catch (error) {
    console.error('加载商品失败:', error)
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  isEdit.value = false
  dialogTitle.value = '新增商品'
  resetForm()
  dialogVisible.value = true
}

const showEditDialog = (product) => {
  isEdit.value = true
  dialogTitle.value = '编辑商品'
  currentProductId.value = product.product_id
  
  Object.assign(productForm, {
    name: product.name,
    description: product.description || '',
    price: product.price,
    stock: product.stock,
    category: product.category,
    status: product.status
  })
  
  dialogVisible.value = true
}

const resetForm = () => {
  productForm.name = ''
  productForm.description = ''
  productForm.price = 0
  productForm.stock = 0
  productForm.category = ''
  productForm.status = 1
  productFormRef.value?.clearValidate()
}

const handleSubmit = async () => {
  if (!productFormRef.value) return
  
  await productFormRef.value.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (isEdit.value) {
          await updateProduct(currentProductId.value, productForm)
          ElMessage.success('更新成功')
        } else {
          await createProduct(productForm)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        loadProducts()
      } catch (error) {
        console.error('提交失败:', error)
      } finally {
        submitLoading.value = false
      }
    }
  })
}

const handleDelete = async (product) => {
  try {
    await ElMessageBox.confirm('确定要删除该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteProduct(product.product_id)
    ElMessage.success('删除成功')
    loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

onMounted(() => {
  loadProducts()
})
</script>

<style scoped>
.product-manage {
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
