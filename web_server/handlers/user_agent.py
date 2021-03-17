import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.user_agent import userAgentModel
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

class UserAgentHandler(BaseHandler, tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(200)

    @tornado.gen.coroutine
    def get(self):
        where = self.get_argument("where")
        useragent = yield self.getUserAgent(where)
        self.write(json_encode(useragent))

    @run_on_executor
    def getUserAgent(self, where):
        return userAgentModel.get(where)



class UserAgentListHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        useragentlist = userAgentModel.get_all()
        self.write(json_encode(useragentlist))