# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpspiderItem(scrapy.Item):
    # reffere
    referer = scrapy.Field()
    # 当前页
    detail_page_url = scrapy.Field()
    logo = scrapy.Field()
    # 公司名
    company = scrapy.Field()
    address = scrapy.Field()
    # category
    category = scrapy.Field()
    # 手机号
    phone = scrapy.Field()
    websiteurl = scrapy.Field()
    # 公司图片
    img_url = scrapy.Field()
    # 描述
    content = scrapy.Field()
    # bussiness_content
    business_content = scrapy.Field()
    # 经纬度
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    # 当前时间
    date_time = scrapy.Field()


class ProxyInfo(scrapy.Item):
    proxy = scrapy.Field()
    date_time = scrapy.Field()




