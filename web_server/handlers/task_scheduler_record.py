import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.task_scheduler_record import taskSchedulerRecordModel
from models.user_token import UserTokenModel
from models.system_admin_token import SystemAdminTokenModel
import time

class TaskSchedulerRecordListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date + ' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and start_time > %s and start_time < %s" % (starttimeStamp, endtimeStamp)
            data = taskSchedulerRecordModel.get_page(int(page_number) - 1, int(page_count), where)
            count = taskSchedulerRecordModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))

class TaskSchedulerRecordHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            task_id = self.get_argument("task_id")
            result = taskSchedulerRecordModel.getByTaskid(task_id)  # 创建新的记录
            if result:
                ret = {'code': 0, 'msg': 'success', 'data': result}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'mag': 'fail, user token not found'}
        self.write(json_encode(ret))
    def post(self):
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            task_id = self.get_argument("task_id")
            task_uuid = self.get_argument("task_uuid")
            start_type = self.get_argument("start_type")
            result = taskSchedulerRecordModel.create(task_id, task_uuid, start_type)  # 创建新的记录
            if result:
                ret = {'code': 0, 'msg': 'success', 'data': result}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'mag': 'fail, user token not found'}
        self.write(json_encode(ret))

    def put(self):
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            task_id = self.get_argument("task_id")
            end_type = self.get_argument("end_type")
            result = taskSchedulerRecordModel.update(task_id, end_type)  # 创建新的记录
            if result > 0:
                ret = {'code': 0, 'msg': 'success'}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'mag': 'fail, user token not found'}
        self.write(json_encode(ret))