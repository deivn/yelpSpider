# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import codecs
# import json
# import re
# from yelpSpider.optutil import OptUtil
# from yelpSpider.mysqlutil import MysqlHelper
# from yelpSpider.dealopt import ServiceCompanyOpt
from datetime import datetime


class ExamplePipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item

    # def __init__(self):
    #     data_path = OptUtil.gen_file()
    #     self.filename = codecs.open(data_path, "w", encoding="utf-8")
    #     self.uid = 100000
    #     self.serviceId = 3000000
    #     self.categories = [
    #         ('Mortgage Company', '06AM'), ('Home Insurance', '09EC'),
    #         ('Real Estate Broker', '09CY'), ('Home inspectors', '09BJ'),
    #         ('Escrow Services', '18AP'), ('Real Estate Appraiser', '12AE'),
    #         ('Title Insurance Company', '06AH'), ('Legal Services', '16BO'),
    #         ('Pest Control Company', '12CP'), ('Hvac Maintenance', '09BE'),
    #         ('Appliance Repair', '12AD'), ('Republic Service', '12BW/12BV'),
    #         ('Landscaping', '09BV'), ('Construction Company', '09AI'),
    #         ('Curtains Installation Service', '09DJ'), ('Cleaning Company', '09BH'),
    #         ('Carpet Cleaning Service', '12AM'),
    #         ('Roof Repair', '09DH'), ('Mortgage  Broker', '18AM'),
    #         ('Flooring Company', '09AV'), ('Security Systems', '09DI/16CE'),
    #         ('Pool Cleaners', '09CH'), ('Tree Cutting Service', '09DS'),
    #         ('Moving Company', '09CA'), ('Interior Design', '09BQ/12DN'),
    #         ('Locksmiths', '09BT'), ('Electricians', '09AP/12AZ'),
    #         ('Garage Door Repair', '09AY'), ('Decks & Railing/ Fence', '09AL'),
    #         ('Awnings', '12AG'), ('Water Purifying Equipment Company', '09DZ'),
    #         ('Gutter Services', '09BC'), ('Childproofing', '09AG')
    #     ]
    #
    # '''
    #     1. 用户先入库
    #     2.再入库t_service_company
    # '''
    # def process_item(self, item, spider):
    #     address_arr = item['address'].split(',')
    #     phone = item['phone']
    #     longitude = item['longitude']
    #     latitude = item['latitude']
    #     if len(address_arr) == 3 and phone and longitude and latitude:
    #         city_name = address_arr[1].strip()
    #         state_id = address_arr[2].strip().split(' ')
    #         result = MysqlHelper.get_one('select id from t_city where state_id = %s and city_ascii= %s', [state_id[0], city_name])
    #         item['state_id'] = state_id[0]
    #         item['zip'] = state_id[1]
    #         if result:
    #             item['city_id'] = result[0]
    #         else:
    #             # 疑问，没有城市的？
    #             state_id_tmp = MysqlHelper.get_one('select id from t_city where state_id= %s limit 1', [state_id[0]])
    #             item['city_id'] = state_id_tmp[0]
    #         category = item['category']
    #         category_pos = category.find(',')
    #         category_info = ''
    #         if category_pos > 0:
    #             categories = category.split(',')
    #             for category_tmp in categories:
    #                 for k, v in self.categories:
    #                     matchInfo = re.match(category_tmp.lower(), k.lower())
    #                     if matchInfo:
    #                         category_info += v + ', '
    #         else:
    #             category_tmp = category.lower().split(' ')[0]
    #             for k, v in self.categories:
    #                 matchInfo = re.match(category_tmp.lower(), k.lower())
    #                 if matchInfo:
    #                     category_info = v
    #                     break
    #         item['category'] = category_info.lstrip()
    #         try:
    #             item['uid'] = self.uid
    #             user_sql, user_params = ServiceCompanyOpt.get_sql_info_by_code(item, "t_user", 1, ())
    #             user_count = MysqlHelper.insert(user_sql, user_params)
    #             print("t_user insert rows: %d" % user_count)
    #         except Exception as e:
    #             print("except info: %s" % e)
    #         finally:
    #             self.uid += 1
    #         try:
    #             item['service_id'] = self.serviceId
    #             service_company_sql, service_params = ServiceCompanyOpt.get_sql_info_by_code(item, "t_service_company", 2, ())
    #             service_count = MysqlHelper.insert(service_company_sql, service_params)
    #             print("t_service_company insert rows: %d" % service_count)
    #         except Exception as e:
    #             print(e)
    #         finally:
    #             self.serviceId += 1
    #         content = json.dumps(dict(item), ensure_ascii=False) + '\n'
    #         self.filename.write(content)
    #     return item

    # def close_spider(self, spider):
    #     self.filename.close()

    # def __init__(self):
    #
    #     # self.filename = codecs.open(OptUtil.gen_file(), 'w', encoding="utf-8")
    #
    # def process_item(self, item, spider):
    #     phone = item['phone']
    #     if phone:
    #         content = json.dumps(dict(item), ensure_ascii=False) + '\n'
    #         self.filename.write(content)
    #     return item
    #

