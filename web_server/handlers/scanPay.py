import requests
import json
import tornado.web
from core.weixin_sdk.utils import Util
from core.weixin_sdk.utils import HttpUtil
from core.logger_helper import logger

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

""" 微信扫码支付 """


class WeiXinScanPayHandler(tornado.web.RequestHandler):
    def post(self):
        print("web2shopRequest=", self.request.body)
        params = {}
        params['service'] = 'pay.weixin.native'
        # params['version'] = '2.0'
        # params['charset'] = 'UTF-8'
        # params['sign_type'] = 'MD5'
        params['mch_id'] = '7551000001'
        params['out_trade_no'] = self.get_argument('out_trade_no')
        # params['device_info'] = '127.0.0.1'
        params['body'] = self.get_argument('body')
        params['attach'] = self.get_argument('attach')
        params['total_fee'] = self.get_argument('total_fee')
        params['mch_create_ip'] = self.get_argument('mch_create_ip')
        params['notify_url'] = 'https://weixin.g-pay.cn/scanPaied'  # 通知地址
        params['time_start'] = self.get_argument('time_start')
        params['time_expire'] = self.get_argument('time_expire')
        # params['op_user_id'] = '7551000001' #操作员账号，默认为商户号
        # params['goods_tag'] = '商品标记,用于优惠券或者满减使用'
        # params['product_id'] = '12345678'  #商品ID
        params['nonce_str'] = Util.generate_nonce()
        sign = Util.get_sign(params, "9d101c97133837e13dde2d32a5054abb");
        params['sign'] = sign
        data = Util.dict_to_xml(params)
        print('shop2weifutong=', data)

        BASE_URL = 'https://pay.swiftpass.cn/pay/gateway'
        r = requests.post(BASE_URL, data.encode('utf-8'))
        if r.status_code == 200:
            print('weifutongResponse==', r.text)
            dic = Util.xml_to_dict(r.text)
            if ('0' == dic['status'] and '0' == dic['result_code']):
                self.render("template.html", url=dic['code_img_url'], mch_id=dic['mch_id'])
            else:
                self.render('orderQueryResult.html', title='请求生成二维码失败', dic=dic)


"""支付宝扫码支付 """


class AliScanPayHandler(tornado.web.RequestHandler):
    def post(self):
        print("data=", self.request.body)
        params = {}
        params['service'] = 'pay.alipay.native'
        # params['version'] = '2.0'
        # params['charset'] = 'UTF-8'
        # params['sign_type'] = 'MD5'
        params['mch_id'] = '7551000001'
        params['out_trade_no'] = self.get_argument('out_trade_no')
        # params['device_info'] = '127.0.0.1'
        params['body'] = self.get_argument('body')
        params['attach'] = self.get_argument('attach')
        params['total_fee'] = self.get_argument('total_fee')
        params['mch_create_ip'] = self.get_argument('mch_create_ip')
        params['notify_url'] = 'https://weixin.g-pay.cn/scanPaied'  # 支付后的异步通知地址
        # params['time_start'] = self.get_argument('time_start')
        # params['time_expire'] = self.get_argument('time_expire')
        # params['op_user_id'] = '101520000465' #操作员账号，默认为商户号
        # params['goods_tag'] = '商品标记,用于优惠券或者满减使用'
        params['product_id'] = '12345678'  # 商品ID
        params['nonce_str'] = Util.generate_nonce()
        sign = Util.get_sign(params, "9d101c97133837e13dde2d32a5054abb");
        params['sign'] = sign
        data = Util.dict_to_xml(params)
        print(data)

        BASE_URL = 'https://pay.swiftpass.cn/pay/gateway'
        r = requests.post(BASE_URL, data.encode('utf-8'))
        if r.status_code == 200:
            print('res==', r.text)
            dic = Util.xml_to_dict(r.text)
            if ('0' == dic['status'] and '0' == dic['result_code']):
                self.render("template.html", url=dic['code_img_url'], mch_id=dic['mch_id'])
            else:
                self.render('orderQueryResult.html', title='请求生成二维码失败', dic=dic)


""" 支付后接收异步通知，并做相应处理"""


class PaiedHandler(tornado.web.RequestHandler):
    def post(self):
        print("return=", self.request.body)
        logger.debug('paidHandler:{}'.format(self.request.body))
        self.write("success")


""" 订单查询 """


class OrderQueryHandler(tornado.web.RequestHandler):
    def post(self):
        print("data=", self.request.body)
        params = {}
        params['service'] = 'unified.trade.query'  # 订单查询接口 必填
        # params['mch_id'] = '101520000465'            #商户号  必填
        params['mch_id'] = '7551000001'
        params['nonce_str'] = Util.generate_nonce()  # 随机串 必填

        out_trade_no = self.get_argument('out_trade_no')
        if (out_trade_no):
            params['out_trade_no'] = out_trade_no  # 商户订单号

        transaction_id = self.get_argument('transaction_id')
        if (transaction_id):
            params['transaction_id'] = transaction_id  # 威富通订单号(与商户订单号必填1个)

        # params['version'] = '2.0'     #版本号 默认值2.0 选填
        # params['charset'] = 'UTF-8' #字符集，默认值UTF-8  选填
        # params['sign_type'] = 'MD5' #签名方式，默认MD5， 选填
        # params['sign_agentno'] = ''   #授权渠道编号 如果不为空，则用授权渠道的秘钥进行签名
        # sign = Util.get_sign(params,"58bb7db599afc86ea7f7b262c32ff42f");
        sign = Util.get_sign(params, '9d101c97133837e13dde2d32a5054abb')
        params['sign'] = sign
        data = Util.dict_to_xml(params)
        print(data)
        BASE_URL = 'https://pay.swiftpass.cn/pay/gateway'
        r = requests.post(BASE_URL, data)
        if r.status_code == 200:
            res = r.text
            print('res==', res)
            dic = Util.xml_to_dict(res)
            if ('0' != dic['status']):
                self.write(dic['message'])
            else:
                self.render('orderQueryResult.html', title='订单查询结果', dic=dic)


""" 退款 """


class TradeRefundHandler(tornado.web.RequestHandler):
    def post(self):
        print("data=", self.request.body)
        params = {}
        params['service'] = 'unified.trade.refund'  # 订单查询接口 必填
        params['mch_id'] = '7551000001'  # 商户号  必填
        params['op_user_id'] = '7551000001'  # 操作员
        params['nonce_str'] = Util.generate_nonce()  # 随机串 必填

        out_trade_no = self.get_argument('out_trade_no')
        if (out_trade_no):
            params['out_trade_no'] = out_trade_no  # 商户订单号

        transaction_id = self.get_argument('out_transaction_id')
        if (transaction_id):
            params['transaction_id'] = transaction_id  # 微信订单号(与商户订单号必填1个)

        params['out_refund_no'] = self.get_argument('out_refund_no')  # 商户退款单号 必填
        params['total_fee'] = self.get_argument('total_fee')
        params['refund_fee'] = self.get_argument('refund_fee')
        sign = Util.get_sign(params, "9d101c97133837e13dde2d32a5054abb");
        params['sign'] = sign
        data = Util.dict_to_xml(params)

        print(data)
        BASE_URL = 'https://pay.swiftpass.cn/pay/gateway'
        r = requests.post(BASE_URL, data)
        if r.status_code == 200:
            res = r.text
            print('res==', res)
            dic = Util.xml_to_dict(res)
            if ('0' != dic['status']):
                self.write(dic['message'])
            else:
                self.render('orderQueryResult.html', title='退款结果页面', dic=dic)


""" 退款查询 """


class RefundQueryHandler(tornado.web.RequestHandler):
    def post(self):
        print("data=", self.request.body)
        params = {}
        params['service'] = 'unified.trade.refundquery'  # 订单查询接口 必填
        params['mch_id'] = '7551000001'  # 商户号  必填
        params['nonce_str'] = Util.generate_nonce()  # 随机串 必填

        out_trade_no = self.get_argument('out_trade_no')
        if (out_trade_no):
            params['out_trade_no'] = out_trade_no  # 商户订单号

        transaction_id = self.get_argument('out_transaction_id')
        if (transaction_id):
            params['transaction_id'] = transaction_id  # 微信订单号

        out_refund_no = self.get_argument('out_refund_no')
        if (out_refund_no):
            params['out_refund_no'] = out_refund_no  # 商户退款单号

        refund_id = self.get_argument('refund_id')
        if (refund_id):
            params['refund_id'] = refund_id  # 微信退款单号

        # params['version'] = '2.0'     #版本号 默认值2.0 选填
        # params['charset'] = 'UTF-8' #字符集，默认值UTF-8  选填
        # params['sign_type'] = 'MD5' #签名方式，默认MD5， 选填
        # params['sign_agentno'] = ''   #授权渠道编号 如果不为空，则用授权渠道的秘钥进行签名
        sign = Util.get_sign(params, "9d101c97133837e13dde2d32a5054abb");
        params['sign'] = sign
        data = Util.dict_to_xml(params)
        print(data)

        BASE_URL = 'https://pay.swiftpass.cn/pay/gateway'
        r = requests.post(BASE_URL, data)
        if r.status_code == 200:
            res = r.text
            print('res==', res)
            dic = Util.xml_to_dict(res)
            if ('0' != dic['status']):
                self.write(dic['message'])
            else:
                self.render('orderQueryResult.html', title='退款查询结果', dic=dic)


""" 订单关闭 """


class OrderCloseHandler(tornado.web.RequestHandler):
    def post(self):
        print("data=", self.request.body)
        params = {}
        params['service'] = 'unified.trade.close'  # 订单查询接口 必填
        params['mch_id'] = '7551000001'  # 商户号  必填
        params['nonce_str'] = Util.generate_nonce()  # 随机串 必填
        params['out_trade_no'] = self.get_argument('out_trade_no')  # 商户订单号
        # params['version'] = '2.0'     #版本号 默认值2.0 选填
        # params['charset'] = 'UTF-8' #字符集，默认值UTF-8  选填
        # params['sign_type'] = 'MD5' #签名方式，默认MD5， 选填
        sign = Util.get_sign(params, "9d101c97133837e13dde2d32a5054abb");
        params['sign'] = sign
        data = Util.dict_to_xml(params)
        print(data)
        BASE_URL = 'https://pay.swiftpass.cn/pay/gateway'
        r = requests.post(BASE_URL, data)
        if r.status_code == 200:
            res = r.text
            print('res==', res)
            dic = Util.xml_to_dict(res)
            if ('0' != dic['status']):
                self.write(dic['message'])
            else:
                self.render('orderQueryResult.html', title='订单关闭结果', dic=dic)


class TEST(object):
    """docstring for TEST"""

    def qcodeRequest(self):
        params = {}
        params['service'] = 'pay.weixin.native'
        params['mch_id'] = '7551000001'
        params['notify_url'] = 'http://www.qq.com'
        params['out_trade_no'] = "123abc457"
        params['body'] = u'测试商品'.encode('utf-8')
        params['total_fee'] = 1
        params['mch_create_ip'] = '127.0.0.1'
        params['nonce_str'] = Util.generate_nonce()
        sign = Util.get_sign(params, "9d101c97133837e13dde2d32a5054abb");
        params['sign'] = sign
        data = Util.dict_to_xml(params)
        BASE_URL = 'https://pay.swiftpass.cn/pay/gateway'
        print(data)
        r = requests.post(BASE_URL, data)
        if r.status_code == 200:
            res = r.text
            print("{}".format(res))


if __name__ == '__main__':
    test = TEST()
    test.qcodeRequest()