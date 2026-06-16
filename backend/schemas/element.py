# -*- coding: utf-8 -*-
"""
元素相关 Pydantic 模式
@Function: 定义元素和定位符的请求和响应模式
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ElementLocatorBase(BaseModel):
    """元素定位符基础模式"""
    locator_type: str = Field(..., description="定位方式")
    locator_value: str = Field(..., description="定位值")
    priority: int = Field(0, description="优先级")
    platform: str = Field("web", description="适用平台")


class ElementLocatorCreate(ElementLocatorBase):
    """创建元素定位符"""
    pass


class ElementLocatorUpdate(BaseModel):
    """更新元素定位符"""
    locator_type: Optional[str] = None
    locator_value: Optional[str] = None
    priority: Optional[int] = None
    platform: Optional[str] = None


class ElementLocatorResponse(ElementLocatorBase):
    """元素定位符响应"""
    id: int
    element_id: int
    success_rate: float = 100.0
    last_success_at: Optional[datetime] = None
    last_failure_at: Optional[datetime] = None
    failure_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class ElementBase(BaseModel):
    """元素基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="元素名称")
    page: str = Field("", description="所属页面")
    module: str = Field("", description="所属模块")
    description: str = Field("", description="元素描述")
    platform: str = Field("web", description="平台")


class ElementCreate(ElementBase):
    """创建元素"""
    locators: List[ElementLocatorCreate] = Field([], description="定位符列表")


class ElementUpdate(BaseModel):
    """更新元素"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    page: Optional[str] = None
    module: Optional[str] = None
    description: Optional[str] = None
    platform: Optional[str] = None
    status: Optional[str] = None


class ElementResponse(ElementBase):
    """元素响应"""
    id: int
    health_score: float = 100.0
    last_check_at: Optional[datetime] = None
    status: str = "active"
    screenshot_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    locators: List[ElementLocatorResponse] = []

    class Config:
        from_attributes = True


class ElementListResponse(BaseModel):
    """元素列表响应"""
    total: int
    items: List[ElementResponse]


class ElementCheckResult(BaseModel):
    """元素检查结果"""
    element_id: int
    element_name: str
    is_valid: bool
    health_score: float
    locator_results: List[Dict[str, Any]]
    check_time: datetime
