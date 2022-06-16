#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-05-14
LastEditTime: 2022-05-14
LastEditors: Bowen
Description: 临时测试使用
FilePath: /fastapi-tutorial/tutorial/test01.py
'''
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

test = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None


# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     return user


# @test.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user