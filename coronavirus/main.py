#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-05-15
LastEditTime: 2022-05-19
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/coronavirus/main.py
'''
import json
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl
import requests
from sqlalchemy.orm import Session

from coronavirus import crud, schemas
from coronavirus.database import engine, Base, SessionLocal
from coronavirus.models import City, Data

application = APIRouter()

templates = Jinja2Templates(directory='./coronavirus/templates')  # 实例化Jinja2对象，并将文件夹路径设置为以templates命令的文件夹

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application.post('/create_city', response_model = schemas.ReadCity)
def create_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.province)
    if db_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='City already registered')
    return crud.create_city(db=db, city=city)


@application.get('/get_city/{city}', response_model=schemas.ReadCity)
def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='City not found')
    return db_city


@application.get('/get_cities', response_model = List[schemas.ReadCity])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return db_cities


@application.post('/create_data', response_model=schemas.ReadData)
def create_data_for_city(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    if db_city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='City not found')
    data = crud.create_city_data(db=db, data=data, city_id=db_city.id)
    return data


@application.get('/get_data', response_model=List[schemas.ReadData])
def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    import sys
    return data


def bg_task(url: HttpUrl, db: Session):
    """这里注意一个坑，不要在后台任务的参数中db: Session = Depends(get_db)这样导入依赖"""

    # city_data = requests.get(url=f'{url}?source=jhu&country_code=CN&timelines=false')
    city_data = json.load(open('./coronavirus/data/cities.json', 'r', encoding='utf-8'))
    # if 200 == city_data.status_code:
    if city_data is not None:
        db.query(City).delete()  # 同步数据前先清空原有数据
        for location in city_data['locations']:
            city = {
                'province': location['province'],
                "country": location["country"],
                "country_code": "CN",
                "country_population": location["country_population"]
            }
            print(city)
            crud.create_city(db=db, city=schemas.CreateCity(**city))

    # coronavirus_data =  requests.get(url=f'{url}?source=jhu&country_code=CN&timelines=true')
    coronavirus_data =  json.load(open('./coronavirus/data/data.json', 'r', encoding='utf-8'))
    # if 200 == coronavirus_data.status_code:
    if coronavirus_data is not None:
        db.query(Data).delete()  # 同步数据前先清空原有数据
        for city in coronavirus_data["locations"]:
            db_city = crud.get_city_by_name(db=db, name=city["province"])
            for date, confirmed in city["timelines"]["confirmed"]["timeline"].items():
                data = {
                    "date": date.split("T")[0],  # 把'2020-12-31T00:00:00Z' 变成 ‘2020-12-31’
                    "confirmed": confirmed,
                    "deaths": city["timelines"]["deaths"]["timeline"][date],
                    "recovered": 0  # 每个城市每天有多少人痊愈，这种数据没有
                }
                print(data)
                # 这个city_id是city表中的主键ID，不是coronavirus_data数据里的ID
                crud.create_city_data(db=db, data=schemas.CreateData(**data), city_id=db_city.id)
    

@application.get('/sync_coronavirus_data/jhu')
def sync_coronavirus_data(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """从Johns Hopkins University同步COVID-19数据"""
    background_tasks.add_task(bg_task, "https://covid-tracker-us.herokuapp.com/v2/locations", db)  # https://covid-tracker-us.herokuapp.com/
    return {"message": "正在后台同步数据..."}


@application.get('/')
def coronavirus(request: Request, city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db=db, city=city, skip=skip, limit=limit)
    return templates.TemplateResponse(
        'home.html', context={
            'request': request,  # 注意，返回模板响应时，必须有request键值对，且值为Request请求对象
            'data': data,
            'sync_data_url': '/coronavirus/sync_coronavirus_data/jhu'
        }
    )

