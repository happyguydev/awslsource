import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.price_dict import priceDictModel
from models.user_token import UserTokenModel
from models.system_admin_token import SystemAdminTokenModel
import json
import decimal
import time

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

class PriceDictListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            member_type = self.get_argument("member_type")
            username = self.get_argument("username")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date+' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and start_time > %s and start_time < %s" % (starttimeStamp, endtimeStamp)
            if member_type != '' and member_type != '会员类型':
                where += " and member_type = '" + member_type + "' "
            if username:
                where += " and username like '%" + username + "%'"
            data = priceDictModel.get_page(int(page_number)-1, int(page_count), where)
            j = json.dumps(data, cls=DecimalEncoder)
            print(j.encode('utf8'))
            count = priceDictModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": json.loads(j)}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))

class PriceDictCurrentListHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            price_id = self.get_argument("id")
            priceDicts = priceDictModel.get(price_id)
            j = json.dumps(priceDicts, cls=DecimalEncoder)
            print(j.encode('utf8'))
            ret = {'code': 0, 'mag': 'success', 'data': json.loads(j)}
        else:
            ret = {'code': 1, 'mag': 'fail, user token not found'}
        self.write(json_encode(ret))
    def post(self):
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            priceDicts = priceDictModel.get_current_all()
            j = json.dumps(priceDicts, cls=DecimalEncoder)
            print(j.encode('utf8'))
            ret = {'code': 0, 'mag': 'success', 'data': json.loads(j)}
        else:
            ret = {'code': 1, 'mag': 'fail, user token not found'}
        self.write(json_encode(ret))

class PriceDictHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            price_week = self.get_argument("price_week")
            price = self.get_argument("price")
            price_quarter = self.get_argument("price_quarter")
            price_half_a_year = self.get_argument("price_half_a_year")

            ip_count = self.get_argument("ip_count")
            member_type = self.get_argument("member_type")
            priceDictModel.update(member_type)  # 自定结束之前的数据
            if price_quarter and price_half_a_year:
                result = priceDictModel.create(price, price_quarter, price_half_a_year, ip_count, member_type, systemAdmin['system_admin_username'])  # 创建新的记录
            else:
                result = priceDictModel.create1(price_week, ip_count, member_type,
                                               systemAdmin['system_admin_username'])  # 创建新的记录
            if result:
                j = json.dumps(result, cls=DecimalEncoder)
                print(j.encode('utf8'))
                ret = {'code': 0, 'msg': 'success', 'data': json.loads(j)}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'mag': 'fail, user token not found'}
        self.write(json_encode(ret))
