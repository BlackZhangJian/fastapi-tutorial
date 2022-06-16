#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-04-25
LastEditTime: 2022-05-16
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/pydantic_tutorial.py
'''
from datetime import date, datetime
from typing import List, Optional
from pathlib import Path

from pydantic import BaseModel, ValidationError, constr
from sqlalchemy import Column, Integer, String
from sqlalchemy .dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base


"""
Data validation and settings management using python type annotations.
使用 python 类型注解来进行数据校验和设置管理。

pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
pydantic 可以在代码运行时提供类型提示，并在数据校验失败时提供用户友好的错误提示。

Define how data should be in pure, canonical python; validate it with pydantic.
定义数据应该如何在纯规范的 python 代码中保存，并用 pydantic 验证它。
"""


class User(BaseModel):
    id: int  # 必填字段
    name: str = "Bowen"  # 有默认值，选填字段
    signup_ts: Optional[datetime] = None
    friends: List[int] = []  # 列表中元素是int类型或者可以直接转成int类型

external_data = {
    "id": "123",
    "signup_ts": "2022-12-25 12:25",
    "friends": [1, 2, "3"]
}

user = User(**external_data)
print(1, user.id, user.friends)  # 实例化后调用属性
print(2, repr(user.signup_ts))
print(3, user.dict())


# 校验失败处理
try:
    User(id=1, signup_ts=datetime.today(), friends=[11, 22, 33, "not number"])
except ValidationError as e:
    print(4, e.json())

# 模型类的属性和方法
print(5, user.dict())
print(6, user.json())
print(7, user.copy())  # 这里是浅拷贝
print(8, User.parse_obj(obj=external_data))
print(9, User.parse_raw('{"id": 123, "name": "Bowen", "signup_ts": "2022-12-25 12:25", "friends": [1, 2, "3"]}'))

path = Path("pydantic_tutorial.json")
path.write_text('{"id": 123, "name": "Bowen", "signup_ts": "2022-12-25 12:25", "friends": [1, 2, "3"]}')
print(10, User.parse_file(path=path))

print(11, User.schema())
print(12, User.schema_json())

user_data = {"id": "error", "name": "Bowen", "signup_ts": "2022-12-25 12:25", "friends": [1, 2, "3"]}
print(13, User.construct(**user_data))  # 不检验数据直接创建模型类，不建议在 construct 方法中传入未经验证的数据, 使用 construct() 方法创建模型通常比创建完整验证的模型块 30 倍

print(14, User.__fields__.keys())


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birthday: date
    weight: Optional[float] = None
    sound: List[Sound]  # 不同的狗有不同的叫声。递归模型（Recursive Models）就是指一个嵌套一个


dogs = Dog(birthday=date.today(), weight=6.66, sound=[{"sound": "aowu aowu ~"},{"sound": "wang wang ~"},{"sound": "ying ying ~"}])

print(15, dogs.dict())


# ORM模型：从类实例创建符合ORM对象的模型
Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = "companines"
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String (63), unique=True)
    domains = Column(ARRAY(String(255)))

class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True

co_orm = CompanyOrm(
    id=123,
    public_key="foobar",
    name="Testing",
    domains=["example.com", "imooc.com"]
)


print(16, CompanyMode.from_orm(co_orm))
