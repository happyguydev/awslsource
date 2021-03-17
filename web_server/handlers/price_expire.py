import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.price_expire import priceExpireModel
from models.user_token import UserTokenModel
from models.system_admin_token import SystemAdminTokenModel
import time
import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

class PriceExpireHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        result = UserTokenModel.getUserToken(token)
        priceExpires = priceExpireModel.get_current(result['user_id'], result['username'])
        self.write(json_encode(priceExpires))

    def post(self):
        order_id = self.get_argument("order_id")
        expire_time = self.get_argument("expire_time")
        ret = priceExpireModel.create(order_id, expire_time)
        # ret = {"status": True, "msg": "create user %s successfully!" % username}
        self.write(json_encode(ret))

class PriceExpireListHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        priceExpires = priceExpireModel.get_all()
        self.write(json_encode(priceExpires))
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            pay_way = self.get_argument("pay_way")
            order_number = self.get_argument('order_number')
            username = self.get_argument("username")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date + ' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and pay_time > %s and pay_time < %s" % (starttimeStamp, endtimeStamp)
            if pay_way != '' and pay_way != '支付方式':
                where += " and pay_way = '" + pay_way + "' "
            if order_number != '':
                where += " and order_number = '" + order_number + "' "
            if username != '':
                where += " and username like '%" + username + "%'"
            data = priceExpireModel.get_page(int(page_number) - 1, int(page_count), where)
            j = json.dumps(data, cls=DecimalEncoder)
            print(j.encode('utf8'))
            count = priceExpireModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": json.loads(j)}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))