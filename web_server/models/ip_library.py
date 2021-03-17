from db.db import dbHelper

class ipLibraryModel(object):

    @classmethod
    def get_all(cls):
        sql = "select id,ip,port,expire_time,country,city,isp,outip,area,switch,agent_protocol from ip_library"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def getById(cls, id):
        sql = "select id,ip,port,expire_time,country,city,isp,outip,area,switch,agent_protocol from ip_library where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get(cls, where):
        sql = "SELECT id,ip,port,expire_time,country,city,isp,outip,area,switch,agent_protocol FROM `ip_library` where %s ORDER BY rand() LIMIT 1;" % (where,)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def create(cls, ip, port, country, city, isp, outip, area, switch, agent_protocol):
        sql = "insert into ip_library(ip,port,country,city,isp,outip,area,switch,agent_protocol)values('%s','%s','%s','%s','%s','%s','%s',%s,'%s')" % (ip, port, country, city, isp, outip, area, switch, agent_protocol)
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.getById(new_id)

    @classmethod
    def delete(cls, id):
        sql = "delete from ip_library where id= %s" % (id,)
        row_count = dbHelper.executeDeleteSql(sql)
        return row_count
