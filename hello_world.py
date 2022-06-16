#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-04-25
LastEditTime: 2022-04-26
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/hello_world.py
'''

from typing import Optional

import uvicorn
from fastapi import  FastAPI
from pydantic import BaseModel

app = FastAPI()

class CityInfo(BaseModel):
    province: str
    country: str
    is_affected: Optional[bool] = None  # 与 bool 的区别是可以不传，默认是 null


@app.get('/')
async def hello_world():
    return {'hello': 'world'}


@app.get('/city/{city}')
async def result(city: str, query_string: Optional[str] = None):
     return {'city': city, 'query_string': query_string}


@app.put('/city/{city}')
async def result(city: str, city_info: CityInfo):
    return {'city': city, 'country': city_info.country, 'is_affected': city_info.is_affected}


# 启动命令：uvicorn hello_world:app --reload
if __name__ == '__main__':
    uvicorn.run('hello_world:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)