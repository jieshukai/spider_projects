# -*- coding: utf-8 -*-
import os

import requests
import scrapy


class RedisdocSpider(scrapy.Spider):
    name = 'redisdoc'
    allowed_domains = ['redisdoc.com']
    start_urls = ['http://redisdoc.com/index.html']
    url = 'http://redisdoc.com/'
    DB = os.path.join(os.path.realpath('./'), 'redisdoc')

    def parse(self, response):
        print('url-----', response.url)
        # 写入主页
        name = response.url.split('/')[-1]
        self.write_body(name, self.DB, response.body)
        # 创建列表文件夹
        # 1. 静态文件
        css_hrefs = response.xpath('/html/head/link[@rel="stylesheet"]/@href').extract()
        for css_href in css_hrefs:
            print(css_href)
            yield scrapy.Request(self.url + css_href, callback=self.parse_detail)
        js_hrefs = response.xpath('/html/head/script[@type="text/javascript"]/@src').extract()
        for js_href in js_hrefs:
            print(js_href)
            yield scrapy.Request(self.url + js_href, callback=self.parse_detail)
        img_hrefs = response.xpath('//img/@src').extract()
        for img_href in img_hrefs:
            print(img_href)
            yield scrapy.Request(self.url + img_href, callback=self.parse_detail)

        #
        # 2. 列表
        title_hrefs = response.xpath("//td//ul/li/a[@class]/@href").extract()
        for title_href in title_hrefs:
            yield scrapy.Request(self.url + title_href, callback=self.parse_detail)

    def parse_detail(self, response):
        print('url---', response.url)
        name = response.url.split('/')[-1]
        if ~name.rfind('#'):
            name = name[:name.index('#')]
        dirname = response.url.split('/')[-2]
        dirs = os.path.join(self.DB, dirname)
        self.write_body(name, dirs, response.body)

    def write_body(self, name, dirs, body):
        path = os.path.join(dirs, name)
        self.dirsetnx(dirs)
        print(path)
        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(body)

    def dirsetnx(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

if __name__ == '__main__':
    # DB = os.path.join(os.path.realpath('./'), 'redisdoc')
    # url = 'http://redisdoc.com/_static/basic.css'
    # name = url.split('/')[-1]
    # dirname = url.split('/')[-2]
    # dirs = os.path.join(DB,dirname)
    #
    # response = requests.get(url)
    # path = os.path.join(dirs,name)
    # print(path)
    # with open(path, 'wb') as f:
    #     f.write(response.content)
    # # import time
    # time.perf_counter()

    ids = [1, 2, 3, 3, 4, 2, 3, 4, 5, 6, 1, 45, 54, 34, 54]

    a2 = list(set(ids))
    print(a2)
    print(ids)
    blist = []
    for i in ids:
        if i not in blist:
            blist.append(i)
    print(blist)
    import logging

    log = logging.basicConfig()
