import pymysql.cursors

mysqlConfig = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'db': 'ip_library',
            'charset': 'utf8'
        }

class dbHelper:
    def executeQuerySql(sql, operType):
        conn = pymysql.connect(**mysqlConfig)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        row_count = cursor.execute(sql)
        print('受影响的行数'+str(row_count))
        if operType == 'one':
            result = cursor.fetchone()
        elif operType == 'many':
            result = cursor.fetchmany(4)
        else:
            result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def executeInsertSql(sql):
        conn = pymysql.connect(**mysqlConfig)
        cursor = conn.cursor()
        cursor.execute(sql)
        new_id = cursor.lastrowid
        print(new_id)
        conn.commit()
        cursor.close()
        conn.close()
        return new_id

    def mysql_escape_string(value):
        conn = pymysql.connect(**mysqlConfig)
        return conn.escape(value)

    def executeUpdateSql(sql):
        conn = pymysql.connect(**mysqlConfig)
        cursor = conn.cursor()
        row_count = cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return row_count

    def executeDeleteSql(sql):
        conn = pymysql.connect(**mysqlConfig)
        cursor = conn.cursor()
        row_count = cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return row_count


