# -*- coding: utf-8 -*-
"""
API 路由模块
@Function: 聚合所有 API 路由
"""

from fastapi import APIRouter
from backend.api.testcases import router as testcases_router
from backend.api.elements import router as elements_router
from backend.api.execution import router as execution_router
from backend.api.reports import router as reports_router
from backend.api.environment import router as environment_router
from backend.api.ai_diagnosis import router as ai_router

router = APIRouter()

# 注册各模块路由
router.include_router(testcases_router, prefix="/testcases", tags=["用例管理"])
router.include_router(elements_router, prefix="/elements", tags=["元素管理"])
router.include_router(execution_router, prefix="/execution", tags=["执行引擎"])
router.include_router(reports_router, prefix="/reports", tags=["测试报告"])
router.include_router(environment_router, prefix="/environment", tags=["环境管理"])
router.include_router(ai_router, prefix="/ai", tags=["AI诊断"])
