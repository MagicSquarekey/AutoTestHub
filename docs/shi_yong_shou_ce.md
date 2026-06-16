# 使用手册

## 快速开始

### 1. 克隆模板
```bash
git clone https://github.com/xxx/AI-XiangMuMoBan.git
```

### 2. 创建新项目
```bash
cd AI-XiangMuMoBan
python utils/create_project.py my-project
```

### 3. 进入项目
```bash
cd my-project
```

### 4. 安装依赖
```bash
make setup
```

### 5. 开始开发
根据项目类型添加相应的框架和代码。

---

## 功能说明

### AI 协作系统
- `CLAUDE.md` — AI 指令文件，定义代码规范和工作流
- `.claude/skills/` — AI 自动技能，根据上下文自动触发
- `.claude/commands/` — 快捷命令，用户主动调用

### 文档系统
- `mu_lu_jie_gou.md` — 自动生成的目录结构
- `ren_wu_mu_biao.md` — 任务目标文档
- `ren_wu_jin_du.md` — 任务进度文档
- `jing_yan_ji_lu.md` — 经验记录

### 项目脚手架
- `utils/create_project.py` — 一键创建新项目
- 自动配置和初始化

### 质量保障
- 代码规范检查
- 依赖安全检查
- 项目健康检查

---

## 命令说明

### 快捷命令

| 命令 | 说明 |
|------|------|
| `/plan` | 任务规划 |
| `/review` | 代码审查 |
| `/fix` | 错误修复 |
| `/commit` | 智能提交 |
| `/docs` | 文档同步 |
| `/status` | 项目状态 |
| `/img` | 图片识别 |

### Make 命令

| 命令 | 说明 |
|------|------|
| `make setup` | 安装依赖 |
| `make clean` | 清理临时文件 |
| `make new-project` | 创建新项目 |
| `make health-check` | 健康检查 |
| `make sync-status` | 同步任务目标状态 |
| `make help` | 显示帮助 |

---

## 项目类型

### 测试项目
```bash
pip install pytest playwright
mkdir page_objects test_cases
```

### 运维项目
```bash
pip install ansible docker
mkdir scripts playbooks
```

### 开发项目
```bash
mkdir src lib docs
```

### 数据分析
```bash
pip install pandas jupyter
mkdir notebooks data
```

---

## 常见问题

### 如何创建新项目？
运行 `python utils/create_project.py`，按提示输入项目信息。

### 如何添加领域特定内容？
创建项目后，根据需要添加相应的框架和代码。

### 如何更新模板？
```bash
cd AI-XiangMuMoBan
git pull origin main
```

### 如何运行健康检查？
```bash
make health-check
# 或
python utils/health_check.py
```

---

## 相关文档

- [README.md](README.md) — 项目简介（GitHub）
- [CLAUDE.md](CLAUDE.md) — AI 指令文件
- [mu_lu_jie_gou.md](mu_lu_jie_gou.md) — 目录结构
- [ren_wu_mu_biao.md](ren_wu_mu_biao.md) — 任务目标
- [ren_wu_jin_du.md](ren_wu_jin_du.md) — 任务进度
- [jing_yan_ji_lu.md](jing_yan_ji_lu.md) — 经验记录
- [zhi_shi_ku.md](zhi_shi_ku.md) — 知识库索引
- [fen_hua_zhi_nan.md](fen_hua_zhi_nan.md) — 分化指南
