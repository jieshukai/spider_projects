# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os

import scrapy
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import arg_to_iter
from twisted.internet.defer import DeferredList

from Tripadvisor2.settings import BASE_DIR, IMAGES_STORE
from manage import section


class Tripadvisor2Pipeline(object):
    name = section.get('name')
    language = section.get('language')

    def open_spider(self, spider):
        self.file = open(os.path.join(BASE_DIR, 'data/json/{}_{}.json'.format(self.name, self.language)), 'w',
                         encoding='utf-8')
        self.file.write('[\n')
        print('open spider ---------')

    def close_spider(self, spider):
        self.file.write('{}]')
        self.file.close()
        print('close_spider ---------')

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False) + ',\n')
        print('写入item')
        return item


class Tripadvisor2ImagePipeline(ImagesPipeline):
    # 允许 图片地址重定向
    MEDIA_ALLOW_REDIRECTS = True
    DEFAULT_IMAGES_URLS_FIELD = 'image_urls'

    def process_item(self, item, spider):
        if item.get('image_urls'):
            info = self.spiderinfo
            requests = arg_to_iter(self.get_media_requests(item, info))
            dlist = [self._process_request(r, info) for r in requests]
            dfd = DeferredList(dlist, consumeErrors=True)
            return dfd.addCallback(self.item_completed, item, info)
        else:
            return item

    def get_media_requests(self, item, info):
        image_urls = item.get('image_urls')
        if image_urls:
            for url in image_urls:
                yield scrapy.Request(url, meta={'item': item}, dont_filter=True)

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = '{}-{}'.format(item['add_time'], request.url.split('/')[-1])
        # image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        print('图片名称', image_guid)
        print(item.get('verbose_name'), item.get('language'), image_guid)

        image_path = '{}/{}/{}.jpg'.format(item['verbose_name'], item['language'], image_guid)
        # path = os.path.join(IMAGES_STORE, image_path)
        # print('-----', path)
        return image_path

    def item_completed(self, results, item, info):
        # 完成后必须返回 item
        image_path = [x['path'] for ok, x in results if ok]

        if image_path:
            print(item['image_urls'])
            item['image_paths'] = image_path
            print('图片下载成功', image_path)
        else:
            log.msg('图片下载失败--{}'.format(item['image_urls']), level=log.WARNING)
        return item
