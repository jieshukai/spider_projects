import configparser
from Tripadvisor.data import datatools
config = configparser.ConfigParser()
config.read('conf/spider.cfg', encoding='utf-8')
section = config['disneyland']
# section['language'] = 'en'
# section['page_num'] = '1'
is_toexcel = True
is_tospider = False
if __name__ == '__main__':
    print(config.sections())
    print(section.get('language'))
    if is_tospider:
        from scrapy import cmdline
        cmdline.execute('scrapy crawl super_compose_all'.split())

    if is_toexcel:
        datatools.main()