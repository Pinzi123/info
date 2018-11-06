# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    """职位 Item

    """
    title = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()


class FoodItem(scrapy.Item):
    label = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    reviewNum = scrapy.Field()
    agvExp = scrapy.Field()
    addr = scrapy.Field()
    fenlei = scrapy.Field()
    quan = scrapy.Field()
    kouwei = scrapy.Field()
    huanjin = scrapy.Field()
    fuwu = scrapy.Field()


class HouseItem(scrapy.Item):
    area = scrapy.Field()
    name = scrapy.Field()
    xiaoqu = scrapy.Field()
    huxing = scrapy.Field()
    mianji = scrapy.Field()
    chaoxiang = scrapy.Field()
    fenlei = scrapy.Field()
    quan = scrapy.Field()
    other = scrapy.Field()
    labels = scrapy.Field()
    price = scrapy.Field()