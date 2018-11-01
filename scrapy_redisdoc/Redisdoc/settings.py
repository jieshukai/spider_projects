# 默认基本配置
BOT_NAME = 'Redisdoc'
SPIDER_MODULES = ['Redisdoc.spiders']
NEWSPIDER_MODULE = 'Redisdoc.spiders'
ROBOTSTXT_OBEY = False

# scrapy——redis 基本配置
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter" # 不用原来scrapy的去重了，使用自定义的去重过滤器
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用自己的调度器
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"  # 优先级队列
# SCHEDULER_PERSIST = False  # 是否可以暂停，是否可以继续爬取
# REDIS_HOST = "localhost"
# REDIS_PORT = 6379

# 管道
ITEM_PIPELINES = {
    'Redisdoc.pipelines.RedisdocPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}

# 爬虫中间件
# SPIDER_MIDDLEWARES = {
#    'Redisdoc.middlewares.RedisdocSpiderMiddleware': 543,
# }
# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    'Redisdoc.middlewares.RedisdocDownloaderMiddleware': 500,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
# 调试配置
# LOG_FILE = 'log.log'
LOG_LEVEL = 'DEBUG'
DOWNLOAD_DELAY = 1

