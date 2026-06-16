# AI 项目模板 / AI Project Template

🤖 一个通用的 AI 辅助开发项目起点 / A universal template for AI-assisted development

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 快速开始 / Quick Start

### 方式一：使用 Makefile（推荐）

```bash
# 1. 克隆模板 / Clone template
git clone https://github.com/MagicSquarekey/AI-XiangMuMoBan.git
cd AI-XiangMuMoBan

# 2. 创建新项目 / Create new project
make new-project

# 3. 按提示输入项目名称，然后进入项目
cd 我的项目名
make setup
```

### 方式二：使用 Python 脚本

```bash
# 1. 克隆模板 / Clone template
git clone https://github.com/MagicSquarekey/AI-XiangMuMoBan.git
cd AI-XiangMuMoBan

# 2. 创建新项目 / Create new project
python utils/create_project.py 我的项目名

# 3. 进入项目 / Enter project
cd 我的项目名
make setup
```

---

## 📁 目录结构 / Directory Structure

```
AI-XiangMuMoBan/
├── .claude/             # Claude 配置（自动生效）
│   ├── commands/        # 快捷命令
│   └── skills/          # 技能定义
├── config/              # 项目配置
│   └── settings.yaml    # 通用设置
├── utils/               # 工具脚本
│   ├── create_project.py    # 创建新项目
│   └── update_directory.py  # 更新目录结构
├── templates/           # 模板文件
├── docs/                # 文档
├── private/             # 🔒 私有部分（不上传到 GitHub）
│   └── (项目特定文件)
├── README.md            # 项目说明（本文件）
├── CLAUDE.md            # AI 指令
├── Makefile             # 常用命令
├── requirements.txt     # Python 依赖
└── .gitignore           # Git 忽略规则
```

---

## 🔧 Makefile 使用教程

Makefile 是一个命令行工具，可以让你用简单的命令执行复杂的操作。

### 常用命令

| 命令 | 说明 | 使用场景 |
|------|------|----------|
| `make help` | 显示所有可用命令 | 不知道有什么命令时 |
| `make setup` | 初始化项目 | 首次进入项目时 |
| `make clean` | 清理临时文件 | 项目变慢或有垃圾文件时 |
| `make new-project` | 创建新项目 | 需要新建项目时 |

### 使用步骤

#### 1. 首次进入项目

```bash
cd 我的项目名
make setup
```

这会：
- 安装 Python 依赖（requirements.txt）
- 显示"项目初始化完成！"

#### 2. 查看可用命令

```bash
make help
```

会显示：
```
可用命令：
clean           清理临时文件
help            显示帮助信息
new-project     创建新项目
setup           初始化项目
```

#### 3. 清理项目

```bash
make clean
```

会删除：
- `__pycache__/` 目录
- `.pytest_cache/` 目录
- `htmlcov/` 目录
- `.coverage` 文件
- `reports/` 目录

#### 4. 创建新项目

```bash
make new-project
```

会启动项目创建向导，按提示输入项目名称即可。

### 常见问题

**Q: 提示 "make: command not found" 怎么办？**

A: Windows 用户需要安装 Make：
- 方法1：使用 Git Bash（自带 make）
- 方法2：使用 `python utils/create_project.py` 代替

**Q: 提示 "No rule to make target 'xxx'" 怎么办？**

A: 说明命令不存在，运行 `make help` 查看可用命令。

**Q: 可以自定义 Makefile 命令吗？**

A: 可以！编辑 Makefile 文件，按照格式添加：
```makefile
my-command: ## 我的命令说明
    要执行的命令
```

---

## 🎯 快捷命令 / Quick Commands

在 Claude Code 中使用这些命令：

| 命令 | 用途 | Command |
|------|------|---------|
| `/plan` | 任务规划 | Task planning |
| `/review` | 代码审查 | Code review |
| `/fix` | 修复问题 | Bug fixing |
| `/commit` | 提交代码 | Smart commit |
| `/docs` | 文档同步 | Document sync |
| `/status` | 查看状态 | Project status |

---

## 📖 使用方法 / Usage

### 创建新项目

```bash
# 方式1：使用 Makefile
make new-project

# 方式2：使用 Python
python utils/create_project.py 项目名称
```

### 开始开发

```bash
cd 项目名称
make setup

# 开始使用 Claude Code 开发
# 输入 /plan 开始任务规划
```

### 私有文件管理

将不想上传到 GitHub 的文件放在 `private/` 目录：

```bash
# 例如：项目文档、笔记、敏感配置等
private/
├── docs/           # 项目文档
├── notes/          # 个人笔记
└── secrets.yaml    # 敏感配置
```

---

## 🔒 安全规范 / Security

### 绝对禁止 / Never Do

- ❌ 不得提交 API Key、密码、密钥
- ❌ 不得提交 .env 文件
- ❌ 不得在代码中硬编码任何凭证

### 发现安全问题时 / When发现安全问题

1. 立即停止提交
2. 告知用户
3. 清理 Git 历史（如已提交）

---

## 📚 更多信息 / More Info

- [CLAUDE.md](CLAUDE.md) - AI 指令 / AI Instructions
- [docs/shi_yong_shou_ce.md](docs/shi_yong_shou_ce.md) - 使用手册 / User Manual

---

## 📄 许可证 / License

MIT License

---

*最后更新 / Last Updated: 2026-06-16*
*维护者 / Maintainer: AI 协作开发团队*
