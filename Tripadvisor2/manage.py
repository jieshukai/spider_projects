# 创建start.py
import configparser
import os
import sys

from scrapy.cmdline import execute
from Tripadvisor2.settings import BASE_DIR

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'Tripadvisor2/conf/spider.cfg'), encoding='utf-8')
section = config['yuyan']
# zhCN 和 en
section['language'] = 'en'

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

    line = 'scrapy crawl {spider_name} -o yuyan.csv'.format(spider_name=section.get('name'))
    execute(line.split())

