# -*- coding: utf-8 -*-
"""
报告相关数据模型
@Function: 定义测试报告的数据库模型
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, Integer, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class TestReport(Base):
    """测试报告模型"""
    __tablename__ = "test_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("execution_tasks.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="报告名称")
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="执行总结")
    total_cases: Mapped[int] = mapped_column(Integer, default=0, comment="总用例数")
    passed_cases: Mapped[int] = mapped_column(Integer, default=0, comment="通过数")
    failed_cases: Mapped[int] = mapped_column(Integer, default=0, comment="失败数")
    skipped_cases: Mapped[int] = mapped_column(Integer, default=0, comment="跳过数")
    pass_rate: Mapped[float] = mapped_column(Float, default=0.0, comment="通过率")
    total_duration: Mapped[int] = mapped_column(Integer, default=0, comment="总执行时长(秒)")
    platform: Mapped[str] = mapped_column(String(50), default="web", comment="执行平台")
    environment_info: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="环境信息")
    failure_analysis: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="失败分析")
    performance_metrics: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="性能指标")
    report_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="报告文件路径")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
