# -*- coding: utf-8 -*-
"""
元素管理 API
@Function: 提供元素和定位符的 CRUD 操作接口
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from backend.database import get_db
from backend.models.element import Element, ElementLocator
from backend.schemas.element import (
    ElementCreate, ElementUpdate, ElementResponse, ElementListResponse,
    ElementLocatorCreate, ElementLocatorUpdate, ElementLocatorResponse,
    ElementCheckResult,
)

router = APIRouter()


@router.get("/", response_model=ElementListResponse)
async def list_elements(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    module: Optional[str] = Query(None, description="模块筛选"),
    page_name: Optional[str] = Query(None, description="页面筛选"),
    platform: Optional[str] = Query(None, description="平台筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    db: AsyncSession = Depends(get_db),
):
    """获取元素列表"""
    query = select(Element)
    
    if module:
        query = query.where(Element.module == module)
    if page_name:
        query = query.where(Element.page == page_name)
    if platform:
        query = query.where(Element.platform == platform)
    if status:
        query = query.where(Element.status == status)
    if keyword:
        query = query.where(
            or_(
                Element.name.contains(keyword),
                Element.description.contains(keyword),
            )
        )
    
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(Element.updated_at.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return ElementListResponse(total=total or 0, items=items)


@router.post("/", response_model=ElementResponse)
async def create_element(
    data: ElementCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建元素"""
    element = Element(
        name=data.name,
        page=data.page,
        module=data.module,
        description=data.description,
        platform=data.platform,
    )
    db.add(element)
    await db.flush()
    
    # 创建定位符
    if data.locators:
        for i, loc_data in enumerate(data.locators):
            locator = ElementLocator(
                element_id=element.id,
                locator_type=loc_data.locator_type,
                locator_value=loc_data.locator_value,
                priority=i,
                platform=loc_data.platform,
            )
            db.add(locator)
    
    await db.commit()
    await db.refresh(element)
    return element


@router.get("/{element_id}", response_model=ElementResponse)
async def get_element(
    element_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取元素详情"""
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(status_code=404, detail="元素不存在")
    return element


@router.put("/{element_id}", response_model=ElementResponse)
async def update_element(
    element_id: int,
    data: ElementUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新元素"""
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(status_code=404, detail="元素不存在")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(element, key, value)
    
    await db.commit()
    await db.refresh(element)
    return element


@router.delete("/{element_id}")
async def delete_element(
    element_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除元素"""
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(status_code=404, detail="元素不存在")
    
    await db.delete(element)
    await db.commit()
    return {"message": "删除成功"}


# ==================== 定位符管理 ====================

@router.get("/{element_id}/locators", response_model=List[ElementLocatorResponse])
async def list_locators(
    element_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取元素的定位符列表"""
    result = await db.execute(
        select(ElementLocator)
        .where(ElementLocator.element_id == element_id)
        .order_by(ElementLocator.priority)
    )
    return result.scalars().all()


@router.post("/{element_id}/locators", response_model=ElementLocatorResponse)
async def create_locator(
    element_id: int,
    data: ElementLocatorCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建定位符"""
    # 检查元素是否存在
    result = await db.execute(select(Element).where(Element.id == element_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="元素不存在")
    
    locator = ElementLocator(
        element_id=element_id,
        locator_type=data.locator_type,
        locator_value=data.locator_value,
        priority=data.priority,
        platform=data.platform,
    )
    db.add(locator)
    await db.commit()
    await db.refresh(locator)
    return locator


@router.put("/{element_id}/locators/{locator_id}", response_model=ElementLocatorResponse)
async def update_locator(
    element_id: int,
    locator_id: int,
    data: ElementLocatorUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新定位符"""
    result = await db.execute(
        select(ElementLocator)
        .where(ElementLocator.id == locator_id, ElementLocator.element_id == element_id)
    )
    locator = result.scalar_one_or_none()
    if not locator:
        raise HTTPException(status_code=404, detail="定位符不存在")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(locator, key, value)
    
    await db.commit()
    await db.refresh(locator)
    return locator


@router.delete("/{element_id}/locators/{locator_id}")
async def delete_locator(
    element_id: int,
    locator_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除定位符"""
    result = await db.execute(
        select(ElementLocator)
        .where(ElementLocator.id == locator_id, ElementLocator.element_id == element_id)
    )
    locator = result.scalar_one_or_none()
    if not locator:
        raise HTTPException(status_code=404, detail="定位符不存在")
    
    await db.delete(locator)
    await db.commit()
    return {"message": "删除成功"}


# ==================== 元素检查 ====================

@router.post("/check/{element_id}", response_model=ElementCheckResult)
async def check_element(
    element_id: int,
    db: AsyncSession = Depends(get_db),
):
    """检查单个元素健康状态"""
    result = await db.execute(select(Element).where(Element.id == element_id))
    element = result.scalar_one_or_none()
    if not element:
        raise HTTPException(status_code=404, detail="元素不存在")
    
    # 获取定位符
    loc_result = await db.execute(
        select(ElementLocator)
        .where(ElementLocator.element_id == element_id)
        .order_by(ElementLocator.priority)
    )
    locators = loc_result.scalars().all()
    
    # TODO: 实际执行元素检查（需要集成 Playwright/Appium）
    # 这里返回模拟结果
    locator_results = []
    for loc in locators:
        locator_results.append({
            "locator_id": loc.id,
            "type": loc.locator_type,
            "value": loc.locator_value,
            "is_valid": True,
            "response_time": 50,
        })
    
    # 更新元素状态
    element.last_check_at = datetime.utcnow()
    element.health_score = 100.0
    await db.commit()
    
    return ElementCheckResult(
        element_id=element.id,
        element_name=element.name,
        is_valid=True,
        health_score=100.0,
        locator_results=locator_results,
        check_time=datetime.utcnow(),
    )


@router.post("/check-batch")
async def check_elements_batch(
    element_ids: List[int],
    db: AsyncSession = Depends(get_db),
):
    """批量检查元素健康状态"""
    results = []
    for element_id in element_ids:
        try:
            result = await check_element(element_id, db)
            results.append(result)
        except HTTPException:
            results.append({
                "element_id": element_id,
                "is_valid": False,
                "error": "元素不存在",
            })
    return results
