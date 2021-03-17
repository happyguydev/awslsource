import tornado.web
from tornado.escape import json_encode
from base import BaseHandler
from models.download import downloadModel
from models.system_admin_token import SystemAdminTokenModel
from models.user_token import UserTokenModel
import time
import os
import decimal
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)
class DownloadHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            id = self.get_argument("id")
            data = downloadModel.getById(int(id))
            if data:
                j = json.dumps(data, cls=DecimalEncoder)
                ret = {'code': 0, "msg": "success!", 'data': json.loads(j)}
            else:
                ret = {'code': 1, "msg": "fail!"}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))

    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            file_url = self.get_argument("file_url")
            file_name = self.get_argument("file_name")
            version = self.get_argument("version")
            size = self.get_argument("size")
            desp = self.get_argument("desp")
            version_type = self.get_argument("version_type")
            result = downloadModel.create(file_name, file_url, version, size, systemAdmin['system_admin_username'], desp, version_type)
            if result:
                j = json.dumps(result, cls=DecimalEncoder)
                ret = {"code": 0, "msg": "success!", 'data': json.loads(j)}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))

    def put(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            file_url = self.get_argument("file_url")
            file_name = self.get_argument("file_name")
            version = self.get_argument("version")
            size = self.get_argument("size")
            desp = self.get_argument("desp")
            version_type = self.get_argument("version_type")
            id = self.get_argument("id")
            result = downloadModel.update(file_name, file_url, version, size, systemAdmin['system_admin_username'], desp, version_type, id)
            if result:
                j = json.dumps(result, cls=DecimalEncoder)
                ret = {"code": 0, "msg": "success!", 'data': json.loads(j)}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))

    def delete(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            id = self.get_argument("id")
            result = downloadModel.delete(int(id))
            if result > 0:
                ret = {'code': 0, 'msg': 'success'}
            else:
                ret = {'code': 2, 'msg': 'fail'}
        else:
            ret = {'code': 1, 'msg': 'fail, user token not found'}
        self.write(json_encode(ret))

class DownloadListHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        token = self.get_argument("token")
        systemAdmin = SystemAdminTokenModel.getSystemAdminToken(token)
        if systemAdmin:
            page_number = self.get_argument("page")
            page_count = self.get_argument("limit")
            start_date = self.get_argument("start")
            end_date = self.get_argument("end")
            version_type = self.get_argument("version_type")
            file_name = self.get_argument("file_name")
            username = self.get_argument("username")
            where = ' 1=1 '
            if start_date and end_date:
                start_date = start_date+' 00:00:00'
                sss = time.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                starttimeStamp = int(time.mktime(sss))
                end_date = end_date + ' 00:00:00'
                sss1 = time.strptime(end_date, "%Y-%m-%d %H:%M:%S")
                endtimeStamp = int(time.mktime(sss1))
                where += " and oper_time > %s and oper_time < %s" % (starttimeStamp, endtimeStamp)
            if version_type != '' and version_type != '版本类型':
                where += " and version_type = '" + version_type + "' "
            if file_name:
                where += " and file_name like '%" + file_name + "%'"
            if username:
                where += " and username like '%" + username + "%'"
            data = downloadModel.get_page(int(page_number)-1, int(page_count), where)
            count = downloadModel.get_count(where)
            j = json.dumps(data, cls=DecimalEncoder)
            ret = {"code": 0, "msg": "success", "count": count['count'], "data": json.loads(j)}
        else:
            ret = {"code": 1, 'msg': "fail,system admin token not found"}
        self.write(json_encode(ret))

class uploadFileHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        bl = False
        file_metas = self.request.files["file"]  # 获取上传文件信息
        for meta in file_metas:  # 循环文件信息
            file_name = meta['filename']  # 获取文件的名称
            import os  # 引入os路径处理模块
            with open(os.path.join('upload', 'file', file_name), 'wb') as up:  # os拼接文件保存路径，以字节码模式打开
                up.write(meta['body'])  # 将文件写入到保存路径目录
                bl = True
        if bl:
            ret = {'code': 0, "msg": "success!", 'data': {'file_path': os.path.join('upload', 'file', file_name), 'title': file_name}}
        else:
            ret = {'code': 1, "msg": "fail!"}
        self.write(json_encode(ret)) # 将上传好的路径返回

class uploadImageHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        print(self.request.host_name)
        print(self.request.host)
        bl = False
        file_metas = self.request.files["file"]  # 获取上传文件信息
        for meta in file_metas:  # 循环文件信息
            file_name = meta['filename']  # 获取文件的名称
            import os  # 引入os路径处理模块
            with open(os.path.join('upload', 'img', file_name), 'wb') as up:  # os拼接文件保存路径，以字节码模式打开
                up.write(meta['body'])  # 将文件写入到保存路径目录
                bl = True
        if bl:
            ret = {'code': 0, "msg": "success!", 'data': {'src': 'http:\\\\' + self.request.host+'\\' + os.path.join('upload', 'img', file_name), 'title': file_name}}
        else:
            ret = {'code': 1, "msg": "fail!"}
        print(json_encode(ret))
        self.write(json_encode(ret)) # 将上传好的路径返回

class versionHandler(BaseHandler, tornado.web.RequestHandler):
    def post(self):
        version_type = self.get_argument("version_type")
        data = downloadModel.get_version(version_type)
        if len(data) > 0:
            j = json.dumps(data, cls=DecimalEncoder)
            ret = {"code": 0, "msg": "success", "data": json.loads(j)}
        else:
            ret = {"code": 1, 'msg': "fail"}
        self.write(json_encode(ret))


class DownloadListUserHandler(BaseHandler, tornado.web.RequestHandler):
    def get(self):
        data_chinese = downloadModel.get_new_chinese()
        data_english = downloadModel.get_new_english()
        datalist = [data_chinese, data_english]
        if datalist:
            j = json.dumps(datalist, cls=DecimalEncoder)
            ret = {"code": 0, "msg": "success", "data": json.loads(j)}
        else:
            ret = {"code": 1, 'msg': "fail"}
        self.write(json_encode(ret))