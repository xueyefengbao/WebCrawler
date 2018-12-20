#!/usr/local/bin/python3.6.5
# -*- coding: utf-8 -*-
# @Time    : 2018/11/13 PM2:54
# @Author  : L
# @Email   : L862608263@163.com
# @File    : 12306.py
# @Software: PyCharm

# 登录
# https://kyfw.12306.cn/otn/resources/login.html

# 单程
# https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=广州,GZQ&ts=深圳北,IOQ&date=2018-11-13&flag=N,N,Y

# 往返

# https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=wf&fs=广州南,IZQ&ts=北京,BJP&date=2018-11-13,2018-11-14&flag=N,N,Y

import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as driverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


from PIL import Image

import random
import base64
import time


class RailwayTickets:
    username = '123123123'
    pwd = '123123123'

    url_of_12306 = "https://kyfw.12306.cn/otn/resources/login.html"

    # 图宽 300, 高190
    # 刷新那个按钮 行高 30
    # start_x 300 / 4(列) / 2(中间点) = 37.5
    # start_y (190 - 30(刷新那个按钮 行高)) / 2(行) / 2(中间点) + 30(起始行高) = 70
    location_list = [ "%d,%d" % (38 + 38 * x, 70 + y * 80) for x in range(0, 7, 2)
                                                           for y in range(0, 2)]
    """
    1 3 5 7
    2 4 6 8
    """

    browser = webdriver.Chrome()

    handler_set = set()

    @staticmethod
    def crop_img(img_path):

        img_list = []

        origin_img = Image.open(img_path)

        img_width, img_height = origin_img.size

        top_rect = (0, 0, img_width, 30)

        origin_img.crop(top_rect)

        # 裁切图片
        top_img = origin_img.crop(top_rect)

        # 保存裁切后的图片
        top_img.save("top_img.png")

        img_list.append("top_img.png")

        bottom_rect = (0, 30, img_width, img_height)

        bottom_img = origin_img.crop(bottom_rect)

        width, height = bottom_img.size

        item_width = int(width / 4)
        item_height = int(height / 2)

        for i in range(4):
            for j in range(2):
                box = (i * item_width, j * item_height, (i + 1) * 73, (j + 1) * 80)
                img = bottom_img.crop(box)
                img.save("%d_%d.png" % (i, j))
                img_list.append("%d_%d.png" % (i, j))
        return img_list

    def login(self):
        browser = webdriver.Chrome()

        wait = driverWait(browser, 100, 0.5)

        browser.get(self.url_of_12306)

        # 等100秒找元素, 0.5秒找一次

        wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'login-account')))

        browser.find_element_by_xpath("//*[@class = 'login-box']/ul/li[2]").click()

        wait.until(ec.visibility_of_element_located((By.ID, 'J-userName')))
        user_name = browser.find_element_by_id('J-userName')
        user_name.click()
        user_name.clear()
        user_name.send_keys(self.username)

        wait.until(ec.visibility_of_element_located((By.ID, 'J-password')))
        password = browser.find_element_by_id('J-password')
        password.click()
        password.clear()
        password.send_keys(self.pwd)

        # 图片元素加载
        wait.until(ec.presence_of_element_located((By.ID, 'J-loginImg')))

        # # 图片
        login_img_src = browser.find_element_by_xpath("//*[@id = 'J-loginImg']").get_attribute("src")
        split_index = login_img_src.find(',')
        base64_str = login_img_src[split_index + 1:]

        # 切图
        # 切成 7份  一份标题  6份内容
        img_data = base64.b64decode(base64_str)

        origin_img_name = 'origin_img.png'

        with open(origin_img_name, 'wb') as origin_img:
            origin_img.write(img_data)
            origin_img.close()

        # google_window_handler = browser.current_window_handle

        # 识别图片

        open_google_vision_js = 'window.open("https://cloud.google.com/vision/")'
        browser.execute_script(open_google_vision_js)

        # wait.until(ec.number_of_windows_to_be(2))
        # newWindow = [window for window in browser.window_handles if window != google_window_handler][0]
        # browser.switch_to.window(newWindow)

        browser.switch_to.window(browser.window_handles[-1])

        wait.until(lambda x: x.find_element_by_id('vision_demo_section'))


        # js_code = "var a = document.documentElement.scrollTop=750"
        # browser.execute_script(js_code)
        # iframe = browser.find_element_by_xpath("//*[@id = 'vision_demo_section']")
        # browser.switch_to.frame(iframe)

        # wait.until(ec.presence_of_element_located((By.ID, 'input')))
        # input_img = browser.find_element_by_xpath("//*[@id = 'input']")
        # input_img.send_keys('/Users/l/Desktop/WebCrawler/Code/12306/top_img.png')

        # # 点击验证码
        # for location in self.location_list:
        #     offset_x, offset_y = location.split(',')
        #     print('click offset_x %s offset_y %s' % (offset_x, offset_y))
        #     ActionChains(driver).move_to_element_with_offset(login_img, offset_x, offset_y).click().perform()
        #
        # # 点击登录
        # login = driver.find_element_by_xpath("//*[@id = 'J-login']")
        # login.click()
        #
        # print(driver.page_source)
        # time.sleep(20)
        # driver.close()




if __name__ == '__main__':
    check_tickets = RailwayTickets()
    check_tickets.login()













