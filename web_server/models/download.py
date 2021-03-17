from db.db import dbHelper

class downloadModel(object):

    @classmethod
    def get_all(cls):
        sql = "select id,file_name,file_url,version,size,oper_time,username,desp,version_type from download"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def getById(cls, id):
        sql = "select id,file_name,file_url,version,size,oper_time,username,desp,version_type from download where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_new_chinese(cls):
        sql = "select id,file_name,file_url,version,size,oper_time,username,desp,version_type from download where version_type='中文版' order by id desc limit 1"
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_new_english(cls):
        sql = "select id,file_name,file_url,version,size,oper_time,username,desp,version_type from download where version_type='英文版' order by id desc limit 1"
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_version(self, version_type):
        sql = "select id,file_name,file_url,version,size,oper_time,username,desp,version_type from download where version_type='" + version_type + "' order by id desc limit 1"
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from `download` where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,file_name,file_url,version,size,oper_time,username,desp,version_type from `download` where %s order by id desc limit %s, %s" % (
            where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def create(cls, file_name, file_url, version, size, username, desp, version_type):
        new_file_url = dbHelper.mysql_escape_string(file_url)
        new_desp = dbHelper.mysql_escape_string(desp)
        sql = "insert into download(file_name,file_url,version,size,oper_time,username,desp,version_type)values('%s',%s,'%s','%s',%s,'%s',%s,'%s')" % (file_name, new_file_url, version, size, 'unix_timestamp(now())', username, new_desp, version_type)
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.getById(new_id)

    @classmethod
    def update(cls, file_name, file_url, version, size, username, desp, version_type, id):
        new_file_url = dbHelper.mysql_escape_string(file_url)
        new_desp = dbHelper.mysql_escape_string(desp)
        sql = "update download set file_name='%s',file_url='%s',version='%s',size='%s',oper_time=%s,username='%s',desp=%s,version_type='%s' where id=%s" % (
            file_name, new_file_url, version, size, 'unix_timestamp(now())', username, new_desp, version_type, id)
        print(sql)
        new_id = dbHelper.executeUpdateSql(sql)
        return cls.getById(id)

    @classmethod
    def delete(cls, id):
        sql = "delete from download where id= %s" % (id,)
        row_count = dbHelper.executeDeleteSql(sql)
        return row_count
