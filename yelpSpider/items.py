# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpspiderItem(scrapy.Item):
    # reffere
    # 当前页
    page_url = scrapy.Field()
    # 公司名称
    company = scrapy.Field()
    # 地址:  录入地址 + 公司名称 + 城市名称 + 州名称
    address = scrapy.Field()
    # 描述
    content = scrapy.Field()
    # 首图
    img_url = scrapy.Field()
    # logo
    logo = scrapy.Field()
    # phone
    phone = scrapy.Field()
    # 业务描述
    business_content = scrapy.Field()
    # websiteurl
    websiteurl = scrapy.Field()
    # category
    category = scrapy.Field()
    # zip
    zip = scrapy.Field()
    # state_id
    state_id = scrapy.Field()
    # city_id
    city_id = scrapy.Field()
    # uid
    uid = scrapy.Field()
    # service_id
    service_id = scrapy.Field()
    # latitude
    latitude = scrapy.Field()
    # longitude
    longitude = scrapy.Field()



