import requests
import tornado.web
import xmltodict
from tornado.escape import json_encode
from base import BaseHandler
from models.order import orderModel
from models.user_token import UserTokenModel
from models.system_admin_token import SystemAdminTokenModel
from models.price_expire import priceExpireModel
from models.price_dict import priceDictModel
import time
import datetime
import decimal
import json
import hashlib
import random
import socket
import string
import os

# 生成随机字符串
def generate_nonce_str(size=32):
    charsets = string.ascii_uppercase + string.digits
    result = []
    for index in range(0, size):
        result.append(random.choice(charsets))
    return "".join(result)

# 生成签名
def sign_func(payload, sign_key=None):
    params_list = []
    for key, value in payload.items():
        if value:
            params_list.append("%s=%s" % (key, value))
    params_list.sort()
    raw_str = "&".join(params_list)
    if sign_key:
        raw_str += "&key=%s" % sign_key
    md5 = hashlib.md5()
    md5.update(raw_str.encode('utf8'))
    return md5.hexdigest().upper()

def re_dict_to_xml(params):
    request_xml_str = '<xml>'
    for key, value in params.items():
        if isinstance(value, str):
            request_xml_str = '%s<%s><![CDATA[%s]]></%s>' % (request_xml_str, key, value, key,)
        else:
            request_xml_str = '%s<%s>%s</%s>' % (request_xml_str, key, value, key,)
    request_xml_str = '%s</xml>' % request_xml_str
    return request_xml_str

def xml_to_dict(xml):
    xmltodict.parse(xml)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)
        
class OrderListHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            where = ' 1=1 and status=1 and is_pay=1'
            count = orderModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count']}
            self.write(json_encode(ret))
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
            self.write(json_encode(ret))
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
            status = self.get_argument('status')
            username = self.get_argument("username")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date+' 00:00:00'
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
            if status != '':
                where += " and status = '" + status + "' "
            if username != '':
                where += " and username like '%" + username + "%'"
            data = orderModel.get_page(int(page_number)-1, int(page_count), where)
            j = json.dumps(data, cls=DecimalEncoder)
            print(j.encode('utf8'))
            count = orderModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": json.loads(j)}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))

class OrderHandler(BaseHandler,tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            where = ' 1=1 and status=1 and is_pay=1'
            count = orderModel.get_distinct_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count']}
            self.write(json_encode(ret))
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
            self.write(json_encode(ret))
    def post(self):
        # 接收参数
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            print(user)
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            pay_way = self.get_argument("pay_way")
            order_number = self.get_argument('order_number')
            status = self.get_argument('status')
            username = self.get_argument('username')
            where = " 1=1 and user_id=%s and username='%s' " % (user['user_id'], user['username'])
            print(where)
            if start_date and end_date:
                start_date = start_date+' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and pay_time > %s and pay_time < %s" % (starttimeStamp, endtimeStamp)
            if pay_way != '' and pay_way != '支付方式':
                where += " and pay_way = '" + pay_way + "' "
            if order_number != '':
                where += " and order_number like '%" + order_number + "%' "
            if status != '' and status != '订单状态':
                where += " and status = '" + status + "' "
            data = orderModel.get_page(int(page_number) - 1, int(page_count), where)
            j = json.dumps(data, cls=DecimalEncoder)
            print(j.encode('utf8'))
            count = orderModel.get_count(where)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": json.loads(j)}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))

class OrderPayHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        # 接收参数
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            price_id = self.get_argument("price_id")
            pay_price = self.get_argument("pay_price")
            pay_way = self.get_argument("pay_way")
            if pay_way == 'ali':
                from alipay import AliPay
                # self.write(j)
                # print(os.path.dirname(os.path.abspath(__file__)))
                app_private_key_string = open(
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_private_key.pem')).read()
                # app_private_key_string = """
                #     -----BEGIN RSA PRIVATE KEY-----
                #     MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCKS1phpCX9QXDwfzVBCYJ9bDy4g6+JefI5cOvLS00MEkqqFwtKUUcK5p9lJIbFJGY+FfqONfgCJa26rpqz7cjR/lWben0hCfZZ+fnj7iG1HerneMATi/+NOomYgD43CXxFN4CbCyAjVVBDVAdCAEiuHb3e/AgaFHhIht6FF+lhiMG5NcFQTDcN078vauqu/o8pk1odjsKAU+vchu/iRfCGHZPZW4+0IKskmzrGlGZ/Zssmia/LaI4gAMNaleT6i0sP9tV3nboQgzWvgReGKVMYT+1mmJbocgDFHzYLj9jxgoqick0vuRzFG5zWr9PBoizfW449LPDiBCLgX8DPqwA3AgMBAAECggEAddeyA4Phj0XFXFm5YlsdI40ozL4BxW7xdfsAIjJfTAsGLpwGVeSeWe6dIo2WfcT/jqYh5C6e0A2VVX9Vej8EIdTM0/jzSUT49EDrrEsN1AzTTzz4x29Dau/XseiNm05s43phDzzSvOkExOqEaLxfMmdLlQhESxzoRj0OvnDawO2L2/lxIrAi+gSOdZlMprOqAwSVC4f1SsGgocLJ2kuGMBSZec+1U3sNuOXAgZ8mmDoSJ0hjqppoOPWMpVI8NH6qCeGsp1LEf9iK91y1UCXpzWtIXZSbdRc2qRuSayK+r5ytr4L629uZil3UaRWA7smo9WY19sEguTfVdlBIToTcYQKBgQDEJgMJjcW1miiLLcC4U4XZSZ8aOeygsfD2dHIf1N+FoEAhClwjM+4+fhGkj7Pct/ap9WCmZUwehaOu2FgID/QvQdIm5gw5xcTYXXIo6+YzfrlZQA6QdbK20oloskB4P0VYLO9hv48o37lX4TH3Mw7TYtL8wqfB1GqFrp0+w5bg0QKBgQC0fhwbwwPBI2TTWrGucdvhRP/CjxV4IF1cEOq+/DxDr+uNHpmfrCJNF/zSCQ5LvY+Ofny+L/ML+Fkju7MTj25d+8/DZhvn1c6jlhjna4DP50++9SjAA8DmJmAdedoaY1S7CGIqGpAEKR8lKfY7MKrP7juH0MBsEhqLNdA2L3/ShwKBgHbzlmP01jGLi4rb9EPUYxeizhnZhubtAnRzqcIkFmmzBTEEV1wB4jmDuq9RdoIkDjKD3FkMlVztLpaaHMjG5A7Em+17FW7zwKx1/wVSCgiwkTbO4gY5WmgExc/4SaCivir7FTDyOp9PDdd9eg+vpw4KoGkooxOo/fCUNEgb1SQBAoGAHKXPjFB9rhASFsHUZd3Iio7LEXRocfKhHtXIjJu4bP3lIzbyJzfJEfd2t1ecn0TtHi7RWdZ+ey3l6BgIqlgfqmcnaNoyH6/95lUSitizT0xlieebmi5+VYlNxB/tEDcn4a/I9OnWZfKo8NsiK+7jjbFAXaQyhnSxJdtaut77KM0CgYBCFpceHpBz3VoriNEzZaTSesNrjklzYJk6IauWoXTpGd1Dc205HhLKdzM5ElegYu9/UaRdE+BnoYhrsgsDdQds4onsUstCVhdS0p4Mg6ZJ779cBncJ+xztT+CmNemQthwl5JKAZzN4LmqZCclIn6NnBtYYwd1FOVTYc7YFGV2k9w==
                #     -----END RSA PRIVATE KEY-----
                # """
                alipay_public_key_string = open(
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alipay_public_key.pem')).read()
                # alipay_public_key_string = """
                #     -----BEGIN PUBLIC KEY-----
                #     MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiktaYaQl/UFw8H81QQmCfWw8uIOviXnyOXDry0tNDBJKqhcLSlFHCuafZSSGxSRmPhX6jjX4AiWtuq6as+3I0f5Vm3p9IQn2Wfn54+4htR3q53jAE4v/jTqJmIA+Nwl8RTeAmwsgI1VQQ1QHQgBIrh293vwIGhR4SIbehRfpYYjBuTXBUEw3DdO/L2rqrv6PKZNaHY7CgFPr3Ibv4kXwhh2T2VuPtCCrJJs6xpRmf2bLJomvy2iOIADDWpXk+otLD/bVd526EIM1r4EXhilTGE/tZpiW6HIAxR82C4/Y8YKKonJNL7kcxRuc1q/TwaIs31uOPSzw4gQi4F/Az6sANwIDAQAB
                #     -----END PUBLIC KEY-----
                # """
                # 业务处理:使用python sdk调用支付宝的支付接口
                # 初始化
                alipay = AliPay(
                    appid="2021001163671530",  # 应用id
                    app_notify_url='http://www.awsl58.com/personal.html',  # 默认回调url
                    app_private_key_string=app_private_key_string,
                    # os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_private_key.pem'),
                    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                    alipay_public_key_string=alipay_public_key_string,
                    # os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alipay_public_key.pem'),
                    sign_type="RSA2",  # RSA 或者 RSA2
                    debug=False  # 默认False
                )
                order_number = orderModel.get_order_code()
                # 调用支付接口
                # 电脑网址支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
                order_string = alipay.api_alipay_trade_page_pay(
                    out_trade_no=order_number,
                    total_amount=str(pay_price),
                    subject="awsl_alipay",
                    return_url='http://www.awsl58.com/personal.html',
                    notify_url=None  # 可选, 不填则使用默认notify url
                )
                result = orderModel.create(order_number, user['user_id'], user['username'], price_id, pay_price, pay_way)
                print(result)
                j = json.dumps(result, cls=DecimalEncoder)
                print(j.encode('utf8'))
                # 返回应答
                pay_url = 'https://openapi.alipay.com/gateway.do?' + order_string
                resp = {"res": pay_way, "pay_url": pay_url, "order_number": order_number}
                self.write(json_encode(resp))
            elif pay_way == 'paypal':
                import paypalrestsdk
                # 配置
                paypalrestsdk.configure({
                    "mode": "sandbox",  # sandbox or live
                    "client_id": "Aa390bSnYStCDF7jV6uHMOnLEI1e2AaynSOtNsGHrxQHGG83Y39PTLVkPwwvYIcbOTRmXfYtoSbon88B",
                    "client_secret": "EDTfAE9NQeLXjp0N6sbzDKX4uYsPCiFQO9vF9fryejK8q5aTDm_vFHwtFPH6qiO8WFosYXV0aAxL8qTI"
                })
                # 创建付款
                payment = paypalrestsdk.Payment({
                    "intent": "sale",
                    "payer": {
                        "payment_method": "paypal"
                    },
                    "redirect_urls": {
                        "return_url": "http://www.paypal.com/return",
                        "cancel_url": "http://www.paypal.com/cancel"
                    },
                    "transactions": [
                        {"item_list":
                            {"items": [
                                {
                                    "name": "item",
                                    "sku": "item",
                                    "price": "5.00",
                                    "currency": "USD",
                                    "quantity": 1
                                }
                            ]},
                            "amount":
                                {"total": "5.00",
                                 "currency": "USD"},
                            "description": "This is the payment transaction description."
                        }
                    ]
                })
                if payment.create():
                    print("Payment %s created successfully" % payment.id)
                else:
                    print(payment.error)
                # 授权付款
                for link in payment.links:
                    if link.rel == "approval_url":
                        # Convert to str to avoid Google App Engine Unicode issue
                        # https://github.com/paypal/rest-api-sdk-python/pull/58
                        approval_url = str(link.href)
                        print("Redirect for approval: %s" % (approval_url))
                        result = orderModel.create(payment.id, user['user_id'], user['username'], price_id, pay_price, pay_way)
                        print(result)
                        j = json.dumps(result, cls=DecimalEncoder)
                        print(j.encode('utf8'))
                        resp = {'code': 0, 'msg': 'success', "res": pay_way, "pay_url": approval_url, "order_number": payment.id}
                        self.write(json_encode(resp))
                        break
                else:
                    resp = {'code': 1, 'msg': 'fail', "res": pay_way, "pay_url": '未获取到返回地址', "order_number": payment.id}
                    self.write(json_encode(resp))

                # # 执行付款
                # payment = paypalrestsdk.Payment.find(payment.id)
                # if payment.execute({"payer_id": "84MHUHMWFTKA8"}):
                #     print("Payment execute successfully")
                # else:
                #     print(payment.error)  # Error Hash

                # 获取付款详细信息
                # Fetch Payment
                # paymentFetch = paypalrestsdk.Payment.find(payment.id)  #  "PAY-57363176S1057143SKE2HO3A"
                # # paymentFetch = paypalrestsdk.Payment.find("PAYID-L3C6CSY02381787GF482545U")  # "PAYID-L3C6CSY02381787GF482545U"
                # print(paymentFetch)
                # Get List of Payments
                # payment_history = paypalrestsdk.Payment.all({"count": 10})
                # payment_history.payments
                #
                # # 支付
                # from paypalrestsdk import Payout, ResourceNotFound
                # payout = Payout({
                #     "sender_batch_header": {
                #         "sender_batch_id": "batch_1",
                #         "email_subject": "You have a payment"},
                #     "items": [
                #         {
                #             "recipient_type": "EMAIL",
                #             "amount": {
                #                 "value": 0.99,
                #                 "currency": "USD"},
                #             "receiver": "shirt-supplier-one@mail.com",
                #             "note": "Thank you.",
                #             "sender_item_id": "item_1"}
                #     ]
                # })
                # if payout.create(sync_mode=True):
                #     print("payout[%s] created successfully" % (payout.batch_header.payout_batch_id))
                # else:
                #     print(payout.error)
                #
                # # 发票
                # from paypalrestsdk import Invoice
                # invoice = Invoice({
                #     'merchant_info': {
                #         "email": "default@merchant.com",
                #     },
                #     "billing_info": [{
                #         "email": "example@example.com"}],
                #     "items": [{
                #         "name": "Widgets",
                #         "quantity": 20,
                #         "unit_price": {
                #             "currency": "USD",
                #             "value": 2}
                #     }],
                # })
                # response = invoice.create()
                # print(response)
                #
                # import paypalrestsdk
                # from paypalrestsdk.openid_connect import Tokeninfo, Userinfo
                # paypalrestsdk.configure({
                #     "mode": "sandbox",
                #     "client_id": "CLIENT_ID",
                #     "client_secret": "CLIENT_SECRET",
                #     "openid_redirect_uri": "http://example.com"})
                # # Generate login url
                # login_url = Tokeninfo.authorize_url({"scope": "openid profile"})
                # # Create tokeninfo with Authorize code
                # tokeninfo = Tokeninfo.create("Replace with Authorize code")
                # # Refresh tokeninfo
                # tokeninfo = tokeninfo.refresh()
                # # Create tokeninfo with refresh_token
                # tokeninfo = Tokeninfo.create_with_refresh_token("Replace with refresh_token")
                # # Get userinfo
                # userinfo = tokeninfo.userinfo()
                # # Get userinfo with access_token
                # userinfo = Userinfo.get("Replace with access_token")
                # # Generate logout url
                # logout_url = tokeninfo.logout_url()
            elif pay_way == 'wx':
                APP_ID = ''
                MCH_ID = ''
                nonce_str = generate_nonce_str()
                # nonce_str = str(int(round(time.time() * 1000))) + str(random.randint(1, 999)) + string.join(random.sample(
                #     ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                #      'u',
                #      'v', 'w', 'x', 'y', 'z'], 5)).replace(" ", "")  # 生成随机字符串
                out_trade_no = orderModel.get_order_code()
                total_fee = ''
                _host_name = socket.gethostname()
                _ip_address = socket.gethostbyname(_host_name)
                spbill_create_ip = _ip_address
                NOTIFY_URL = ''
                product_id = ''
                params = {
                    "appid": APP_ID,
                    "mch_id": MCH_ID,
                    "nonce_str": nonce_str,
                    "out_trade_no": out_trade_no,
                    "body": 'xxxx',
                    "total_fee": total_fee,
                    "spbill_create_ip": spbill_create_ip,
                    "notify_url": NOTIFY_URL,
                    "trade_type": "NATIVE",
                    "product_id": product_id,
                }
                API_KEY = ''
                sign = self.sign_func(params, API_KEY)  # 调用签名生成函数
                params["sign"] = sign
                req_xml = self.re_dict_to_xml(params)  # 调用函数将dict转为xml格式
                UNIFIED_ORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
                res_xml = requests.post(UNIFIED_ORDER_URL, req_xml, verify=False)  # 调用统一下单API
                res_xml.encoding = 'utf-8'
                _, res_obj = self.xml_to_dict(res_xml.text)  # 调用函数将结果转成dict 方便后续的解析
                code_url = res_obj["code_url"]  # 此处获得二维码url
                if code_url:
                    result = orderModel.create(out_trade_no, user['user_id'], user['username'], price_id, pay_price,
                                               pay_way)
                    print(result)
                    j = json.dumps(result, cls=DecimalEncoder)
                    print(j.encode('utf8'))
                    return_url = "http://www.awsl58.com/wx_qrcode.html?code_url=" + code_url
                    resp = {'code': 0, 'msg': 'success', "res": pay_way, "pay_url": return_url, "order_number": out_trade_no}
                else:
                    resp = {'code': 1, 'msg': 'fail', "res": pay_way, "pay_url": '二维码失效', "order_number": out_trade_no}
                self.write(json_encode(resp))
            else:
                pass
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
            self.write(json_encode(ret))


class OrderPayCheckHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        user = UserTokenModel.getUserToken(token)
        if user:
            # 接收参数
            order_number = self.get_argument("order_number")
            print(order_number)
            pay_way = self.get_argument("pay_way")
            if pay_way == 'ali':
                from alipay import AliPay
                # 业务处理:使用python sdk调用支付宝的支付接口
                # 初始化
                app_private_key_string = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_private_key.pem')).read()
                alipay_public_key_string = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alipay_public_key.pem')).read()
                alipay = AliPay(
                    appid="2021001163671530",  # 应用id
                    app_notify_url='http://www.awsl58.com/personal.html',  # 默认回调url
                    app_private_key_string=app_private_key_string,
                    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                    alipay_public_key_string=alipay_public_key_string,
                    sign_type="RSA2",  # RSA 或者 RSA2
                    debug=False  # 默认False
                )
                ret = {}
                while True:
                    response = alipay.api_alipay_trade_query(out_trade_no=order_number)
                    print(response)
                    # {'code': '10000', 'msg': 'Success', 'buyer_logon_id': 'wei***@foxmail.com',
                    #  'buyer_pay_amount': '0.00', 'buyer_user_id': '2088502994100875', 'invoice_amount': '0.00',
                    #  'out_trade_no': '202006121717225892644', 'point_amount': '0.00', 'receipt_amount': '0.00',
                    #  'send_pay_date': '2020-06-12 17:18:02', 'total_amount': '0.01',
                    #  'trade_no': '2020061222001400871418663435', 'trade_status': 'TRADE_SUCCESS'}

                    code = response.get('code')
                    if code == '10000' and response.get("trade_status") == "TRADE_SUCCESS":
                        trade_no = response.get("trade_no")
                        order = orderModel.getByOrderNumber(order_number)
                        if order:
                            price_expire = priceExpireModel.getByOrderId(order['id'])
                            if price_expire is None:
                                pricedict = priceDictModel.get(order['price_id'])
                                addDays = 0
                                if pricedict['price_week'] == order['pay_price']:
                                    addDays = 7
                                if pricedict['price'] == order['pay_price']:
                                    addDays = 30
                                if pricedict['price_quarter'] == order['pay_price']:
                                    addDays = 90
                                if pricedict['price_half_a_year'] == order['pay_price']:
                                    addDays = 180
                                rtn = orderModel.update(order_number, trade_no)
                                date = datetime.datetime.now() + datetime.timedelta(days=addDays)
                                timeArray = time.strptime(str(date), "%Y-%m-%d %H:%M:%S.%f")
                                timeStamp = int(time.mktime(timeArray))
                                priceExpireModel.create(order['id'], timeStamp)
                                if rtn > 0:
                                    ret['code'] = 0
                                    ret['msg'] = 'success'
                                else:
                                    ret['code'] = 3
                                    ret['msg'] = 'fail,database fail'
                            else:
                                ret['code'] = 6
                                ret['msg'] = 'fail,The result already exists'
                        else:
                            ret['code'] = 4
                            ret['msg'] = 'fail,order not found'
                        break
                    elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                        time.sleep(5)
                        continue
                    else:
                        ret['code'] = 2
                        ret['msg'] = 'fail'
                        break
                print(json_encode(ret))
                self.write(json_encode(ret))
            elif pay_way == 'paypal':
                import paypalrestsdk
                # order_number = payment.id
                # resp = {"res": pay_way, "pay_url": pay_url, "order_number": order_number}
                # self.write(json_encode(resp))
                ret = {}
                while True:
                    paymentFetch = paypalrestsdk.Payment.find(order_number)  # "PAY-57363176S1057143SKE2HO3A"
                    # paymentFetch = paypalrestsdk.Payment.find("PAYID-L3C6CSY02381787GF482545U")  # "PAYID-L3C6CSY02381787GF482545U"
                    print(type(paymentFetch))
                    print(paymentFetch)
                    state = paymentFetch.state
                    if state == 'created':
                        print('已创建')
                        payer = paymentFetch.payer
                        if payer:
                            payer_id = paymentFetch.payer.payer_info.payer_id
                            print(payer_id)
                            if paymentFetch.execute({"payer_id": payer_id}):
                                print("Payment execute successfully")
                                break
                            else:
                                print(paymentFetch.error)  # Error Hash
                    elif state == 'approved':
                        print('支付成功')
                        order = orderModel.getByOrderNumber(order_number)
                        if order:
                            rtn = orderModel.update(order_number, '')
                            date = datetime.datetime.now() + datetime.timedelta(days=30)
                            timeArray = time.strptime(str(date), "%Y-%m-%d %H:%M:%S")
                            timeStamp = int(time.mktime(timeArray))
                            priceExpireModel.create(order['id'], timeStamp)
                            if rtn > 0:
                                ret['code'] = 0
                                ret['msg'] = 'success'
                            else:
                                ret['code'] = 3
                                ret['msg'] = 'fail,database fail'
                        else:
                            ret['code'] = 4
                            ret['msg'] = 'fail,order not found'
                        return ret
                    elif state == 'failed':
                        print('支付失败')
                        ret['code'] = 2
                        ret['msg'] = 'fail'
                        return ret
                    else:
                        print('未知状态')
                        ret['code'] = 4
                        ret['msg'] = 'fail, unknown error'
                        return ret
                self.write(json_encode(ret))
            elif pay_way == 'wx':
                ret = {}
                while True:
                    data = {
                        'out_trade_no': order_number,
                        'pay_status': 0,
                        'err_msg': None
                    }
                    nonce_str = generate_nonce_str()
                    APP_ID = ''
                    MCH_ID = ''
                    params = {
                        "appid": APP_ID,
                        "mch_id": MCH_ID,
                        "nonce_str": nonce_str,
                        "out_trade_no": order_number,
                    }
                    API_KEY = ''
                    sign = sign_func(params, API_KEY)
                    params["sign"] = sign
                    req_xml = re_dict_to_xml(params)
                    QUERY_ORDER_URL = "https://api.mch.weixin.qq.com/pay/orderquery"
                    res_xml = requests.post(QUERY_ORDER_URL, req_xml, verify=False)
                    res_xml.encoding = 'utf8'
                    _, res_obj = xml_to_dict(res_xml.text)
                    if res_obj["return_code"] == "FAIL":
                        ret['code'] = 2
                        ret['msg'] = 'fail'
                        return res_obj["err_code_des"]
                    else:
                        result_code = res_obj["result_code"]
                        trade_state = res_obj["trade_state"]
                        if result_code == "SUCCESS":
                            if trade_state == "SUCCESS":
                                order = orderModel.getByOrderNumber(order_number)
                                if order:
                                    data['pay_status'] = 1
                                    rtn = orderModel.update(order_number, res_obj["transaction_id"])
                                    date = datetime.datetime.now() + datetime.timedelta(days=30)
                                    timeArray = time.strptime(str(date), "%Y-%m-%d %H:%M:%S")
                                    timeStamp = int(time.mktime(timeArray))
                                    priceExpireModel.create(order['id'], timeStamp)
                                    if rtn > 0:
                                        ret['code'] = 0
                                        ret['msg'] = 'success'
                                    else:
                                        ret['code'] = 3
                                        ret['msg'] = 'fail,database fail'
                                else:
                                    ret['code'] = 4
                                    ret['msg'] = 'fail,order not found'
                            else:
                                ret['code'] = 4
                                ret['msg'] = res_obj['trade_state_desc']
                                data['err_msg'] = res_obj['trade_state_desc']
                        else:
                            ret['code'] = 4
                            ret['msg'] = res_obj['err_code_des']
                            data['err_msg'] = res_obj['err_code_des']
                    return data
                self.write(json_encode(ret))
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
            self.write(json_encode(ret))


class OrderPayCheckManualHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            order_number = self.get_argument("order_number")
            print(order_number)
            pay_way = self.get_argument("pay_way")
            from alipay import AliPay
            # 业务处理:使用python sdk调用支付宝的支付接口
            # 初始化
            app_private_key_string = open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_private_key.pem')).read()
            alipay_public_key_string = open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alipay_public_key.pem')).read()
            alipay = AliPay(
                appid="2021001163671530",  # 应用id
                app_notify_url=None,  # 默认回调url
                app_private_key_string=app_private_key_string,
                # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                alipay_public_key_string=alipay_public_key_string,
                sign_type="RSA2",  # RSA 或者 RSA2
                debug=False  # 默认False
            )
            ret = {}
            response = alipay.api_alipay_trade_query(out_trade_no=order_number)
            print(response)
            code = response.get('code')
            if code == '10000' and response.get("trade_status") == "TRADE_SUCCESS":
                trade_no = response.get("trade_no")
                order = orderModel.getByOrderNumber(order_number)
                if order:
                    pricedict = priceDictModel.get(order['price_id'])
                    addDays = 0
                    if pricedict['price_week'] == order['pay_price']:
                        addDays = 7
                    if pricedict['price'] == order['pay_price']:
                        addDays = 30
                    if pricedict['price_quarter'] == order['pay_price']:
                        addDays = 90
                    if pricedict['price_half_a_year'] == order['pay_price']:
                        addDays = 180
                    rtn = orderModel.update(order_number, trade_no)
                    date = datetime.datetime.now() + datetime.timedelta(days=addDays)
                    timeArray = time.strptime(str(date), "%Y-%m-%d %H:%M:%S.%f")
                    timeStamp = int(time.mktime(timeArray))
                    priceExpireModel.create(order['id'], timeStamp)
                    if rtn > 0:
                        ret['code'] = 0
                        ret['msg'] = 'success'
                    else:
                        ret['code'] = 3
                        ret['msg'] = 'fail,database fail'
                else:
                    ret['code'] = 4
                    ret['msg'] = 'fail,order not found'
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                ret['code'] = 5
                ret['msg'] = 'fail,wait buyer pay'
            else:
                ret['code'] = 2
                ret['msg'] = 'fail'
            self.write(json_encode(ret))
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
            self.write(json_encode(ret))

# public static void main(String[] args) {
# /** 开放平台应用APPID */
# String appid = "";
# /** 开放平台应用APPID对应私钥 */
#     String privateKey = "";
# /** 开放平台应用APPID对应支付宝公钥 */
#     String alipayPublicKey = "";
# // sdk初始化
# AlipayClient alipayClient = new DefaultAlipayClient("https://openapi.alipay.com/gateway.do",appid,privateKey, "json","utf-8",alipayPublicKey, "RSA2");
# AlipayTradePagePayRequest request = new AlipayTradePagePayRequest();
# AlipayTradePagePayModel model = new AlipayTradePagePayModel();
# model.setBody("测试内容");
# model.setSubject("商品名称");
# model.setTotalAmount("0.01");
# model.setOutTradeNo("2020021500000001");
# request.setBizModel(model);
# try {
# AlipayTradePagePayResponse response = alipayClient.pageExecute(request);
# if (response.isSuccess()) {
# System.out.println("调用成功, 网页支付表单:" + response.getBody());
# }
# else {
# System.out.println("调用失败:" + response.getSubMsg());
# }
# }
# catch (AlipayApiException e) {
# System.out.println("接口调用异常:" + JSONObject.toJSONString(e));
# }
# }



