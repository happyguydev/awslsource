from db.db import dbHelper

class userAgentModel(object):

    @classmethod
    def get_all(cls):
        sql = "select id,system,browser,content from user_agent"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get(cls, where):
        sql = "SELECT * FROM `user_agent` AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM `user_agent` where %s)-(SELECT MIN(id) FROM `user_agent` where %s))+(SELECT MIN(id) FROM `user_agent` where %s)) AS id) AS t2 WHERE t1.id >= t2.id ORDER BY t1.id LIMIT 1;" % (where, where, where)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def create(cls, system, browser, content):
        sql = "insert into user_agent(system,browser,content)values(%s)" % (system, browser, content)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.get(new_id)