# -*- coding: utf-8 -*-
"""
环境管理 API
@Function: 提供环境配置和设备管理接口
"""

import platform
import psutil
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class SystemInfo(BaseModel):
    """系统信息"""
    os: str
    os_version: str
    python_version: str
    cpu_count: int
    memory_total: int
    memory_available: int
    memory_percent: float
    disk_total: int
    disk_used: int
    disk_free: int
    disk_percent: float


class DriverInfo(BaseModel):
    """驱动信息"""
    name: str
    version: Optional[str] = None
    status: str
    path: Optional[str] = None


class BrowserInfo(BaseModel):
    """浏览器信息"""
    name: str
    version: Optional[str] = None
    path: Optional[str] = None
    is_default: bool = False


@router.get("/system", response_model=SystemInfo)
async def get_system_info():
    """获取系统信息"""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    
    return SystemInfo(
        os=platform.system(),
        os_version=platform.version(),
        python_version=platform.python_version(),
        cpu_count=psutil.cpu_count(),
        memory_total=memory.total,
        memory_available=memory.available,
        memory_percent=memory.percent,
        disk_total=disk.total,
        disk_used=disk.used,
        disk_free=disk.free,
        disk_percent=disk.percent,
    )


@router.get("/drivers", response_model=List[DriverInfo])
async def get_drivers():
    """获取已安装的驱动列表"""
    # TODO: 实际检测已安装的驱动
    # 这里返回示例数据
    drivers = [
        DriverInfo(
            name="Playwright",
            version="1.40.0",
            status="installed",
        ),
        DriverInfo(
            name="ChromeDriver",
            version=None,
            status="not_installed",
        ),
        DriverInfo(
            name="Appium",
            version=None,
            status="not_installed",
        ),
    ]
    return drivers


@router.get("/browsers", response_model=List[BrowserInfo])
async def get_browsers():
    """获取已安装的浏览器列表"""
    # TODO: 实际检测已安装的浏览器
    browsers = [
        BrowserInfo(
            name="Chromium",
            version="120.0.6099.109",
            is_default=True,
        ),
        BrowserInfo(
            name="Firefox",
            version=None,
        ),
        BrowserInfo(
            name="WebKit",
            version=None,
        ),
    ]
    return browsers


@router.post("/drivers/install/{driver_name}")
async def install_driver(driver_name: str):
    """安装指定驱动"""
    # TODO: 实现驱动安装逻辑
    if driver_name.lower() == "playwright":
        return {"message": "请使用命令安装: pip install playwright && playwright install"}
    elif driver_name.lower() == "chromedriver":
        return {"message": "请使用命令安装: pip install webdriver-manager"}
    elif driver_name.lower() == "appium":
        return {"message": "请参考 Appium 官方文档安装"}
    else:
        raise HTTPException(status_code=400, detail=f"不支持的驱动: {driver_name}")


@router.post("/drivers/check/{driver_name}")
async def check_driver(driver_name: str):
    """检查驱动状态"""
    # TODO: 实现驱动状态检查
    return {
        "name": driver_name,
        "status": "unknown",
        "message": "功能待实现",
    }


@router.get("/devices")
async def get_devices(platform: Optional[str] = None):
    """获取已连接的设备列表"""
    # TODO: 实现设备检测
    devices = []
    
    if platform == "web" or platform is None:
        devices.append({
            "id": "chrome",
            "name": "Chrome",
            "platform": "web",
            "status": "available",
        })
        devices.append({
            "id": "firefox",
            "name": "Firefox",
            "platform": "web",
            "status": "available",
        })
    
    return devices


@router.get("/config")
async def get_config():
    """获取当前环境配置"""
    from config.settings import get_settings
    settings = get_settings()
    
    return {
        "backend_port": settings.server.backend_port,
        "frontend_port": settings.server.frontend_port,
        "debug": settings.server.debug,
        "database_url": settings.database.url.replace(
            "sqlite://", "sqlite+aiosqlite://"
        ) if "sqlite" in settings.database.url else "***",
        "ai_configured": bool(settings.ai.api_key),
        "notification_configured": any([
            settings.notification.smtp_host,
            settings.notification.dingtalk_webhook,
            settings.notification.wechat_webhook,
        ]),
    }
