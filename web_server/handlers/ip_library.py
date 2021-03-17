import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.ip_library import ipLibraryModel
import requests


class IpLibraryHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        where = self.get_argument("where")
        ipLibrary = ipLibraryModel.get(where)
        self.write(json_encode(ipLibrary))

    def post(self):
        ip = self.get_argument("ip")
        port = self.get_argument("port")
        country = self.get_argument("country")
        city = self.get_argument("city")
        isp = self.get_argument("isp")
        outip = self.get_argument("outip")
        area = self.get_argument("area")
        switch = self.get_argument("switch")
        agent_protocol = self.get_argument("agent_protocol")
        result = ipLibraryModel.create(ip, port, country, city, isp, outip, area, switch, agent_protocol)
        ret = {'code': 0, "msg": "success!", 'data': result}
        self.write(json_encode(ret))

    def delete(self):
        id = self.get_argument("id")
        ret = ipLibraryModel.delete(int(id))
        self.write(json_encode(ret))

class IpLibraryTestHandler(BaseHandler,tornado.web.RequestHandler):
    def get(self):
        url = 'http://http.tiqu.alicdns.com/getip3?num=3&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
        result = requests.get(url)
        trans = result.json()
        print(trans)
        for item in trans['data']:
            print(item['ip'])
            print(item['port'])
        # print(trans['data'][0]["ip"])