<template>
  <div class="dashboard-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #409eff">
            <el-icon size="28"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalCases }}</div>
            <div class="stat-label">测试用例</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #67c23a">
            <el-icon size="28"><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.passRate }}%</div>
            <div class="stat-label">通过率</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #e6a23c">
            <el-icon size="28"><VideoPlay /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalExecutions }}</div>
            <div class="stat-label">执行次数</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background-color: #909399">
            <el-icon size="28"><Pointer /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalElements }}</div>
            <div class="stat-label">元素数量</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <span>执行趋势</span>
          </template>
          <div class="chart-placeholder">
            <el-empty description="暂无数据" />
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <span>失败分布</span>
          </template>
          <div class="chart-placeholder">
            <el-empty description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 最近执行 -->
    <el-card class="recent-card">
      <template #header>
        <div class="card-header">
          <span>最近执行</span>
          <el-button type="primary" link>查看全部</el-button>
        </div>
      </template>
      
      <el-table :data="recentExecutions" stripe>
        <el-table-column prop="name" label="任务名称" min-width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="total_cases" label="用例数" width="100" />
        <el-table-column prop="passed_cases" label="通过" width="80" />
        <el-table-column prop="failed_cases" label="失败" width="80">
          <template #default="{ row }">
            <span :class="{ 'text-danger': row.failed_cases > 0 }">
              {{ row.failed_cases }}
            </span>
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
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import dayjs from 'dayjs'

const stats = ref({
  totalCases: 0,
  passRate: 0,
  totalExecutions: 0,
  totalElements: 0,
})

const recentExecutions = ref([])

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
    cancelled: 'info',
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
  }
  return map[status] || status
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

onMounted(() => {
  // TODO: 获取统计数据
})
</script>

<style scoped lang="scss">
.dashboard-container {
  .stat-cards {
    margin-bottom: 20px;
  }
  
  .stat-card {
    :deep(.el-card__body) {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 20px;
    }
  }
  
  .stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
  }
  
  .stat-info {
    .stat-value {
      font-size: 28px;
      font-weight: 600;
      color: #303133;
    }
    
    .stat-label {
      font-size: 14px;
      color: #909399;
      margin-top: 4px;
    }
  }
  
  .chart-row {
    margin-bottom: 20px;
  }
  
  .chart-card {
    .chart-placeholder {
      height: 300px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
  
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .text-danger {
    color: #f56c6c;
    font-weight: 600;
  }
}
</style>
