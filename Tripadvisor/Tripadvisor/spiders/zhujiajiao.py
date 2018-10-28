# -*- coding: utf-8 -*-
import time

import scrapy
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Tripadvisor.items import TripadvisorItem


class ZhujiajiaoSpider(scrapy.Spider):
    name = 'zhujiajiao'
    allowed_domains = ['tripadvisor.cn', 'ccm.ddcdn.com']
    start_urls = [
        'https://www.tripadvisor.cn/Attraction_Review-g308272-d1805650-Reviews-Zhujiajiao_Ancient_Town-Shanghai.html',
    ]
    page_url = 'https://www.tripadvisor.cn/Attraction_Review-g308272-d1805650-Reviews-or{}-Zhujiajiao_Ancient_Town-Shanghai.html'

    # 可选语种 en,zhCN,zhTW
    language = 'en'

    def parse(self, response):
        print('1--开始爬虫', response.url)
        # print(response.xpath("//div[@class='review-container']/text()"))

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 不打开chrome GUI的情况在Chrome下执行我们的Selenium脚本。
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get(response.url)
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.partial_entry')))

        # 切换语种
        if self.language != 'zhCN':
            try:
                # driver.find_element_by_xpath("//div[@class='taLnk']").click()
                driver.find_element_by_xpath("//div[@data-value='{}']".format(self.language)).click()
                wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.partial_entry')))
                time.sleep(1)
                if self.language == 'en':
                    try:
                        driver.find_element_by_xpath(
                            "//div[@class='ui_column is-9']//span[@class='taLnk ulBlueLinks']").click()
                        print('展示全部信息成功-----')
                    except Exception as e:
                        raise e
            except Exception as e:
                print(e)

        # try:
        #     driver.find_element_by_xpath("//div[@class='entry'][1]/p/span[@class='taLnk ulBlueLinks']").click()
        #     wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.taLnk')))
        # except Exception as e:
        #     print(e)
        page_num = 1
        while 1:
            print('2--等待 出现tbody')
            html = etree.HTML(driver.page_source)
            pbody = html.xpath("//div[@class='rev_wrap ui_columns is-multiline']")

            total_num = html.xpath("//a[contains(@class,'pageNum last')]/text()")[0]
            if page_num > 2:
                # if page_num > int(total_num) - 1:
                break
            for commit_p in pbody:
                item = TripadvisorItem()
                # ui2
                username = commit_p.xpath("./div[1]//div[@class='info_text']/div[1]/text()")[0]
                user_loc = ''.join(commit_p.xpath("./div[1]//div[@class='info_text']/div[2]/strong/text()"))
                # ui9
                # bubble
                bubble = commit_p.xpath('./div[2]//span[1]/@class')[0][-2:]
                # add_time
                add_time = commit_p.xpath('./div[2]//span[2]/@title')[0]
                # title
                title = commit_p.xpath('./div[2]//div/a/span/text()')[0]
                # 环比
                content = commit_p.xpath('./div[2]//div/div/p/text()')[0]
                # image_url
                image_urls = commit_p.xpath("./div[2]//div[@class='inlinePhotosWrapper']//img/@data-lazyurl")
                item['username'] = username
                item['user_loc'] = user_loc
                item['bubble'] = bubble
                item['add_time'] = add_time
                item['title'] = title
                item['content'] = content
                item['image_urls'] = image_urls
                item['language'] = self.language
                yield item
            try:
                time.sleep(0.2)
                driver.get(self.page_url.format(page_num * 10))
                wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.partial_entry')))
            except Exception as e:
                print("出错了==", e)
                print("当前页数===============", page_num)
            page_num += 1

        driver.quit()


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl zhujiajiao'.split())
