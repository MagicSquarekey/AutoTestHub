# -*- coding: utf-8 -*-
# @File: backend/init_db.py
# @Description: 数据库初始化脚本
# @Author: AutoTest Hub

import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.database import engine, Base
from backend.models import testcase, element, execution, report


async def init_database():
    """初始化数据库，创建所有表"""
    print("正在初始化数据库...")
    
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
    
    print("数据库初始化完成！")
    print(f"数据库文件位置: {engine.url}")


async def drop_database():
    """删除所有表（危险操作）"""
    print("警告: 即将删除所有数据库表！")
    confirm = input("输入 'yes' 确认: ")
    
    if confirm.lower() == 'yes':
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("所有表已删除。")
    else:
        print("操作已取消。")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        asyncio.run(drop_database())
    else:
        asyncio.run(init_database())
