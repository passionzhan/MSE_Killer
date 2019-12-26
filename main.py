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
pwd                     = 'xxxxx'
# login_url               = 'https://member.neea.cn/login/'
need_login_flag_str     = '//button[@id="login_button"]'
login_flag_str          = '//li/a[contains(text(),"退出")]'

# '//form[@id="loginForm"]//input[@id="loginName"]'
# '//form[@id="loginForm"]//input[@id="loginPwd"]'
# //*[@id="loginName"]
'//*[@id="loginName"]'
# uNode_Str        = '//input[@name="loginName"]'
uNode_Str        = '//form//input[@id="loginName"]'
pNode_Str        = '//form//input[@id="loginPwd"]'
vNode_Str        = '//form//input[@id="verificationCode"]'
sNode_Str        = '//button[@id="login_button"]'

agree_btn_str    = '//div[contains(@class,"page-container")]//input[@value="同意"]'


exam_Name_str           = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="time_id"]/a[contains(text(),"2020-04-25 KETPET青少版")]'
exam_region_selector_str        = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd/select[@name="addr"]'
exam_region_name                = "北京市"
exam_type_str        = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="projectType"]/a[contains(text(),"PET青少版")]'
base_exam_address   = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="orglist"]/a[contains(text(),"s%")]'
exam_address_name_list = [
    '海淀区上地西路41号院宏达商务中心层朴新教育',
    '朝阳区定福庄水利水电考点',
    '朝阳区慧忠北里119号',
    '海淀区西二旗大街19号外附培训学校',
    '海淀区清河一街83号巨人清河教学部',
    '海淀区知春路113号杰睿学校（海淀黄庄校区）',
    '海淀区北辛庄路考场',
    '朝阳区管庄路盛世环球培优常营校区',
    '丰台区南四环路129号怡海花园',
    '大兴区创新路2号外研社国际会议中心',
    '丰台区东铁营顺三条8号院北京方庄文化学校',
    '朝阳区花家地街19号',
    '北京外国语大学国际教育集团',
    '北京外国语大学国际教育集团第一分考点',
    '北京外国语大学国际教育集团第二分考点',
    '北京外国语大学国际教育集团第三分考点',
    '北京王府学校',
]

# exam_address_str1        = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="orglist"]/a[contains(text(),"北京外国语大学国际教育集团第一分考点")]'
# exam_address_str2        = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="orglist"]/a[contains(text(),"北京外国语大学国际教育集团第二分考点")]'

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
    entry_enroll_button_str = BrowserHelper.find_element(browser, entry_enroll_button_str,)
    BrowserHelper.eleClick(entry_enroll_button_str)

    # 处理新打开页面情况
    time.sleep(2)
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
    login_url = browser.current_url
    print(login_url)

    # 登录成功就直接进行下一步
    max_Try_Num = 5 #  最大重试5次
    login_successed = False
    while not BrowserHelper.isLogin(browser, login_flag_str):
        #  需要登录，用户名，密码登录
        if max_Try_Num > 0:
            login_successed = BrowserHelper.login_up(browser, login_flag_str, sNode_Str, uNode_Str, pNode_Str, user, pwd, vNode_Str)
            if login_successed:
                # 登陆成功，保存cookie
                # 保存cookie
                # todo
                # RedisHelper.saveCookie(self.browser, self.name)
                # 登录成功
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
        for address in exam_address_name_list:
            exam_address_btn_str = base_exam_address % address
            exam_address_btn = BrowserHelper.find_element(browser, exam_address_btn_str, wTime=0.5,)
            BrowserHelper.eleClick(exam_address_btn)
            radio_selector_btn = BrowserHelper.find_element(browser, radio_selector_str, wTime=0.5,)
            if radio_selector_btn:
                next_step_btn = BrowserHelper.find_element(browser, next_step_btn_str, wTime=0.5, )
                if next_step_btn:
                    BrowserHelper.eleClick(next_step_btn)
                    logger.info("恭喜你，报名成功！请抓紧填写报名信息并在24小时内确认缴费")
                    break

finally:
    browser.close()