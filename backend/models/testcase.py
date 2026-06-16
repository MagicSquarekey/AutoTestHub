# -*- coding: utf-8 -*-
"""
用例相关数据模型
@Function: 定义测试用例、测试步骤、测试套件的数据库模型
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Integer, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class TestCase(Base):
    """测试用例模型"""
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="用例名称")
    module: Mapped[str] = mapped_column(String(100), default="", comment="所属模块")
    tags: Mapped[Optional[str]] = mapped_column(Text, default="", comment="标签，逗号分隔")
    description: Mapped[Optional[str]] = mapped_column(Text, default="", comment="用例描述")
    priority: Mapped[str] = mapped_column(String(20), default="P1", comment="优先级: P0/P1/P2")
    status: Mapped[str] = mapped_column(String(20), default="draft", comment="状态: draft/ready/deprecated")
    platform: Mapped[str] = mapped_column(String(50), default="web", comment="平台: web/android/ios/miniapp")
    suite_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("test_suites.id"), nullable=True)
    data_driver: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="数据驱动配置")
    variables: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="变量配置")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    steps: Mapped[List["TestStep"]] = relationship(back_populates="test_case", cascade="all, delete-orphan")
    suite: Mapped[Optional["TestSuite"]] = relationship(back_populates="test_cases")


class TestStep(Base):
    """测试步骤模型"""
    __tablename__ = "test_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    test_case_id: Mapped[int] = mapped_column(Integer, ForeignKey("test_cases.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="步骤名称")
    keyword: Mapped[str] = mapped_column(String(100), nullable=False, comment="关键字")
    params: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="步骤参数")
    element_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("elements.id"), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0, comment="步骤顺序")
    timeout: Mapped[int] = mapped_column(Integer, default=30, comment="超时时间(秒)")
    retry: Mapped[int] = mapped_column(Integer, default=0, comment="重试次数")
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="父步骤ID，用于嵌套")
    step_type: Mapped[str] = mapped_column(String(50), default="action", comment="步骤类型: action/condition/loop/group")
    condition: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="条件配置")
    loop_config: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, comment="循环配置")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否启用")
    breakpoint: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否断点")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 关系
    test_case: Mapped["TestCase"] = relationship(back_populates="steps")


class TestSuite(Base):
    """测试套件模型"""
    __tablename__ = "test_suites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="套件名称")
    description: Mapped[Optional[str]] = mapped_column(Text, default="", comment="套件描述")
    suite_type: Mapped[str] = mapped_column(String(50), default="regression", comment="类型: smoke/regression/custom")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    test_cases: Mapped[List["TestCase"]] = relationship(back_populates="suite")
