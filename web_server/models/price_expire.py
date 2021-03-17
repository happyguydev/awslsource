from db.db import dbHelper

class priceExpireModel(object):

    @classmethod
    def get(cls, id):
        sql = "select id,order_id,expire_time from price_expire where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def getByOrderId(cls, order_id):
        sql = "select id,order_id,expire_time from price_expire where order_id=%s" % (order_id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_all(cls):
        sql = "select id,order_id,expire_time from price_expire"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_current(cls, user_id, username):
        sql = "select price_expire.id,order_id,expire_time,order_number,user_id,username,price_id,pay_price,pay_way,is_pay,pay_time,status from price_expire left join `order` on price_expire.order_id = `order`.id where user_id=%s and username='%s' order by expire_time desc" % (user_id, username)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from price_expire left join `order` on price_expire.order_id = `order`.id where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select price_expire.id,order_id,expire_time,order_number,trade_no,user_id,username,price_id,pay_price,pay_way,is_pay,pay_time,status from price_expire left join `order` on price_expire.order_id = `order`.id where %s order by id desc limit %s, %s" % (
            where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def create(cls, order_id, expire_time):
        sql = "insert into price_expire(order_id, expire_time)values(%s, %s)" % (order_id, expire_time)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.get(new_id)