import datetime
import os

# 默认基本配置
import sys

BOT_NAME = 'Tripadvisor2'
SPIDER_MODULES = ['Tripadvisor2.spiders']
NEWSPIDER_MODULE = 'Tripadvisor2.spiders'
ROBOTSTXT_OBEY = False
BASE_DIR = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
# 文件存储
# FILES_STORE = '/data1/files'
IMAGES_STORE = '/data1/images'
# CLOSESPIDER_ITEMCOUNT = 100  # 最大爬取数量
# 管道 数值越小越优先
ITEM_PIPELINES = {
    'Tripadvisor2.pipelines.tripsitem.Tripadvisor2Pipeline': 101,
    'Tripadvisor2.pipelines.tripsitem.Tripadvisor2ImagePipeline': 100,

    # 'Tripadvisor2.pipelines.es.EsWriter': 800,

    # 'scrapy_redis.pipelines.RedisPipeline': 400,  # 是否存储到redis

}
#
# # 爬虫中间件
# # SPIDER_MIDDLEWARES = {
# #    'Tripadvisor2.middlewares.Tripadvisor2SpiderMiddleware': 543,
# # }
# # 下载中间件
DOWNLOADER_MIDDLEWARES = {

    'Tripadvisor2.middlewares.SeleniumMiddleware': 501,
    'Tripadvisor2.middlewares.Tripadvisor2DownloaderMiddleware': 500,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
# # 调试配置
# DEBUG = True
# if DEBUG:
#     LOG_LEVEL = 'DEBUG'
# else:
#     now = datetime.datetime.now()
#     LOG_FILE_PATH = os.path.join(BASE_DIR, 'log/scrapy_{}_{}_{}.log'.format(now.year, now.month, now.day))
#     LOG_FILE = LOG_FILE_PATH
#     # 日志等级 debug、error
#     LOG_LEVEL = 'ERROR'
#
DOWNLOAD_DELAY = 1
#
# # 线程数量
CONCURRENT_REQUESTS = 32
#
# # scrapy——redis 基本配置
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 不用原来scrapy的去重了，使用自定义的去重过滤器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用自己的调度器
# # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"  # 优先级队列
# # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue" # 普通队列
# # SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack" # 栈
# # REDIS_START_URLS_KEY = '%(name)s:start_urls'
# # REDIS_ITEMS_KEY = '%(spider)s:items'
# # SCHEDULER_FLUSH_ON_START = True  # 开始爬取自动flush
SCHEDULER_PERSIST = True  # 增量爬取
#
# # 数据库配置
# # master 设置
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PWD = ''
REDIS_DB = 2
# slaver 设置
REDIS_URL = 'redis://:{pwd}@{host}:{port}/{db}'.format(pwd=REDIS_PWD, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
#
# # mysql 基本配置
# MYSQL_DBNAME = 'novel_collect'
# MYSQL_URI = 'mysql+pymysql://root:root@localhost:3306'
# # ES数据库配置
# ES_PIPELINE_URL = 'http://es:9200/Tripadvisor2/property'
#
# # spider 配置文件路径
# CONF_PATH = os.path.join(BASE_DIR, 'Tripadvisor2/conf/spiders.cfg')

# 扩展设置
COMMANDS_MODULE = 'Tripadvisor2.conf.task'  # 设置自己的命令
