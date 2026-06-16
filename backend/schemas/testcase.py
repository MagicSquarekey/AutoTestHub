# -*- coding: utf-8 -*-
"""
用例相关 Pydantic 模式
@Function: 定义用例、步骤、套件的请求和响应模式
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class TestStepBase(BaseModel):
    """测试步骤基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="步骤名称")
    keyword: str = Field(..., description="关键字")
    params: Optional[Dict[str, Any]] = Field(None, description="步骤参数")
    element_id: Optional[int] = Field(None, description="关联元素ID")
    order: int = Field(0, description="步骤顺序")
    timeout: int = Field(30, ge=0, description="超时时间(秒)")
    retry: int = Field(0, ge=0, description="重试次数")
    parent_id: Optional[int] = Field(None, description="父步骤ID")
    step_type: str = Field("action", description="步骤类型")
    condition: Optional[Dict[str, Any]] = Field(None, description="条件配置")
    loop_config: Optional[Dict[str, Any]] = Field(None, description="循环配置")
    enabled: bool = Field(True, description="是否启用")
    breakpoint: bool = Field(False, description="是否断点")


class TestStepCreate(TestStepBase):
    """创建测试步骤"""
    pass


class TestStepUpdate(BaseModel):
    """更新测试步骤"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    keyword: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    element_id: Optional[int] = None
    order: Optional[int] = None
    timeout: Optional[int] = Field(None, ge=0)
    retry: Optional[int] = Field(None, ge=0)
    step_type: Optional[str] = None
    condition: Optional[Dict[str, Any]] = None
    loop_config: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None
    breakpoint: Optional[bool] = None


class TestStepResponse(TestStepBase):
    """测试步骤响应"""
    id: int
    test_case_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TestCaseBase(BaseModel):
    """测试用例基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="用例名称")
    module: str = Field("", description="所属模块")
    tags: str = Field("", description="标签")
    description: str = Field("", description="用例描述")
    priority: str = Field("P1", description="优先级")
    status: str = Field("draft", description="状态")
    platform: str = Field("web", description="平台")
    suite_id: Optional[int] = Field(None, description="所属套件ID")
    data_driver: Optional[Dict[str, Any]] = Field(None, description="数据驱动配置")
    variables: Optional[Dict[str, Any]] = Field(None, description="变量配置")


class TestCaseCreate(TestCaseBase):
    """创建测试用例"""
    steps: Optional[List[TestStepCreate]] = Field([], description="测试步骤列表")


class TestCaseUpdate(BaseModel):
    """更新测试用例"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    module: Optional[str] = None
    tags: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    platform: Optional[str] = None
    suite_id: Optional[int] = None
    data_driver: Optional[Dict[str, Any]] = None
    variables: Optional[Dict[str, Any]] = None


class TestCaseResponse(TestCaseBase):
    """测试用例响应"""
    id: int
    created_at: datetime
    updated_at: datetime
    steps: List[TestStepResponse] = []

    class Config:
        from_attributes = True


class TestCaseListResponse(BaseModel):
    """测试用例列表响应"""
    total: int
    items: List[TestCaseResponse]


class TestSuiteBase(BaseModel):
    """测试套件基础模式"""
    name: str = Field(..., min_length=1, max_length=200, description="套件名称")
    description: str = Field("", description="套件描述")
    suite_type: str = Field("regression", description="类型")


class TestSuiteCreate(TestSuiteBase):
    """创建测试套件"""
    test_case_ids: List[int] = Field([], description="关联用例ID列表")


class TestSuiteUpdate(BaseModel):
    """更新测试套件"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    suite_type: Optional[str] = None
    test_case_ids: Optional[List[int]] = None


class TestSuiteResponse(TestSuiteBase):
    """测试套件响应"""
    id: int
    created_at: datetime
    updated_at: datetime
    test_case_count: int = 0

    class Config:
        from_attributes = True


class TestSuiteListResponse(BaseModel):
    """测试套件列表响应"""
    total: int
    items: List[TestSuiteResponse]
