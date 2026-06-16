<template>
  <div class="testcases-container">
    <!-- 工具栏 -->
    <el-card class="toolbar-card">
      <div class="toolbar">
        <div class="toolbar-left">
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            新建用例
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
          
          <el-select v-model="filters.priority" placeholder="优先级" clearable style="width: 120px">
            <el-option label="P0" value="P0" />
            <el-option label="P1" value="P1" />
            <el-option label="P2" value="P2" />
            <el-option label="P3" value="P3" />
          </el-select>
          
          <el-select v-model="filters.status" placeholder="状态" clearable style="width: 120px">
            <el-option label="草稿" value="draft" />
            <el-option label="就绪" value="ready" />
            <el-option label="已废弃" value="deprecated" />
          </el-select>
          
          <el-input
            v-model="filters.keyword"
            placeholder="搜索用例名称"
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
    
    <!-- 用例表格 -->
    <el-card>
      <el-table
        v-loading="loading"
        :data="testCases"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="name" label="用例名称" min-width="200">
          <template #default="{ row }">
            <el-link type="primary" @click="handleEdit(row)">{{ row.name }}</el-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="module" label="模块" width="120" />
        
        <el-table-column prop="priority" label="优先级" width="80">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)" size="small">
              {{ row.priority }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="platform" label="平台" width="80">
          <template #default="{ row }">
            <el-tag size="small">{{ row.platform }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="steps.length" label="步骤数" width="80" />
        
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
            <el-button type="primary" link size="small" @click="handleRun(row)">
              执行
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
    
    <!-- 用例编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      destroy-on-close
    >
      <TestCaseForm
        v-if="dialogVisible"
        :data="currentCase"
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
import { testcaseApi, TestCase } from '@/api/testcase'
import TestCaseForm from './components/TestCaseForm.vue'

const loading = ref(false)
const testCases = ref<TestCase[]>([])
const selectedCases = ref<TestCase[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const currentCase = ref<TestCase | null>(null)

const filters = reactive({
  platform: '',
  priority: '',
  status: '',
  keyword: '',
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

const getPriorityType = (priority: string) => {
  const map: Record<string, string> = {
    P0: 'danger',
    P1: 'warning',
    P2: '',
    P3: 'info',
  }
  return map[priority] || 'info'
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    draft: 'info',
    ready: 'success',
    deprecated: 'danger',
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    draft: '草稿',
    ready: '就绪',
    deprecated: '已废弃',
  }
  return map[status] || status
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await testcaseApi.getList({
      page: pagination.page,
      page_size: pagination.pageSize,
      ...filters,
    })
    testCases.value = res.items
    pagination.total = res.total
  } catch (error) {
    console.error('获取用例列表失败:', error)
  } finally {
    loading.value = false
  }
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

const handleSelectionChange = (selection: TestCase[]) => {
  selectedCases.value = selection
}

const handleCreate = () => {
  dialogTitle.value = '新建用例'
  currentCase.value = null
  dialogVisible.value = true
}

const handleEdit = (row: TestCase) => {
  dialogTitle.value = '编辑用例'
  currentCase.value = { ...row }
  dialogVisible.value = true
}

const handleRun = (row: TestCase) => {
  ElMessage.info(`准备执行用例: ${row.name}`)
  // TODO: 跳转到执行页面
}

const handleDelete = async (row: TestCase) => {
  try {
    await ElMessageBox.confirm('确定要删除该用例吗？', '提示', {
      type: 'warning',
    })
    await testcaseApi.delete(row.id)
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
  try {
    if (currentCase.value?.id) {
      await testcaseApi.update(currentCase.value.id, data)
      ElMessage.success('更新成功')
    } else {
      await testcaseApi.create(data)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    console.error('保存失败:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.testcases-container {
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
  
  .pagination {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
