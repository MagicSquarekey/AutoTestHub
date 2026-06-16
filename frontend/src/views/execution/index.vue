<template>
  <div class="execution-container">
    <!-- 快速执行区 -->
    <el-card class="quick-execute-card">
      <template #header>
        <span>快速执行</span>
      </template>
      
      <el-form :model="executeForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="选择用例">
              <el-select
                v-model="executeForm.test_case_ids"
                multiple
                filterable
                placeholder="选择要执行的用例"
                style="width: 100%"
              >
                <el-option
                  v-for="item in testCaseOptions"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="8">
            <el-form-item label="运行模式">
              <el-radio-group v-model="executeForm.run_mode">
                <el-radio value="single">顺序执行</el-radio>
                <el-radio value="parallel">并行执行</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          
          <el-col :span="8">
            <el-form-item label="浏览器">
              <el-select v-model="executeForm.browser" placeholder="选择浏览器">
                <el-option label="Chromium" value="chromium" />
                <el-option label="Firefox" value="firefox" />
                <el-option label="WebKit" value="webkit" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="任务名称">
              <el-input v-model="executeForm.name" placeholder="输入任务名称" />
            </el-form-item>
          </el-col>
          
          <el-col :span="8">
            <el-form-item label="失败重试">
              <el-input-number v-model="executeForm.retry_count" :min="0" :max="5" />
            </el-form-item>
          </el-col>
          
          <el-col :span="8">
            <el-form-item>
              <el-button type="primary" @click="handleExecute" :loading="executing">
                <el-icon><VideoPlay /></el-icon>
                开始执行
              </el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
    
    <!-- 执行历史 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>执行历史</span>
          <el-button @click="fetchData" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="executions"
        border
        stripe
      >
        <el-table-column prop="name" label="任务名称" min-width="150" />
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="platform" label="平台" width="80" />
        
        <el-table-column label="进度" width="150">
          <template #default="{ row }">
            <el-progress
              :percentage="getProgress(row)"
              :status="getProgressStatus(row.status)"
              :stroke-width="10"
            />
          </template>
        </el-table-column>
        
        <el-table-column prop="total_cases" label="总用例" width="80" />
        <el-table-column prop="passed_cases" label="通过" width="80">
          <template #default="{ row }">
            <span class="text-success">{{ row.passed_cases }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="failed_cases" label="失败" width="80">
          <template #default="{ row }">
            <span :class="{ 'text-danger': row.failed_cases > 0 }">{{ row.failed_cases }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="duration" label="耗时" width="100">
          <template #default="{ row }">
            {{ formatDuration(row.duration) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="执行时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleViewDetail(row)">
              详情
            </el-button>
            <el-button type="primary" link size="small" @click="handleViewLogs(row)">
              日志
            </el-button>
            <el-button
              v-if="row.status === 'running'"
              type="warning"
              link
              size="small"
              @click="handleStop(row)"
            >
              停止
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
    
    <!-- 日志对话框 -->
    <el-dialog v-model="logDialogVisible" title="执行日志" width="800px">
      <div class="log-container">
        <div v-for="(log, index) in currentLogs" :key="index" class="log-item" :class="'log-' + log.level">
          <span class="log-time">{{ formatTime(log.timestamp) }}</span>
          <span class="log-level">[{{ log.level.toUpperCase() }}]</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
        <el-empty v-if="currentLogs.length === 0" description="暂无日志" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

const loading = ref(false)
const executing = ref(false)
const executions = ref([])
const testCaseOptions = ref([])
const logDialogVisible = ref(false)
const currentLogs = ref([])

const executeForm = reactive({
  test_case_ids: [],
  name: '',
  run_mode: 'single',
  browser: 'chromium',
  retry_count: 0,
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
    cancelled: 'info',
    paused: 'warning',
  }
  return map[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    pending: '待执行',
    running: '执行中',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消',
    paused: '已暂停',
  }
  return map[status] || status
}

const getProgress = (row: any) => {
  if (!row.total_cases) return 0
  const completed = (row.passed_cases || 0) + (row.failed_cases || 0) + (row.skipped_cases || 0)
  return Math.round((completed / row.total_cases) * 100)
}

const getProgressStatus = (status: string) => {
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'exception'
  return undefined
}

const formatDuration = (seconds: number) => {
  if (!seconds) return '-'
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return minutes > 0 ? `${minutes}分${secs}秒` : `${secs}秒`
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

const fetchData = async () => {
  loading.value = true
  // TODO: 调用 API 获取执行历史
  setTimeout(() => {
    loading.value = false
  }, 500)
}

const handleExecute = async () => {
  if (executeForm.test_case_ids.length === 0) {
    ElMessage.warning('请选择要执行的用例')
    return
  }
  
  executing.value = true
  // TODO: 调用执行 API
  setTimeout(() => {
    executing.value = false
    ElMessage.success('执行任务已创建')
    fetchData()
  }, 1000)
}

const handleViewDetail = (row: any) => {
  // TODO: 查看执行详情
  ElMessage.info('查看详情功能开发中')
}

const handleViewLogs = (row: any) => {
  // TODO: 获取执行日志
  currentLogs.value = []
  logDialogVisible.value = true
}

const handleStop = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要停止该任务吗？', '提示', {
      type: 'warning',
    })
    // TODO: 调用停止 API
    ElMessage.success('任务已停止')
    fetchData()
  } catch (error) {
    // 取消
  }
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除该执行记录吗？', '提示', {
      type: 'warning',
    })
    // TODO: 调用删除 API
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    // 取消
  }
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  fetchData()
}

const handlePageChange = (page: number) => {
  pagination.page = page
  fetchData()
}

onMounted(() => {
  fetchData()
  // TODO: 获取用例选项
})
</script>

<style scoped lang="scss">
.execution-container {
  .quick-execute-card {
    margin-bottom: 16px;
  }
  
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .text-success {
    color: #67c23a;
    font-weight: 600;
  }
  
  .text-danger {
    color: #f56c6c;
    font-weight: 600;
  }
  
  .pagination {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
  
  .log-container {
    max-height: 400px;
    overflow-y: auto;
    background: #1e1e1e;
    padding: 16px;
    border-radius: 4px;
  }
  
  .log-item {
    font-family: 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.6;
    color: #d4d4d4;
    
    .log-time {
      color: #6a9955;
      margin-right: 8px;
    }
    
    .log-level {
      margin-right: 8px;
      font-weight: bold;
    }
    
    &.log-info .log-level {
      color: #4fc1ff;
    }
    
    &.log-warning .log-level {
      color: #cca700;
    }
    
    &.log-error .log-level {
      color: #f44747;
    }
  }
}
</style>
