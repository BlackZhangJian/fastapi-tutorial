#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-04-26
LastEditTime: 2022-05-18
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/run.py
'''
from time import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# from starlette.exceptions import HTTPException as StarletteHTTPException  # 等同于 from fastapi.exceptions import HTTPException
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse


from tutorial import app03, app04, app05, app06, app07, app08, test
from coronavirus import application

app = FastAPI(
    title="FastAPI Tutorial and Coronavirus Tracker API Docs",
    description="FastAPI 教程、新冠病毒疫情跟踪器API接口文档，项目代码地址：xxxxxxxxxxxxxxx",
    version="1.0.1",
    docs_url="/docs",
    redoc_url="/redocs",
)

"""FastAPI 项目的静态文件配置"""
# mount 表示将某个目录下一个完全独立的应用挂载过来，这个不会在 API 交互文档中显示
app.mount("/static", app=StaticFiles(directory="./coronavirus/static"), name="static")


# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):  # 重写HTTPException异常处理器
#     '''
#     @description: 
#     @param {*} request: 这个参数不能省略
#     @param {*} exc：
#     @return {*}：
#     '''
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):  # 重写请求验证异常异常处理器
#     '''
#     @description: 
#     @param {*} request: 这个参数不能省略
#     @param {*} exc：
#     @return {*}：
#     '''
#     return PlainTextResponse(str(exc), status_code=400)

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):  # call_next 将接收request请求做为参数
    start_time = time()
    response = await call_next(request)
    processtime = time() - start_time
    response.headers['X-Process-Time'] = str(processtime)  # 添加自定义的以“X-”开头的请求头
    return response

"""跨域设置"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
app.include_router(app03, prefix='/chapter03', tags=["第三章 请求参数和验证"])
app.include_router(app04, prefix='/chapter04', tags=["第四章 响应处理和FastAPI配置"])
app.include_router(app05, prefix='/chapter05', tags=["第五章 FastAPI的依赖注入系统"])
app.include_router(app06, prefix='/chapter06', tags=["第六章 FastAPI的安全、认证和授权"])
app.include_router(app07, prefix='/chapter07', tags=["第七章 FastAPI的数据库操作和多应用的目录结构设计"])
app.include_router(application, prefix='/coronavirus', tags=["新冠病毒疫情跟踪器API"])
app.include_router(app08, prefix='/chapter08', tags=["第八章 中间件、跨域资源共享、后台任务、测试用例"])
app.include_router(test, prefix='/test', tags=["测试"])



@app.get('/')
async def root():
    return {'message': 'Hello World'}


if __name__ == '__main__':
    print(213)
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
