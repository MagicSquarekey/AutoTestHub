# -*- coding: utf-8 -*-
"""
执行引擎 API
@Function: 提供测试执行任务管理接口
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.database import get_db
from backend.models.execution import ExecutionTask, ExecutionResult, ExecutionLog
from backend.models.testcase import TestCase
from backend.schemas.execution import (
    ExecutionTaskCreate, ExecutionTaskResponse, ExecutionTaskListResponse,
    ExecutionResultResponse, ExecutionLogResponse, ExecutionControl,
)

router = APIRouter()


@router.get("/", response_model=ExecutionTaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="状态筛选"),
    platform: Optional[str] = Query(None, description="平台筛选"),
    db: AsyncSession = Depends(get_db),
):
    """获取执行任务列表"""
    query = select(ExecutionTask)
    
    if status:
        query = query.where(ExecutionTask.status == status)
    if platform:
        query = query.where(ExecutionTask.platform == platform)
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(ExecutionTask.created_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return ExecutionTaskListResponse(total=total or 0, items=items)


@router.post("/", response_model=ExecutionTaskResponse)
async def create_task(
    data: ExecutionTaskCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建执行任务"""
    # 验证用例存在
    if data.test_case_ids:
        result = await db.execute(
            select(TestCase).where(TestCase.id.in_(data.test_case_ids))
        )
        test_cases = result.scalars().all()
        if len(test_cases) != len(data.test_case_ids):
            raise HTTPException(status_code=400, detail="部分测试用例不存在")
    
    # 创建任务
    task = ExecutionTask(
        name=data.name,
        task_type="manual",
        status="pending",
        platform=data.config.platform,
        device_id=data.config.device_id,
        config=data.config.model_dump(),
        total_cases=len(data.test_case_ids),
    )
    db.add(task)
    await db.flush()
    
    # 创建执行结果记录
    for tc_id in data.test_case_ids:
        tc_result = await db.execute(select(TestCase).where(TestCase.id == tc_id))
        tc = tc_result.scalar_one_or_none()
        if tc:
            exec_result = ExecutionResult(
                task_id=task.id,
                test_case_id=tc_id,
                test_case_name=tc.name,
                status="pending",
            )
            db.add(exec_result)
    
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/{task_id}", response_model=ExecutionTaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取执行任务详情"""
    result = await db.execute(select(ExecutionTask).where(ExecutionTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="执行任务不存在")
    return task


@router.get("/{task_id}/results", response_model=List[ExecutionResultResponse])
async def get_task_results(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取任务执行结果"""
    result = await db.execute(
        select(ExecutionResult)
        .where(ExecutionResult.task_id == task_id)
        .order_by(ExecutionResult.created_at)
    )
    return result.scalars().all()


@router.get("/{task_id}/logs", response_model=List[ExecutionLogResponse])
async def get_task_logs(
    task_id: int,
    level: Optional[str] = Query(None, description="日志级别筛选"),
    db: AsyncSession = Depends(get_db),
):
    """获取任务执行日志"""
    query = select(ExecutionLog).where(ExecutionLog.task_id == task_id)
    
    if level:
        query = query.where(ExecutionLog.level == level)
    
    query = query.order_by(ExecutionLog.timestamp)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/{task_id}/start")
async def start_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """启动执行任务"""
    result = await db.execute(select(ExecutionTask).where(ExecutionTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="执行任务不存在")
    
    if task.status not in ["pending", "failed"]:
        raise HTTPException(status_code=400, detail=f"任务状态为 {task.status}，无法启动")
    
    task.status = "running"
    task.started_at = datetime.utcnow()
    
    # 添加日志
    log = ExecutionLog(
        task_id=task_id,
        level="info",
        message="任务开始执行",
    )
    db.add(log)
    
    await db.commit()
    
    # TODO: 实际启动执行引擎
    # 这里应该调用执行服务来异步执行任务
    
    return {"message": "任务已启动", "task_id": task_id}


@router.post("/{task_id}/control")
async def control_task(
    task_id: int,
    control: ExecutionControl,
    db: AsyncSession = Depends(get_db),
):
    """控制执行任务"""
    result = await db.execute(select(ExecutionTask).where(ExecutionTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="执行任务不存在")
    
    if control.action == "pause":
        if task.status != "running":
            raise HTTPException(status_code=400, detail="只有运行中的任务才能暂停")
        task.status = "paused"
        log_msg = "任务已暂停"
    elif control.action == "resume":
        if task.status != "paused":
            raise HTTPException(status_code=400, detail="只有暂停的任务才能恢复")
        task.status = "running"
        log_msg = "任务已恢复"
    elif control.action == "cancel":
        if task.status not in ["running", "paused", "pending"]:
            raise HTTPException(status_code=400, detail="任务状态无法取消")
        task.status = "cancelled"
        task.completed_at = datetime.utcnow()
        if task.started_at:
            task.duration = int((task.completed_at - task.started_at).total_seconds())
        log_msg = "任务已取消"
    else:
        raise HTTPException(status_code=400, detail=f"不支持的操作: {control.action}")
    
    # 添加日志
    log = ExecutionLog(
        task_id=task_id,
        level="info",
        message=log_msg,
    )
    db.add(log)
    
    await db.commit()
    return {"message": log_msg}


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除执行任务"""
    result = await db.execute(select(ExecutionTask).where(ExecutionTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="执行任务不存在")
    
    if task.status == "running":
        raise HTTPException(status_code=400, detail="运行中的任务不能删除")
    
    await db.delete(task)
    await db.commit()
    return {"message": "删除成功"}
