#!/bin/bash
# AutoTest Hub 启动脚本 (Linux/Mac)

set -e

echo "==================================="
echo "  AutoTest Hub 启动脚本"
echo "==================================="

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $python_version"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装后端依赖
echo "安装后端依赖..."
pip install -r requirements.txt

# 安装 Playwright 浏览器
echo "安装 Playwright 浏览器..."
playwright install chromium

# 初始化数据库
echo "初始化数据库..."
python -m backend.init_db

# 创建必要的目录
mkdir -p data/screenshots
mkdir -p data/reports
mkdir -p data/logs

echo ""
echo "==================================="
echo "  启动后端服务..."
echo "==================================="
echo "后端地址: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
echo ""

# 启动后端（后台运行）
python -m backend.main &
BACKEND_PID=$!

echo ""
echo "==================================="
echo "  启动前端服务..."
echo "==================================="
echo "前端地址: http://localhost:5173"
echo ""

# 启动前端
cd frontend
npm install
npm run dev

# 等待后端进程
wait $BACKEND_PID
