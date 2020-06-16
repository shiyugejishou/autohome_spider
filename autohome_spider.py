# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from time import sleep
import random

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
base_url = 'https://k.autohome.com.cn/528/index_{}.html#dataList'


def get_max_page():
    """

    :return: 口碑最大页码
    """
    try:
        browser.get(base_url.format('1'))
        # print(base_url.format('1'))
        step_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'first-next-step'))
        )
        sleep(2)
        step_btn.click()
        step_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'second-next-step'))
        )
        sleep(1)
        step_btn.click()
        step_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'go'))
        )
        sleep(1)
        step_btn.click()
        max_num = browser.find_element_by_class_name('page-item-info').text\
            .replace('共', '').replace('页', '').strip()
        max_num = int(max_num)
        return max_page
    except TimeoutException:
        print("获取超时，开始重试...")
        get_max_page()


def get_content(page):
    """

    :param page: 页码
    :return: 爬取内容URL
    """
    new_url = base_url.format(str(page))
    browser.get(new_url)
    html = browser.page_source
    doc = pq(html)
    text_urls = doc('.mouth-remak div > a[href*="k.autohome.com.cn/detail/"]').items()
    for item in text_urls:
        url = item.attr('href')
        sleep(random.randint(1,2))
        get_detail(url)
        sleep(1)


def get_detail(url):
    open_script = 'window.open("{}")'.format(url)
    browser.execute_script(open_script)
    handler = browser.window_handles
    browser.switch_to.window(handler[-1])
    detail_html = browser.page_source
    detail_doc =pq(detail_html)
    # print(detail_doc)
    text_content = detail_doc('.text-con').text()
    print(text_content)
    browser.close()
    browser.switch_to.window(handler[0])
    return text_content


if __name__ == '__main__':
    max_page = get_max_page()
    for page in range(1, max_page):
        print('开始爬取第 ' + str(page) + '页')
        get_content(page)
        sleep(random.randint(1, 5))



