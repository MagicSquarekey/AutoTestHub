@echo off
REM AutoTest Hub 启动脚本 (Windows)

echo ===================================
echo   AutoTest Hub 启动脚本
echo ===================================

REM 检查 Python 版本
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装后端依赖
echo 安装后端依赖...
pip install -r requirements.txt

REM 安装 Playwright 浏览器
echo 安装 Playwright 浏览器...
playwright install chromium

REM 初始化数据库
echo 初始化数据库...
python -m backend.init_db

REM 创建必要的目录
if not exist "data\screenshots" mkdir data\screenshots
if not exist "data\reports" mkdir data\reports
if not exist "data\logs" mkdir data\logs

echo.
echo ===================================
echo   启动后端服务...
echo ===================================
echo 后端地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.

REM 启动后端（后台运行）
start "AutoTest Hub Backend" python -m backend.main

echo.
echo ===================================
echo   启动前端服务...
echo ===================================
echo 前端地址: http://localhost:5173
echo.

REM 启动前端
cd frontend
call npm install
call npm run dev

pause
