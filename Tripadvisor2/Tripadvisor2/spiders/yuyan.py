# -*- coding: utf-8 -*-
import re
import time

import scrapy
from scrapy import Selector
from scrapy.loader.processors import MapCompose, Compose
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from Tripadvisor2.items import Tripadvisor2Item, MyLoader

from scrapy_redis import spiders


class TripsSpider(spiders.RedisSpider):
    name = 'yuyan'
    allowed_domains = []
    start_urls = ['https://www.tripadvisor.cn/Attraction_Review-g308272-d324259-Reviews-Yu_Garden_Yuyuan-Shanghai.html']
    verbose_name = '上海豫园'
    language = 'en'
    start_url = 'https://www.tripadvisor.cn/Attraction_Review-g308272-d324259-Reviews-Yu_Garden_Yuyuan-Shanghai.html'

    def start_requests(self):
        if self.language == 'en':
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 不打开chrome GUI的情况在Chrome下执行我们的Selenium脚本。
            chrome_options.add_argument('--disable-gpu')
            # self.browser = webdriver.Chrome(chrome_options=chrome_options)
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
            self.wait = WebDriverWait(self.browser, 10)
            self.browser.set_page_load_timeout(30)  # 最长等待时间
            self.count = 0
            # self.browser.get(self.start_url)
            # print('打开浏览器成功')
            # 点击英文
            # self.browser.find_element_by_xpath("//div[@data-value='en']").click()
            # print('点击英文成功')
            # time.sleep(2)
        # return self.next_requests()
        yield scrapy.Request(self.start_url)
    # 开始请求
    def parse(self, response):
        """
        1. 请求第一页 url1 = section.get('start_url')
            获取 item 信息 并打印
            计数 1
            获取总 评论数量
        2. 循环：判断 计数 < 总品评论数量/10
            请求 下一页 url2 = url1.replace('','10')
            计数 2
        """
        print('请求---', response.url)
        # 总评论数
        total_comment = response.xpath("//a[contains(@class,'pageNum last')]//text()").extract_first()
        for block in response.xpath("//div[contains(@class,'rev_wrap ui_columns is-multiline')]"):
            loader = MyLoader(item=Tripadvisor2Item())
            loader.selector = Selector(text=block.get())
            loader.add_value('language', self.language)
            loader.add_value('verbose_name', self.verbose_name)
            # 评论列表 爬取
            loader.add_xpath('username', "//div[@class='info_text']/div[1]/text()")
            loader.add_xpath('user_loc', "//div[@class='userLoc']//text()")
            loader.add_xpath('bubble', '//div[@class="ui_column is-9"]/span[1]/@class', MapCompose(lambda x: x[-2:]))
            loader.add_xpath('add_time', '//div[@class="ui_column is-9"]/span[2]/@title')
            loader.add_xpath('title', '//div[@class="ui_column is-9"]/div[1]/a/span/text()')
            loader.add_xpath('content', '//div[@class="ui_column is-9"]/div/div/p/text()')
            # image_urls = scrapy.Field()

            # MapCompose 和 Compose 区分
            loader.add_xpath('image_urls',
                             "//div[@class='inlinePhotosWrapper']//img/@src",
                             MapCompose(lambda x: x.replace('photo-l', 'photo-s')),
                             Compose(lambda x: [i for i in x if i.startswith('https')]))
            # images = scrapy.Field()
            # image_paths = scrapy.Field()
            yield loader.load_item()
            #

        while self.count < int(total_comment):
            self.count += 1
            next_url = self.start_url.replace('-Reviews-', '-Reviews-or{}-'.format(self.count * 10))
            print('下一次请求', next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)
    #
    # def closed(self, spider):
    #     print("spider closed")
    #     self.browser.close()
