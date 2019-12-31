#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: Zhan
# @Date  : 12/25/2019
# @Desc  : 剑桥mse报名脚本
import json
from functools import reduce

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

from utility import *

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("开始输入")
with open('user_config_CAE.cfg', 'r',encoding='utf-8') as f:
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
    logger.info(login_url)

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
    # 等待3秒，确保新页面出现
    time.sleep(20)

    order_url = browser.current_url
    successed = False
    while not successed:
        # step4、 选择考点，报名项目、报名
        # 选考试名称
        alert_model_str = basic_config['alert_model']
        alert_model_close_str = basic_config['alert_model_close_btn']
        alert_model = BrowserHelper.find_element(browser,alert_model_str)
        alert_model_close_btn = BrowserHelper.find_element(alert_model, alert_model_close_str)

        exam_Name_str = basic_config['base_exam_name'] % user_config['exam_name']
        exam_Name_btn = BrowserHelper.find_element(browser, exam_Name_str,)
        BrowserHelper.eleClick(exam_Name_btn)
        if alert_model.is_displayed():
            BrowserHelper.eleClick(alert_model_close_btn)
        # 选地区
        region_Selector = Select(BrowserHelper.find_element(browser,basic_config['exam_region_selector']))  # 实例化Select
        time.sleep(2)
        region_Selector.select_by_visible_text(user_config['exam_region_name'])
        if alert_model.is_displayed():
            BrowserHelper.eleClick(alert_model_close_btn)

        # 选科目
        time.sleep(2)
        exam_type_str = basic_config['base_exam_type'] % user_config['exam_type_name']
        exam_type_btn = BrowserHelper.find_element(browser, exam_type_str,)
        exam_type_id = exam_type_btn.get_attribute("attrval")
        BrowserHelper.eleClick(exam_type_btn)
        if alert_model.is_displayed():
            BrowserHelper.eleClick(alert_model_close_btn)

        next_step_btn = None
        radio_selector_btn = None


        i = 0
        #  不停选择考点

        while i < len(user_config['exam_address_name_list'])+2:
            address = user_config['exam_address_name_list'][i]#  选考点
            # logger.info(address)
            i += 1
            if i == len(user_config['exam_address_name_list']):
                i = 0

            exam_address_btn_str = basic_config['base_exam_address'] % address
            exam_address_btn = BrowserHelper.find_element(browser, exam_address_btn_str, wTime=0.5,)
            BrowserHelper.eleClick(exam_address_btn)
            if alert_model.is_displayed():
                #  出错，则关闭弹出窗，继续
                BrowserHelper.eleClick(alert_model_close_btn)
            # radio_selector_btn_str = basic_config['base_radio_selector'] % exam_type_id
            # 分析页面后改进
            cur_url = browser.current_url
            radio_selector_btn_str = basic_config['base_radio_selector']
            radio_selector_btn = BrowserHelper.find_element(browser, radio_selector_btn_str, wTime=0.5,)
            excute_status = 0
            # 1 抢票成功
            # 2 出错，出现弹窗，关闭弹窗继续
            # 3 点击后页面打不开
            if radio_selector_btn:
                next_step_btn = BrowserHelper.find_element(browser, basic_config['next_step_btn'], wTime=0.5, )
                if next_step_btn:
                    BrowserHelper.eleClick(next_step_btn)
                    # 判断是否成功
                    wait_time = 0
                    while True:
                        forward_url = browser.current_url
                        if forward_url != cur_url: # 发生跳转,成功
                            logger.info("恭喜你，报名成功！请抓紧填写报名信息并在24小时内确认缴费")
                            vStr = input('信息填写完毕输入exit退出秒杀程序:')
                            successed = True
                            break
                        elif alert_model.is_displayed(): # 有延时或者错误
                            BrowserHelper.eleClick(alert_model_close_btn)
                            successed = False
                            break
                        else:
                            time.sleep(0.1)
                            wait_time += 0.1
                            if wait_time > 5.0:
                                successed = False
                                break
                    break

        BrowserHelper.openUrl(order_url)
        # time.sleep(3)

finally:
    browser.close()