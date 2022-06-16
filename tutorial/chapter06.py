#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-04-26
LastEditTime: 2022-05-16
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/tutorial/chapter06.py
'''

from calendar import timegm
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

app06 = APIRouter()

"""OAuth2 密码模式和 FastAPI 的 OAuth2PasswordBearer"""
"""
OAuth2PasswordBearer 是接收 URL 作为参数的一个类：客户端会向该 URL 发送 username 和 password 参数，然后得到一个 token 值
OAuth2PasswordBearer 并不会创建相应的 URL 路径操作，只是指明客户端用来请求 token 的 URL 地址
当请求到来的时候，FastAPI 会检查请求的 Authorization 头信息，如果没有找到 Authorization头信息，或者头信息的内容不是 Bearer token，它会返回 401 状态码（UNAUTHORIZED）
"""

fake_users_db = {
    "jake": {
        "username": "jake",
        "full_name": "jake Doe",
        "email": "jakedoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": True,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": False,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/chapter06/token")  # 请求token的地址是 http://localhost:8000/chapter06/token


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token: str):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user
    

@app06.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app06.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


"""OAuth2 with Password (and hashing), Bearer with JWT tokens. 开发基于 JSON Web Token 的认证"""

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"  # 加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期时间 分钟

fake_users_db.update({
    "jake": {
        "username": "jake",
        "full_name": "jake Doe",
        "email": "jakedoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
})

class Token(BaseModel):
    """返回给用户的 token"""
    access_token: str
    token_type: str


class TokeData(BaseModel):
    username: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/chapter06/jwt/token")  # 请求token的地址是 http://localhost:8000/chapter06/jwt/token


def verity_password(plain_password, hash_password):
    """对密码进行校验"""
    return pwd_context.verify(plain_password, hash_password)


def get_password_hash():
    return pwd_context.hash


def jwt_get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def jwt_authenticate_user(fake_db, username: str, password: str):
    user = jwt_get_user(fake_db, username)
    if not user:
        return False
    if not verity_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # 设置 15mins token 过期
    to_encode.update({"expire": timegm(expire.utctimetuple())})  # jwt包默认exp 自定义键值需要转换类型
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


@app06.post("/jwt/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = jwt_authenticate_user(fake_db=fake_users_db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"}


async def jwt_get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        playload = jwt.decode(token, key=SECRET_KEY,algorithms=ALGORITHM)
        username: str = playload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokeData(username=username)
    except JWTError:
        raise credentials_exception
    user = jwt_get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def jwt_get_current_active_user(current_user: User = Depends(jwt_get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    return current_user


@app06.get("/jwt/users/me")
async def jwt_read_users_me(current_user: User = Depends(jwt_get_current_active_user)):
    return current_user
