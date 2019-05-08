#! /usr/bin/env python  
# -*- coding:utf-8 -*-
from datetime import datetime


class SqlUtil(object):

    @classmethod
    def gen_sql_sql(self, tab_name, _fields):
        """
        用来生成sql字符串语句
        :param _fields:
        :return:
        """
        fields = ",".join(_fields)
        placeholders = []
        for i in range(0, len(_fields)):
            placeholders.append("%s")
        placeholder_str = ",".join(placeholders)
        sql = "insert into %s (%s) values (%s)" % (tab_name, fields, placeholder_str)
        return sql

    @classmethod
    def gen_current_time(self):
        today = datetime.now()
        current_time = '{}-{}-{} {}:{}:{}'.format(today.year, today.month, today.day, today.hour, today.minute,
                                                  today.second)
        return current_time