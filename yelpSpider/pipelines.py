# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from yelpSpider.optutil import OptUtil
from yelpSpider.sqlutil import SqlUtil
from yelpSpider.mysqlutil import MysqlHelper
from yelpSpider.dealopt import ServiceCompanyOpt
# from datetime import datetime


class YelpspiderPipeline(object):

    def __init__(self):
        data_path = OptUtil.gen_file()
        self.filename = codecs.open(data_path, "w", encoding="utf-8")
        # self.uid = 100000
        # self.serviceId = 3000000
        # self.categories = [
        #     ('Mortgage Company', '06AM'), ('Home Insurance', '09EC'),
        #     ('Real Estate Broker', '09CY'), ('Home inspectors', '09BJ'),
        #     ('Escrow Services', '18AP'), ('Real Estate Appraiser', '12AE'),
        #     ('Title Insurance Company', '06AH'), ('Legal Services', '16BO'),
        #     ('Pest Control Company', '12CP'), ('Hvac Maintenance', '09BE'),
        #     ('Appliance Repair', '12AD'), ('Republic Service', '12BW/12BV'),
        #     ('Landscaping', '09BV'), ('Construction Company', '09AI'),
        #     ('Curtains Installation Service', '09DJ'), ('Cleaning Company', '09BH'),
        #     ('Carpet Cleaning Service', '12AM'),
        #     ('Roof Repair', '09DH'), ('Mortgage  Broker', '18AM'),
        #     ('Flooring Company', '09AV'), ('Security Systems', '09DI/16CE'),
        #     ('Pool Cleaners', '09CH'), ('Tree Cutting Service', '09DS'),
        #     ('Moving Company', '09CA'), ('Interior Design', '09BQ/12DN'),
        #     ('Locksmiths', '09BT'), ('Electricians', '09AP/12AZ'),
        #     ('Garage Door Repair', '09AY'), ('Decks & Railing/ Fence', '09AL'),
        #     ('Awnings', '12AG'), ('Water Purifying Equipment Company', '09DZ'),
        #     ('Gutter Services', '09BC'), ('Childproofing', '09AG')
        # ]

    '''
        1. 用户先入库
        2.再入库t_service_company
    '''
    def process_item(self, item, spider):
        phone = item['phone']
        longitude = item['longitude']
        latitude = item['latitude']
        if item['address'] and phone and longitude and latitude:
            item['date_time'] = SqlUtil.gen_current_time()
            user_sql, user_params = ServiceCompanyOpt.get_sql_info_by_code(item, "service_crawl_data")
            try:
                user_count = MysqlHelper.insert(user_sql, user_params)
                print("act rows: %d" % user_count)
            except Exception as e:
                print(e)
            content = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.filename.write(content)
        return item

    def close_spider(self, spider):
        self.filename.close()

    def __init__(self):
        # pass
        self.filename = codecs.open(OptUtil.gen_file(), 'w', encoding="utf-8")


