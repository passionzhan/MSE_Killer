#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   jonsdump.py    
@Contact :   9824373@qq.com
@License :   (C)Copyright 2017-2018, Zhan
@Desc    :     
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/26 22:58   zhan      1.0         None
'''
import json

user_config = {}
user_config['user']                    = 'xxxxx'
user_config['pwd']                    = 'xxxxx'
user_config['exam_name'] = "2020-04-25 KETPET青少版"
user_config['exam_address_name_list']  = [
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

user_config['exam_type_name'] = 'PET青少版'
user_config['exam_region_name'] = "北京市"
basic_config = {}
basic_config['MSE_url']          = 'http://mse.neea.edu.cn/' # 剑桥通用考级官网
basic_config['exam_entry_button']     = '//div[contains(@class,"gobt")]//a[contains(text(),"进入报名")]' # 进入报名按钮
basic_config['login_flag']          = '//li/a[contains(text(),"退出")]'
basic_config['user_input']        = '//form//input[@id="loginName"]'
basic_config['pwd_input']        = '//form//input[@id="loginPwd"]'
basic_config['verifiction_input']        = '//form//input[@id="verificationCode"]'
basic_config['submit_bnt']        = '//button[@id="login_button"]'
basic_config['agree_btn'] = '//div[contains(@class,"page-container")]//input[@value="同意"]'
basic_config['base_exam_name'] \
    = '//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="time_id"]/a[contains(text(),"%s")]'
basic_config['base_exam_address'] \
    = r'//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="orglist"]/a[contains(text(),"%s")]'
basic_config['base_exam_type'] \
    = r'//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd[@id="projectType"]/a[contains(text(),"%s")]'
basic_config['exam_region_selector'] \
    = r'//div[contains(@class,"selectNumberScreen")]/div[@id="selectList"]/dl/dd/select[@name="addr"]'
basic_config['base_radio_selector'] = '//table[contains(@class,"store_cart_content")]//tr/td/input[@name="selectId"]'
basic_config['next_step_btn'] = '//div[@id="submit_but"]/button[@onclick="submit()" and contains(text(),"下一步")]'
# 声明浏览器对象，将chromedriver驱动放在chrome浏览器安装目录下，指定驱动的绝对路径
# browser = webdriver.Chrome(executable_path=r'D:\Google\Chrome\Application\chromedriver')

user_config_str = json.dumps(user_config,indent=4,ensure_ascii=False)
basic_config_str = json.dumps(basic_config,indent=4,ensure_ascii=False)

with open('user_config.cfg','x',encoding='utf-8')as f:
    f.write(user_config_str)

with open('basic_config.cfg','x',encoding='utf-8')as f:
    f.write(basic_config_str)



