import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.system_admin_token import SystemAdminTokenModel

class SystemAdminTokenHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        users = SystemAdminTokenModel.get_all()
        ret = {"code": 0, "data": users}
        self.write(json_encode(ret))

    def post(self):
        system_admin_id = self.get_argument("system_admin_id")
        system_admin_username = self.get_argument("system_admin_username")
        token = SystemAdminTokenModel.create(system_admin_id, system_admin_username)
        ret = {"code": 0, "msg": "success", "data": {"token": token}}
        self.write(json_encode(ret))

    def put(self):
        token = self.get_argument("token")
        rowcount = SystemAdminTokenModel.update(token)
        if rowcount > 0:
            ret = {"code": 0, "msg": "success", "data": {"token": token}}
        else:
            ret = {"code": 1, "msg": "fail"}
        self.write(json_encode(ret))