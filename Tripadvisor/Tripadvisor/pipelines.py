# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import scrapy
from hashlib import md5
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.defer import defer_result, mustbe_deferred
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.request import request_fingerprint
from twisted.internet.defer import DeferredList, Deferred

from Tripadvisor.settings import BASE_DIR
from Tripadvisor.start import section


class TripadvisorPipeline(object):
    """
    属性 ： name，language
    方法 ： open_spider: 创建 json文件
            close_spider: 写入 item数据
            process_item: 关闭文件
    """
    name = section.get('name')
    language = section.get('language')

    def open_spider(self, spider):
        self.file = open(os.path.join(BASE_DIR, 'data/json/{}_{}.json'.format(self.name, self.language)), 'a+',
                         encoding='utf-8')
        self.file.write('[\n')
        print('open spider ---------')

    def close_spider(self, spider):
        self.file.write('{}]')
        self.file.close()
        print('close_spider ---------')

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False) + ',\n')
        return item


class TripadvisorImagePipeline(ImagesPipeline):
    """
    请求顺序总结
        1. get_media_requests ： 获取 image_urls 加入到 Request队列
            "image_urls": [
                "https://ccm.ddcdn.com/photo-l/12/ac/59/81/photo0jpg.jpg"
            ],
        2. file_path ： 获取图片名称和路径，根据网页配置
            path = '{}'.format('_'.join(request.url.split('/')[-5:]))
        3. item_completed：当图片下载完, images 将被更新到结构中,这个组将包含一个字典列表,
            "images": [
              {
                "url": "https://ccm.ddcdn.com/photo-l/12/ac/59/81/photo0jpg.jpg",
                "path": "12_ac_59_81_photo0jpg.jpg",
                "checksum": "352c4ce9b7105e9075c8f5574fb8471e"
              }
            ]
            根据字典结构存储 image_paths
            item['image_paths'] = [os.path.join(IMAGES_STORE, x['path']) for ok, x in results if ok]

    """
    DEFAULT_IMAGES_URLS_FIELD = 'image_urls'

    # DEFAULT_IMAGES_RESULT_FIELD = 'image_'
    def process_item(self, item, spider):
        info = self.spiderinfo
        requests = arg_to_iter(self.get_media_requests(item, info))
        dlist = [self._process_request(r, info) for r in requests]
        dfd = DeferredList(dlist, consumeErrors=True)
        return dfd.addCallback(self.item_completed, item, info)

    def get_media_requests(self, item, info):
        image_urls = item['image_urls']
        for url in image_urls:
            yield scrapy.Request(url, meta={'item': item}, dont_filter=True)

    def file_path(self, request, response=None, info=None):
        item = request.meta['add_time']
        image_name = '{}-{}.jpg'.format(item['add_time'], md5(request.url.encode('utf-8')).hexdigest())
        image_path = os.path.join(item['verbase_name'], item['language'])
        print('图片路径', os.path.join(image_path, image_name), '开始下载')
        return os.path.join(image_path, image_name)

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.images_result_field in item.fields:
            item[self.images_result_field] = [x for ok, x in results if ok]
        item['image_paths'] = [os.path.join('images_{}'.format(section.get('verbose_name')), x['path']) for ok, x in
                               results if ok]
        print(item['image_paths'], 'aaaaaaaaa')
        return item
    def _process_request(self, request, info):
        fp = request_fingerprint(request)
        cb = request.callback or (lambda _: _)
        eb = request.errback
        request.callback = None
        request.errback = None

        # Return cached result if request was already seen
        if fp in info.downloaded:
            return defer_result(info.downloaded[fp]).addCallbacks(cb, eb)

        # Otherwise, wait for result
        wad = Deferred().addCallbacks(cb, eb)
        info.waiting[fp].append(wad)

        # Check if request is downloading right now to avoid doing it twice
        if fp in info.downloading:
            return wad

        # Download request checking media_to_download hook output first
        info.downloading.add(fp)
        dfd = mustbe_deferred(self.media_to_download, request, info)
        dfd.addCallback(self._check_media_to_download, request, info)
        dfd.addBoth(self._cache_result_and_execute_waiters, fp, info)
        # dfd.addErrback(lambda f: logger.error(
        #     f.value, exc_info=failure_to_exc_info(f), extra={'spider': info.spider})
        # )
        return dfd.addBoth(lambda _: wad)  # it must return wad at last

if __name__ == '__main__':
    print(md5('1231'.encode('utf-8')).hexdigest())
