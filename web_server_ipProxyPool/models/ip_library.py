from db.db import dbHelper


class ip_libraryModel(object):

    @classmethod
    def getTopLimit(cls, index):
        sql = "select id,ip,port,oper_time,last_check_oper_time from ip_library order by oper_time,id limit %s,1" % (index,)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def getByLastCheckOperTime(cls):
        sql = "select id,ip,port,oper_time,last_check_oper_time from ip_library order by last_check_oper_time desc limit 1"
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def getByIp(cls, ip):
        sql = "select id,ip,port,oper_time,last_check_oper_time from ip_library where ip='%s'  limit 1" % (ip,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def update(cls, id):
        sql = "update ip_library set last_check_oper_time=%s where id='%s'" % ('unix_timestamp(now())', id)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count

    @classmethod
    def delete(cls, id):
        sql = "delete from ip_library where id= '%s'" % (id,)
        row_count = dbHelper.executeDeleteSql(sql)
        return row_count



