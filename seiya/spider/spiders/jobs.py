import random

import scrapy

from seiya.spider.items import JobItem


class JobsSpider(scrapy.Spider):
    """拉勾网职位数据爬虫

    """
    name = 'jobs'
    allowed_domains = ['lagou.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Cookie': 'WEBTJ-ID=20181021174314-1669601d6de1fd-0ac713cbe7a9ea-163c6656-1296000-1669601d6df203; _ga=GA1.2.1144826558.1540114995; _gid=GA1.2.795058912.1540114995; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1540114995; user_trace_token=20181021174315-bb812772-d515-11e8-94e6-525400f775ce; LGSID=20181021174315-bb81289d-d515-11e8-94e6-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3DUTF-8%26wd%3D%25E6%258B%2589%25E5%258B%25BE; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; LGUID=20181021174315-bb812a9b-d515-11e8-94e6-525400f775ce; X_HTTP_TOKEN=7d8a590e965a8601f319f97f1ed9d1f2; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221669601e3287b4-01764f9d3ce963-163c6656-1296000-1669601e329b45%22%2C%22%24device_id%22%3A%221669601e3287b4-01764f9d3ce963-163c6656-1296000-1669601e329b45%22%2C%22props%22%3A%7B%22%24latest_utm_source%22%3A%22m_cf_cpt_baidu_pc%22%7D%7D; sm_auth_id=q62g00kh91e8mmmy; LG_LOGIN_USER_ID=ca7fc88a5bf252c71f51354b2bca8efa8c6b297bb980414e; _putrc=96AC3588A2B714E1; JSESSIONID=ABAAABAAADEAAFI0E3F47657A2082ED5A0F303FEF080DB6; login=true; unick=%E7%8E%8B%E4%BA%9A%E8%90%8D; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=134; gate_login_token=472fa094a5356637019b2d42d65aadeb22b3c67eb6eb79e3; index_location_city=%E4%B8%8A%E6%B5%B7; _gat=1; LGRID=20181021174521-06c57d8e-d516-11e8-8035-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1540115121',
    }

    def start_requests(self):
        urls = [
            'https://www.lagou.com/zhaopin/{}/'.format(i) for i in range(1, 31)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for job in response.css('ul.item_con_list li'):
            title = job.css(
                'div.list_item_top div.p_top h3::text').extract_first()
            city = job.css(
                'div.list_item_top div.p_top em::text').extract_first()
            salary = job.css(
                'div.list_item_top div.p_bot span.money::text').extract_first()
            experience, education = job.css(
                'div.list_item_top div.p_bot div.li_b_l::text').re(r'(.+)\s*/\s*(.+)')
            tags = job.css(
                'div.list_item_bot div.li_b_l span::text').extract()
            company = job.css(
                'div.list_item_top div.company_name a::text').extract_first()
            yield JobItem({
                'title': title,
                'city': city,
                'salary': salary,
                'experience': experience,
                'education': education,
                'tags': tags,
                'company': company,
            })

        # 自动发现下一页链接，连续爬取可能会被重定向到登录页，导致无法爬取后续页面
        # pages = response.css(
        #     'div.pager_container a.page_no::attr(href)').extract()
        # if pages and pages[-1].startswith('https://'):
        #     yield response.follow(pages[-1], callback=self.parse)
