from db.db import dbHelper

class ipAgentPoolModel(object):

    @classmethod
    def get(cls, id):
        sql = "select id,url_web,url_api,country,area,oper_time,username,switch,agent_protocol from ip_agent_pool where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result
    @classmethod
    def get_all(cls):
        sql = "select id,url_web,url_api,country,area,oper_time,username,switch,agent_protocol from ip_agent_pool"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_random(cls, where):
        sql = "SELECT id,url_web,url_api,country,area,oper_time,username,switch,agent_protocol FROM `ip_agent_pool` where  %s ORDER BY rand() LIMIT 1;" % (where,)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from ip_agent_pool where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,url_web,url_api,country,area,oper_time,username,switch,agent_protocol from ip_agent_pool where %s order by id desc limit %s, %s" % (
            where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def create(cls, url_web, url_api, country, area, username, agent_protocol):
        sql = "insert into ip_agent_pool(url_web,url_api,country,area,oper_time,username,switch,agent_protocol)values('%s','%s','%s','%s',%s,'%s',%s,'%s')" % (url_web, url_api, country, area, 'unix_timestamp(now())', username, 1, agent_protocol)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.get(new_id)

    @classmethod
    def delete(cls, id):
        sql = "delete from ip_agent_pool where id= %s" % (id,)
        row_count = dbHelper.executeDeleteSql(sql)
        return row_count