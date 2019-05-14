# -*- coding: utf-8 -*-
import scrapy
import json
from yelpSpider.optutil import OptUtil
from yelpSpider.items import YelpspiderItem


class YelpSpider(scrapy.Spider):
    name = 'yelp'
    allowed_domains = ['yelp.com']
    offset = 0
    start_urls = ['https://www.yelp.com/search?find_desc=Carpet+Cleaning+Service&find_loc=New+York%2C+NY&ns=1&start='+str(offset)]

    def parse(self, response):
        urls = response.xpath('//div[@class="lemon--div__373c0__1mboc businessName__373c0__1fTgn border-color--default__373c0__2oFDT"]//h3/a[contains(@href, "/biz")]/@href').extract()
        logos = response.xpath('//div[@class="lemon--div__373c0__1mboc u-space-r2 border-color--default__373c0__2oFDT"]//a[contains(@href, "/biz/")]/img/@src').extract()
        if not logos:
            logos = response.xpath('//div[@class="lemon--div__373c0__1mboc on-click-container border-color--default__373c0__2oFDT"]/a[contains(@href, "/biz")]/img/@src').extract()
        url_prefix_domain = 'https://www.yelp.com'
        for url, logo in zip(urls, logos):
            yield scrapy.Request(url_prefix_domain + url, callback=self.parse_item, meta={'_logo': logo})
        if self.offset < 233*10:
            self.offset += 10
            yield scrapy.Request('https://www.yelp.com/search?find_desc=Carpet+Cleaning+Service&find_loc=New+York%2C+NY&ns=1&start='+ str(self.offset), callback=self.parse)

    def parse_item(self, response):
        item = YelpspiderItem()
        item['referer'] = response.request.headers['Referer'].decode(encoding='utf-8')
        item['detail_page_url'] = response.url
        item['logo'] = response.meta['_logo']
        # 公司名
        item['company'] = self.get_company(response)
        item['address'] = self.get_address(response)
        # category
        item['category'] = self.get_category(response)
        # 手机号
        item['phone'] = self.get_phone(response)
        # 公司链接
        item['websiteurl'] = self.get_websiteurl(response)
        # 公司图片,多张以逗号分隔
        item['img_url'] = self.get_img_url(response)
        # 描述
        item['content'] = self.get_content(response)
        # bussiness_content
        item['business_content'] = self.get_bussiness_content(response)
        # 经纬度
        item['latitude'] = self.get_latitude(response)
        item['longitude'] = self.get_longitude(response)
        yield item

    def get_company(self, response):
        company = response.xpath('//div[@class="top-shelf"]//h1/text()').extract()
        if company:
            return ' '.join(company)
        else:
            return ''

    def get_address(self, response):
        address = response.xpath('//div[@class="top-shelf"]//div[@class="mapbox"]//address/text()').extract()
        if address:
            return address[0].strip()
        else:
            return ''

    def get_category(self, response):
        category = response.xpath('//div[@class="price-category"]/span[@class="category-str-list"]/a[contains(@href, "/c/")]/text()').extract()
        if category:
            if len(category) > 1:
                return ",".join(category).strip()
            else:
                return category[0].strip()
        else:
            return ''

    def get_phone(self, response):
        phone = response.xpath('//div[@class="top-shelf"]//span[@class="biz-phone"]/text()').extract()
        if phone:
            return phone[0].strip()
        else:
            return ''

    def get_websiteurl(self, response):
        websiteurl = response.xpath('//div[@class="top-shelf"]//span/a[contains(@href, "biz_redir")]/@href').extract()
        if websiteurl:
            websiteurl = websiteurl[0]
            return OptUtil.urlDecoder(websiteurl[websiteurl.index("=") + 1:websiteurl.index("&")])
        else:
            return ''

    def get_img_url(self, response):
        img_url = response.xpath('//a[contains(@href, "/biz_photos")]/img/@src').extract()
        if img_url:
            return img_url[0]
        else:
            return ''

    def get_content(self, response):
        content = response.xpath(
            '//div[contains(@class, "island")]/div[@class="from-biz-owner-content"]/p[position()<=3]').extract()
        if content:
            return ''.join(content).replace("<p>", "").replace("</p>", "").replace("\n", "").replace("\xa0",
                                                                                                     "").replace("<br>",
                                                                                                                 "").strip()
        else:
            return ''

    def get_bussiness_content(self, response):
        business_content = response.xpath(
            '//div[contains(@class, "island")]/div[@class="from-biz-owner-content"]/p[position()>3]').extract()
        if business_content:
            return ''.join(business_content).replace("<p>", "").replace("</p>", "").replace("\n", "").replace("\xa0",
                                                                                                              "").replace(
                "<br>", "").strip()
        else:
            return ''

    def get_location(self, response):
        data_map_state = response.xpath('//div[@class="mapbox-map"]/div/@data-map-state').extract()
        json_result = json.loads(data_map_state[0]) if data_map_state else {}
        markers = json_result.get('markers')[1] if json_result and json_result.get('markers') and len(
            json_result.get('markers')) >= 2 else {}
        if markers and markers.get('location'):
            return markers.get('location')
        else:
            return {}

    def get_latitude(self, response):
        location = self.get_location(response)
        if location and location.get('latitude'):
            return location.get('latitude')
        else:
            return ''

    def get_longitude(self, response):
        location = self.get_location(response)
        if location and location.get('longitude'):
            return location.get('longitude')
        else:
            return ''



