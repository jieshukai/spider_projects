# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
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
        self.file = open('./data/json/{}_{}.json'.format(self.name, self.language), 'a+', encoding='utf-8')
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

    def get_media_requests(self, item, info):
        image_urls = item['image_urls']
        for url in image_urls:
            yield scrapy.Request(url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        image_name = '{}'.format('_'.join(request.url.split('/')[-5:]))
        return os.path.join(request.meta['item']['language'], image_name)

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.images_result_field in item.fields:
            item[self.images_result_field] = [x for ok, x in results if ok]
        item['image_paths'] = [os.path.join('images_{}'.format(section.get('verbose_name')), x['path']) for ok, x in results if ok]
        return item


if __name__ == '__main__':
    print()
