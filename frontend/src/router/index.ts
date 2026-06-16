import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘', icon: 'Odometer' },
      },
      {
        path: 'testcases',
        name: 'TestCases',
        component: () => import('@/views/testcases/index.vue'),
        meta: { title: '用例管理', icon: 'Document' },
      },
      {
        path: 'elements',
        name: 'Elements',
        component: () => import('@/views/elements/index.vue'),
        meta: { title: '元素管理', icon: 'Pointer' },
      },
      {
        path: 'execution',
        name: 'Execution',
        component: () => import('@/views/execution/index.vue'),
        meta: { title: '测试执行', icon: 'VideoPlay' },
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/reports/index.vue'),
        meta: { title: '测试报告', icon: 'DataAnalysis' },
      },
      {
        path: 'environment',
        name: 'Environment',
        component: () => import('@/views/environment/index.vue'),
        meta: { title: '环境管理', icon: 'Monitor' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
