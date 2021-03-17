import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.ip_library import ip_libraryModel
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class ip_libraryHandler(BaseHandler, tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(200)

    @tornado.gen.coroutine
    def get(self):
        ret = yield self.getIpLibrary()
        self.write(json_encode(ret))

    @run_on_executor
    def getIpLibrary(self):
        data = ip_libraryModel.getByLastCheckOperTime()
        ret = {'code': 0, "msg": "success!", 'data': data}
        return ret

    def put(self):
        id = self.get_argument("id")
        result = ip_libraryModel.update(id)
        if result > 0:
            ret = {'code': 0, 'msg': 'success'}
        else:
            ret = {'code': 1, 'msg': 'fail'}
        self.write(json_encode(ret))

    def delete(self):
        id = self.get_argument("id")
        result = ip_libraryModel.delete(id)
        if result > 0:
            ret = {'code': 0, 'msg': 'success'}
        else:
            ret = {'code': 1, 'msg': 'fail'}
        self.write(json_encode(ret))

class ip_libraryListHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        index = self.get_argument("index")
        data = ip_libraryModel.getTopLimit(index)
        ret = {'code': 0, "msg": "success!", 'data': data}
        self.write(json_encode(ret))