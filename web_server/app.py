import threading
import tornado.ioloop
import asyncio
import tornado.web
import tornado.httpserver
import platform
import os
from tornado.routing import URLSpec
from handlers.user import UserListHandler, UserHandler, UserLoginHandler
from handlers.user_token import UserTokenHandler
from handlers.system_admin import SystemAdminListHandler, SystemAdminHandler, SystemAdminLoginHandler
from handlers.ip_library import IpLibraryHandler
from handlers.price_dict import PriceDictHandler, PriceDictCurrentListHandler, PriceDictListHandler
from handlers.optimize_configuration import OptimizeConfigurationHandler, OptimizeConfigurationListHandler, OptimizeConfigurationKeywordRankListHandler, OptimizeConfigurationSourceWebsiteRankListHandler, OptimizeConfigurationTargetWebsiteRankListHandler
from handlers.price_expire import PriceExpireHandler, PriceExpireListHandler
from handlers.order import OrderListHandler, OrderHandler, OrderPayHandler, OrderPayCheckHandler, OrderPayCheckManualHandler
from handlers.user_agent import UserAgentHandler
from handlers.task_scheduler_record import TaskSchedulerRecordListHandler, TaskSchedulerRecordHandler
from handlers.task_scheduler import TeskSchedulerHandler
from handlers.ip_agent_pool import IpAgentPoolHandler, IpAgentPoolListHandler
from handlers.ip_library import IpLibraryTestHandler
from handlers.download import DownloadHandler, DownloadListHandler, uploadFileHandler, uploadImageHandler, versionHandler, DownloadListUserHandler
from handlers.news import NewsHandler, NewsListHandler, NewsListUserHandler
from handlers.contact_us import ContactUsHandler, ContactUsUserHandler
from handlers.system_config import SystemConfigHandler

current_path = os.path.dirname(__file__)

HANDLERS = {
    (r"/api/users", UserListHandler),
    (r"/api/user", UserHandler),
    (r"/api/user/login", UserLoginHandler),
    (r"/api/systemAdmins", SystemAdminListHandler),
    (r"/api/systemAdmin", SystemAdminHandler),
    (r"/api/systemAdmin/login", SystemAdminLoginHandler),
    (r"/api/userToken", UserTokenHandler),
    (r"/api/ip_library", IpLibraryHandler),
    (r"/api/price_dict", PriceDictHandler),
    (r"/api/priceDictCurrentList", PriceDictCurrentListHandler),
    (r"/api/priceDicts", PriceDictListHandler),
    (r"/api/optimize_configuration", OptimizeConfigurationHandler),
    (r"/api/optimizeConfigurations", OptimizeConfigurationListHandler),
    (r"/api/optimizeConfigurations_keyword_rank", OptimizeConfigurationKeywordRankListHandler),
    (r"/api/optimizeConfigurations_sourcewebsite_rank", OptimizeConfigurationSourceWebsiteRankListHandler),
    (r"/api/optimizeConfigurations_targetwebsite_rank", OptimizeConfigurationTargetWebsiteRankListHandler),
    (r"/api/price_expire", PriceExpireHandler),
    (r"/api/price_expires", PriceExpireListHandler),
    (r"/api/orders", OrderListHandler),
    (r"/api/user_orders", OrderHandler),
    (r"/api/order", OrderPayHandler),
    (r"/api/ordercheck", OrderPayCheckHandler),
    (r"/api/ordercheckmanual", OrderPayCheckManualHandler),
    (r"/api/userAgent", UserAgentHandler),
    (r"/api/taskschedulerrecord", TaskSchedulerRecordHandler),
    (r"/api/taskschedulerrecords", TaskSchedulerRecordListHandler),
    (r"/api/taskscheduler", TeskSchedulerHandler),
    (r"/api/ipAgentPool", IpAgentPoolHandler),
    (r"/api/ipAgentPools", IpAgentPoolListHandler),
    (r"/api/ipLibraryTest", IpLibraryTestHandler),
    (r"/api/download", DownloadHandler),
    (r"/api/downloads", DownloadListHandler),
    (r"/api/uploadFile", uploadFileHandler),
    (r"/api/uploadImage", uploadImageHandler),
    (r"/api/version", versionHandler),
    (r"/api/user_downloads", DownloadListUserHandler),
    (r"/api/new", NewsHandler),
    (r"/api/news", NewsListHandler),
    (r"/api/user_news", NewsListUserHandler),
    (r"/api/contactus", ContactUsHandler),
    (r"/api/user_contactus", ContactUsUserHandler),
    (r"/api/systemConfig", SystemConfigHandler),
    URLSpec(r"/upload/(.*)", tornado.web.StaticFileHandler, {"path": "upload"}),
}

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.set_event_loop(asyncio.new_event_loop())

class WebServer(threading.Thread):
    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        app = tornado.web.Application(
            HANDLERS,
            debug=True,
            static_path=os.path.join(current_path, "upload"),
            cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
            login_url="/api/system_admin/login"
        )
        http_server = tornado.httpserver.HTTPServer(app)
        port = 8091
        http_server.listen(port)
        print("server started on port {}".format(port))
        tornado.ioloop.IOLoop.instance().start()

WebServer().start()