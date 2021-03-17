import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.contact_us import contactUsModel
from models.system_admin_token import SystemAdminTokenModel


class ContactUsHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            data = contactUsModel.get()
            if data:
                ret = {'code': 0, "msg": "success!", 'data': data}
            else:
                ret = {'code': 1, "msg": "fail!"}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))


    def put(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            phone = self.get_argument("phone")
            tel_kefu = self.get_argument("tel_kefu")
            email = self.get_argument("email")
            linker = self.get_argument("linker")
            id = self.get_argument("id")
            result = contactUsModel.update(phone, tel_kefu, email, linker, id)
            if result:
                ret = {"code": 0, "msg": "success!", 'data': result}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))


class ContactUsUserHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        data = contactUsModel.get()
        if data:
            ret = {'code': 0, "msg": "success!", 'data': data}
        else:
            ret = {'code': 1, "msg": "fail!"}
        self.write(json_encode(ret))
