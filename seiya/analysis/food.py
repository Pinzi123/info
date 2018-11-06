from io import BytesIO

from sqlalchemy import func, Float, select, and_
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from seiya.db import engine, Session, FoodModel


def count_top10_quan():
    """商圈前十的商圈
        rows = session.query(
        JobModel.city,
        func.count(JobModel.city).label('count')
    ).group_by(JobModel.city).order_by('count desc').limit(10)
    """
    session = Session()
    rows = session.query(
        FoodModel.quan,
        func.count(FoodModel.quan).label('count')
    ).group_by(FoodModel.quan).order_by('count desc').limit(10)
    return [row._asdict() for row in rows]


def count_top10_quan_1():
    """商圈前十的商圈
        rows = session.query(
        JobModel.city,
        func.count(JobModel.city).label('count')
    ).group_by(JobModel.city).order_by('count desc').limit(10)
    """
    session = Session()
    rows = session.query(
        FoodModel.quan,
        func.count(FoodModel.quan).label('count')
    ).group_by(FoodModel.quan).order_by('count desc').limit(10)
    res = []
    for row in rows:
        res.append(row.quan)
    return res


def count_top10_lei():
    """商圈前十的分类
    """
    session = Session()
    rows = session.query(
        FoodModel.fenlei,
        func.count(FoodModel.fenlei).label('count')
    ).group_by(FoodModel.fenlei).order_by('count desc').limit(10)
    return [row._asdict() for row in rows]


def count_top10_lei_1():
    """商圈前十的分类
    """
    session = Session()
    rows = session.query(
        FoodModel.fenlei,
        func.count(FoodModel.fenlei).label('count')
    ).group_by(FoodModel.fenlei).order_by('count desc').limit(10)
    res = []
    for row in rows:
        res.append(row.fenlei)
    return res


def exp_top10_quan():
    """人均消费前十的商圈
    """
    session = Session()
    rows = session.query(
        FoodModel.quan,
        func.avg(FoodModel.agvExp).cast(Float).label('agvExp')
    ).group_by(FoodModel.quan).order_by('agvExp desc').limit(10)
    return [row._asdict() for row in rows]


def exp_top10_lei():
    """人均消费前十的分类
    """
    session = Session()
    rows = session.query(
        FoodModel.fenlei,
        func.avg(FoodModel.agvExp).cast(Float).label('agvExp')
    ).group_by(FoodModel.fenlei).order_by('agvExp desc').limit(10)
    return [row._asdict() for row in rows]


def hot_res():
    session = Session()
    rows = session.query(
        FoodModel.name,
        ((FoodModel.kouwei+FoodModel.huanjin+FoodModel.fuwu)*FoodModel.reviewNum).label('sum')
    ).order_by('sum desc').limit(10)
    return [row._asdict() for row in rows]


def fenlei_and_quan():
    """热门分类在热门商圈的人均消费对比

    """
    session = Session()
    rows = session.query(
        FoodModel.fenlei,
        FoodModel.quan,
        func.avg(FoodModel.agvExp).cast(Float).label('agvExp')
    ).filter(
        and_(FoodModel.fenlei.in_(count_top10_lei_1()), FoodModel.quan.in_(count_top10_quan_1()))
    ).group_by(FoodModel.fenlei, FoodModel.quan).order_by(FoodModel.quan.desc())
    return [row._asdict() for row in rows]
