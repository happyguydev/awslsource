import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.user_token import UserTokenModel

class UserTokenHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument("username")
        user_token = UserTokenModel.getTop1ByUserName(username)
        ret = {"code": 0, "data": user_token}
        self.write(json_encode(ret))

    def post(self):
        user_id = self.get_argument("user_id")
        username = self.get_argument("username")
        token = UserTokenModel.create(user_id, username)
        ret = {"code": 0, "msg": "success", "data": {"token": token}}
        self.write(json_encode(ret))

    def put(self):
        token = self.get_argument("token")
        rowcount = UserTokenModel.update(token)
        if rowcount > 0:
            ret = {"code": 0, "msg": "success"}
            # ret = {"code": 0, "msg": "success", "data": {"token": token}}
        else:
            ret = {"code": 1, "msg": "fail"}
        self.write(json_encode(ret))