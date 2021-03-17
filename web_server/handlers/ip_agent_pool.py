import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.ip_agent_pool import ipAgentPoolModel
from models.system_admin_token import SystemAdminTokenModel
import requests
import time


class IpAgentPoolHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        where = self.get_argument("where")
        ipLibrary = ipAgentPoolModel.get_random(where)
        ret = {'code': 0, "msg": "success!", 'data': ipLibrary}
        self.write(json_encode(ret))

    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            url_web = self.get_argument("url_web")
            url_api = self.get_argument("url_api")
            country = self.get_argument("country")
            area = self.get_argument("area")
            agent_protocol = self.get_argument("agent_protocol")
            result = ipAgentPoolModel.create(url_web, url_api, country, area, systemAdmin['system_admin_username'], agent_protocol)
            if result:
                ret = {"code": 0, "msg": "success!", 'data': result}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'mag': 'fail, user token not found'}
        self.write(json_encode(ret))

    def delete(self):
        id = self.get_argument("id")
        ret = ipAgentPoolModel.delete(int(id))
        self.write(json_encode(ret))

class IpAgentPoolListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            area = self.get_argument("area")
            url_web = self.get_argument("url_web")
            url_api = self.get_argument("url_api")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date+' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and oper_time > %s and oper_time < %s" % (starttimeStamp, endtimeStamp)
            if area != '' and area != '国家区域':
                where += " and area = '" + area + "' "
            if url_web:
                where += " and url_web like '%" + url_web + "%'"
            if url_api:
                where += " and url_api like '%" + url_api + "%'"
            data = ipAgentPoolModel.get_page(int(page_number)-1, int(page_count), where)
            count = ipAgentPoolModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))

class IpAgentPoolTestHandler(BaseHandler,tornado.web.RequestHandler):
    def get(self):
        url = 'http://http.tiqu.alicdns.com/getip3?num=3&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
        result = requests.get(url)
        trans = result.json()
        print(trans)
        for item in trans['data']:
            print(item['ip'])
            print(item['port'])
        # print(trans['data'][0]["ip"])