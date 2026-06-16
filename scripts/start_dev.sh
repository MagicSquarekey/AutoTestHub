#!/bin/bash
# AutoTest Hub 开发模式启动脚本

set -e

echo "==================================="
echo "  AutoTest Hub 开发模式"
echo "==================================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 启动后端（开发模式，自动重载）
echo ""
echo "启动后端 (开发模式)..."
echo "后端地址: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
echo ""

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 启动前端（开发模式）
echo ""
echo "启动前端 (开发模式)..."
echo "前端地址: http://localhost:5173"
echo ""

cd frontend
npm run dev &
FRONTEND_PID=$!

# 等待进程
wait $BACKEND_PID $FRONTEND_PID
