#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-05-15
LastEditTime: 2022-05-17
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/coronavirus/models.py
'''

from sqlalchemy import Column, ForeignKey, String, Integer, BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base

class City(Base):
    __tablename__ = 'city'  # 数据表的表名
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
    country = Column(String(100), nullable=False, comment='国家')
    country_code = Column(String(100), nullable=False, comment='国家代码')
    country_population = Column(BigInteger, nullable=False, comment='国家人口')
    data = relationship('Data', back_populates='city')  # 'Data' 是关联的类名；'back_populates' 来指定反向查询的属性名
    
    create_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {"order_by": country_code}  #  默认正序，倒序加上country_code.dese() 方法
    
    def __repr__(self) -> str:
        return f'{self.country}_{self.province}'
    
class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), comment='所属省/直辖市')  # ForeignKey 里面的字符串格式不是 类名.属性名，而是 表明.字段名
    date = Column(Date, nullable=False, comment='数据日期')
    confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
    death = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
    recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
    city = relationship('City', back_populates='data')

    create_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    __mapper_args__ = {"order_by": date.desc()} 
    
    def __repr__(self) -> str:
        return f'{repr(self.date)}: 确诊{self.confirmed}例'