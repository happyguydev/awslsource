import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.system_admin import systemAdminModel
from models.system_admin_token import SystemAdminTokenModel
import time
import base64

class SystemAdminListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            username = self.get_argument("username")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date + ' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and registe_date > %s and registe_date < %s" % (starttimeStamp, endtimeStamp)
            if username:
                where += " and username like '%" + username + "%'"
            data = systemAdminModel.get_page(int(page_number) - 1, int(page_count), where)
            count = systemAdminModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))

class SystemAdminLoginHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username")
        pwd = self.get_argument("pwd")
        pwd_ = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')
        user = systemAdminModel.getAdmin(username, pwd_)
        if user:
            token = SystemAdminTokenModel.create(user['id'], user['username'])
            ret = {"code": 0, "msg": "success", "data": {"token": token, 'username': user['username']}}
        else:
            ret = {"code": 1, "msg": "fail"}
        self.write(json_encode(ret))

class SystemAdminHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            username = self.get_argument("username")
            pwd = self.get_argument("pwd")
            # 判断是否用户名重复
            result = systemAdminModel.getByUsername(username)
            if len(result) == 0:
                pwd_ = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')
                result1 = systemAdminModel.create(username, pwd_)
                if result1:
                    ret = {"code": 0, "msg": "success"}
                else:
                    ret = {"code": 2, "msg": "fail"}
            else:
                ret = {"code": 3, "msg": "username %s already exists!" % username}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        print(ret)
        self.write(json_encode(ret))

    def put(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            pwd = self.get_argument("pwd")
            pwd_ = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')
            result = systemAdminModel.update_pwd(int(systemAdmin['system_admin_id']), pwd_)
            if result > 0:
                ret = {"code": 0, "msg": "success"}
            else:
                ret = {"code": 2, "msg": "fail"}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))
    
    def delete(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            id = self.get_argument("id")
            result = systemAdminModel.delete(int(id))
            if result > 0:
                ret = {"code": 0, "msg": "success"}
            else:
                ret = {"code": 2, "msg": "fail"}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))


