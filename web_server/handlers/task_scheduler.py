import tornado.web
from tornado.escape import json_encode
from concurrent.futures import ThreadPoolExecutor
from base import BaseHandler
from models.optimize_configuration import optimizeConfigurationModel
from models.user_token import UserTokenModel
from models.ip_library import ipLibraryModel
from models.ip_agent_pool import ipAgentPoolModel
from models.user_agent import userAgentModel
from selenium import webdriver
import datetime
import time
import random
import os
import requests
import re

class Executor(ThreadPoolExecutor):
    """ 创建多线程的线程池，线程池的大小为10
    创建多线程时使用了单例模式，如果Executor的_instance实例已经被创建，
    则不再创建，单例模式的好处在此不做讲解
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=10)
        return cls._instance

class TeskSchedulerHandler(BaseHandler, tornado.web.RequestHandler):
    executor = Executor()

    def exee(self, links, browser, num):
        print(links)
        lencoun = len(links)
        print("链接数量："+str(lencoun))
        print('----------------------')
        for _ in range(lencoun):
            tempint = random.randint(0, lencoun-1)
            print(tempint)
            time.sleep(10)
            url = links[tempint].get_attribute("href")
            if url:
                print(url)
                tgt = links[tempint].get_attribute("target")
                print(tgt)
                if tgt:
                    if not "_blank" in tgt:
                        print('站内')
                    else:
                        print('站外')
                    try:
                        if num < 2:
                            links[tempint].click()
                            time.sleep(10)
                            newlinks1 = browser.find_elements_by_tag_name("a")
                            num += 1
                            print('当前运行到第几次'+str(num))
                            self.exee(newlinks1, browser, num)
                        else:
                            try:
                                import urllib3
                                urllib3.poolmanager.PoolManager.clear()
                                browser.close()
                                browser.quit()
                                # os.system('taskkill /im chromedriver.exe /F')
                                print(datetime.datetime.now())
                                ret = {"code": 0, 'msg': "success", 'data': {'start_time': '', 'end_time': str(datetime.datetime.now())}}
                                self.write(json_encode(ret))
                                break
                            except Exception as e:
                                print(e)
                                self.write(json_encode(e))
                    except Exception:
                        print("异常")
                        self.write(json_encode('异常'))
                        continue
                else:
                    print('站外')
                print('-----------------------------------')


    def browserSet(self, user_agent, visiter):
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('--headless')

        # chromeOptions.add_argument('--disable-gpu')
        ip_info = self.getIp(visiter)
        proxy = 'http://'+str(ip_info['ip'])+':'+str(ip_info['port'])
        print(proxy)
        # proxy = 'http://202.20.16.82:10152'
        # chromeOptions.add_argument("--proxy-server="+proxy)

        user_agent = self.getUserAgentRandom(user_agent)
        print(user_agent['content'])
        user_agent = user_agent['content']
        # user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        chromeOptions.add_argument('user-agent=' + user_agent + '')
        browser = webdriver.Chrome(chrome_options=chromeOptions)
        return browser

    @tornado.concurrent.run_on_executor
    def task_execute(self, operType, targetUrl, sourceUrl, keyWord, user_agent, visiter):
        browser = self.browserSet(user_agent, visiter)
        if sourceUrl != '' and operType == '流量':
            browser.get(sourceUrl)
            links = browser.find_elements_by_tag_name("a")
            for link in links:
                targetUrl1 = link.get_attribute("href")
                if targetUrl1 == targetUrl:
                    link.click()
                    browser.close()
                    all_handles = browser.window_handles
                    print(all_handles)
                    browser.switch_to.window(all_handles[-1])
                    newlinks = browser.find_elements_by_tag_name("a")
                    self.exee(newlinks, browser, 0)
        else:
            if operType == '流量' and sourceUrl == '':
                browser.get(targetUrl)
                links = browser.find_elements_by_tag_name("a")
                self.exee(links, browser, 0)
            if operType == '下拉':
                browser.maximize_window()
                allnum = random.randint(1, 10)
                print(targetUrl)
                self.exeescroll(targetUrl, browser, 0, allnum)
            if operType == '关键词排名':
                print(keyWord)
                print(targetUrl)
                currentTargetUrl = self.exee_search_engine(keyWord, targetUrl)
                if currentTargetUrl is not None:
                    print(currentTargetUrl)
                    if 'http://' not in currentTargetUrl:
                        currentTargetUrl = 'http://' + currentTargetUrl
                    browser.get(currentTargetUrl)
                    links = browser.find_elements_by_tag_name("a")
                    self.exee(links, browser, 0)

    def exeescroll(self, url, browser, num, allnum):
        if num < allnum:
            browser.get(url)
            # print(browser.current_url)
            time.sleep(1)
            # browser.execute_script("document.body.style.zoom = '150%';")
            # body = browser.find_element_by_tag_name('body')
            # body.send_keys(Keys.PAGE_DOWN)
            # print('下拉呀')
            js = "return action=document.body.scrollHeight"
            # 初始化现在滚动条所在高度为0
            height = 0
            # 当前窗口总高度
            new_height = browser.execute_script(js)
            print(new_height)

            while height < new_height:
                # 将滚动条调整至页面底部
                for i in range(height, new_height, 100):
                    # body.send_keys(Keys.PAGE_DOWN)
                    browser.execute_script('window.scrollTo(0, {})'.format(i))
                    time.sleep(0.5)
                height = new_height
                time.sleep(2)
                new_height = browser.execute_script(js)
            else:
                nextlist = ['下一话', '下一篇']
                for item in nextlist:
                    try:
                        links = browser.find_element_by_xpath("//*[contains(text(),'" + item + "')]")
                        links.click()
                        break
                    except:
                        print('元素不存在')
                        continue
                num += 1
                url = browser.current_url
                self.exeescroll(url, browser, num, allnum)
        else:
            browser.quit()

    def exee_search_engine(self, keyword, search_url):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.16 Safari/537.36",
        }
        site_baidu = u"http://www.baidu.com/s?wd=%s&pn=%d0"
        site_google = 'https://www.google.com/search?q=%s&start=%d0'
        page = 0
        i = 0
        tt = 0
        while(tt == 0):
            url = site_baidu % (keyword, page)
            data = requests.get(url, headers=headers)
            searchTxt = data.content
            page = page + 1
            try:
                pattern = re.compile(b'class="c-showurl" style="text-decoration:none;">(.*?)&nbsp', re.S)
                result = pattern.findall(searchTxt)
                for item in result:
                    item_str = str(item, encoding="utf8")
                    i = i + 1
                    new_item_str = item_str.replace('<b>', '').replace('</b>', '')
                    print("rank %d: %s" % (i, new_item_str))
                    if search_url in new_item_str:
                        print("baidu输入的关键词排在第 %d 名" % i)
                        tt = 1
                        return new_item_str
            except Exception as e:
                print(e)
                return None

        newheaders = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
        }

        # tt1 = 0
        # while(tt1==0):
        #     url = site_google % (keyword, page)
        #     data = requests.get(url, headers=newheaders)
        #     print(data.status_code)
        #     if data.status_code == 200:
        #         searchTxt = data.content
        #         # print(searchTxt.decode('utf-8'))
        #         page = page + 1
        #         try:
        #             pattern = re.compile(b'class="C8nzq BmP5tf" href="(.*?)"', re.S)
        #             result = pattern.findall(searchTxt)
        #             for item in result:
        #                 item_str = str(item, encoding="utf8")
        #                 i = i + 1
        #                 print("rank %d: %s" % (i, item_str))
        #
        #                 # rank 1: https://www.java.com/
        #                 # rank 2: https://www.java.com/download/
        #                 # rank 3: https://www.oracle.com/java/technologies/javase-downloads.html
        #                 # rank 4: https://www.oracle.com/java/technologies/
        #                 # rank 5: https://en.m.wikipedia.org/wiki/Java_(programming_language)
        #                 # rank 6: https://en.m.wikipedia.org/wiki/Java
        #                 # rank 7: https://www.w3schools.com/java/java_intro.asp
        #                 # rank 8: https://openjdk.java.net/
        #                 # rank 9: https://go.java/
        #
        #
        #                 if search_url in item_str:
        #                     print('-----------------------------------')
        #                     print("google输入的关键词排在第 %d 名" % i)
        #                     print('-----------------------------------')
        #                     tt1 = 1
        #         except Exception as e:
        #             print(e)

    def getIPwithAPI(self, ip_API):
        # url = 'http://dev.qydailiip.com/api/?apikey=50f7fdbe16e0038821d1f562786212cd7d7b7600&num=1&type=json&line=win&proxy_type=putong&sort=rand&model=all&protocol=http&address=&kill_address=&port=&kill_port=&today=false&abroad=&isp=&anonymity='
        url = ip_API['url_api']
        print(url)
        result = requests.get(url)
        trans = result.json()
        print(trans)
        if ip_API['url_web'] == 'https://www.7yip.cn':
            for item in trans:
                ip = item.split(':')[0]
                port = item.split(':')[1]
                ipLibraryModel.create(ip, port, ip_API['country'], '', '', '', ip_API['area'])
        else:
            if trans['code'] == 0:
                for item in trans['data']:
                    print(item['ip'])
                    print(item['port'])
                    ipLibraryModel.create(item['ip'], item['port'], ip_API['country'], '', '', '', ip_API['area'])

    def getIPwithAPI_always(self, where):
        print('where', where)
        ip_info = ipLibraryModel.get(where)
        if ip_info is None:
            ip_API = ipAgentPoolModel.get_random(where)
            self.getIPwithAPI(ip_API)
            time.sleep(2)
            return self.getIPwithAPI_always(where)
        else:
            return ip_info


    def getIp(self, visiter):
        where_visiter = ' 1=1 '
        if visiter:
            where_visiter += ' and area in( '
            tesm = ""
            if visiter.find('中国') > -1:
                tesm += "'中国',"
            if visiter.find('欧美') > -1:
                tesm += "'欧美',"
            if visiter.find('韩国') > -1:
                tesm += "'韩国',"
            if visiter.find('日本') > -1:
                tesm += "'日本',"
            if visiter.find('东南亚') > -1:
                tesm += "'东南亚',"
            where_visiter += tesm[:-1]
            where_visiter += ")"
        ip_info = self.getIPwithAPI_always(where_visiter)
        print('ip_info', ip_info)
        success_ip_info = self.checkIP(ip_info, where_visiter)
        print('success_ip_info', success_ip_info)
        return success_ip_info


    def checkIP(self, ip_info, where):
        ip = ip_info['ip']
        print('ip', ip)
        # ip = '202.20.16.82'
        backinfo = os.system('ping -n 1 -w 1 %s' % ip)  # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
        print(backinfo)
        if backinfo:
            ipLibraryModel.delete(int(ip_info['id']))
            return self.checkIP(ip_info, where)
        else:
            return ip_info

    def getUserAgentRandom(self, user_agent):
        where_user_agent = ' 1=1 '
        if user_agent:
            where_user_agent += " and system in("
            temm = ""
            if user_agent.find("百度PC") > -1:
                temm += "'windows','mac',"
            if user_agent.find("百度手机") > -1:
                temm += "'ios','android',"
            if user_agent.find("谷歌PC") > -1:
                temm += "'windows','mac',"
            if user_agent.find("谷歌手机") > -1:
                temm += "'ios','android',"
            where_user_agent += temm[:-1]
            where_user_agent += ")"
        return userAgentModel.get(where_user_agent)

    @tornado.gen.coroutine
    def post(self):
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            oper_type = self.get_argument("oper_type")
            optimizeConfigurations = optimizeConfigurationModel.get_current(user['user_id'], user['username'], oper_type)
            sourceUrl = optimizeConfigurations['source_website']
            targetUrl = optimizeConfigurations['target_website']
            keyWord = optimizeConfigurations['key_word']
            user_agent = optimizeConfigurations['search_engines_check']
            visiter = optimizeConfigurations['visitor_check']
            operType = optimizeConfigurations['oper_type']
            print("当前时间：", datetime.datetime.now())
            yield self.task_execute(operType, targetUrl, sourceUrl, keyWord, user_agent, visiter)
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
            self.write(json_encode(ret))


        # chromeOptions = webdriver.ChromeOptions()
        # # chromeOptions.add_argument('--headless')
        #
        # # chromeOptions.add_argument('--disable-gpu')
        #
        # # proxy = 'http://202.20.16.82:10152'
        # # chromeOptions.add_argument("--proxy-server="+proxy)
        # user_agent = self.getRandom()
        # print(user_agent[2])
        # # useragent = 'Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)'
        # chromeOptions.add_argument('user-agent='+user_agent[2]+'')
        # browser = webdriver.Chrome(chrome_options=chromeOptions)
        # # wait = WebDriverWait(browser, 10)
        # if operType == '流量':
        #     if sourceUrl == '':
        #         browser.get(targetUrl)
        #     else:
        #         browser.get(sourceUrl)
        #     current_window = browser.current_window_handle
        #     print(current_window)
        #     print('---------------------')
        #     links = browser.find_elements_by_tag_name("a")
        #     if sourceUrl == '':
        #         print('没有来源地址')
        #         self.exee(links, browser)
        #     else:
        #         for link in links:
        #             targetUrl1 = link.get_attribute("href")
        #             if targetUrl1 == targetUrl:
        #                 link.click()
        #                 time.sleep(10)
        #                 # 如果是流量
        #                 all_handles = browser.window_handles
        #                 print(all_handles)
        #                 browser.switch_to.window(all_handles[-1])
        #                 linek1 = browser.find_elements_by_tag_name("a")
        #                 self.exee(linek1, browser)
        #                 break
        # elif operType == '下拉':
        #     browser.get(targetUrl)
        #     self.exeescroll(targetUrl, browser)



