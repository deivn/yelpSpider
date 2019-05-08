#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import math
import time
from yelpSpider.sqlutil import SqlUtil


class ServiceCompanyOpt(object):

    def __init__(self):
        pass

    @staticmethod
    def get_sql_info_by_code(item, tab_name, code, *origin_req):
        """
        功能：根据表名，字段列表，生成sql语句
        :param tab_name: 表名
        :param item: 网页爬取的信息
        :return:
        """
        _fields = ServiceCompanyOpt().get_fields_by_code(code)
        sql = SqlUtil.gen_sql_sql(tab_name, _fields)
        params = ServiceCompanyOpt().get_params_by_user_item(item, code, *origin_req)
        return (sql, params)

    def get_fields_by_code(self, code):
        """
        功能：根据code生成对应表的字段列表
        :param code: 字段标识code =1（用户表 t_user） 2 服务商表t_service_company
        :return:
        """
        _fields = []
        if code == 1:
            _fields = [
                'id', 'phone', 'email', 'password', 'nickname', 'firstname', 'middlename',
                'lastname', 'sex', 'orgin', 'head_url', 'status', 'type', 'email_status',
                'state_id', 'city_id', 'address', 'zip', 'hxusername', 'phone_area_code_id',
                'create_time', 'company_name', 'thirdPartyToken'
            ]
        elif code == 2:
            _fields = [
                'id', 'company', 'address', 'state_id', 'city_id', 'content',
                'img_url', 'bgi', 'logo', 'contacts_name', 'email', 'company_code', 'fk_customer_id',
                'create_time', 'shelf_status', 'check_status', 'business_content', 'longitude', 'latitude', 'sort',
                'count_view', 'heat', 'count_share', 'phone', 'websiteurl', 'category']
        return _fields

    def get_params_by_user_item(self, item, code, *origin_req):
        """
        功能：根据用户item生成数据库表的参数列表
        :param item:
        :param code:1用户表t_user参数 2服务商表 t_service_company
        :param id: primary key
        :param ids: 房源数据里要用到各个要关联的外键ID
        :return:
        """
        params = []
        create_time = math.floor(time.time())
        if code == 1:
            # 当前时间 yyyy-MM-dd HH:mm:ss
            current_time = SqlUtil.gen_current_time()
            params = [
                item['uid'], item['phone'], ' ', ' ', ' ', ' ', ' ', ' ',
                3, 1, ' ', 1, 1, 1, item['state_id'], item['city_id'],
                item['address'], item['zip'], ' ', ' ', current_time, item['company'], ' '
            ]
        elif code == 2:
            params = [
                item['service_id'], item['company'], item['address'], item['state_id'], item['city_id'],
                item['content'], item['img_url'], ' ', item['logo'], ' ', ' ', ' ', item['uid'], create_time,
                1, 2, item['business_content'], item['longitude'], item['latitude'], 1, 0, 0, 0, item['phone'], item['websiteurl'], item['category']
            ]
        return params
