# -*- coding: utf-8 -*-
"""
AI 诊断 API
@Function: 提供 AI 辅助的失败分析和修复建议
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class FailureInput(BaseModel):
    """失败输入"""
    error_message: str = Field(..., description="错误信息")
    error_type: Optional[str] = Field(None, description="错误类型")
    screenshot_path: Optional[str] = Field(None, description="截图路径")
    step_name: Optional[str] = Field(None, description="失败步骤名称")
    element_info: Optional[Dict[str, Any]] = Field(None, description="元素信息")
    page_url: Optional[str] = Field(None, description="页面URL")
    browser_logs: Optional[List[str]] = Field(None, description="浏览器日志")


class DiagnosisResult(BaseModel):
    """诊断结果"""
    root_cause: str = Field(..., description="根本原因")
    category: str = Field(..., description="失败类别")
    confidence: float = Field(..., description="置信度 0-1")
    suggestions: List[Dict[str, Any]] = Field(..., description="修复建议")
    related_elements: Optional[List[Dict[str, Any]]] = Field(None, description="相关元素")


class RepairAction(BaseModel):
    """修复动作"""
    action_type: str = Field(..., description="动作类型: update_locator/add_locator/modify_step/skip_step")
    target_id: Optional[int] = Field(None, description="目标ID")
    details: Dict[str, Any] = Field(..., description="修复详情")


@router.post("/diagnose", response_model=DiagnosisResult)
async def diagnose_failure(data: FailureInput):
    """诊断测试失败原因"""
    # TODO: 集成 AI 模型进行诊断
    # 这里返回示例结果
    
    # 简单的规则匹配
    error_msg = data.error_message.lower()
    
    if "timeout" in error_msg or "等待" in error_msg:
        return DiagnosisResult(
            root_cause="元素定位超时，可能是页面加载慢或元素不存在",
            category="timeout",
            confidence=0.8,
            suggestions=[
                {
                    "type": "increase_timeout",
                    "description": "增加等待超时时间",
                    "action": "将超时时间从 30s 增加到 60s",
                },
                {
                    "type": "check_element",
                    "description": "检查元素是否存在",
                    "action": "使用元素检查工具验证元素状态",
                },
            ],
        )
    elif "not found" in error_msg or "找不到" in error_msg or "no such element" in error_msg:
        return DiagnosisResult(
            root_cause="元素定位失败，定位器可能已失效",
            category="element_not_found",
            confidence=0.9,
            suggestions=[
                {
                    "type": "update_locator",
                    "description": "更新元素定位器",
                    "action": "使用元素拾取器重新获取元素定位信息",
                },
                {
                    "type": "use_alternative",
                    "description": "使用备选定位器",
                    "action": "切换到其他定位方式（如从 xpath 切换到 css）",
                },
            ],
            related_elements=data.element_info and [data.element_info] or None,
        )
    elif "click" in error_msg or "点击" in error_msg:
        return DiagnosisResult(
            root_cause="元素点击失败，可能被遮挡或不可交互",
            category="interaction_error",
            confidence=0.7,
            suggestions=[
                {
                    "type": "scroll_into_view",
                    "description": "滚动到元素可见位置",
                    "action": "在点击前添加滚动操作",
                },
                {
                    "type": "wait_element",
                    "description": "等待元素可交互",
                    "action": "添加等待元素可点击的步骤",
                },
            ],
        )
    else:
        return DiagnosisResult(
            root_cause="未知错误，需要人工分析",
            category="unknown",
            confidence=0.3,
            suggestions=[
                {
                    "type": "manual_review",
                    "description": "人工审查",
                    "action": "请检查截图和日志，分析失败原因",
                },
            ],
        )


@router.post("/repair", response_model=Dict[str, Any])
async def suggest_repair(data: FailureInput):
    """获取修复建议"""
    # 先诊断
    diagnosis = await diagnose_failure(data)
    
    # 根据诊断结果生成修复动作
    actions = []
    
    for suggestion in diagnosis.suggestions:
        if suggestion["type"] == "update_locator":
            actions.append(RepairAction(
                action_type="update_locator",
                details={
                    "reason": diagnosis.root_cause,
                    "suggestion": suggestion["action"],
                },
            ))
        elif suggestion["type"] == "increase_timeout":
            actions.append(RepairAction(
                action_type="modify_step",
                details={
                    "param": "timeout",
                    "new_value": 60,
                    "reason": suggestion["action"],
                },
            ))
    
    return {
        "diagnosis": diagnosis.model_dump(),
        "actions": [a.model_dump() for a in actions],
    }


@router.get("/stats")
async def get_ai_stats():
    """获取 AI 诊断统计"""
    # TODO: 实现诊断统计
    return {
        "total_diagnoses": 0,
        "success_rate": 0.0,
        "common_categories": {},
        "ai_available": False,
    }
