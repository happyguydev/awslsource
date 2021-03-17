from db.db import dbHelper

class priceDictModel(object):

    @classmethod
    def get(cls, id):
        sql = "select id,price_week,price,price_quarter,price_half_a_year,ip_count,start_time,end_time,member_type,username from price_dict where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_all(cls):
        sql = "select id,price_week,price,price_quarter,price_half_a_year,ip_count,start_time,end_time,member_type,username from price_dict"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from price_dict where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,price_week,price,price_quarter,price_half_a_year,ip_count,start_time,end_time,member_type,username from price_dict where %s order by id desc limit %s, %s" % (
        where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_current_all(cls):
        sql = "select id,price_week,price,price_quarter,price_half_a_year,ip_count,start_time,end_time,member_type,username from price_dict where end_time is null or end_time = 0 order by price "
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def create(cls, price, price_quarter, price_half_a_year, ip_count, member_type, username):
        sql = "insert into price_dict(price,price_quarter,price_half_a_year,ip_count,start_time,member_type,username)values(%s, %s, %s, %s, %s, '%s', '%s')" % (price, price_quarter, price_half_a_year, ip_count, 'unix_timestamp(now())', member_type, username)
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.get(new_id)

    @classmethod
    def create1(cls, price_week, ip_count, member_type, username):
        sql = "insert into price_dict(price_week,ip_count,start_time,member_type,username)values(%s, %s, %s, '%s', '%s')" % (
        price_week, ip_count, 'unix_timestamp(now())', member_type, username)
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.get(new_id)

    @classmethod
    def update(cls, member_type):
        sql = "update price_dict set end_time=%s where member_type='%s' and (end_time is null or end_time=0)" % ('unix_timestamp(now())', member_type)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count