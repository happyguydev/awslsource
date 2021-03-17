# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time
import pymysql
import uuid

class IpproxypoolPipeline:
    # 初始化的操作，这里我们做本地化直接写成文件，所以初始化文件对象
    def __init__(self):
        dbparams = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'ip_library',
            'charset': 'utf8'
        }

        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        oper_time = int(time.time())
        data = (str(uuid.uuid1()), item['ip'], item['port'], oper_time)
        self.cursor.execute(self.sql, data)
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into ip_library (id,ip,port,oper_time)
                values (%s,%s,%s,%s)
                """
            return self._sql
        return self._sql

