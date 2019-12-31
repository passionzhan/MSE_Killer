#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Zhan
# @Date  : 12/27/2019
# @Desc  :

import json
from functools import reduce

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

from utility import *

# 火狐浏览器
browser = webdriver.Firefox()
# url = r'file:///' + reduce(os.path.join,[os.getcwd(),'testHtml','main.html'])
# BrowserHelper.openUrl(browser, url)
#
#
# vNode = BrowserHelper.find_element(browser, '//input', )
# div = BrowserHelper.find_element(browser, '//div', )
# print(div.is_displayed())
# successed = False
# cur_url = browser.current_url
# wait_time = 0
# while not successed:
#     vStr = input('输入值: ')
#     vNode.clear()
#     vNode.send_keys(vStr)
#
#     btn = BrowserHelper.find_element(browser, '//button[contains(text(),"开始演示模态框")]', )
#     BrowserHelper.eleClick(btn)
#
#     wait_time = 0
#     while True:
#         forward_url = browser.current_url
#         if forward_url != cur_url:
#             successed = True
#             print("恭喜，成功！")
#             break
#         elif div.is_displayed():
#             close_btn = BrowserHelper.find_element(div,'//button[contains(text(),"×")]')
#             BrowserHelper.eleClick(close_btn)
#             successed = False
#         else:
#             time.sleep(0.2)
#             wait_time += 0.2
#             if wait_time > 3:
#                 successed = False
#                 break





url = r'file:///' + reduce(os.path.join,[os.getcwd(),'mse_source','order.html'])
BrowserHelper.openUrl(browser, url)

div = BrowserHelper.find_element(browser, '//div[@id="alert_model"]', )

print(div.is_displayed())
repr(div)

loadingBg_div = BrowserHelper.find_element(browser, '//div[@id="loadingBg"]', wTime=0.5, wStr=u"没有找到等待框！")
if loadingBg_div:
    browser.execute_script("arguments[0].remove();", loadingBg_div)

if div.is_displayed():
    close_btn = BrowserHelper.find_element(div,'//a[@id="closeThePage" and contains(text(),"x")]')
    BrowserHelper.eleClick(close_btn)

# browser.
print(repr(div))


# while True:
#     myWait = WebDriverWait(browser, 0.5)
#     myWait.until(EC.presence_of_element_located((By.XPATH, lStr)))



