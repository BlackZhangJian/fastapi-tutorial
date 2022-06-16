#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-05-19
LastEditTime: 2022-05-19
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/tutorial/test_chapter08.py
'''

from urllib import response
from fastapi.testclient import TestClient
from run import app

client = TestClient(app)  # 先pip install pytest


def test_run_bg_task():  # # 函数名用“test_”开头是 pytest 的规范。注意不是async def
    response = client.post(url="/chapter08/background_tasks?framework=FastAPI")
    assert response.status_code == 200
    assert response.json() == {"message": "任务已在后台运行"}


def test_dependency_run_bg_task():
    response = client.post(url='/chapter08/dependency/background_tasks')
    assert response.status_code == 200
    assert response.json() is None


def test_dependency_run_bg_task_q():
    response = client.post(url='/chapter08/dependency/background_tasks?q=1')
    assert response.status_code == 200
    assert response.json() == {"message": "README2.md更新成功"}