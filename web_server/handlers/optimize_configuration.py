import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.optimize_configuration import optimizeConfigurationModel
from models.user_token import UserTokenModel
from models.system_admin_token import SystemAdminTokenModel
import time

class OptimizeConfigurationHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        result = UserTokenModel.getUserToken(token)
        oper_type = self.get_argument("oper_type")
        rest = optimizeConfigurationModel.get_current(result['user_id'], result['username'], oper_type)
        ret = {'code': 0, 'msg': 'success', 'data': rest}
        self.write(json_encode(ret))

    def post(self):
        token = self.get_argument("token")
        result = UserTokenModel.getUserToken(token)
        user_id = result['user_id']
        username = result['username']
        target_website = self.get_argument("target_website")
        last_page_number = self.get_argument("last_page_number")
        key_word = self.get_argument("key_word")
        ip_flow_everyday_selected = self.get_argument("ip_flow_everyday_selected")
        ip_flow_fixed_count = self.get_argument("ip_flow_fixed_count")
        ip_flow_random_count_start = self.get_argument("ip_flow_random_count_start")
        ip_flow_random_count_end = self.get_argument("ip_flow_random_count_end")
        search_engines_check = self.get_argument("search_engines_check")
        visitor_check = self.get_argument("visitor_check")
        page_random_count_start = self.get_argument("page_random_count_start")
        page_random_count_end = self.get_argument("page_random_count_end")
        length_of_stay_first_page_start = self.get_argument("length_of_stay_first_page_start")
        length_of_stay_first_page_end = self.get_argument("length_of_stay_first_page_end")
        length_of_stay_deep_page_start = self.get_argument("length_of_stay_deep_page_start")
        length_of_stay_deep_page_end = self.get_argument("length_of_stay_deep_page_end")
        time_interval = self.get_argument("time_interval")
        oper_type = self.get_argument("oper_type")
        rest = optimizeConfigurationModel.create(target_website, last_page_number, key_word, ip_flow_everyday_selected, ip_flow_fixed_count, ip_flow_random_count_start,
                                                ip_flow_random_count_end, search_engines_check, visitor_check, page_random_count_start, page_random_count_end,
                                                 length_of_stay_first_page_start, length_of_stay_first_page_end, length_of_stay_deep_page_start,
                                                 length_of_stay_deep_page_end,time_interval, oper_type, user_id, username)
        ret = {"code": 0, "msg": "success", 'data': rest}
        self.write(json_encode(ret))

class OptimizeConfigurationListHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        optimizeConfigurations = optimizeConfigurationModel.get_all()
        self.write(json_encode(optimizeConfigurations))

    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            oper_type = self.get_argument("oper_type")
            username = self.get_argument("username")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date + ' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and commit_time > %s and commit_time < %s" % (starttimeStamp, endtimeStamp)
            if oper_type != '' and oper_type != '操作类型':
                where += " and oper_type = '" + oper_type + "' "
            if username != '':
                where += " and username like '%" + username + "%'"
            data = optimizeConfigurationModel.get_page(int(page_number) - 1, int(page_count), where)
            count = optimizeConfigurationModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))


class OptimizeConfigurationKeywordRankListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            data = optimizeConfigurationModel.get_keyword_rank_page(int(page_number) - 1, int(page_count))
            count = optimizeConfigurationModel.get_keyword_rank_count()
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))


class OptimizeConfigurationSourceWebsiteRankListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            data = optimizeConfigurationModel.get_sourcewebsite_rank_page(int(page_number) - 1, int(page_count))
            count = optimizeConfigurationModel.get_sourcewebsite_rank_count()
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))


class OptimizeConfigurationTargetWebsiteRankListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            data = optimizeConfigurationModel.get_targetwebsite_rank_page(int(page_number) - 1, int(page_count))
            count = optimizeConfigurationModel.get_targetwebsite_rank_count()
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": data}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))