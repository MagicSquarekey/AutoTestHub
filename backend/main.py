# -*- coding: utf-8 -*-
"""
AutoTest Hub 后端主入口
@Function: FastAPI 应用初始化、路由注册、中间件配置
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import get_settings
from backend.database import init_db
from backend.api import router as api_router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    settings.ensure_dirs()
    yield
    # 关闭时清理资源


app = FastAPI(
    title="AutoTest Hub",
    description="单人自动化测试平台",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """健康检查接口"""
    return {"message": "AutoTest Hub API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=settings.server.backend_port,
        reload=settings.server.debug,
    )
