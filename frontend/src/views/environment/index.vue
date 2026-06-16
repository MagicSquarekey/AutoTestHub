<template>
  <div class="environment-container">
    <!-- 系统信息 -->
    <el-card class="info-card">
      <template #header>
        <span>系统信息</span>
      </template>
      
      <el-descriptions :column="3" border>
        <el-descriptions-item label="操作系统">{{ systemInfo.os }} {{ systemInfo.os_version }}</el-descriptions-item>
        <el-descriptions-item label="Python 版本">{{ systemInfo.python_version }}</el-descriptions-item>
        <el-descriptions-item label="CPU 核心数">{{ systemInfo.cpu_count }}</el-descriptions-item>
        <el-descriptions-item label="内存使用">
          <el-progress
            :percentage="systemInfo.memory_percent"
            :format="() => formatSize(systemInfo.memory_available) + ' 可用'"
          />
        </el-descriptions-item>
        <el-descriptions-item label="磁盘使用">
          <el-progress
            :percentage="systemInfo.disk_percent"
            :format="() => formatSize(systemInfo.disk_free) + ' 可用'"
          />
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <!-- 驱动管理 -->
    <el-card class="driver-card">
      <template #header>
        <div class="card-header">
          <span>驱动管理</span>
          <el-button @click="checkDrivers" :loading="checkingDrivers">
            <el-icon><Refresh /></el-icon>
            检测驱动
          </el-button>
        </div>
      </template>
      
      <el-table :data="drivers" border>
        <el-table-column prop="name" label="驱动名称" width="150" />
        <el-table-column prop="version" label="版本" width="120">
          <template #default="{ row }">
            {{ row.version || '未安装' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'installed' ? 'success' : 'danger'">
              {{ row.status === 'installed' ? '已安装' : '未安装' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button
              v-if="row.status !== 'installed'"
              type="primary"
              size="small"
              @click="handleInstallDriver(row)"
            >
              安装
            </el-button>
            <el-button
              v-else
              type="primary"
              size="small"
              @click="handleUpdateDriver(row)"
            >
              更新
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 浏览器管理 -->
    <el-card class="browser-card">
      <template #header>
        <div class="card-header">
          <span>浏览器管理</span>
          <el-button @click="checkBrowsers" :loading="checkingBrowsers">
            <el-icon><Refresh /></el-icon>
            检测浏览器
          </el-button>
        </div>
      </template>
      
      <el-table :data="browsers" border>
        <el-table-column prop="name" label="浏览器" width="150" />
        <el-table-column prop="version" label="版本" width="120">
          <template #default="{ row }">
            {{ row.version || '未安装' }}
          </template>
        </el-table-column>
        <el-table-column prop="is_default" label="默认" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.is_default" type="success" size="small">默认</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleSetDefault(row)" :disabled="row.is_default">
              设为默认
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 配置信息 -->
    <el-card class="config-card">
      <template #header>
        <span>配置信息</span>
      </template>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="后端端口">{{ config.backend_port }}</el-descriptions-item>
        <el-descriptions-item label="前端端口">{{ config.frontend_port }}</el-descriptions-item>
        <el-descriptions-item label="调试模式">
          <el-tag :type="config.debug ? 'warning' : 'info'">
            {{ config.debug ? '开启' : '关闭' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="AI 诊断">
          <el-tag :type="config.ai_configured ? 'success' : 'danger'">
            {{ config.ai_configured ? '已配置' : '未配置' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="通知服务">
          <el-tag :type="config.notification_configured ? 'success' : 'danger'">
            {{ config.notification_configured ? '已配置' : '未配置' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const checkingDrivers = ref(false)
const checkingBrowsers = ref(false)

const systemInfo = reactive({
  os: '',
  os_version: '',
  python_version: '',
  cpu_count: 0,
  memory_total: 0,
  memory_available: 0,
  memory_percent: 0,
  disk_total: 0,
  disk_free: 0,
  disk_percent: 0,
})

const drivers = ref([])
const browsers = ref([])

const config = reactive({
  backend_port: 8000,
  frontend_port: 5173,
  debug: true,
  ai_configured: false,
  notification_configured: false,
})

const formatSize = (bytes: number) => {
  if (!bytes) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let i = 0
  let size = bytes
  while (size >= 1024 && i < units.length - 1) {
    size /= 1024
    i++
  }
  return size.toFixed(1) + ' ' + units[i]
}

const fetchSystemInfo = async () => {
  // TODO: 获取系统信息
}

const checkDrivers = async () => {
  checkingDrivers.value = true
  // TODO: 检测驱动
  setTimeout(() => {
    checkingDrivers.value = false
  }, 1000)
}

const checkBrowsers = async () => {
  checkingBrowsers.value = true
  // TODO: 检测浏览器
  setTimeout(() => {
    checkingBrowsers.value = false
  }, 1000)
}

const handleInstallDriver = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确定要安装 ${row.name} 吗？`, '提示', {
      type: 'info',
    })
    // TODO: 安装驱动
    ElMessage.info('安装功能开发中')
  } catch (error) {
    // 取消
  }
}

const handleUpdateDriver = (row: any) => {
  ElMessage.info('更新功能开发中')
}

const handleSetDefault = (row: any) => {
  // TODO: 设置默认浏览器
  ElMessage.success(`已将 ${row.name} 设为默认浏览器`)
}

onMounted(() => {
  fetchSystemInfo()
})
</script>

<style scoped lang="scss">
.environment-container {
  .info-card,
  .driver-card,
  .browser-card,
  .config-card {
    margin-bottom: 16px;
  }
  
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
