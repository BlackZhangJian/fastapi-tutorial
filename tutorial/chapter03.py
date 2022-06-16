#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-04-26
LastEditTime: 2022-05-09
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/tutorial/chapter03.py
'''
from enum import Enum
from typing import Optional, List
from datetime import date

from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, Query, Cookie, Header


app03 = APIRouter()

"""Path parameters and number validations. 路径参数和数字验证。"""

@app03.get("/path/parameters")  # 函数顺序就是路由顺序
def path_params01():
    return {"message": "this is path_params01`s message"}

@app03.get("/path/{parameters}")
def path_params02(parameters: str):
    return {"message": parameters}


class CityName(str, Enum):
    Shenzhen = "Shenzhen China"
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"
    Guangzhou = "Guangzhou China"


@app03.get("/enum/{city}")  # 枚举类型参数
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name": city, "confirmed": 11480, "death": 20}
    if city == CityName.Shenzhen:
        return {"city_name": city, "confirmed": 120, "death": 3}
    if city == CityName.Beijing:
        return {"city_name": city, "confirmed": 709, "death": 10}
    return {"city_name": city, "latest": "unknown"}


@app03.get("/files/{file_path: path}")  # 通过 path parameters 传递文件路径
def filepath(file_path: str):
    return f"The file path is {file_path}"


@app03.get("/path_/{num}")
def num_params_validate(
    num: int = Path(..., title="Your number", description="不可描述", ge=1, le=10)
):
    return num


"""Query parameters and string validations. 查询参数和字符串验证。"""
@app03.get("/query")
def page_limit(page: int=1, limit: Optional[int]=None):  # 给了默认值就是选填参数，没给默认值就是必填参数 
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


@app03.get("/query/bool/conversion")
def type_conversion(param: bool = False):  # bool 类型转换：yes、on、1、True、true 会转换成true，其他的会报错或返回 false
     return param


@app03.get("/query/validations")
def query_params_validate(
    value: str = Query(..., min_length=8, max_length=16, regex="^a"),
    values: List[str] = Query(default=["v1", "v2"], alias="alias_name")
):  # 多个查询参数的列表。参数别名
    return value, values


"""Request body and fields. 请求体和字段"""
class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing")  # example 只是注解的作用，值不会被验证
    country: str
    country_code: Optional[str ] = None
    country_population: int = Field(default=800, title="人口数量", description="国家的人口数量", ge=800)

    class Config:
        schema_extra = {
            "example":{
                "name": "Shanghai",
                "country": "China",
                "country_code": "CN",
                "country_population": 14000000000
            }
        }


@app03.post("/request_body/city")
def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()

    

"""Request body + path parameters + query parameters. 多参数输混合验证。"""
@app03.put("/request_body/city/{name}")
def mix_city_info(
    name: str,
    city01: CityInfo,  
    city02: CityInfo,  # Body 可以定义多个
    confirmed: int = Query(ge=0, description="确诊数", default=0),
    death: int = Query(ge=0, description="死亡数", default=0) 
):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.dict(), city02.dict()


"""Request Body - Nested Models 数据格式嵌套的请求体"""
class Data(BaseModel):
    city: Optional[List[CityInfo]] = None  # 这里就是定义数据格式嵌套的请求体
    date: date
    confirmed: int = Field(ge=0, description="确诊数", default=0)
    death: int = Field(ge=0, description="死亡数", default=0) 
    recovered: int = Field(ge=0, description="痊愈数", default=0) 

@app03.put("/request_body/nested")
def nested_models(data: Data):
    print(data)
    return data


"""Cookie 和 Header 参数"""
@app03.get("/cookie")  # 效果只能用Postman测试
def cookie(cookie_id: Optional[str]= Cookie(None)):  # 定义Cookie参数需要使用Cookie类， 否则就是查询参数
    return {"cookie_id": cookie_id}


@app03.get("/header")
def header(user_agent: Optional[str]=Header(None, convert_underscores=True), x_token: List[str]=Header(None)):
    """有些HTTP代理服务器是不允许在请求头中带有下划线的，所有Header提供的covert_underscores属性将_变成-，如: user_ager变成user-agent """    
    return {"uesr-agent": user_agent, "x_token": x_token}