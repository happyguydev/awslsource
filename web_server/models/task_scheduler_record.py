from db.db import dbHelper

class taskSchedulerRecordModel(object):

    @classmethod
    def get(cls, id):
        sql = "select id,task_id,task_uuid,start_time,start_type,end_time,end_type from task_scheduler_record where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def getByTaskid(cls, task_id):
        sql = "select id,task_id,task_uuid,start_time,start_type,end_time,end_type from task_scheduler_record where task_id=%s order by id desc" % (task_id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_all(cls):
        sql = "select id,task_id,task_uuid,start_time,start_type,end_time,end_type from task_scheduler_record"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result



    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from task_scheduler_record where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,task_id,task_uuid,start_time,start_type,end_time,end_type from task_scheduler_record where %s order by id desc limit %s, %s" % (
            where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def create(cls, task_id, task_uuid, start_type):
        sql = "insert into task_scheduler_record(task_id,task_uuid,start_time,start_type)values(%s,'%s',%s,%s)" % (task_id, task_uuid, "unix_timestamp(now())", start_type)
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.get(new_id)

    @classmethod
    def update(cls, task_id, end_type):
        sql = "update task_scheduler_record set end_time=%s, end_type=%s where task_id=%s and end_time is null" % (
        'unix_timestamp(now())', end_type, task_id)
        print(sql)
        row_count = dbHelper.executeUpdateSql(sql)
        return row_count