from db.db import dbHelper
import binascii
import os
class SystemAdminTokenModel(object):
    @classmethod
    def create(cls, user_id, username):
        result = binascii.b2a_base64(os.urandom(24))[:-1]
        token = str(result, encoding="utf-8")
        sql = "insert into system_admin_token(system_admin_id,system_admin_username, token, start_date,end_date)values(%s, '%s', '%s', %s,%s)" % (
        user_id, username, token, 'unix_timestamp(now())', 0)
        new_id = dbHelper.executeInsertSql(sql)
        return token

    @classmethod
    def update(cls, token):
        sql = "update system_admin_token set end_date=%s where token='%s'" % ('unix_timestamp(now())', token)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count

    @classmethod
    def getSystemAdminToken(cls, token):
        sql = "select id,system_admin_id,system_admin_username,token,start_date,end_date from system_admin_token where token='%s'" % token
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get(cls, id):
        sql = "select id,system_admin_id,system_admin_username,token,start_date,end_date from system_admin_token where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from system_admin_token where "+where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result



    @classmethod
    def get_all(cls):
        sql = "select username,pwd,email,registe_date from user"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,username,email,registe_date from user where %s order by id limit %s, %s" % (where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result




    @classmethod
    def update_pwd(cls, id, pwd):
        sql = "update user set pwd=%s where id=%s" % (pwd, id)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count

    @classmethod
    def update_email(cls, id, email):
        sql = "update user set email=%s where id=%s" % (email, id)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count

    @classmethod
    def delete(cls, id):
        sql = "delete from user where id= %s" % (id,)
        row_count = dbHelper.executeDeleteSql(sql)
        return row_count