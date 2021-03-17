from db.db import dbHelper
import time

class orderModel(object):

    @classmethod
    def getById(cls, id):
        sql = "select id,order_number,user_id,username,price_id,pay_price,pay_way,is_pay,pay_time,status,trade_no from `order` where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def getByOrderNumber(cls, order_number):
        sql = "select id,order_number,user_id,username,price_id,pay_price,pay_way,is_pay,pay_time,status,trade_no from `order` where order_number=%s" % (
        order_number,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from `order` where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_distinct_count(cls, where):
        sql = "select count(distinct(user_id)) as count from `order` where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,order_number,user_id,username,price_id,pay_price,pay_way,is_pay,pay_time,status,trade_no from `order` where %s order by id desc limit %s, %s" % (
            where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_all(cls):
        sql = "select id,order_number,user_id,username,price_id,pay_price,pay_way,is_pay,pay_time,status,trade_no from `order` "
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_order_code(self):
        order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + str(time.time()).replace('.', '')[-7:]
        return order_no

    @classmethod
    def create(cls, order_number, user_id, username, price_id, pay_price, pay_way):
        sql = "insert into `order`(order_number,user_id,username,price_id,pay_price,pay_way,is_pay,pay_time,status)values('%s',%s, '%s', %s, %s, '%s', '%s', %s, '%s')" % (order_number, user_id, username, price_id, pay_price, pay_way, 0, "unix_timestamp(now())", 0)
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.getById(new_id)
    
    @classmethod
    def update(cls, order_number, trade_no):
        sql = "update `order` set trade_no='%s',is_pay=1, status=1 where order_number='%s' and is_pay=0 and status=0" % (trade_no, order_number)
        print(sql)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count