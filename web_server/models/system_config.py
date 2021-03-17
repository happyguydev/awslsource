from db.db import dbHelper

class systemConfigModel(object):

    @classmethod
    def getSystemConfigByKey(cls, key):
        sql = "select id,`key`,value,options from `system_config` where `key`='%s'" % (key,)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def setSystemConfigByKey(cls, key, value):
        sql = "update `system_config` set value='%s' where `key`='%s'" % (value, key)
        print(sql)
        result = dbHelper.executeUpdateSql(sql)
        return result