# -*- coding: utf-8 -*-
import os
import time
import scrapy
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Tripadvisor.items import TripadvisorItem
from Tripadvisor.start import section


class ZhujiajiaoSpider(scrapy.Spider):
    """
    属性：
        name： spider名称
    方法：

    """
    name = 'super_compose_all'
    allowed_domains = ['tripadvisor.cn', 'ccm.ddcdn.com']
    start_urls = [
        section.get('start_url'),
    ]
    page_url = start_urls[0].replace('-Reviews-', '-Reviews-or{}-')
    # 可选语种 en,zhCN,zhTW
    language = section.get('language')

    def parse(self, response):
        print('1--开始爬虫', response.url)
        page_num = int(section.get('page_num'))

        # 创建 浏览器
        driver, wait = self.create_selenium_chrome(response.url)
        # 访问url
        #   page_num 为1 访问原网页
        #   page_num 不为1 访问 指定页数
        if page_num == 1:
            driver.get(response.url)
        else:
            driver.get(self.page_url.format(page_num * 10))

        wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.partial_entry')))

        # 切换语种

        if self.language != 'zhCN':
            self.change_language(self.language, driver, wait)

        while 1:
            print('2--等待 出现tbody')
            html = etree.HTML(driver.page_source)
            pbody = html.xpath("//div[contains(@class,'rev_wrap ui_columns is-multiline')]")

            total_num = html.xpath("//a[contains(@class,'pageNum last')]/text()")[0]
            print(page_num, total_num)
            # if page_num > 2:
            if page_num > int(total_num) - 1:
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
                add_time = commit_p.xpath('./div[2]/span[2]/@title')[0]
                # title
                title = '_'.join(commit_p.xpath('./div[2]/div[1]/a/span/text()'))
                # 环比
                content = commit_p.xpath('./div[2]//div/div/p/text()')[0]
                # image_url
                image_urls = commit_p.xpath(
                    ".//div[@class='inlinePhotosWrapper']//img/@src | ./div[2]//div[@class='inlinePhotosWrapper']//img/@data-lazyurl")
                item['username'] = username
                item['user_loc'] = user_loc
                item['bubble'] = bubble
                item['add_time'] = add_time
                item['title'] = title
                item['content'] = content
                item['image_urls'] = [i.replace('photo-l', 'photo-s') for i in image_urls]
                item['language'] = self.language
                yield item

            try:
                time.sleep(0.2)
                driver.get(self.page_url.format(page_num * 10))
                wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.partial_entry')))
                if self.language == 'en':
                    self.click_more(driver, wait)
            except Exception as e:
                print("出错了==", e)
                print("当前页数===============", page_num)
            page_num += 1

        driver.quit()

    def create_selenium_chrome(self, url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 不打开chrome GUI的情况在Chrome下执行我们的Selenium脚本。
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        wait = WebDriverWait(driver, 10)
        print('-----创建浏览器和等待成功')
        return driver, wait

    def change_language(self, language, driver, wait):
        print('访问成功------，切换语种')
        if language == 'en':
            try:
                driver.find_element_by_xpath("//div[@data-value='en']").click()
                print('en点击成功')
                wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.partial_entry')))
                time.sleep(2)
                if self.language == 'en':
                    self.click_more(driver, wait)
            except Exception as e:
                print(e)
                raise e

    def write_local(self, name, data):
        if not os.path.exists(name):
            with open(name, 'w', encoding='utf-8') as f:
                f.write(data)
        else:
            print('已存在该文件')
            # raise Exception

    def click_more(self, driver, wait):
        try:
            # self.write_local('./data/en.html', driver.page_source)
            wait.until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//div[@class='ui_column is-9']//p[@class='partial_entry']/span")))

            driver.find_element_by_xpath(
                "//div[@class='ui_column is-9']//p[@class='partial_entry']/span").click()
            print('展示全部信息成功-----')
            wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.partial_entry')))
            time.sleep(1)
        except Exception as e:
            raise e


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl super_compose_all'.split())
