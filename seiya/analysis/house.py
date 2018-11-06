import re

from sqlalchemy import func, Float, select, and_
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from seiya.db import engine, Session, JobModel, HouseModel


def count_top10():
    session = Session()
    rows = session.query(
        HouseModel.xiaoqu,
        func.count(HouseModel.xiaoqu).label('count')
    ).group_by(HouseModel.xiaoqu).order_by('count desc').limit(10)
    return [row._asdict() for row in rows]


def all_huxing():
    session = Session()
    rows = session.query(
        (HouseModel.huxing).label('item'),
        func.count(HouseModel.huxing).label('count'),
        func.count(HouseModel.huxing).label('percent')
    ).group_by(HouseModel.huxing).order_by('count desc')
    result = [row._asdict() for row in rows]
    total = 0
    for row in result:
        total += int(row['count'])
    for row in result:
        row['percent'] = round(row['count']/total,2)
    results = {'total':total,'data':result}
    return results


def all_area():
    session = Session()
    rows = session.query(HouseModel.mianji)
    return [float(row._asdict()['mianji']) for row in rows]


def remove2(data):
    al1 = re.findall(r"\d+",data.group(0))
    return al1[0]


def _count_years():
    df = pd.read_sql(select([HouseModel.years]), engine)
    df = df.iloc[:, 0].str.replace(r'\d+.+', remove2)
    dict = {'index': df.index, 'years': df.values}
    df = pd.DataFrame(dict)
    df.index = df['years']
    df = df.filter(regex='\d+', axis=0)
    return df.groupby('years').size().sort_index(ascending=False)


def count_years():
    rows = []
    for item in _count_years().items():
        result = 2018 - int(item[0])
        rows.append({'year': str(result), 'value': item[1]})
    return rows

def _count_years2():
    df = pd.read_sql(select([HouseModel.years]), engine)
    df = df.iloc[:, 0].str.replace(r'\d+.+', remove2)
    dict = {'index': df.index, 'years': df.values}
    df = pd.DataFrame(dict)
    df.index = df['years']
    df = df.filter(regex='\d+', axis=0)
    return df.groupby('years').size().sort_values(ascending=False)


def count_years2():
    rows = []
    for item in _count_years2().items():
        result = 2018 - int(item[0])
        rows.append({'year': str(result), 'value': item[1]})
    return rows


def price_by_xiaoqu_and_huxing():
    df = pd.read_sql(select([HouseModel.xiaoqu,HouseModel.huxing,HouseModel.price]), engine)

    grouped = df.groupby(['huxing', 'xiaoqu'])['price'].mean().groupby(level=0, group_keys=False).nlargest(10)
    print(df.groupby(['huxing', 'xiaoqu']).sum()['price'])
    print(grouped)
    print(grouped.index)
    j = 0
    rows = []
    for i in grouped.index.labels[0]:
        a = grouped.index.labels[0][j]
        b = grouped.index.labels[1][j]
        huxing = grouped.index.levels[0][a]
        xiaoqu = grouped.index.levels[1][b]
        price = grouped[j]
        j = j + 1
        rows.append({'huxing': huxing, 'xiaoqu': xiaoqu, 'price': price})
    return rows
