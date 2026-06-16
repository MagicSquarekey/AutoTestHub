<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-width="100px"
  >
    <el-form-item label="元素名称" prop="name">
      <el-input v-model="form.name" placeholder="请输入元素名称" />
    </el-form-item>
    
    <el-form-item label="所属页面" prop="page_name">
      <el-input v-model="form.page_name" placeholder="请输入所属页面名称" />
    </el-form-item>
    
    <el-form-item label="平台" prop="platform">
      <el-radio-group v-model="form.platform">
        <el-radio value="web">Web</el-radio>
        <el-radio value="app">App</el-radio>
      </el-radio-group>
    </el-form-item>
    
    <el-divider content-position="left">定位符配置</el-divider>
    
    <el-form-item label="XPath">
      <el-input v-model="form.locator_xpath" placeholder="请输入 XPath 表达式" />
    </el-form-item>
    
    <el-form-item label="CSS">
      <el-input v-model="form.locator_css" placeholder="请输入 CSS 选择器" />
    </el-form-item>
    
    <el-form-item label="ID">
      <el-input v-model="form.locator_id" placeholder="请输入元素 ID" />
    </el-form-item>
    
    <el-form-item label="Name">
      <el-input v-model="form.locator_name" placeholder="请输入元素 Name 属性" />
    </el-form-item>
    
    <el-form-item label="文本内容">
      <el-input v-model="form.locator_text" placeholder="请输入元素文本内容" />
    </el-form-item>
    
    <el-form-item label="标签类型">
      <el-input v-model="form.element_type" placeholder="如: input, button, div" />
    </el-form-item>
    
    <el-form-item label="父容器">
      <el-input v-model="form.parent_element_id" placeholder="父元素 ID（可选）" />
    </el-form-item>
    
    <el-form-item label="截图">
      <el-upload
        action="#"
        :auto-upload="false"
        :limit="1"
        accept="image/*"
      >
        <el-button size="small">选择图片</el-button>
        <template #tip>
          <div class="el-upload__tip">上传元素截图，便于识别</div>
        </template>
      </el-upload>
    </el-form-item>
    
    <el-form-item label="描述">
      <el-input
        v-model="form.description"
        type="textarea"
        :rows="3"
        placeholder="请输入元素描述"
      />
    </el-form-item>
    
    <div class="form-actions">
      <el-button @click="$emit('cancel')">取消</el-button>
      <el-button type="primary" @click="handleVerify">验证元素</el-button>
      <el-button type="primary" @click="handleSubmit">确定</el-button>
    </div>
  </el-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  data?: any
}>()

const emit = defineEmits<{
  submit: [data: any]
  cancel: []
}>()

const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  page_name: '',
  platform: 'web',
  locator_xpath: '',
  locator_css: '',
  locator_id: '',
  locator_name: '',
  locator_text: '',
  element_type: '',
  parent_element_id: '',
  screenshot: '',
  description: '',
})

const rules: FormRules = {
  name: [
    { required: true, message: '请输入元素名称', trigger: 'blur' },
    { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' },
  ],
  page_name: [
    { required: true, message: '请输入所属页面', trigger: 'blur' },
  ],
  platform: [
    { required: true, message: '请选择平台', trigger: 'change' },
  ],
}

const handleVerify = () => {
  // TODO: 验证元素是否存在
  ElMessage.info('验证功能开发中')
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
.form-actions {
  margin-top: 24px;
  text-align: right;
}
</style>
