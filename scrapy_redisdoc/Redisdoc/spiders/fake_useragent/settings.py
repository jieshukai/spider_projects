# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

import requests

__version__ = '0.1.11'
# 修改 默认DB: 当前文件夹下
DB = os.path.join(
    os.path.realpath('./'),
    'fake_useragent_{version}.json'.format(
        version=__version__,
    ),
)

CACHE_SERVER = 'https://fake-useragent.herokuapp.com/browsers/{version}'.format(
    version=__version__,
)

BROWSERS_STATS_PAGE = 'https://www.w3schools.com/browsers/default.asp'

BROWSER_BASE_PAGE = 'http://useragentstring.com/pages/useragentstring.php?name={browser}'  # noqa

BROWSERS_COUNT_LIMIT = 50

REPLACEMENTS = {
    ' ': '',
    '_': '',
}

SHORTCUTS = {
    'internet explorer': 'internetexplorer',
    'ie': 'internetexplorer',
    'msie': 'internetexplorer',
    'edge': 'internetexplorer',
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

OVERRIDES = {
    'Edge/IE': 'Internet Explorer',
    'IE/Edge': 'Internet Explorer',
}

HTTP_TIMEOUT = 5

HTTP_RETRIES = 2

HTTP_DELAY = 0.1

if __name__ == '__main__':
    # 爬取服务器上fake_useragent.json 写入本地
    response = requests.get(CACHE_SERVER)
    if response.status_code == 200:
        with open(DB, 'w') as f:
            f.write(response.text)
            print('写入成功', response.status_code)
            print(DB)
    else:
        print('写入失败', response.status_code)
        print('写入失败,请升级fake-useragent','pip install -U fake-useragent')