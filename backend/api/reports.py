# -*- coding: utf-8 -*-
"""
测试报告 API
@Function: 提供测试报告查询和分析接口
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.database import get_db
from backend.models.report import TestReport
from backend.models.execution import ExecutionTask
from backend.schemas.report import (
    TestReportResponse, TestReportListResponse, ReportSummary, FailureAnalysis,
)

router = APIRouter()


@router.get("/", response_model=TestReportListResponse)
async def list_reports(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    platform: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取测试报告列表"""
    query = select(TestReport)
    
    if platform:
        query = query.where(TestReport.platform == platform)
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(TestReport.created_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return TestReportListResponse(total=total or 0, items=items)


@router.get("/{report_id}", response_model=TestReportResponse)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取测试报告详情"""
    result = await db.execute(select(TestReport).where(TestReport.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    return report


@router.get("/summary/", response_model=ReportSummary)
async def get_report_summary(
    days: int = Query(30, ge=1, le=365, description="统计天数"),
    db: AsyncSession = Depends(get_db),
):
    """获取报告统计摘要"""
    # 获取总报告数
    total_reports = await db.scalar(select(func.count(TestReport.id)))
    
    # 获取最近通过率
    recent_reports = await db.execute(
        select(TestReport)
        .order_by(TestReport.created_at.desc())
        .limit(10)
    )
    recent = recent_reports.scalars().all()
    
    recent_pass_rate = 0.0
    if recent:
        recent_pass_rate = sum(r.pass_rate for r in recent) / len(recent)
    
    # 获取趋势数据
    trend_reports = await db.execute(
        select(TestReport)
        .order_by(TestReport.created_at.desc())
        .limit(days)
    )
    trend_data = [
        {
            "date": r.created_at.strftime("%Y-%m-%d"),
            "pass_rate": r.pass_rate,
            "total": r.total_cases,
            "passed": r.passed_cases,
            "failed": r.failed_cases,
        }
        for r in trend_reports.scalars().all()
    ]
    trend_data.reverse()
    
    # 平台统计
    platform_stats = {}
    platform_counts = await db.execute(
        select(TestReport.platform, func.count(TestReport.id))
        .group_by(TestReport.platform)
    )
    for platform, count in platform_counts:
        platform_stats[platform] = count
    
    return ReportSummary(
        total_reports=total_reports or 0,
        recent_pass_rate=recent_pass_rate,
        trend_data=trend_data,
        platform_stats=platform_stats,
    )


@router.get("/failure-analysis/", response_model=FailureAnalysis)
async def get_failure_analysis(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    """获取失败分析"""
    # 获取有失败用例的报告
    reports = await db.execute(
        select(TestReport)
        .where(TestReport.failed_cases > 0)
        .order_by(TestReport.created_at.desc())
        .limit(days)
    )
    failed_reports = reports.scalars().all()
    
    total_failures = sum(r.failed_cases for r in failed_reports)
    
    # 分析失败原因
    failure_categories = {}
    common_errors = []
    
    for report in failed_reports:
        if report.failure_analysis:
            # 从报告的失败分析中提取信息
            analysis = report.failure_analysis
            if "categories" in analysis:
                for cat, count in analysis["categories"].items():
                    failure_categories[cat] = failure_categories.get(cat, 0) + count
            if "errors" in analysis:
                common_errors.extend(analysis["errors"])
    
    return FailureAnalysis(
        total_failures=total_failures,
        failure_categories=failure_categories,
        common_errors=common_errors[:10],  # 只返回前10个
    )


@router.post("/generate/{task_id}")
async def generate_report(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    """为执行任务生成报告"""
    # 获取执行任务
    result = await db.execute(select(ExecutionTask).where(ExecutionTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="执行任务不存在")
    
    if task.status not in ["completed", "failed"]:
        raise HTTPException(status_code=400, detail="只有完成或失败的任务才能生成报告")
    
    # 检查是否已有报告
    existing = await db.execute(
        select(TestReport).where(TestReport.task_id == task_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="该任务已有报告")
    
    # 生成报告
    pass_rate = 0.0
    if task.total_cases > 0:
        pass_rate = (task.passed_cases / task.total_cases) * 100
    
    report = TestReport(
        task_id=task_id,
        name=f"{task.name} - 执行报告",
        total_cases=task.total_cases,
        passed_cases=task.passed_cases,
        failed_cases=task.failed_cases,
        skipped_cases=task.skipped_cases,
        pass_rate=pass_rate,
        total_duration=task.duration or 0,
        platform=task.platform,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    
    return report


@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除测试报告"""
    result = await db.execute(select(TestReport).where(TestReport.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    await db.delete(report)
    await db.commit()
    return {"message": "删除成功"}
