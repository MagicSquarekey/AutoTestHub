<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-width="100px"
  >
    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本信息" name="basic">
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入用例名称" />
        </el-form-item>
        
        <el-form-item label="所属模块" prop="module">
          <el-input v-model="form.module" placeholder="请输入模块名称" />
        </el-form-item>
        
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="form.priority" placeholder="请选择优先级">
            <el-option label="P0 - 最高" value="P0" />
            <el-option label="P1 - 高" value="P1" />
            <el-option label="P2 - 中" value="P2" />
            <el-option label="P3 - 低" value="P3" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="平台" prop="platform">
          <el-radio-group v-model="form.platform">
            <el-radio value="web">Web</el-radio>
            <el-radio value="app">App</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft" />
            <el-option label="就绪" value="ready" />
            <el-option label="已废弃" value="deprecated" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="标签">
          <el-input v-model="form.tags" placeholder="多个标签用逗号分隔" />
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入用例描述"
          />
        </el-form-item>
      </el-tab-pane>
      
      <el-tab-pane label="测试步骤" name="steps">
        <div class="steps-toolbar">
          <el-button type="primary" size="small" @click="addStep">
            <el-icon><Plus /></el-icon>
            添加步骤
          </el-button>
        </div>
        
        <el-table :data="form.steps" border>
          <el-table-column type="index" label="序号" width="60" />
          
          <el-table-column prop="name" label="步骤名称" min-width="150">
            <template #default="{ row }">
              <el-input v-model="row.name" size="small" placeholder="步骤名称" />
            </template>
          </el-table-column>
          
          <el-table-column prop="keyword" label="关键字" width="150">
            <template #default="{ row }">
              <el-select v-model="row.keyword" size="small" placeholder="选择关键字">
                <el-option-group label="浏览器">
                  <el-option label="打开页面" value="open_page" />
                  <el-option label="点击元素" value="click" />
                  <el-option label="输入文本" value="input" />
                  <el-option label="获取文本" value="get_text" />
                  <el-option label="等待元素" value="wait_element" />
                  <el-option label="截图" value="screenshot" />
                </el-option-group>
                <el-option-group label="断言">
                  <el-option label="断言文本" value="assert_text" />
                  <el-option label="断言元素存在" value="assert_element" />
                  <el-option label="断言URL" value="assert_url" />
                  <el-option label="断言标题" value="assert_title" />
                </el-option-group>
                <el-option-group label="流程控制">
                  <el-option label="条件判断" value="if" />
                  <el-option label="循环" value="loop" />
                  <el-option label="等待" value="sleep" />
                </el-option-group>
              </el-select>
            </template>
          </el-table-column>
          
          <el-table-column prop="timeout" label="超时(秒)" width="100">
            <template #default="{ row }">
              <el-input-number v-model="row.timeout" size="small" :min="0" :max="300" />
            </template>
          </el-table-column>
          
          <el-table-column prop="enabled" label="启用" width="70">
            <template #default="{ row }">
              <el-switch v-model="row.enabled" size="small" />
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="120">
            <template #default="{ $index }">
              <el-button type="primary" link size="small" @click="moveStep($index, -1)" :disabled="$index === 0">
                上移
              </el-button>
              <el-button type="primary" link size="small" @click="moveStep($index, 1)" :disabled="$index === form.steps.length - 1">
                下移
              </el-button>
              <el-button type="danger" link size="small" @click="removeStep($index)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
    
    <div class="form-actions">
      <el-button @click="$emit('cancel')">取消</el-button>
      <el-button type="primary" @click="handleSubmit">确定</el-button>
    </div>
  </el-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

const props = defineProps<{
  data?: any
}>()

const emit = defineEmits<{
  submit: [data: any]
  cancel: []
}>()

const formRef = ref<FormInstance>()
const activeTab = ref('basic')

const form = reactive({
  name: '',
  module: '',
  priority: 'P1',
  platform: 'web',
  status: 'draft',
  tags: '',
  description: '',
  steps: [] as any[],
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入用例名称', trigger: 'blur' },
    { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' },
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' },
  ],
  platform: [
    { required: true, message: '请选择平台', trigger: 'change' },
  ],
}

const addStep = () => {
  form.steps.push({
    name: '',
    keyword: '',
    timeout: 30,
    enabled: true,
  })
}

const removeStep = (index: number) => {
  form.steps.splice(index, 1)
}

const moveStep = (index: number, direction: number) => {
  const newIndex = index + direction
  if (newIndex < 0 || newIndex >= form.steps.length) return
  
  const temp = form.steps[index]
  form.steps[index] = form.steps[newIndex]
  form.steps[newIndex] = temp
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate((valid) => {
    if (valid) {
      emit('submit', { ...form })
    }
  })
}

onMounted(() => {
  if (props.data) {
    Object.assign(form, props.data)
  }
})
</script>

<style scoped lang="scss">
.steps-toolbar {
  margin-bottom: 12px;
}

.form-actions {
  margin-top: 24px;
  text-align: right;
}
</style>
