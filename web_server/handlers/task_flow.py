import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.optimize_configuration import optimizeConfigurationModel
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
# import logging

scheduler = None

# 初始化
def init_scheduler():
    global scheduler
    executor = ThreadPoolExecutor(max_workers=20)  # 最多20个线程同时执行
    scheduler = TornadoScheduler()
    scheduler.add_executor(executor)
    scheduler.start()
    print('[Scheduler Init]APScheduler has been started')

    # logging.basicConfig()
    # logging.getLogger('apscheduler').setLevel(logging.DEBUG)

class TeskFlowHandler(BaseHandler, tornado.web.RequestHandler):
    init_scheduler()

    def get(self):
        sss = scheduler.get_jobs()
        print(sss)

    def task11(self):
        print('12323232323')
        # print(logging.DEBUG)

    def post(self):
        tt = scheduler.add_job(self.task11, 'cron', second=2, id="0001")
        print(tt.id)
        # print('task')

    def put(self):
        id = self.get_argument("id")
        oper = self.get_argument("operType")
        rtn = scheduler.get_job(job_id=id)
        print(rtn)
        if rtn:
            if oper == 0:
                scheduler.pause_job(job_id=id)
                print('暂停成功')
            if oper == 1:
                scheduler.resume_job(job_id=id)
                print('恢复成功')
        else:
            print('未找到')

    def delete(self):
        id = self.get_argument("id")
        rtn = scheduler.get_job(job_id=id)
        print(rtn)
        if rtn:
            scheduler.remove_job(id)
            print('移除成功')
        else:
            print('未找到')


        # user_id = self.get_argument("user_id")
        # username = self.get_argument("username")
        # oper_type = self.get_argument("oper_type")
        # optimizeConfigurations = optimizeConfigurationModel.get_current(user_id, username, oper_type)
        # self.headers = {
        #     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)"
        # }
        # if optimizeConfigurations[1] == '':
        #     pass
        # else:
        #     html = requests.get(optimizeConfigurations[2], headers=self.headers)
        #     selector = etree.HTML(html.text)
        #     links = selector.xpath('//a/@href')
        # self.write(json_encode(optimizeConfigurations))



        # scheduler.get_job(job_id="0001")
        # scheduler.shutdown()