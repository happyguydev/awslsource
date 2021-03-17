import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.user import UserModel
from models.user_token import UserTokenModel
from models.system_admin_token import SystemAdminTokenModel
import traceback
import json
import datetime
import time
import base64

# class DateEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(obj, datetime.date):
#             return obj.strftime("%Y-%m-%d")
#
#         else:
#             return json.JSONEncoder.default(self, obj)

class UserListHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            where = ' 1=1 '
            count = UserModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count']}
            self.write(json_encode(ret))
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
            self.write(json_encode(ret))
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
                start_date = start_date+' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and registe_date > %s and registe_date < %s" % (starttimeStamp, endtimeStamp)
            if username:
                where += " and username like '%" + username + "%'"
            data = UserModel.get_page(int(page_number)-1, int(page_count), where)
            count = UserModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))

class UserHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username")
        pwd = self.get_argument("pwd")
        email = self.get_argument("email")
        result = UserModel.getByUsername(username)
        if len(result) == 0:
            pwd_ = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')
            user = UserModel.create(username, pwd_, email)
            if user:
                token = UserTokenModel.create(user['id'], user['username'])
                ret = {"code": 0, "msg": "success", "data": {"token": token, 'username': user['username']}}
            else:
                ret = {"code": 1, "msg": "fail"}
        else:
            ret = {"code": 2, "msg": "username %s already exists!" % username}
        self.write(json_encode(ret))

    def put(self):
        token = self.get_argument("token")
        oper_type = self.get_argument("oper_type")
        user = UserTokenModel.getUserToken(token)
        if user:
            if oper_type == 'pwd':
                pwd_old = self.get_argument('pwd_old')
                pwd_old_ = base64.b64encode(pwd_old.encode('utf-8')).decode('utf-8')
                userinfo = UserModel.get(user['user_id'])
                print(userinfo['pwd'])
                if pwd_old_ == userinfo['pwd']:
                    pwd = self.get_argument("pwd")
                    pwd_ = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')
                    result = UserModel.update_pwd(user['user_id'], pwd_)
                    if result > 0:
                        ret = {"code": 0, "msg": "success"}
                    else:
                        ret = {"code": 1, "msg": "fail"}
                else:
                    ret = {"code": 1, "msg": "fail, old pwd error"}
                self.write(json_encode(ret))
            else:
                email = self.get_argument("email")
                result = UserModel.update_email(user['user_id'], email)
                if result > 0:
                    ret = {"code": 0, "msg": "success"}
                else:
                    ret = {"code": 1, "msg": "fail"}
                self.write(json_encode(ret))
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
            self.write(json_encode(ret))

    def delete(self):
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            result = UserModel.delete(user['user_id'])
            if result > 0:
                ret = {"code": 0, "msg": "success"}
            else:
                ret = {"code": 1, "msg": "fail"}
            self.write(json_encode(ret))
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
            self.write(json_encode(ret))

class UserLoginHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username")
        pwd = self.get_argument("pwd")
        pwd_ = base64.b64encode(pwd.encode('utf-8')).decode('utf-8')
        user = UserModel.getUser(username, pwd_)
        if user:
            token = UserTokenModel.create(user['id'], user['username'])
            ret = {"code": 0, "msg": "success", "data": {"token": token, 'username': user['username']}}
        else:
            ret = {"code": 1, "msg": "fail"}
        self.write(json_encode(ret))
