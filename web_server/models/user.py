from db.db import dbHelper
class UserModel(object):

    @classmethod
    def get(cls, id):
        sql = "select id,username,pwd,email,registe_date from user where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from user where "+where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def getUser(cls, username, pwd):
        sql = "select id,username,pwd,email,registe_date from user where username='%s' and pwd='%s'" % (username, pwd)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_all(cls):
        sql = "select id,username,pwd,email,registe_date from user"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,username,email,registe_date from user where %s order by id desc limit %s, %s" % (where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def create(cls, username, pwd, email):
        sql = "insert into user(username, pwd, email, registe_date)values('%s', '%s', '%s', %s)" % (username, pwd, email, 'unix_timestamp(now())')
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.get(new_id)

    @classmethod
    def update_pwd(cls, id, pwd):
        sql = "update user set pwd='%s' where id=%s" % (pwd, id)
        print(sql)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count

    @classmethod
    def update_email(cls, id, email):
        sql = "update user set email='%s' where id=%s" % (email, id)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count

    @classmethod
    def delete(cls, id):
        sql = "delete from user where id= %s" % (id,)
        row_count = dbHelper.executeDeleteSql(sql)
        return row_count

    @classmethod
    def getByUsername(cls, username):
        sql = "select id,username,pwd,email,registe_date from user where username='%s'" % (username,)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result
