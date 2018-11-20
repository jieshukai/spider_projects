import configparser
from Tripadvisor.data import datatools
config = configparser.ConfigParser()
config.read('conf/spider.cfg', encoding='utf-8')
section = config['yuyan']
section['language'] = 'en'
# section['page_num'] = '1'
is_toexcel = False
is_tospider = True
if __name__ == '__main__':
    print(config.sections())
    print(section.get('language'))
    if is_tospider:
        from scrapy import cmdline
        cmdline.execute('scrapy crawl super_compose_all -o yuyan_en.csv'.split())

    if is_toexcel:
        datatools.main()
