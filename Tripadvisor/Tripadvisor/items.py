# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    def __init__(self):
        super(TripadvisorItem, self).__init__()
        print('item 模型建立')
    # language
    language = scrapy.Field()
    # 评论列表 爬取
    username = scrapy.Field()
    user_loc = scrapy.Field()
    #   等级
    bubble = scrapy.Field()
    #   时间
    add_time = scrapy.Field()
    #   标题
    title = scrapy.Field()
    #   内容
    content = scrapy.Field()
    #   链接
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()

