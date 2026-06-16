# -*- coding: utf-8 -*-
"""
数据模型模块
@Function: 定义所有数据库模型
"""

from backend.models.testcase import TestCase, TestStep, TestSuite
from backend.models.element import Element, ElementLocator
from backend.models.execution import ExecutionTask, ExecutionResult, ExecutionLog
from backend.models.report import TestReport

__all__ = [
    "TestCase",
    "TestStep", 
    "TestSuite",
    "Element",
    "ElementLocator",
    "ExecutionTask",
    "ExecutionResult",
    "ExecutionLog",
    "TestReport",
]
