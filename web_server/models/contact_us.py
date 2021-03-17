from db.db import dbHelper

class contactUsModel(object):

    @classmethod
    def get(cls):
        sql = "select id,phone,tel_kefu,email,linker from contact_us order by id desc limit 1"
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def getById(cls, id):
        sql = "select id,phone,tel_kefu,email,linker from contact_us where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def update(cls, phone,tel_kefu,email,linker, id):
        sql = "update contact_us set phone='%s',tel_kefu='%s',email='%s',linker='%s' where id=%s" % (
            phone,tel_kefu,email,linker, id)
        print(sql)
        new_id = dbHelper.executeUpdateSql(sql)
        return cls.getById(id)

