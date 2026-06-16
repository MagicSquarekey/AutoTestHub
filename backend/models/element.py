# -*- coding: utf-8 -*-
"""
元素相关数据模型
@Function: 定义元素和元素定位符的数据库模型
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Integer, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class Element(Base):
    """元素模型"""
    __tablename__ = "elements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment="元素名称")
    page: Mapped[str] = mapped_column(String(200), default="", comment="所属页面")
    module: Mapped[str] = mapped_column(String(100), default="", comment="所属模块")
    description: Mapped[Optional[str]] = mapped_column(Text, default="", comment="元素描述")
    platform: Mapped[str] = mapped_column(String(50), default="web", comment="平台: web/android/ios/miniapp")
    health_score: Mapped[float] = mapped_column(Float, default=100.0, comment="健康度评分")
    last_check_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="最后检查时间")
    status: Mapped[str] = mapped_column(String(20), default="active", comment="状态: active/inactive/deprecated")
    screenshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="元素截图路径")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    locators: Mapped[List["ElementLocator"]] = relationship(back_populates="element", cascade="all, delete-orphan")


class ElementLocator(Base):
    """元素定位符模型"""
    __tablename__ = "element_locators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    element_id: Mapped[int] = mapped_column(Integer, ForeignKey("elements.id"), nullable=False)
    locator_type: Mapped[str] = mapped_column(String(50), nullable=False, comment="定位方式: xpath/css/id/name/accessibility/ocr/image/coordinate/relative")
    locator_value: Mapped[str] = mapped_column(Text, nullable=False, comment="定位值")
    priority: Mapped[int] = mapped_column(Integer, default=0, comment="优先级，数字越小优先级越高")
    platform: Mapped[str] = mapped_column(String(50), default="web", comment="适用平台")
    success_rate: Mapped[float] = mapped_column(Float, default=100.0, comment="成功率")
    last_success_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_failure_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    failure_count: Mapped[int] = mapped_column(Integer, default=0, comment="失败次数")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # 关系
    element: Mapped["Element"] = relationship(back_populates="locators")
