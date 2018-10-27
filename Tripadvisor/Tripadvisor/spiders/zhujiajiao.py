# -*- coding: utf-8 -*-
import scrapy


class ZhujiajiaoSpider(scrapy.Spider):
    name = 'zhujiajiao'
    allowed_domains = ['tripadvisor.cn']
    start_urls = ['http://tripadvisor.cn/']

    def parse(self, response):
        pass
