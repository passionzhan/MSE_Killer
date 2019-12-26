# -*- coding: utf-8 -*-
'''
提供常用的功能函数
'''
import re
import time
import random
import os
import logging
import urllib.request
import urllib.parse
import json


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from redis.client import Redis

logger = logging.getLogger(__name__)

def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path


def extractTxtImage(allConten,imageUrlPre,imagePathPre):
    '''
    从xpath节点列表中抽取正文和图片链接
    :param allConten:利用xpath抽取的所有节点
    :param imageUrlPre:用来补全的图片链接的前缀
    :param imagePathPre:图片保存路径前缀
    :return:
    '''
    txtStr = ""
    images = []
    imgUrlSet = set([])
    for pContent in allConten:
        txtStr += pContent.xpath('string(.)').extract_first().strip() + os.linesep
        #  获取图像连接，img标签，具有src属性
        for img in pContent.xpath('.//img[@src]'):
            src = img.xpath("./@src").extract_first().strip()
            if len(src) > 0:
                if not src.startswith("http"):
                    src = imageUrlPre + src
                if src not in imgUrlSet:
                    imgUrlSet.add(src)
                    txtStr += '======<img src="' + src + '">======' + os.linesep
                    fName = strip(src.split("/")[-1])

                    # images[src] = os.path.join(self.name,fName)
                    images.append({
                        "url": src,
                        "path": os.path.join(imagePathPre, fName)
                    })
    return txtStr,images

    # if len(images) > 0:
    #     tmpItem["images"] = images


class BrowserHelper():
    '''
    浏览器操作的辅助类
    '''
    @staticmethod
    def find_element(onwer, lStr, wTime=5, wStr='Element can not be found', \
                     methodName='find_element_by_xpath'):
        '''
        利用xpath定位元素
        :param onwer: browser或者上下文节点
        :param lStr: 定位xpath字符串
        :param logger:日志记录器
        :param wStr:定位不成功提示信息
        :param methodName: 定位方法
        :return: 不成功None,成功返回定位元素
        '''
        rtnEle = None;
        try:
            #  隐式等待
            if isinstance(onwer, webdriver.Firefox):
                myWait = WebDriverWait(onwer, wTime)
                myWait.until(EC.presence_of_element_located((By.XPATH, lStr)))
            if methodName == "find_element_by_xpath":
                rtnEle = onwer.find_element_by_xpath(lStr)
            elif methodName == "find_elements_by_xpath":
                rtnEle = onwer.find_elements_by_xpath(lStr)
            else:
                logger.warning("Now do not support this method")
        except Exception as e:
            logger.error(e)
            logger.warning(wStr)

        return rtnEle

    @staticmethod
    def openUrl(browser, url, maxTryNum=5,INTERVAL = (4,8)):
        '''
        浏览器打开制定url，
        :param browser:
        :param url:
        :param logger:
        :param maxTryNum:
        :return: 成功 返回True,不成功 返回 False
        '''
        isSuccess = False
        i = 0;
        while i <= maxTryNum:
            try:
                browser.get(url)
                time.sleep(random.randint(*INTERVAL))
                isSuccess = True
                break;
            except Exception as e:
                i += 1
                logger.error(e)
                logger.info("try to open the url: " + url + " " + str(i) + " times!")
                time.sleep(5)

        if isSuccess == False:
            logger.warning("Can not open the url, please check you network!")
        return isSuccess

    @staticmethod
    def openUrl_exit(browser, url, maxTryNum=5):
        isOpened = BrowserHelper.openUrl(browser, url, maxTryNum)
        if isOpened == False:
            strF = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            strF += "_" + str(random.randint(1, 61))
            browser.save_screenshot(os.getcwd() + os.sep + "errorShot" + os.sep + strF + ".jpg")
            browser.quit()
            logger.warning("Your network seems to have some promlem, please check it. Try to exit!")
            exit(1)

    @staticmethod
    def eleClick(eleNode,):
        successFlag = False
        try:
            eleNode.click()
            successFlag = True
        except Exception as e:
            logger.error(repr(e))
            logger.warning("please check status of your network!")
            successFlag = False
        return successFlag

    @staticmethod
    def isLogin(browser, judeStr):
        '''
        判断登陆是否成功
        :param browser:
        :param judeStr:
        :return:
        '''
        loginSuc = False

        warningStr = "Can not find the login element"
        loginEle = BrowserHelper.find_element(browser, judeStr, 10, warningStr)
        if loginEle is not None:
            loginSuc = True
        else:
            loginSuc = False

        return loginSuc

    @staticmethod
    def login_up(browser,judeStr,sBtnStr,uNodeStr,pNodeStr,user,pwd,vNodeStr="",):
        '''
        通过用户名密码登陆
        :param browser:
        :param judeStr:
        :param sBtnStr:
        :param uNodeStr:
        :param pNodeStr:
        :param user:
        :param pwd:
        :param vNodeStr:
        :param vcode:
        :return:
        '''
        rtnFlag = False
        try:
            uNode = BrowserHelper.find_element(browser,uNodeStr, )
            pNode = BrowserHelper.find_element(browser,pNodeStr, )
            uNode.clear()
            uNode.send_keys(user)
            pNode.clear()
            pNode.send_keys(pwd)
            loginBtn = BrowserHelper.find_element(browser, sBtnStr, )

            if vNodeStr != "":
                vNode = BrowserHelper.find_element(browser,vNodeStr,)
                vStr = input('请输入验证码: ')
                vNode.clear()
                vNode.send_keys(vStr)

            BrowserHelper.eleClick(loginBtn)

            time.sleep(random.randint(3, 7))

            #  判断登陆是否成功
            if BrowserHelper.isLogin(browser,judeStr,):
                rtnFlag = True
        except Exception as loginExe:
            logger.warning("登陆出错，出错原因：" + repr(loginExe))
            rtnFlag = False

        return  rtnFlag

    @staticmethod
    def login_cookie(browser,spiderName,domain):
        '''
        通过cookie登录
        :param browser:
        :param spiderName:
        :return:
        '''
        cookikLst = RedisHelper.getCookie(spiderName)
        browser.delete_all_cookies()
        for tmpCookie in cookikLst:
            browser.add_cookie({'domain': domain, \
                                'name': tmpCookie["name"], \
                                'value': tmpCookie["value"], \
                                'path': '/', \
                                'expires': None, \
                        })
        time.sleep(random.randint(2,5))
        # browser

    @staticmethod
    def scroll2Bottom(browser, noDataFlag_XPath, maxCount=None):
        # allBodyPre = browser.page_source
        iCount = 0
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            iCount += 1
            time.sleep(random.randint(1, 5))
            logger.info("%sth time Scroll to the bottom to fetch more information" % iCount)

            if maxCount is not None:
                if iCount > maxCount:
                    break
            # allBodySrolled = browser.page_source

            if BrowserHelper.find_element(browser,noDataFlag_XPath,5,'noDataFlag can not be found!'):
                logger.info("no more information can be found!")
                break
            # else:
            #     allBodyPre = allBodySrolled

def requestPost_Json(url,para,headers):
    '''
    封装 ajax 请求，通过post 获取json数据
    :param url:
    :param para:
    :param headers:
    :return: 字典
    '''
    # 将字典格式化成能用的形式
    try:
        data = urllib.parse.urlencode(para).encode('utf-8')
        request = urllib.request.Request(url, data, headers)
        # 访问
        rawJson = urllib.request.urlopen(request).read().decode('utf-8')
    except:
        logger.warning('请求：{0}出错,请检查!'.format(url))
        rawJson = None

    if rawJson:
        return  json.loads(rawJson)
    else:
        return  rawJson






