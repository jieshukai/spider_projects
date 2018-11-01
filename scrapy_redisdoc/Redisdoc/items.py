# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedisdocItem(scrapy.Item):
    # define the fields for your item here like:

    # 列表页
    list_name = scrapy.Field()

    # 详情页
    detail_name = scrapy.Field()
