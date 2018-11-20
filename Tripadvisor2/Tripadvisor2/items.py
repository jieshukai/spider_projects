# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import socket
from urllib.parse import urlparse

import scrapy
from pytz import unicode
from scrapy import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity, Compose


# from twisted.python import unicode


class Tripadvisor2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    language = scrapy.Field()
    # 评论列表 爬取
    username = scrapy.Field()
    verbose_name = scrapy.Field()
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
    image_paths = scrapy.Field()

    server = scrapy.Field()


def lower_processor(self, values):
    for v in values:
        yield v.upper()


class MyLoader(ItemLoader):
    # 定义默认 输入输出
    # 输入 自定义到 spiders中
    # 这里只进行 输出定义
    default_output_processor = TakeFirst()
    # default_input_processor = TakeFirst()

    # username_in = MapCompose(unicode.title)
    # username_out = Join()

    # content_in = MapCompose(unicode.strip)

    image_urls_out = Identity()
    images_out = Identity()
    image_paths_out = Identity()


if __name__ == '__main__':
    # item 常用方法练习
    item = Tripadvisor2Item()
    # 1. 赋值
    item['username'] = 'a123人'
    item.setdefault('content', 'aaa')
    item.__setitem__('content', 'ccc')
    # 2. 判断
    print(item.__contains__('content'))
    # 3. 获取
    print(item.__getitem__('content'))
    print(item.get('content'))
    # 4. 更新 删除
    print(item.update({'username': '1234'}))
    item.pop('username')
    # 4 查看
    print(item.values())
    print(item.items())

    # itemloader 常用方法练习
    # il = ItemLoader(item=Tripadvisor2Item())
    il = MyLoader(item=Tripadvisor2Item())
    # il.add_value('username', [u'Welcome to my', u'<strong>website</strong>'])
    # il.add_value('content', [u'&euro;', u'<span>1000</span>'])
    # 输入  value  xpath
    il.selector = Selector(text='<span>  1000a </span><span>2222</span><span>3333</span>')
    # 类型转换
    il.add_xpath('content', '//span/text()', TakeFirst(), float, re=r'[.0-9]+')

    il.selector = Selector(text='<span>asdf<img src="aaa"></span><span>123<img src="bbb" ></span><span>SDFG</span>')
    il.add_xpath('title', '//span', )
    il.add_xpath('username', '//img/@src', MapCompose(unicode.strip))

    #  断点提取
    img = il.nested_xpath('//span')
    img.add_xpath('image_urls', './img/@src')
    # 输出 get value xpath
    print('gent_value--:', il.get_value('content', TakeFirst()))
    # 正则的使用
    print('get_xpath--:', il.get_xpath('//span', re=r'\d+'))
    print()
    il.add_xpath('bubble', '//span', MapCompose(lambda x: x[-2:]))

    # 自定义输出  列表 需要 MapCompose
    # il.bubble_out = Identity()
    # il.content_out = MapCompose(unicode.strip)
    # context 传递
    il.context['a'] = 1
    print(il.context.get('a'))
    il.add_value('server',
                 'https://www.tripadvisor.cn/Attraction_Review-g308272-d324259-Reviews-or10-Yu_Garden_Yuyuan-Shanghai.html',
                 MapCompose(lambda x: urlparse(x).netloc))
    print(urlparse(
        'https://www.tripadvisor.cn/Attraction_Review-g308272-d324259-Reviews-or10-Yu_Garden_Yuyuan-Shanghai.html').netloc)
    # item = il.load_item()
    # print(il.load_item().get('bubble'))
    # print(il.item)
    # print(list(il.item))
    # print(il.item.get('bubble'))

    loader = MyLoader(item=il.load_item())
    loader.selector = Selector(text='<a />')
    loader.add_value('user_loc','中国')
    print(loader.load_item())
