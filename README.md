# AutoTest Hub

单人自动化测试管理系统 - 专为独立测试工程师和小型团队设计的本地化测试管理平台。

## 项目概述

AutoTest Hub 是一个轻量级的自动化测试管理平台，旨在帮助测试工程师高效管理测试用例、元素、执行和报告。系统采用前后端分离架构，支持 Web 和 App 自动化测试。

### 核心特性

- **用例编排**: 支持可视化用例编辑、步骤管理、流程控制
- **元素管理**: 多定位符管理、元素健康巡检、失效预警
- **执行引擎**: 基于 Playwright 的自动化执行，支持多浏览器
- **测试报告**: 详细的执行报告、趋势统计、失败分析
- **AI 诊断**: 智能失败分析、修复建议（可选）
- **环境管理**: 驱动检测、浏览器管理、设备管理

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: SQLite (aiosqlite)
- **ORM**: SQLAlchemy 2.0 (async)
- **测试引擎**: Playwright

### 前端
- **框架**: Vue 3 + TypeScript
- **UI 组件**: Element Plus
- **构建工具**: Vite
- **状态管理**: Pinia
- **HTTP 客户端**: Axios

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- npm 或 pnpm

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repository-url>
cd AutoTestHub
```

#### 2. 后端设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python -m backend.init_db

# 启动后端服务
python -m backend.main
```

后端服务将在 http://localhost:8000 启动

#### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:5173 启动

#### 4. 访问应用

打开浏览器访问 http://localhost:5173

## 项目结构

```
AutoTestHub/
├── backend/                    # 后端代码
│   ├── api/                   # API 路由
│   │   ├── __init__.py
│   │   ├── testcases.py      # 用例管理 API
│   │   ├── elements.py       # 元素管理 API
│   │   ├── execution.py      # 执行引擎 API
│   │   ├── reports.py        # 测试报告 API
│   │   ├── environment.py    # 环境管理 API
│   │   └── ai_diagnosis.py   # AI 诊断 API
│   ├── models/                # 数据库模型
│   │   ├── __init__.py
│   │   ├── base.py           # 基础模型
│   │   ├── testcase.py       # 用例模型
│   │   ├── element.py        # 元素模型
│   │   ├── execution.py      # 执行模型
│   │   └── report.py         # 报告模型
│   ├── schemas/               # Pydantic 模式
│   │   ├── __init__.py
│   │   ├── testcase.py
│   │   ├── element.py
│   │   ├── execution.py
│   │   └── report.py
│   ├── core/                  # 核心功能
│   │   ├── __init__.py
│   │   ├── database.py       # 数据库连接
│   │   └── security.py       # 安全配置
│   ├── main.py                # 应用入口
│   └── init_db.py             # 数据库初始化
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── api/              # API 调用
│   │   ├── assets/           # 静态资源
│   │   ├── components/       # 公共组件
│   │   ├── layouts/          # 布局组件
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # 状态管理
│   │   ├── styles/           # 样式文件
│   │   ├── utils/            # 工具函数
│   │   └── views/            # 页面视图
│   │       ├── dashboard/    # 仪表盘
│   │       ├── testcases/    # 用例管理
│   │       ├── elements/     # 元素管理
│   │       ├── execution/    # 测试执行
│   │       ├── reports/      # 测试报告
│   │       └── environment/  # 环境管理
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── config/                    # 配置文件
│   ├── __init__.py
│   └── settings.py           # 应用配置
├── data/                      # 数据目录
│   ├── autotest.db           # SQLite 数据库
│   ├── screenshots/          # 截图存储
│   ├── reports/              # 报告存储
│   └── logs/                 # 日志目录
├── .env.example               # 环境变量示例
├── .gitignore
├── requirements.txt
└── README.md
```

## 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并配置以下变量：

```bash
# 数据库配置
DATABASE_URL=sqlite+aiosqlite:///./data/autotest.db

# 服务器配置
BACKEND_PORT=8000
FRONTEND_PORT=5173
DEBUG=true

# AI 配置（可选）
AI_API_KEY=your_api_key_here
AI_API_URL=https://api.example.com

# 通知配置（可选）
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_password
```

## 使用指南

### 1. 创建测试用例

1. 进入「用例管理」页面
2. 点击「新建用例」按钮
3. 填写用例基本信息（名称、模块、优先级等）
4. 添加测试步骤（选择关键字、配置参数）
5. 保存用例

### 2. 管理元素

1. 进入「元素管理」页面
2. 点击「新建元素」按钮
3. 填写元素信息（名称、所属页面）
4. 配置定位符（支持 XPath、CSS、ID、Name 等多种方式）
5. 保存元素

### 3. 执行测试

1. 进入「测试执行」页面
2. 选择要执行的用例
3. 配置执行参数（浏览器、运行模式等）
4. 点击「开始执行」
5. 查看执行进度和结果

### 4. 查看报告

1. 进入「测试报告」页面
2. 查看报告列表和统计信息
3. 点击报告查看详细内容
4. 可导出报告为 HTML 格式

## 开发指南

### 添加新的 API 接口

1. 在 `backend/models/` 中定义数据库模型
2. 在 `backend/schemas/` 中定义 Pydantic 模式
3. 在 `backend/api/` 中创建路由
4. 在 `backend/main.py` 中注册路由

### 添加新的前端页面

1. 在 `frontend/src/views/` 中创建页面组件
2. 在 `frontend/src/router/index.ts` 中添加路由
3. 在 `frontend/src/api/` 中添加 API 调用

### 数据库迁移

```bash
# 生成迁移脚本
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head
```

## 常见问题

### Q: 如何重置数据库？

A: 删除 `data/autotest.db` 文件，然后重新运行初始化脚本：

```bash
python -m backend.init_db
```

### Q: 如何配置 AI 诊断功能？

A: 在 `.env` 文件中配置 AI 相关的环境变量：

```bash
AI_API_KEY=your_api_key_here
AI_API_URL=https://api.example.com
```

### Q: 如何添加新的浏览器支持？

A: 在 `backend/api/environment.py` 中的 `get_browsers()` 函数中添加新的浏览器配置。

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue 或联系开发团队。

---

**AutoTest Hub** - 让自动化测试更简单、更高效！
