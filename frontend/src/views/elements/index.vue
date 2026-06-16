<template>
  <div class="elements-container">
    <!-- 工具栏 -->
    <el-card class="toolbar-card">
      <div class="toolbar">
        <div class="toolbar-left">
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            新建元素
          </el-button>
          <el-button @click="handleHealthCheck">
            <el-icon><CircleCheck /></el-icon>
            健康巡检
          </el-button>
          <el-button @click="handleImport">
            <el-icon><Upload /></el-icon>
            导入
          </el-button>
          <el-button @click="handleExport">
            <el-icon><Download /></el-icon>
            导出
          </el-button>
        </div>
        
        <div class="toolbar-right">
          <el-select v-model="filters.platform" placeholder="平台" clearable style="width: 120px">
            <el-option label="Web" value="web" />
            <el-option label="App" value="app" />
          </el-select>
          
          <el-select v-model="filters.status" placeholder="状态" clearable style="width: 120px">
            <el-option label="正常" value="normal" />
            <el-option label="失效" value="invalid" />
            <el-option label="待验证" value="pending" />
          </el-select>
          
          <el-input
            v-model="filters.keyword"
            placeholder="搜索元素名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>
    </el-card>
    
    <!-- 元素表格 -->
    <el-card>
      <el-table
        v-loading="loading"
        :data="elements"
        border
        stripe
      >
        <el-table-column prop="name" label="元素名称" min-width="150">
          <template #default="{ row }">
            <el-link type="primary" @click="handleEdit(row)">{{ row.name }}</el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="page_name" label="所属页面" width="120" />
        
        <el-table-column prop="platform" label="平台" width="80">
          <template #default="{ row }">
            <el-tag size="small">{{ row.platform }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="定位符" min-width="200">
          <template #default="{ row }">
            <div class="locator-list">
              <el-tag
                v-for="(locator, index) in getLocators(row)"
                :key="index"
                size="small"
                class="locator-tag"
                :type="locator.status === 'normal' ? '' : 'danger'"
              >
                {{ locator.type }}: {{ truncate(locator.value, 30) }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="used_count" label="使用次数" width="100" />
        
        <el-table-column prop="updated_at" label="更新时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.updated_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="primary" link size="small" @click="handleVerify(row)">
              验证
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
    
    <!-- 元素编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="700px"
      destroy-on-close
    >
      <ElementForm
        v-if="dialogVisible"
        :data="currentElement"
        @submit="handleFormSubmit"
        @cancel="dialogVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'
import ElementForm from './components/ElementForm.vue'

const loading = ref(false)
const elements = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const currentElement = ref(null)

const filters = reactive({
  platform: '',
  status: '',
  keyword: '',
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

const getLocators = (row: any) => {
  const locators = []
  if (row.locator_xpath) {
    locators.push({ type: 'xpath', value: row.locator_xpath, status: row.xpath_status || 'normal' })
  }
  if (row.locator_css) {
    locators.push({ type: 'css', value: row.locator_css, status: row.css_status || 'normal' })
  }
  if (row.locator_id) {
    locators.push({ type: 'id', value: row.locator_id, status: row.id_status || 'normal' })
  }
  if (row.locator_name) {
    locators.push({ type: 'name', value: row.locator_name, status: row.name_status || 'normal' })
  }
  return locators
}

const truncate = (str: string, len: number) => {
  if (!str) return ''
  return str.length > len ? str.substring(0, len) + '...' : str
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    normal: 'success',
    invalid: 'danger',
    pending: 'warning',
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    normal: '正常',
    invalid: '失效',
    pending: '待验证',
  }
  return map[status] || status
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

const fetchData = async () => {
  loading.value = true
  // TODO: 调用 API 获取元素列表
  setTimeout(() => {
    loading.value = false
  }, 500)
}

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  fetchData()
}

const handlePageChange = (page: number) => {
  pagination.page = page
  fetchData()
}

const handleCreate = () => {
  dialogTitle.value = '新建元素'
  currentElement.value = null
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogTitle.value = '编辑元素'
  currentElement.value = { ...row }
  dialogVisible.value = true
}

const handleVerify = (row: any) => {
  ElMessage.info(`验证元素: ${row.name}`)
  // TODO: 验证元素是否存在
}

const handleHealthCheck = () => {
  ElMessage.info('开始健康巡检...')
  // TODO: 执行全量健康巡检
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该元素吗？', '提示', {
      type: 'warning',
    })
    // TODO: 调用删除 API
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    // 取消删除
  }
}

const handleImport = () => {
  ElMessage.info('导入功能开发中')
}

const handleExport = () => {
  ElMessage.info('导出功能开发中')
}

const handleFormSubmit = async (data: any) => {
  // TODO: 调用保存 API
  ElMessage.success('保存成功')
  dialogVisible.value = false
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.elements-container {
  .toolbar-card {
    margin-bottom: 16px;
  }
  
  .toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .toolbar-left {
    display: flex;
    gap: 8px;
  }
  
  .toolbar-right {
    display: flex;
    gap: 8px;
  }
  
  .locator-list {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
  }
  
  .locator-tag {
    max-width: 100%;
  }
  
  .pagination {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
