# -*- coding: utf-8 -*-
"""
用例管理 API
@Function: 提供测试用例的 CRUD 操作接口
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from backend.database import get_db
from backend.models.testcase import TestCase, TestStep, TestSuite
from backend.schemas.testcase import (
    TestCaseCreate, TestCaseUpdate, TestCaseResponse, TestCaseListResponse,
    TestStepCreate, TestStepUpdate, TestStepResponse,
    TestSuiteCreate, TestSuiteUpdate, TestSuiteResponse, TestSuiteListResponse,
)

router = APIRouter()


# ==================== 用例管理 ====================

@router.get("/", response_model=TestCaseListResponse)
async def list_test_cases(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    module: Optional[str] = Query(None, description="模块筛选"),
    platform: Optional[str] = Query(None, description="平台筛选"),
    priority: Optional[str] = Query(None, description="优先级筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    db: AsyncSession = Depends(get_db),
):
    """获取测试用例列表"""
    query = select(TestCase)
    
    # 筛选条件
    if module:
        query = query.where(TestCase.module == module)
    if platform:
        query = query.where(TestCase.platform == platform)
    if priority:
        query = query.where(TestCase.priority == priority)
    if status:
        query = query.where(TestCase.status == status)
    if keyword:
        query = query.where(
            or_(
                TestCase.name.contains(keyword),
                TestCase.description.contains(keyword),
                TestCase.tags.contains(keyword),
            )
        )
    
    # 获取总数
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(TestCase.updated_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return TestCaseListResponse(total=total or 0, items=items)


@router.post("/", response_model=TestCaseResponse)
async def create_test_case(
    data: TestCaseCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建测试用例"""
    # 创建用例
    test_case = TestCase(
        name=data.name,
        module=data.module,
        tags=data.tags,
        description=data.description,
        priority=data.priority,
        status=data.status,
        platform=data.platform,
        suite_id=data.suite_id,
        data_driver=data.data_driver,
        variables=data.variables,
    )
    db.add(test_case)
    await db.flush()
    
    # 创建步骤
    if data.steps:
        for i, step_data in enumerate(data.steps):
            step = TestStep(
                test_case_id=test_case.id,
                name=step_data.name,
                keyword=step_data.keyword,
                params=step_data.params,
                element_id=step_data.element_id,
                order=i,
                timeout=step_data.timeout,
                retry=step_data.retry,
                parent_id=step_data.parent_id,
                step_type=step_data.step_type,
                condition=step_data.condition,
                loop_config=step_data.loop_config,
                enabled=step_data.enabled,
                breakpoint=step_data.breakpoint,
            )
            db.add(step)
    
    await db.commit()
    await db.refresh(test_case)
    return test_case


@router.get("/{case_id}", response_model=TestCaseResponse)
async def get_test_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取测试用例详情"""
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    test_case = result.scalar_one_or_none()
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return test_case


@router.put("/{case_id}", response_model=TestCaseResponse)
async def update_test_case(
    case_id: int,
    data: TestCaseUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新测试用例"""
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    test_case = result.scalar_one_or_none()
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    # 更新字段
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(test_case, key, value)
    
    await db.commit()
    await db.refresh(test_case)
    return test_case


@router.delete("/{case_id}")
async def delete_test_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除测试用例"""
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    test_case = result.scalar_one_or_none()
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    await db.delete(test_case)
    await db.commit()
    return {"message": "删除成功"}


# ==================== 步骤管理 ====================

@router.get("/{case_id}/steps", response_model=List[TestStepResponse])
async def list_steps(
    case_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取用例的步骤列表"""
    result = await db.execute(
        select(TestStep)
        .where(TestStep.test_case_id == case_id)
        .order_by(TestStep.order)
    )
    return result.scalars().all()


@router.post("/{case_id}/steps", response_model=TestStepResponse)
async def create_step(
    case_id: int,
    data: TestStepCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建测试步骤"""
    # 检查用例是否存在
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="测试用例不存在")
    
    step = TestStep(
        test_case_id=case_id,
        name=data.name,
        keyword=data.keyword,
        params=data.params,
        element_id=data.element_id,
        order=data.order,
        timeout=data.timeout,
        retry=data.retry,
        parent_id=data.parent_id,
        step_type=data.step_type,
        condition=data.condition,
        loop_config=data.loop_config,
        enabled=data.enabled,
        breakpoint=data.breakpoint,
    )
    db.add(step)
    await db.commit()
    await db.refresh(step)
    return step


@router.put("/{case_id}/steps/{step_id}", response_model=TestStepResponse)
async def update_step(
    case_id: int,
    step_id: int,
    data: TestStepUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新测试步骤"""
    result = await db.execute(
        select(TestStep)
        .where(TestStep.id == step_id, TestStep.test_case_id == case_id)
    )
    step = result.scalar_one_or_none()
    if not step:
        raise HTTPException(status_code=404, detail="测试步骤不存在")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(step, key, value)
    
    await db.commit()
    await db.refresh(step)
    return step


@router.delete("/{case_id}/steps/{step_id}")
async def delete_step(
    case_id: int,
    step_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除测试步骤"""
    result = await db.execute(
        select(TestStep)
        .where(TestStep.id == step_id, TestStep.test_case_id == case_id)
    )
    step = result.scalar_one_or_none()
    if not step:
        raise HTTPException(status_code=404, detail="测试步骤不存在")
    
    await db.delete(step)
    await db.commit()
    return {"message": "删除成功"}


# ==================== 套件管理 ====================

@router.get("/suites/", response_model=TestSuiteListResponse)
async def list_suites(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    suite_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取测试套件列表"""
    query = select(TestSuite)
    
    if suite_type:
        query = query.where(TestSuite.suite_type == suite_type)
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(TestSuite.updated_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return TestSuiteListResponse(total=total or 0, items=items)


@router.post("/suites/", response_model=TestSuiteResponse)
async def create_suite(
    data: TestSuiteCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建测试套件"""
    suite = TestSuite(
        name=data.name,
        description=data.description,
        suite_type=data.suite_type,
    )
    db.add(suite)
    await db.flush()
    
    # 关联用例
    if data.test_case_ids:
        result = await db.execute(
            select(TestCase).where(TestCase.id.in_(data.test_case_ids))
        )
        test_cases = result.scalars().all()
        for tc in test_cases:
            tc.suite_id = suite.id
    
    await db.commit()
    await db.refresh(suite)
    return suite


@router.get("/suites/{suite_id}", response_model=TestSuiteResponse)
async def get_suite(
    suite_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取测试套件详情"""
    result = await db.execute(select(TestSuite).where(TestSuite.id == suite_id))
    suite = result.scalar_one_or_none()
    if not suite:
        raise HTTPException(status_code=404, detail="测试套件不存在")
    return suite


@router.put("/suites/{suite_id}", response_model=TestSuiteResponse)
async def update_suite(
    suite_id: int,
    data: TestSuiteUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新测试套件"""
    result = await db.execute(select(TestSuite).where(TestSuite.id == suite_id))
    suite = result.scalar_one_or_none()
    if not suite:
        raise HTTPException(status_code=404, detail="测试套件不存在")
    
    update_data = data.model_dump(exclude_unset=True)
    test_case_ids = update_data.pop("test_case_ids", None)
    
    for key, value in update_data.items():
        setattr(suite, key, value)
    
    # 更新关联用例
    if test_case_ids is not None:
        # 清除旧关联
        old_cases = await db.execute(
            select(TestCase).where(TestCase.suite_id == suite_id)
        )
        for tc in old_cases.scalars().all():
            tc.suite_id = None
        
        # 设置新关联
        if test_case_ids:
            new_cases = await db.execute(
                select(TestCase).where(TestCase.id.in_(test_case_ids))
            )
            for tc in new_cases.scalars().all():
                tc.suite_id = suite.id
    
    await db.commit()
    await db.refresh(suite)
    return suite


@router.delete("/suites/{suite_id}")
async def delete_suite(
    suite_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除测试套件"""
    result = await db.execute(select(TestSuite).where(TestSuite.id == suite_id))
    suite = result.scalar_one_or_none()
    if not suite:
        raise HTTPException(status_code=404, detail="测试套件不存在")
    
    # 清除关联
    cases = await db.execute(
        select(TestCase).where(TestCase.suite_id == suite_id)
    )
    for tc in cases.scalars().all():
        tc.suite_id = None
    
    await db.delete(suite)
    await db.commit()
    return {"message": "删除成功"}
