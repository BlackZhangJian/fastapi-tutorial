#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-04-26
LastEditTime: 2022-05-09
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/tutorial/chapter04.py
'''

from typing import List, Optional, Set, Union

from fastapi import APIRouter, status, Form, File, UploadFile, HTTPException

from pydantic import BaseModel, EmailStr

app04 = APIRouter()


"""Response Model 响应模型"""
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = "10086"
    address: Optional[str] = None
    fullname: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    mobile: str = "10086"
    address: Optional[str] = None
    fullname: Optional[str] = None


users = {
    "user01": {"username": "user01", "password":"123456", "email":"user01@example.com"},
    "user02": {"username": "user02", "password":"123123", "email":"user02@example.com", "mobile":"1010101010"}
}


@app04.post("/response_model/", response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    """response_model_exclude_unset=True 表示默认值不包含在响应中，仅包含实际给的值， 如果实际给的值与默认值相同也会包含在响应中"""
    print(user.password)
    return users["user02"]


@app04.post(
    "/response_model/attributes", 
    # response_model=UserOut,
    # response_model=Union[UserIn, UserOut],
    response_model=List[UserOut],
    response_model_include={"username", "email", "mobile"},
    response_model_exclude={"password"}
)
async def response_model_attributes(user: UserIn):
    # del user.password  # Union[UserIn, UserOut]后，响应返回中删除password属性
    return [user, user]


"""Response status code 响应状态码"""
@app04.post("/status_code", status_code=status.HTTP_200_OK)
async def status_code():
    return {"status_code": 200}

@app04.post("/status_attribute", status_code=status.HTTP_200_OK)
async def status_attribute():
    print(type(status.HTTP_200_OK))
    return {"status_code": status.HTTP_200_OK}


"""Form Data 表单处理"""
@app04.post("/login")
async def login(username: str = Form(..., max_length=24), password: str = Form(...)):  # 定义表单参数。 ...即Ellipsis，是内置常量，在FastAPI中表示必填参数
    return {"username": username}


"""Request Files 上传文件"""
@app04.post("/upload_file")
async def upload_file(file: bytes = File(...)):  # 如果要上传多个文件 file: List[bytes]=File(...)
    """使用 File 类 文件内容会以 bytes 的形式读入内存 适合于上传小文件"""
    return {"file_size": len(file)}

@app04.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):  # 如果要上传单个文件 file: UploadFile = File(...)
    """
    使用UploadFile类的优势
    1、文件存储在内存中，使用的存储达到阈值会，会将文件保存到内存中
    2、适合于图片、视频大文件
    3、可以获取上传的文件的元数据，如文件名，创建时间
    4、有文件对象的异步接口
    5、上传的文件时Python对象，可以使用 wirte(), read(), seek(), close()操作
    """
    out: List[dict] = []
    for file in files:
        contents = await file.read()
        temp = {}
        temp["filename"]=file.filename
        temp["content_type"]=file.content_type
        out.append(temp)
    return out

"""Request Forms and Files 请求表单和文件"""
@app04.post("/files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "file_content_type": fileb.content_type,
    }


"""Handling Errors 处理错误"""
items = {"foo": "the Foo Wrestlers"}

@app04.get("/http_exception/{item_id}")
async def http_exception(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

"""Add custom headers 添加自定义头"""
@app04.get("/http_exception_header/{item_id}")
async def http_exception_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},  # 自定义头
        )
    return {"item": items[item_id]}

@app04.get("/override_http_exception_header/{item_id}")
async def override_http_exception_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=418,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


"""Path Operation Configuration 路径操作配置"""
@app04.post(
    "/path_operation_configuration",
    response_model=UserOut,
    # tags=["Path", "Operation", "Configuration"],
    summary="This is summary",
    description="This is description",
    response_description="this is response description",
    # deprecated=True,
    status_code=status.HTTP_200_OK
)
async def path_operation_configuration(user: UserIn):
    print(type(user))
    return user.dict()
 