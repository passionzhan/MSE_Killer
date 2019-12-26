#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: Zhan
# @Date  : 12/25/2019
# @Desc  : 剑桥mse报名脚本
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

from utility import *

with open('user_config.cfg', 'r',encoding='utf-8') as f:
    user_config = json.load(f)

with open('basic_config.cfg', 'r',encoding='utf-8') as f:
    basic_config = json.load(f)

# 火狐浏览器
browser = webdriver.Firefox()
try:
    # step1、打开MSE官网
    while True:
        if BrowserHelper.openUrl(browser, basic_config['MSE_url'],):
            break
        logger.error("尝试打开MSE官网出现问题，请检查网络状况，1分钟后重试")
        time.sleep(60)

    #  step2、进入报名页面，并登录
    entry_enroll_button = BrowserHelper.find_element(browser, basic_config['exam_entry_button'], )
    BrowserHelper.eleClick(entry_enroll_button)

    # 处理新打开页面情况
    time.sleep(2)
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
    login_url = browser.current_url
    print(login_url)

    # 登录成功就直接进行下一步
    max_Try_Num = 5 #  最大重试5次
    login_successed = False
    while not BrowserHelper.isLogin(browser, basic_config['login_flag']):
        #  需要登录，用户名，密码登录
        if max_Try_Num > 0:
            login_successed = BrowserHelper.login_up(browser,
                                                     basic_config['login_flag'],
                                                     basic_config['submit_bnt'],
                                                     basic_config['user_input'],
                                                     basic_config['pwd_input'],
                                                     user_config['user'],
                                                     user_config['pwd'],
                                                     basic_config['verifiction_input'])
            if login_successed:
                # 登陆成功，保存cookie
                # todo
                # RedisHelper.saveCookie(self.browser, self.name)
                break
            else:
                max_Try_Num -= 1
                logger.error("登录不成功,请检查,30s后尝试重新登录")
                time.sleep(15)
                # 登陆不成功,一定要重新打开登陆页面,防止之前登陆操作点击登陆按钮页面发生跳转
                BrowserHelper.openUrl(browser, login_url, )
                time.sleep(15)

    if not login_successed:
        logger.error("尝试登录一直不成功，请检查，将退出程序")
        exit(1)

    # step3、 考试协议，选择同意
    # 拖动使同意按钮可见
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    agreeBtn = BrowserHelper.find_element(browser, basic_config['agree_btn'], )
    BrowserHelper.eleClick(agreeBtn)


    # step4、 选择考点，报名项目、报名
    # 选考试名称
    exam_Name_str = basic_config['base_exam_name'] % user_config['exam_name']
    exam_Name_btn = BrowserHelper.find_element(browser, exam_Name_str,)
    BrowserHelper.eleClick(exam_Name_btn)
    # 选地区
    region_Selector = Select(BrowserHelper.find_element(browser,basic_config['exam_region_selector']))  # 实例化Select
    region_Selector.select_by_visible_text(user_config['exam_region_name'])
    # 选科目
    exam_type_str = basic_config['base_exam_type'] % user_config['exam_type_name']
    exam_type_btn = BrowserHelper.find_element(browser, exam_type_str,)
    exam_type_id = exam_type_btn.get_attribute("attrval")
    BrowserHelper.eleClick(exam_type_btn)

    next_step_btn = None
    radio_selector_btn = None
    while True:
        #  选考点
        for address in user_config['exam_address_name_list']:
            exam_address_btn_str = basic_config['base_exam_address'] % address
            exam_address_btn = BrowserHelper.find_element(browser, exam_address_btn_str, wTime=0.5,)
            BrowserHelper.eleClick(exam_address_btn)
            radio_selector_btn_str = basic_config['base_radio_selector'] % exam_type_id
            radio_selector_btn = BrowserHelper.find_element(browser, radio_selector_btn_str, wTime=0.5,)
            if radio_selector_btn:
                next_step_btn = BrowserHelper.find_element(browser, basic_config['next_step_btn'], wTime=0.5, )
                if next_step_btn:
                    BrowserHelper.eleClick(next_step_btn)
                    logger.info("恭喜你，报名成功！请抓紧填写报名信息并在24小时内确认缴费")
                    break

finally:
    browser.close()