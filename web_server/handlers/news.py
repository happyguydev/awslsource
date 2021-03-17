import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.news import newsModel
from models.system_admin_token import SystemAdminTokenModel
import time


class NewsHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            id = self.get_argument("id")
            data = newsModel.getById(int(id))
            if data:
                ret = {'code': 0, "msg": "success!", 'data': data}
            else:
                ret = {'code': 1, "msg": "fail!"}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))

    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            oper_type = self.get_argument("oper_type")
            title = self.get_argument("title")
            summary = self.get_argument("summary")
            content = self.get_argument("content")
            result = newsModel.create(oper_type, title, summary, content, systemAdmin['system_admin_username'])
            if result:
                ret = {"code": 0, "msg": "success!", 'data': result}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))

    def put(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            # oper_type = self.get_argument("oper_type")
            oper_type = '帮助'
            title = self.get_argument("title")
            summary = self.get_argument("summary")
            content = self.get_argument("content")
            id = self.get_argument("id")
            result = newsModel.update(oper_type, title, summary, content, systemAdmin['system_admin_username'], id)
            if result:
                ret = {"code": 0, "msg": "success!", 'data': result}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))

    def delete(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            id = self.get_argument("id")
            result = newsModel.delete(int(id))
            if result > 0:
                ret = {'code': 0, 'msg': 'success'}
            else:
                ret = {'code': 0, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))


class NewsListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            content = self.get_argument("content")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date + ' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and oper_time > %s and oper_time < %s" % (starttimeStamp, endtimeStamp)
            if content:
                where += " and title like '%" + content + "%' or content like '%" + content + "%'"
            data = newsModel.get_page(int(page_number) - 1, int(page_count), where)
            count = newsModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))


class NewsListUserHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id")
        data = newsModel.getById(int(id))
        if data:
            ret = {'code': 0, "msg": "success!", 'data': data}
        else:
            ret = {'code': 1, "msg": "fail!"}
        self.write(json_encode(ret))

    def post(self):
        page_number = self.get_argument("page")
        page_count = self.get_argument("limit")
        oper_type = self.get_argument("oper_type")
        where = ' 1=1 '
        where += " and oper_type='" + oper_type + "'"
        data = newsModel.get_page(int(page_number) - 1, int(page_count), where)
        count = newsModel.get_count(where)
        ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        self.write(json_encode(ret))
