#! /usr/bin/env python  
# -*- coding:utf-8 -*-
import math
import time
from yelpSpider.sqlutil import SqlUtil


class ServiceCompanyOpt(object):

    def __init__(self):
        pass

    @staticmethod
    def get_sql_info_by_code(item, tab_name):
        """
        功能：根据表名，字段列表，生成sql语句
        :param tab_name: 表名
        :param item: 网页爬取的信息
        :return:
        """
        _fields = ServiceCompanyOpt().get_fields_by_code()
        sql = SqlUtil.gen_sql_sql(tab_name, _fields)
        params = ServiceCompanyOpt().get_params_by_user_item(item)
        return (sql, params)

    def get_fields_by_code(self):
        """
        功能：根据code生成对应表的字段列表
        :param code: 字段标识code =1（用户表 t_user） 2 服务商表t_service_company
        :return:
        """
        return ['referer', 'detail_page_url', 'logo', 'company', 'address', 'category', 'phone', 'websiteurl', 'img_url', 'content', 'business_content', 'latitude', 'longitude', 'date_time']

    def get_params_by_user_item(self, item):
        """
        功能：根据用户item生成数据库表的参数列表
        :param item:
        :return:
        """
        params = [
            item['referer'], item['detail_page_url'], item['logo'], item['company'],
            item['address'], item['category'], item['phone'],item['websiteurl'],
            item['img_url'], item['content'], item['business_content'], item['latitude'],
            item['longitude'], item['date_time']
        ]
        return params
