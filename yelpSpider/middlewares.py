# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import base64
from scrapy.conf import settings
from scrapy import signals
from urllib import request
from urllib.parse import quote
import json
import string
import ssl

# USER-AGENT中间件代理类


class RandomUserAgent(object):

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        # 加载IPLIST
        return cls(settings['USER_AGENTS'])

    # 该方法在引擎发送http request请求给下载器时会经过下载中间件，可以设置ip代理，User-Agent, 设置关闭cookie
    def process_request(self, request, spider):
        """
        从配置文件读取user-agent池中的数据，每次请求都随机选一个user-agent
        :param request: 在引擎发送给下载器的http request请求
        :param spider: 引擎
        :return:
        """
        request.headers["User-Agent"] = random.choice(self.agents)


'''
动态设置代理ip
'''
class RandomProxy(object):

    def __init__(self, proxies):
        self.proxies = proxies

    @classmethod
    def from_crawler(cls, crawler):
        proxies = []
        proxy_list = []
        url = 'https://dps.kdlapi.com/api/getdps/?orderid=955728569976197' \
              '&num=100&area=%E5%8C%97%E4%BA%AC%2C%E4%B8%8A%E6%B5%B7%2C%E6%B5%99%E6%B1%9F%2C%E6%B1%9F%E8%A5%BF%2C%E6%B2%B3%E5%8C%97%2C%E5%B9%BF%E5%B7%9E%2C%E9%A6%99%E6%B8%AF' \
              '&pt=1&f_citycode=1&format=json&sep=1'
        ssl._create_default_https_context = ssl._create_unverified_context
        result = request.urlopen(quote(url, safe=string.printable))
        info = result.read().decode(encoding='utf-8')
        print("私密代理接口接口获取IP列表结果返回信息: info= %s" % info)
        if info:
            result_info = json.loads(info)
            if result_info and result_info.get("data"):
                data = result_info.get("data")
                if data and data.get("proxy_list"):
                    proxy_list = data.get("proxy_list")
        if proxy_list:
            for _ip in proxy_list:
                ip_port = _ip.split(",")[0]
                proxies.append({"ip_port": ip_port, "user_pass": settings['USER_PASS']})
        return cls(proxies)

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        if proxy['user_pass']:
            # 参数是bytes对象,要先将字符串转码成bytes对象
            encoded_user_pass = base64.b64encode(proxy['user_pass'].encode('utf-8'))
            request.headers['Proxy-Authorization'] = 'Basic ' + str(encoded_user_pass, 'utf-8')
            request.meta['proxy'] = "http://" + proxy['ip_port']
        else:
            request.meta['proxy'] = "http://" + proxy['ip_port']




class ForsalecrawlSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ForsalecrawlDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
