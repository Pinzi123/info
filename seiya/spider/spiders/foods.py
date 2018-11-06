import random

import scrapy

from seiya.spider.items import FoodItem


class FoodsSpider(scrapy.Spider):
    """拉勾网职位数据爬虫

    """
    name = 'foods'
    allowed_domains = ['dianping.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Cookie': 'navCtgScroll=25; showNav=#nav-tab|0|2; navCtgScroll=0; showNav=#nav-tab|0|1; s_ViewType=10; _lxsdk_cuid=166a14b51c6c8-0dc79372e0dd45-163a6651-13c680-166a14b51c6c8; _lxsdk=166a14b51c6c8-0dc79372e0dd45-163a6651-13c680-166a14b51c6c8; _hc.v=3c28667e-f6bd-0dea-f01d-bba568c369a0.1540304360; cy=1; cye=shanghai; dper=69862c9a5da0ab84a12ef4a99e63d17c51264367c4d9622a9510508c379d23ebee67a560c3963699e119bf371c32141c8546e7c47199c53249dd47f3cceea037fa92a4201eff7d8a3dcd74b75c1c1278d599c6bfcc14ad8a22fcd1159b8701fd; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_36384909147; ctu=ff249063815705c3f221aa3dc34716da3b709620fb383dfa449e2b2fc583edd1; uamo=18702515287; _lxsdk_s=%7C%7C3'
    }

    def start_requests(self):
        urls = [
            'http://www.dianping.com/shanghai/ch10/r1326p{}'.format(i) for i in range(2, 51)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for job in response.css('#shop-all-list > ul > li'):
            label = '上海,地铁2号线'
            name = job.css(
                'div.txt div.tit h4::text').extract_first()
            # //#shop-all-list > ul > li:nth-child(4) > div.txt > div.comment > span
            score = job.css(
                'div.txt div.comment span.sml-rank-stars::attr(class)').extract_first()
            # //div.txt > div.comment > a.review-num > b
            reviewNum = job.css(
                'div.txt  div.comment  a.review-num  b::text').extract_first()
            # div.txt > div.comment > a.mean-price
            agvExp = job.css(
                'div.txt  div.comment  a.mean-price b::text').extract_first()
            fenlei = job.css(
                'div.txt  div.tag-addr  span.tag::text').extract_first()
            #  div.txt > div.tag-addr > a:nth-child(3) > span
            quan = job.css(
                'div.txt  div.tag-addr a:nth-child(3) span::text').extract_first()
            addr = job.css(
                'div.txt  div.tag-addr  span.addr::text').extract_first()
            # div.txt > span > span:nth-child(1)
            kouwei = job.css(
                'div.txt  span.comment-list  span:nth-child(1) b::text').extract_first()
            huanjin = job.css(
                'div.txt  span.comment-list  span:nth-child(2) b::text').extract_first()
            fuwu = job.css(
                'div.txt  span.comment-list  span:nth-child(3) b::text').extract_first()
            yield FoodItem({
                'label' : label,
                'name' : name,
                'score' : score,
                'reviewNum' : reviewNum,
                'agvExp' : agvExp,
                'fenlei' : fenlei,
                'quan' : quan,
                'addr' : addr,
                'kouwei' : kouwei,
                'huanjin' : huanjin,
                'fuwu' : fuwu
            })

        # 自动发现下一页链接，连续爬取可能会被重定向到登录页，导致无法爬取后续页面
        # pages = response.css(
        #     'div.pager_container a.page_no::attr(href)').extract()
        # if pages and pages[-1].startswith('https://'):
        #     yield response.follow(pages[-1], callback=self.parse)
