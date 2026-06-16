# -*- coding: utf-8 -*-
"""
执行相关 Pydantic 模式
@Function: 定义执行任务和结果的请求和响应模式
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ExecutionConfig(BaseModel):
    """执行配置"""
    platform: str = Field("web", description="执行平台")
    device_id: Optional[str] = Field(None, description="设备/浏览器")
    headless: bool = Field(False, description="是否无头模式")
    timeout: int = Field(30, description="超时时间(秒)")
    retry_on_failure: int = Field(0, description="失败重试次数")
    screenshot_on_failure: bool = Field(True, description="失败时截图")
    video_recording: bool = Field(False, description="是否录屏")
    parallel: bool = Field(False, description="是否并行执行")
    max_workers: int = Field(1, description="最大并行数")


class ExecutionTaskCreate(BaseModel):
    """创建执行任务"""
    name: str = Field(..., min_length=1, max_length=200, description="任务名称")
    test_case_ids: List[int] = Field(..., description="要执行的用例ID列表")
    suite_id: Optional[int] = Field(None, description="套件ID")
    config: ExecutionConfig = Field(default_factory=ExecutionConfig, description="执行配置")


class ExecutionTaskResponse(BaseModel):
    """执行任务响应"""
    id: int
    name: str
    task_type: str
    status: str
    platform: str
    device_id: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[int] = None
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    skipped_cases: int = 0
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExecutionTaskListResponse(BaseModel):
    """执行任务列表响应"""
    total: int
    items: List[ExecutionTaskResponse]


class ExecutionResultResponse(BaseModel):
    """执行结果响应"""
    id: int
    task_id: int
    test_case_id: int
    test_case_name: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration: Optional[int] = None
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None
    video_path: Optional[str] = None
    step_results: Optional[Dict[str, Any]] = None
    retry_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class ExecutionLogResponse(BaseModel):
    """执行日志响应"""
    id: int
    task_id: int
    timestamp: datetime
    level: str
    step_name: Optional[str] = None
    message: str
    details: Optional[Dict[str, Any]] = None
    screenshot_path: Optional[str] = None

    class Config:
        from_attributes = True


class ExecutionControl(BaseModel):
    """执行控制"""
    action: str = Field(..., description="控制动作: pause/resume/cancel")
