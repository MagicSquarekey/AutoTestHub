import request from '@/utils/request'

// 用例接口
export interface TestCase {
  id: number
  name: string
  module: string
  tags: string
  description: string
  priority: string
  status: string
  platform: string
  suite_id?: number
  data_driver?: any
  variables?: any
  created_at: string
  updated_at: string
  steps: TestStep[]
}

export interface TestStep {
  id: number
  test_case_id: number
  name: string
  keyword: string
  params?: any
  element_id?: number
  order: number
  timeout: number
  retry: number
  step_type: string
  enabled: boolean
  breakpoint: boolean
}

export interface TestSuite {
  id: number
  name: string
  description: string
  suite_type: string
  test_case_count: number
  created_at: string
  updated_at: string
}

export interface TestCaseQuery {
  page?: number
  page_size?: number
  module?: string
  platform?: string
  priority?: string
  status?: string
  keyword?: string
}

export interface TestCaseCreate {
  name: string
  module?: string
  tags?: string
  description?: string
  priority?: string
  status?: string
  platform?: string
  suite_id?: number
  steps?: Partial<TestStep>[]
}

// 用例 API
export const testcaseApi = {
  // 获取用例列表
  getList(params: TestCaseQuery) {
    return request.get<{ total: number; items: TestCase[] }>('/testcases/', { params })
  },
  
  // 获取用例详情
  getById(id: number) {
    return request.get<TestCase>(`/testcases/${id}`)
  },
  
  // 创建用例
  create(data: TestCaseCreate) {
    return request.post<TestCase>('/testcases/', data)
  },
  
  // 更新用例
  update(id: number, data: Partial<TestCaseCreate>) {
    return request.put<TestCase>(`/testcases/${id}`, data)
  },
  
  // 删除用例
  delete(id: number) {
    return request.delete(`/testcases/${id}`)
  },
  
  // 获取步骤列表
  getSteps(caseId: number) {
    return request.get<TestStep[]>(`/testcases/${caseId}/steps`)
  },
  
  // 创建步骤
  createStep(caseId: number, data: Partial<TestStep>) {
    return request.post<TestStep>(`/testcases/${caseId}/steps`, data)
  },
  
  // 更新步骤
  updateStep(caseId: number, stepId: number, data: Partial<TestStep>) {
    return request.put<TestStep>(`/testcases/${caseId}/steps/${stepId}`, data)
  },
  
  // 删除步骤
  deleteStep(caseId: number, stepId: number) {
    return request.delete(`/testcases/${caseId}/steps/${stepId}`)
  },
}

// 套件 API
export const suiteApi = {
  // 获取套件列表
  getList(params?: { page?: number; page_size?: number; suite_type?: string }) {
    return request.get<{ total: number; items: TestSuite[] }>('/testcases/suites/', { params })
  },
  
  // 创建套件
  create(data: { name: string; description?: string; suite_type?: string; test_case_ids?: number[] }) {
    return request.post<TestSuite>('/testcases/suites/', data)
  },
  
  // 更新套件
  update(id: number, data: Partial<TestSuite>) {
    return request.put<TestSuite>(`/testcases/suites/${id}`, data)
  },
  
  // 删除套件
  delete(id: number) {
    return request.delete(`/testcases/suites/${id}`)
  },
}
