import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    # 解决跨域问题
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        # self.set_header('Access-Control-Allow-Origin', 'http://localhost:8080')
        # self.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
        self.set_header('Content-Type', 'application/json; charset=UTF-8;')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type')


    def options(self):
        pass

    # def get(self):
    #     self.write('request get')
    #
    # def post(self):
    #     self.write('request post')
    #
    # # vue一般需要访问options方法， 如果报错则很难继续，所以只要通过就行了，当然需要其他逻辑就自己控制。
    # def options(self):
    #     # 返回方法1
    #     self.set_status(204)
    #     self.finish()
    #     # 返回方法2
    #     self.write('{"errorCode":"00","errorMessage","success"}')
