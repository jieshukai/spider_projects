# -*- coding: utf-8 -*-

# Scrapy settings for Tripadvisor project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# 默认基本配置
import os


BOT_NAME = 'Tripadvisor'
SPIDER_MODULES = ['Tripadvisor.spiders']
NEWSPIDER_MODULE = 'Tripadvisor.spiders'
ROBOTSTXT_OBEY = False

# scrapy——redis 基本配置
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter" # 不用原来scrapy的去重了，使用自定义的去重过滤器
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用自己的调度器
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"  # 优先级队列
# SCHEDULER_PERSIST = False  # 是否可以暂停，是否可以继续爬取
# REDIS_HOST = "localhost"
# REDIS_PORT = 6379

# 管道
# pipeline的权重越小优先级越高, 优先下载，在进行媒体爬取
ITEM_PIPELINES = {
    'Tripadvisor.pipelines.TripadvisorPipeline': 302,
    'Tripadvisor.pipelines.TripadvisorImagePipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}

# 爬虫中间件
# SPIDER_MIDDLEWARES = {
#    'Tripadvisor.middlewares.TripadvisorSpiderMiddleware': 543,
# }
# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    'Tripadvisor.middlewares.TripadvisorDownloaderMiddleware': 500,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
# 调试配置
# LOG_FILE = 'log.log'
LOG_LEVEL = 'DEBUG'
DOWNLOAD_DELAY = 2
# IMAGES_THUMBS = {  #缩略小图和大图的尺寸设置
#     'small':(50,50),
#     'big':(270,270),
# }
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
IMAGES_STORE = os.path.join(BASE_DIR, 'images')
CONCURRENT_REQUESTS = 32

if __name__ == '__main__':
    print(BASE_DIR)
