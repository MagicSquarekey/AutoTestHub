# -*- coding: utf-8 -*-
"""
执行相关数据模型
@Function: 定义执行任务、执行结果、执行日志的数据库模型
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Integer, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class ExecutionTask(Base):
    """执行任务模型"""
    __tablename__ = "execution_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="任务名称")
    task_type: Mapped[str] = mapped_column(String(50), default="manual", comment="类型: manual/scheduled/api")
    status: Mapped[str] = mapped_column(String(20), default="pending", comment="状态: pending/running/completed/failed/cancelled")
    platform: Mapped[str] = mapped_column(String(50), default="web", comment="执行平台")
    device_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="执行设备/浏览器")
    config: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="执行配置")
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="执行时长(秒)")
    total_cases: Mapped[int] = mapped_column(Integer, default=0, comment="总用例数")
    passed_cases: Mapped[int] = mapped_column(Integer, default=0, comment="通过数")
    failed_cases: Mapped[int] = mapped_column(Integer, default=0, comment="失败数")
    skipped_cases: Mapped[int] = mapped_column(Integer, default=0, comment="跳过数")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="错误信息")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 关系
    results: Mapped[List["ExecutionResult"]] = relationship(back_populates="task", cascade="all, delete-orphan")
    logs: Mapped[List["ExecutionLog"]] = relationship(back_populates="task", cascade="all, delete-orphan")


class ExecutionResult(Base):
    """执行结果模型"""
    __tablename__ = "execution_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("execution_tasks.id"), nullable=False)
    test_case_id: Mapped[int] = mapped_column(Integer, ForeignKey("test_cases.id"), nullable=False)
    test_case_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="用例名称(冗余)")
    status: Mapped[str] = mapped_column(String(20), nullable=False, comment="状态: passed/failed/skipped/error")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="执行时长(秒)")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="错误信息")
    screenshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="失败截图路径")
    video_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="录屏路径")
    step_results: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="步骤执行结果详情")
    retry_count: Mapped[int] = mapped_column(Integer, default=0, comment="重试次数")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 关系
    task: Mapped["ExecutionTask"] = relationship(back_populates="results")


class ExecutionLog(Base):
    """执行日志模型"""
    __tablename__ = "execution_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("execution_tasks.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    level: Mapped[str] = mapped_column(String(20), default="info", comment="日志级别: debug/info/warning/error")
    step_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="步骤名称")
    message: Mapped[str] = mapped_column(Text, nullable=False, comment="日志内容")
    details: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="详细信息")
    screenshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="截图路径")

    # 关系
    task: Mapped["ExecutionTask"] = relationship(back_populates="logs")
