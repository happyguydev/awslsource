import threading
import tornado.ioloop
import asyncio
import tornado.web
import tornado.httpserver
import platform
import os
from handlers.ip_library import ip_libraryHandler, ip_libraryListHandler

current_path = os.path.dirname(__file__)

HANDLERS = {
    (r"/api/ip_library", ip_libraryHandler),
    (r"/api/ip_librarys", ip_libraryListHandler),
}

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.set_event_loop(asyncio.new_event_loop())

class WebServer(threading.Thread):
    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        app = tornado.web.Application(
            HANDLERS,
            debug=True
        )
        http_server = tornado.httpserver.HTTPServer(app)
        port = 8003
        http_server.listen(port)
        print("server started on port {}".format(port))
        tornado.ioloop.IOLoop.instance().start()

WebServer().start()