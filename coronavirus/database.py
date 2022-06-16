#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-05-15
LastEditTime: 2022-05-15
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/coronavirus/database.py
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///./coronavirus.sqlite3'
# SQLALCHEMY_DATABASE_URL = 'postgresql://username:password@host:port/database_name'  # MySQL 或者 PostgreSQL 的连接方法

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    encoding="utf-8",
    echo=True,  # echo=True 表示引擎将用 repr() 函数记录所有语句及其参数列表到日志
    connect_args={"check_same_thread": False}  # 由于 SQLAlchemy 是多线程，指定 check_same_thread=False 来建立的对象任意线程都可用。这个参数只在用 SQLite 数据库时设置
)
# 在 SQLAlchemy 中，CRUD 都是通过会话（Session）进行的，所以我们必须先创建会话，每一个 SessionLocal 实例就是一个数据库的 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True)

# 创建基本的映射类
Base = declarative_base(bind=engine, name='Base')