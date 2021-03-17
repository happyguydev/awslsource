from db.db import dbHelper


class newsModel(object):

    @classmethod
    def get_all(cls):
        sql = "select id,oper_type,title,summary,content,oper_time,username from news"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def getById(cls, id):
        sql = "select id,oper_type,title,summary,content,oper_time,username from news where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from `news` where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,oper_type,title,summary,content,oper_time,username from `news` where %s order by id desc limit %s, %s" % (
            where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def create(cls, oper_type, title, summary, content, username):
        new_content = dbHelper.mysql_escape_string(content)
        sql = "insert into news(oper_type,title,summary,content,oper_time,username)values('%s','%s','%s',%s,%s,'%s')" % (
        oper_type, title, summary, new_content, 'unix_timestamp(now())', username)
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.getById(new_id)

    @classmethod
    def update(cls, oper_type, title, summary, content, username, id):
        new_content = dbHelper.mysql_escape_string(content)
        sql = "update news set oper_type='%s',title='%s',summary='%s',content=%s,oper_time=%s,username='%s' where id=%s" % (
            oper_type, title, summary, new_content, 'unix_timestamp(now())', username, id)
        print(sql)
        new_id = dbHelper.executeUpdateSql(sql)
        return cls.getById(id)

    @classmethod
    def delete(cls, id):
        sql = "delete from news where id= %s" % (id,)
        row_count = dbHelper.executeDeleteSql(sql)
        return row_count
