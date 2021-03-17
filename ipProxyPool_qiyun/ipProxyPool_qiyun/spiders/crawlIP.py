import scrapy
import json
from ipProxyPool_qiyun.items import IpproxypoolQiyunItem

class CrawlipSpider(scrapy.Spider):
    name = 'crawlIP'
    allowed_domains = ['dev.qydailiip.com']
    start_urls = [
        'http://dev.qydailiip.com/api/?apikey=50f7fdbe16e0038821d1f562786212cd7d7b7600&num=30&type=json&line=win&proxy_type=putong&sort=4&model=all&protocol=http&address=&kill_address=&port=&kill_port=&today=true&abroad=1&isp=&anonymity=']

    def parse(self, response):
        respon = response.text
        for im in eval(respon):
            if im is not "":
                item = IpproxypoolQiyunItem()
                item["ip"] = im.split(':')[0]
                item["port"] = im.split(':')[1]
                yield item

        # resp = json.loads(respon)
        # print(resp)
        # if resp['code'] == 0:
        #     for itm in resp['data']:
        #         item = IpproxypoolQiyunItem()
        #         item["ip"] = itm['ip']
        #         item["port"] = itm['port']
        #         yield item

        # for im in eval(respon):
        #     item = IpproxypoolQiyunItem()
        #     item["ip"] = im['ip']
        #     item["port"] = im['port']
        #     yield item