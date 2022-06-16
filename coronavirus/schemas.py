#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-05-15
LastEditTime: 2022-05-17
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/coronavirus/schemas.py
'''

from datetime import datetime
from datetime import date as date_
from pydantic import BaseModel


class CreateData(BaseModel):
    date: date_
    confirmed: int = 0
    death: int =0
    recovered: int = 0


class CreateCity(BaseModel):
    province: str
    country: str
    country_code: str
    country_population: int


class ReadData(CreateData):
    id: int
    city_id: int
    update_at: datetime
    create_at: datetime

    class Config:
        orm_mode = True   


class ReadCity(CreateCity):
    id: int
    update_at: datetime
    create_at: datetime

    class Config:
        orm_mode = True 