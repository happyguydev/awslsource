from db.db import dbHelper

class optimizeConfigurationModel(object):
    @classmethod
    def get(cls, id):
        sql = "select id,target_website,last_page_number,key_word,ip_flow_everyday_selected,ip_flow_fixed_count,ip_flow_random_count_start,ip_flow_random_count_end,search_engines_check,visitor_check,page_random_count_start,page_random_count_end,length_of_stay_first_page_start,length_of_stay_first_page_end,length_of_stay_deep_page_start,length_of_stay_deep_page_end,time_interval,oper_type,user_id,username,commit_time from optimize_configuration where id=%s" % (id,)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_all(cls):
        sql = "select id,target_website,last_page_number,key_word,ip_flow_everyday_selected,ip_flow_fixed_count,ip_flow_random_count_start,ip_flow_random_count_end,search_engines_check,visitor_check,page_random_count_start,page_random_count_end,length_of_stay_first_page_start,length_of_stay_first_page_end,length_of_stay_deep_page_start,length_of_stay_deep_page_end,time_interval,oper_type,user_id,username,commit_time from optimize_configuration"
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_keyword_rank_count(cls):
        sql = "select count(*) as count from (select count(*) from optimize_configuration where oper_type='关键词排名' GROUP BY key_word) as oc_keyword_rank"
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_keyword_rank_page(cls, page_number, page_count):
        sql = "SELECT @rownum := @rownum + 1 AS number, a.key_word, a.count FROM(SELECT key_word, COUNT(*) AS count FROM optimize_configuration where oper_type = '关键词排名' GROUP BY key_word ORDER BY count desc limit %s, %s) AS a, (SELECT @rownum := 0) r" % (page_number * page_count, page_count)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_sourcewebsite_rank_count(cls):
        sql = "select count(*) as count from (select count(*) from optimize_configuration where oper_type='流量' and ISNULL(source_website)=0 and LENGTH(trim(source_website))>0 GROUP BY source_website) as oc_source_website_rank"
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_sourcewebsite_rank_page(cls, page_number, page_count):
        sql = "SELECT @rownum := @rownum + 1 AS number, a.count FROM(SELECT COUNT(*) AS count FROM optimize_configuration where oper_type = '流量' and ISNULL(source_website)=0 and LENGTH(trim(source_website))>0 GROUP BY source_website ORDER BY count desc limit %s, %s) AS a, (SELECT @rownum := 0) r" % (
        page_number * page_count, page_count)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_targetwebsite_rank_count(cls):
        sql = "select count(*) as count from (select count(*) from optimize_configuration GROUP BY target_website) as oc_target_website_rank"
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_targetwebsite_rank_page(cls, page_number, page_count):
        sql = "SELECT @rownum := @rownum + 1 AS number, a.target_website, a.count FROM(SELECT target_website, COUNT(*) AS count FROM optimize_configuration GROUP BY target_website ORDER BY count desc limit %s, %s) AS a, (SELECT @rownum := 0) r" % (
            page_number * page_count, page_count)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result


    @classmethod
    def get_count(cls, where):
        sql = "select count(*) as count from optimize_configuration where " + where
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def get_page(cls, page_number, page_count, where):
        sql = "select id,target_website,last_page_number,key_word,ip_flow_everyday_selected,ip_flow_fixed_count,ip_flow_random_count_start,ip_flow_random_count_end,search_engines_check,visitor_check,page_random_count_start,page_random_count_end,length_of_stay_first_page_start,length_of_stay_first_page_end,length_of_stay_deep_page_start,length_of_stay_deep_page_end,time_interval,oper_type,user_id,username,commit_time from optimize_configuration where %s order by id desc limit %s, %s" % (
            where, page_number * page_count, page_count)
        print(sql)
        result = dbHelper.executeQuerySql(sql, 'all')
        return result

    @classmethod
    def get_current(cls, user_id, username, oper_type):
        sql = "select id,target_website,last_page_number,key_word,ip_flow_everyday_selected,ip_flow_fixed_count,ip_flow_random_count_start,ip_flow_random_count_end,search_engines_check,visitor_check,page_random_count_start,page_random_count_end,length_of_stay_first_page_start,length_of_stay_first_page_end,length_of_stay_deep_page_start,length_of_stay_deep_page_end,time_interval,oper_type,user_id,username,commit_time from optimize_configuration where user_id=%s and username='%s' and oper_type='%s' order by commit_time desc" % (user_id, username, oper_type)
        result = dbHelper.executeQuerySql(sql, 'one')
        return result

    @classmethod
    def create(cls, target_website,last_page_number, key_word, ip_flow_everyday_selected,ip_flow_fixed_count,ip_flow_random_count_start,ip_flow_random_count_end,search_engines_check,visitor_check,page_random_count_start,page_random_count_end,length_of_stay_first_page_start,length_of_stay_first_page_end,length_of_stay_deep_page_start,length_of_stay_deep_page_end,time_interval,oper_type,user_id,username):
        sql = "insert into optimize_configuration(target_website, last_page_number,key_word, ip_flow_everyday_selected, ip_flow_fixed_count, ip_flow_random_count_start, ip_flow_random_count_end, search_engines_check, visitor_check, page_random_count_start, page_random_count_end,length_of_stay_first_page_start,length_of_stay_first_page_end,length_of_stay_deep_page_start,length_of_stay_deep_page_end, time_interval, oper_type, user_id, username, commit_time)values('%s', %s, '%s', %s, %s, %s, %s, '%s', '%s', %s, %s, %s,%s,%s,%s,%s,'%s', %s, '%s', %s)" \
              % (target_website,last_page_number, key_word, ip_flow_everyday_selected, ip_flow_fixed_count,
                 ip_flow_random_count_start, ip_flow_random_count_end, search_engines_check, visitor_check,
                 page_random_count_start, page_random_count_end, length_of_stay_first_page_start,length_of_stay_first_page_end,length_of_stay_deep_page_start,length_of_stay_deep_page_end, time_interval, oper_type, user_id, username,
                 'unix_timestamp(now())')
        print(sql)
        new_id = dbHelper.executeInsertSql(sql)
        return cls.get(new_id)
