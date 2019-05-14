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
import string
import ssl
import time
from yelpSpider.items import ProxyInfo
from yelpSpider.sqlutil import SqlUtil
from yelpSpider.dealopt import ServiceCompanyOpt
from yelpSpider.mysqlutil import MysqlHelper
import json
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.http import HtmlResponse


# USER-AGENT中间件代理类


class RandomUserAgent(object):
    proxies = []

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
    proxies = []

    def __init__(self, proxies):
        self.proxies = self.get_ip_proxy()
        if self.proxies:
            proxy_items = []
            for proxy in self.proxies:
                proxy_item = ProxyInfo()
                proxy_item['proxy'] = str(json.dumps(dict(proxy), ensure_ascii=False))
                proxy_item['date_time'] = SqlUtil.gen_current_time()
                proxy_items.append(proxy_item)
            if proxy_items:
                for proxy_item in proxy_items:
                    user_sql, user_params = ServiceCompanyOpt.get_sql_info_by_code(proxy_item, "proxy_info", 2)
                    user_count = MysqlHelper.insert(user_sql, user_params)
    @classmethod
    def from_crawler(cls, crawler):
        return cls(cls.proxies)

    def process_request(self, request, spider):
        if self.proxies:
            proxy = random.choice(self.proxies)
            if proxy['user_pass']:
                # 参数是bytes对象,要先将字符串转码成bytes对象
                encoded_user_pass = base64.b64encode(proxy['user_pass'].encode('utf-8'))
                request.headers['Proxy-Authorization'] = 'Basic ' + str(encoded_user_pass, 'utf-8')
                request.meta['proxy'] = "http://" + proxy['ip_port']
            else:
                request.meta['proxy'] = "http://" + proxy['ip_port']

    def get_ip_proxy(self):
        proxy_list = []
        url = 'https://dps.kdlapi.com/api/getdps/?orderid=915771133465773&num=20&area=%E5%B9%BF%E4%B8%9C%2C%E7%A6%8F%E5%BB%BA%2C%E6%B5%99%E6%B1%9F%2C%E6%B1%9F%E8%A5%BF%2C%E5%8C%97%E4%BA%AC%2C%E6%B9%96%E5%8D%97%2C%E9%A6%99%E6%B8%AF%2C%E4%BA%91%E5%8D%97%2C%E5%A4%A9%E6%B4%A5%2C%E5%B9%BF%E8%A5%BF&pt=1&dedup=1&format=json&sep=1&signature=27zcmsq40fqnyk506ev51impu1hc0ipy'
        ssl._create_default_https_context = ssl._create_unverified_context
        result = request.urlopen(quote(url, safe=string.printable))
        info = None
        try:
            info = result.read().decode(encoding='utf-8')
            if info:
                result_info = json.loads(info)
                if result_info and result_info.get("data"):
                    data = result_info.get("data")
                    if data and data.get("proxy_list"):
                        proxy_list = data.get("proxy_list")
            if proxy_list:
                for _ip in proxy_list:
                    ip_port = _ip.split(",")[0]
                    self.proxies.append({"ip_port": ip_port, "user_pass": settings['USER_PASS']})
        except Exception as e:
            info = e
        return self.proxies


class ProcessAllExceptionMiddleware(object):

    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)
    proxies = []

    def __init__(self, proxies):
        self.proxies = proxies

    def process_response(self, request, response, spider):
        if response.status != 200:
            print('状态码异常')
            reason = self.response_status_message(response.status)
            self.proxy_opt(self, request)
            time.sleep(random.randint(3, 5))
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            # 在日志中打印异常类型
            print('Got exception: %s' % (exception))
            self.proxy_opt(self, request)
            # 随意封装一个response，返回给spider
            response = HtmlResponse(url='exception')
            return response
        # 打印出未捕获到的异常
        print('not contained exception: %s' % exception)

    def proxy_opt(self, request):
        # 移除代理，并随机选一个代理
        self.proxies = self.get_ip_proxy()
        if self.proxies:
            # 删除失效的代理
            self.del_proxy(request.meta.get('proxy', False), self.proxies)
            # 生产一批新的入库
            self.get_proxies()
            if self.proxies:
                # 设置代理
                self.process_request(request)

    def del_proxy(self, proxy, res=None):
        print('删除代理')
        proxies = MysqlHelper.get_all('select proxy from proxy_info', [])
        if proxies and proxy in proxies:
            print('已过期需要删除的代理: %s' % proxy)
            MysqlHelper.delete('delete from proxy_info where proxy= %s', [proxy])

    '''功能：获取新的可用的代理list'''
    def get_proxies(self):
        proxies = self.get_ip_proxy()
        if proxies:
            for proxy in proxies:
                user_sql, user_params = ServiceCompanyOpt.get_sql_info_by_code(proxy, "proxy_info", 2)
                MysqlHelper.insert(user_sql, user_params)
            self.proxies = proxies
        else:
            proxies = MysqlHelper.get_all('select proxy from proxy_info', [])
            if proxies:
                self.proxies = proxies

    def process_request(self, request):
        if self.proxies:
            proxy = random.choice(self.proxies)
            if proxy['user_pass']:
                # 参数是bytes对象,要先将字符串转码成bytes对象
                encoded_user_pass = base64.b64encode(proxy['user_pass'].encode('utf-8'))
                request.headers['Proxy-Authorization'] = 'Basic ' + str(encoded_user_pass, 'utf-8')
                request.meta['proxy'] = "http://" + proxy['ip_port']
            else:
                request.meta['proxy'] = "http://" + proxy['ip_port']

    def get_ip_proxy(self):
        proxy_list = []
        url = 'https://dps.kdlapi.com/api/getdps/?orderid=915771133465773&num=20&area=%E5%B9%BF%E4%B8%9C%2C%E7%A6%8F%E5%BB%BA%2C%E6%B5%99%E6%B1%9F%2C%E6%B1%9F%E8%A5%BF%2C%E5%8C%97%E4%BA%AC%2C%E6%B9%96%E5%8D%97%2C%E9%A6%99%E6%B8%AF%2C%E4%BA%91%E5%8D%97%2C%E5%A4%A9%E6%B4%A5%2C%E5%B9%BF%E8%A5%BF&pt=1&dedup=1&format=json&sep=1&signature=27zcmsq40fqnyk506ev51impu1hc0ipy'
        ssl._create_default_https_context = ssl._create_unverified_context
        result = request.urlopen(quote(url, safe=string.printable))
        info = None
        try:
            info = result.read().decode(encoding='utf-8')
            if info:
                result_info = json.loads(info)
                if result_info and result_info.get("data"):
                    data = result_info.get("data")
                    if data and data.get("proxy_list"):
                        proxy_list = data.get("proxy_list")
            if proxy_list:
                for _ip in proxy_list:
                    ip_port = _ip.split(",")[0]
                    self.proxies.append({"ip_port": ip_port, "user_pass": settings['USER_PASS']})
        except Exception as e:
            info = e
        return self.proxies


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
