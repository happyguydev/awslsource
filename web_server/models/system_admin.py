from db.db import dbHelper

class systemAdminModel(object):

    @classmethod
    def getById(cls, id):
        sql = "select id,username,pwd,registe_date from system_admin where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def getByUsername(cls, username):
        sql = "select id,username,pwd,registe_date from system_admin where username='%s'" % (username,)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from system_admin where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def getAdmin(cls, username, pwd):
        sql = "select id,username,pwd,registe_date from system_admin where username='%s' and pwd='%s'" % (username, pwd)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_all(cls):
        sql = "select id,username,pwd,registe_date from system_admin"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,username,registe_date from system_admin where %s order by id desc limit %s, %s" % (
        where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def create(cls, username, pwd):
        sql = "insert into system_admin(username, pwd,registe_date)values('%s', '%s',%s)" % (username, pwd, 'unix_timestamp(now())')
        new_id = dbHelper.executeInsertSql(sql)
        return cls.getById(new_id)

    @classmethod
    def update_pwd(cls, id, pwd):
        sql = "update system_admin set pwd='%s' where id=%s" % (pwd, id)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count

    @classmethod
    def delete(cls, id):
        sql = "delete from system_admin where id= %s" % (id,)
        row_count = dbHelper.executeDeleteSql(sql)
        return row_count
    
