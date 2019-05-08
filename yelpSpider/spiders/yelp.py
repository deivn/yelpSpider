# -*- coding: utf-8 -*-
import scrapy
import json
from yelpSpider.optutil import OptUtil
from yelpSpider.items import YelpspiderItem


class YelpSpider(scrapy.Spider):
    name = 'yelp'
    allowed_domains = ['yelp.com']
    offset = 0
    start_urls = ['https://www.yelp.com/search?find_desc=Mortgage%20Company&find_loc=New%20York%2C%20NY&start='+str(offset)]

    def parse(self, response):
        urls = response.xpath('//div[@class="lemon--div__373c0__1mboc businessName__373c0__1fTgn border-color--default__373c0__2oFDT"]//h3/a[contains(@href, "/biz")]/@href').extract()
        logos = response.xpath('//div[@class="lemon--div__373c0__1mboc u-space-r2 border-color--default__373c0__2oFDT"]//a[contains(@href, "/biz/")]/img/@src').extract()
        url_prefix_domain = 'https://www.yelp.com'
        for url, logo in zip(urls, logos):
            yield scrapy.Request(url_prefix_domain + url, callback=self.parse_item, meta={'_logo': logo})
        if self.offset < (60-1)*10:
            self.offset += 10
            yield scrapy.Request('https://www.yelp.com/search?find_desc=Mortgage%20Company&find_loc=New%20York%2C%20NY&start='+ str(self.offset), callback=self.parse)

    def parse_item(self, response):
        item = YelpspiderItem()
        item['logo'] = response.meta['_logo']
        item['page_url'] = response.url
        # 公司名
        item['company'] = ' '.join(response.xpath('//div[@class="top-shelf"]//h1/text()').extract())
        item['address'] = response.xpath('//div[@class="top-shelf"]//div[@class="mapbox"]//address/text()').extract()[0].strip()
        # category
        category = response.xpath('//div[@class="price-category"]/span[@class="category-str-list"]/a/text()').extract()
        item['category'] = category[0].strip() if len(category) else ''
        # 手机号
        item['phone'] = response.xpath('//div[@class="top-shelf"]//span[@class="biz-phone"]/text()').extract()[0].strip()
        # 公司链接
        websiteurl = response.xpath('//div[@class="top-shelf"]//span/a[contains(@href, "biz_redir")]/@href').extract()
        if len(websiteurl):
            websiteurl = websiteurl[0]
            item['websiteurl'] = OptUtil.urlDecoder(websiteurl[websiteurl.index("=") + 1:websiteurl.index("&")])
        else:
            item['websiteurl'] = ''

        # 公司图片,多张以逗号分隔
        img_url = response.xpath('//a[contains(@href, "/biz_photos")]/img/@src').extract()
        item['img_url'] = img_url[0] if len(img_url) else ''

        # 描述
        content = response.xpath('//div[contains(@class, "island")]/div[@class="from-biz-owner-content"]/p[position()<=3]').extract()
        item['content'] = ''.join(content).replace("<p>", "").replace("</p>", "").replace("\n", "").replace("\xa0", "").replace("<br>", "").strip() if len(content) else ''
        # bussiness_content
        business_content = response.xpath('//div[contains(@class, "island")]/div[@class="from-biz-owner-content"]/p[position()>3]').extract()
        item['business_content'] = ''.join(business_content).replace("<p>", "").replace("</p>", "").replace("\n", "").replace("\xa0", "").replace("<br>", "").strip() if len(business_content) else ''

        data_map_state = response.xpath('//div[@class="mapbox-map"]/div/@data-map-state').extract()
        json_result = json.loads(data_map_state[0]) if data_map_state else {}
        markers = json_result.get('markers')[1] if json_result and json_result.get('markers') and len(json_result.get('markers')) >= 2 else {}
        location = markers.get('location') if markers.get('location') else {}
        # 经纬度
        item['latitude'] = location.get('latitude') if location and location.get('latitude') else ''
        item['longitude'] = location.get('longitude') if location and location.get('longitude') else ''
        yield item




