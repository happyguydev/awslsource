import scrapy
import json
from ipProxyPool.items import IpproxypoolItem

class CrawlipSpider(scrapy.Spider):
    name = "crawlIP"
    # allowed_domains = ["h.feizhuip.com"]
    # allowed_domains = ['dev.qydailiip.com']
    allowed_domains = ['api10.uuhttp.com']
    # start_urls = ['http://120.79.85.144/index.php/api/entry?method=proxyServer.tiqu_api_url&packid=2&fa=0&fetch_key=&groupid=0&qty=60&time=1&port=1&format=json&ss=5&css=&ipport=1&et=1&pi=1&co=1&pro=&city=&dt=1&usertype=22']
    # start_urls = ['http://dev.qydailiip.com/api/?apikey=50f7fdbe16e0038821d1f562786212cd7d7b7600&num=60&type=json&line=win&proxy_type=putong&sort=4&model=all&protocol=http&address=&kill_address=&port=&kill_port=&today=true&abroad=1&isp=&anonymity=']
    start_urls = ['http://api10.uuhttp.com:39010/index/api/return_data?mode=http&count=30&b_time=180&e_time=300&return_type=2&line_break=1&ttl=1&secert=MTg2ODgxODAwMTY6YzE0OTk4MGZhZmIzZDY0YTNhMDEzYWM3ZGRmMjkxYmU=']

    def parse(self, response):
        respon = response.text
        # for im in eval(respon):
        #     if im is not "":
        #         item = IpproxypoolItem()
        #         item["ip"] = im.split(':')[0]
        #         item["port"] = im.split(':')[1]
        #         yield item

        # if resp['code'] == 0:
        #     for itm in resp['data']:
        #         item = IpproxypoolItem()
        #         item["ip"] = itm['IP'].split(':')[0]
        #         item["port"] = itm['IP'].split(':')[1]
        #         yield item

        # resp = json.loads(respon)
        # print(resp)
        # if resp['code'] == 0:
        #     for itm in resp['data']:
        #         item = IpproxypoolItem()
        #         item["ip"] = itm['ip']
        #         item["port"] = itm['port']
        #         yield item
        if respon.find('账户到期') == -1:
            for im in eval(respon):
                    item = IpproxypoolItem()
                    item["ip"] = im['ip']
                    item["port"] = im['port']
                    yield item
        else:
            print('账户到期')