# -*- coding: utf-8 -*-
"""
报告相关 Pydantic 模式
@Function: 定义测试报告的请求和响应模式
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class TestReportResponse(BaseModel):
    """测试报告响应"""
    id: int
    task_id: int
    name: str
    summary: Optional[str] = None
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    skipped_cases: int = 0
    pass_rate: float = 0.0
    total_duration: int = 0
    platform: str = "web"
    environment_info: Optional[Dict[str, Any]] = None
    failure_analysis: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    report_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TestReportListResponse(BaseModel):
    """测试报告列表响应"""
    total: int
    items: List[TestReportResponse]


class ReportSummary(BaseModel):
    """报告统计摘要"""
    total_reports: int = 0
    recent_pass_rate: float = 0.0
    trend_data: List[Dict[str, Any]] = []
    failure_reasons: Dict[str, int] = {}
    platform_stats: Dict[str, int] = {}


class FailureAnalysis(BaseModel):
    """失败分析"""
    total_failures: int = 0
    failure_categories: Dict[str, int] = {}
    top_failing_cases: List[Dict[str, Any]] = []
    common_errors: List[Dict[str, Any]] = []
    ai_suggestions: Optional[List[Dict[str, Any]]] = None
