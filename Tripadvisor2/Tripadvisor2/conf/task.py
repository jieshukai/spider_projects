import os
import sys

import redis
from scrapy.cmdline import execute
from scrapy.commands import ScrapyCommand

from Tripadvisor2.settings import REDIS_HOST, REDIS_PORT, REDIS_PWD, REDIS_DB, BASE_DIR
from manage import section, config


class Command(ScrapyCommand):
    default_settings = {'LOG_ENABLED': False}

    def run(self, args, opts):
        # sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
        # line = 'scrapy crawl {spider_name}'.format(spider_name=section.get('name'))
        # execute(line.split())
        if 'list' in args.split():
            print(config.sections())
        print('hello')

    def start_id(self, args, opts):
        client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD, db=REDIS_DB)

        redis_key = section.get('name') + ':start_urls'
        start_url = section.get('start_url')
        client.lpush(redis_key, start_url)

    def list(self, args, pits):
        print(config.sections())
