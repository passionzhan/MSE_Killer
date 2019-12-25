#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: Zhan
# @Date  : 12/25/2019
# @Desc  : 剑桥mse报名脚本

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


from utility import *

MSE_url          = 'http://mse.neea.edu.cn/' # 剑桥通用考级官网
entry_enroll_button_str     = '//div[contains(@class,"gobt")]//a[contains(text(),"进入报名")]' # 进入报名按钮
user                    = 'xxxxx'
pwd                     = 'xxxxxxx'
# login_url               = 'https://member.neea.cn/login/'
need_login_flag_str     = '//button[@id="login_button"]'
login_flag_str          = '//li/a[contains(text(),"退出")]'

# '//form[@id="loginForm"]//input[@id="loginName"]'
# '//form[@id="loginForm"]//input[@id="loginPwd"]'
# //*[@id="loginName"]
'//*[@id="loginName"]'
# uNode_Str        = '//input[@name="loginName"]'
uNode_Str        = '//input[@id="loginName"]'
pNode_Str        = '//input[@name="loginPwd"]'
vNode_Str        = '//input[@name="verificationCode"]'
sNode_Str        = '//button[@id="login_button"]'

agree_btn_str    = '//div[contains(@class,"page-container")]//input[@value="同意"]'


exam_Name_str           = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="time_id"]/a[contains(text(),"2020-04-25 KETPET青少版")]'
exam_region_selector_str        = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd/select[@name="addr"]'
exam_region_name                = "北京"
exam_type_str        = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="projectType"]/a[contains(text(),"CAE")]'
exam_adress_str1        = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="orglist"]/a[contains(text(),"北京外国语大学国际教育集团第一分考点")]'
exam_adress_str2        = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="orglist"]/a[contains(text(),"北京外国语大学国际教育集团第二分考点")]'

radio_selector_str  = '//table[contains(@class,"store_cart_content")]//tr/td/input[@name="selectId"]'
next_step_btn_str = '//div[@id="submit_but"]/button[@onclick="submit()" and contains(text(),"下一步")]'
# 声明浏览器对象，将chromedriver驱动放在chrome浏览器安装目录下，指定驱动的绝对路径
# browser = webdriver.Chrome(executable_path=r'D:\Google\Chrome\Application\chromedriver')

# 火狐浏览器
browser = webdriver.Firefox()
try:
    # step1、打开MSE官网
    while True:
        if BrowserHelper.openUrl(browser, MSE_url,):
            break
        logger.error("尝试打开MSE官网出现问题，请检查网络状况，1分钟后重试")
        time.sleep(60)

    #  step2、进入报名页面，并登录
    entry_enroll_button_str = BrowserHelper.find_element(browser, entry_enroll_button_str, )
    BrowserHelper.eleClick(entry_enroll_button_str)

    while True:
        login_url = browser.current_url
        # 判断是否需要登录
        if BrowserHelper.isLogin(browser, login_flag_str):
            break

        #  需要登录，用户名，密码登录
        if BrowserHelper.login_up(browser, login_flag_str, sNode_Str, uNode_Str, pNode_Str, user, pwd, vNode_Str):
            # 登陆成功，保存cookie
            # 保存cookie
            # todo
            # RedisHelper.saveCookie(self.browser, self.name)
            break

        logger.error("登录不成功,请检查,1分钟后尝试重新登录")
        time.sleep(60)
        while True:
            # 登陆不成功,一定要重新打开登陆页面,防止之前登陆操作点击登陆按钮页面发生跳转
            if BrowserHelper.openUrl(browser, login_url, ):
                break
            logger.error("尝试打开登陆页面出现问题，请检查网络状况，3分钟后重试")



    # step3、 考试协议，选择同意
    agreeBtn = BrowserHelper.find_element(browser, agree_btn_str, )
    BrowserHelper.eleClick(agreeBtn)


    # step4、 选择考点，报名项目、报名
    # 选考试名称
    exam_Name_btn = BrowserHelper.find_element(browser, exam_Name_str, )
    BrowserHelper.eleClick(exam_Name_btn)
    # 选地区
    region_Selector = Select(BrowserHelper.find_element(browser,exam_region_selector_str))  # 实例化Select
    region_Selector.select_by_visible_text(exam_region_name)
    # 选科目
    exam_type_btn = BrowserHelper.find_element(browser, exam_type_str, )
    BrowserHelper.eleClick(exam_type_btn)

    next_step_btn = None
    radio_selector_btn = None
    while True:
        #  选考点
        exam_adress1_btn = BrowserHelper.find_element(browser, exam_adress_str1, wTime=0.5,)
        radio_selector_btn = BrowserHelper.find_element(browser, exam_adress_str1, wTime=0.5,)
        if radio_selector_btn:
            next_step_btn = BrowserHelper.find_element(browser, exam_adress_str1, wTime=0.5, )
            if next_step_btn:
                BrowserHelper.eleClick(next_step_btn)
                logger.info("恭喜你，报名成功！请抓紧填写报名信息并在24小时内确认缴费")
                break

        exam_adress2_btn = BrowserHelper.find_element(browser, exam_adress_str2, wTime=0.5, )
        radio_selector_btn = BrowserHelper.find_element(browser, exam_adress_str1, wTime=0.5,)
        if radio_selector_btn:
            next_step_btn = BrowserHelper.find_element(browser, exam_adress_str1, wTime=0.5, )
            if next_step_btn:
                BrowserHelper.eleClick(next_step_btn)
                logger.info("恭喜你，报名成功！请抓紧填写报名信息并在24小时内确认缴费")
                break

finally:
    browser.close()