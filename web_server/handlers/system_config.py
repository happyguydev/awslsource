import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.system_config import systemConfigModel

class SystemConfigHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument("key")
        data = systemConfigModel.getSystemConfigByKey(key)
        ret = {'code': 0, "msg": "success!", 'data': data}
        self.write(json_encode(ret))

    def post(self):
        key = self.get_argument("key")
        value = self.get_argument("value")
        data = systemConfigModel.setSystemConfigByKey(key, value)
        ret = {'code': 0, "msg": "success!", 'data': data}
        self.write(json_encode(ret))