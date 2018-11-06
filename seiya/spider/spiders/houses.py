import random

import scrapy

from seiya.spider.items import HouseItem


class HousesSpider(scrapy.Spider):
    """链家网租房数据爬虫

    """
    name = 'houses'
    allowed_domains = ['lianjia.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'}

    def start_requests(self):
        urls = [
            'https://sh.lianjia.com/zufang/pudong/pg{}rco10/'.format(i) for i in range(100, 101)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for job in response.css('ul#house-lst li'):
            name = job.css(
                'div.info-panel > h2 > a::text').extract_first()
            xiaoqu = job.css(
                'div.where span.region::text').extract_first()
            huxing = job.css(
                'div.where span.zone span::text').extract_first()
            mianji = job.css(
                'div.where span.meters::text').extract_first()
            chaoxiang = job.css(
                'div.where > span:nth-child(4)::text').extract_first()
            quan = job.css(
                'div.other > div > a::text').extract_first()
            other = job.css(
                'div.other div.con::text').extract()
            price = job.css(
                'div.price > span::text').extract_first()
            labels = job.css(
                'div.chanquan div.view-label span::text').extract()

            yield HouseItem({
                'area':'上海,浦东',
                'name': name,
                'xiaoqu':xiaoqu,
                'huxing':huxing,
                'mianji':mianji,
                'chaoxiang':chaoxiang,
                'quan':quan,
                'other':other,
                'labels':labels,
                'price':price,
            })

        # 自动发现下一页链接，连续爬取可能会被重定向到登录页，导致无法爬取后续页面
        # pages = response.css(
        #     'div.pager_container a.page_no::attr(href)').extract()
        # if pages and pages[-1].startswith('https://'):
        #     yield response.follow(pages[-1], callback=self.parse)
