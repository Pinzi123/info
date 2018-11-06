# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import re

from sqlalchemy.orm import sessionmaker

from seiya.db import engine, Session, JobModel,FoodModel,HouseModel
from seiya.spider.items import JobItem,FoodItem,HouseItem


class PersistentPipeline(object):
    """持久化数据 Pipeline

    """

    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            return self._process_job_item(item)
        elif isinstance(item, FoodItem):
            return self._process_food_item(item)
        elif isinstance(item, HouseItem):
            return self._process_house_item(item)
        else:
            return item

    def _process_job_item(self, item):
        city = item['city'].split('·')[0]

        salary_lower, salary_upper = 0, 0
        m = re.match(r'[^\d]*(\d+)k-(\d+)k', item['salary'])
        if m is not None:
            salary_lower, salary_upper = int(m.group(1)), int(m.group(2))

        experience_lower, experience_upper = 0, 0
        m = re.match(r'[^\d]*(\d+)-(\d+)', item['experience'])
        if m is not None:
            experience_lower, experience_upper = int(
                m.group(1)), int(m.group(2))

        tags = ' '.join(item['tags'])

        model = JobModel(
            title=item['title'],
            city=city,
            salary_lower=salary_lower,
            salary_upper=salary_upper,
            experience_lower=experience_lower,
            experience_upper=experience_upper,
            education=item['education'],
            tags=tags,
            company=item['company'],
        )

        self.session.add(model)

        return item

    def _process_food_item(self, item):
        agvExp,score=0,0
        m = re.match(r'￥(\d+)', item['agvExp'])
        if m is not None:
            agvExp = int(m.group(1))
        m = re.match(r'(.*)(\d{2})', item['score'])
        if m is not None:
            score = int(m.group(2))/10.0
        model = FoodModel(
            label = item['label'],
            name = item['name'],
            score = score,
            reviewNum = int(item['reviewNum']),
            agvExp = agvExp,
            fenlei = item['fenlei'],
            quan = item['quan'],
            addr = item['addr'],
            kouwei = float(item['kouwei']),
            huanjin = float(item['huanjin']),
            fuwu = float(item['fuwu']),
        )

        self.session.add(model)

        return item

    def _process_house_item(self, item):
        mianji = item['mianji'].split('平米')[0]
        louceng = item['other'][0]
        years = item['other'][1]
        model = HouseModel(
            area = item['area'],
            name = item['name'],
            xiaoqu = item['xiaoqu'].replace("\xa0\xa0", ""),
            huxing = item['huxing'].replace("\xa0\xa0", ""),
            mianji = float(mianji),
            chaoxiang = item['chaoxiang'],
            quan = item['quan'],
            louceng = louceng,
            years = years,
            labels = ' '.join(item['labels']),
            price = int(item['price']),
        )
        self.session.add(model)
        return item
