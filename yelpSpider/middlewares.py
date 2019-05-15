# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import base64
from scrapy.conf import settings
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
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import re



# USER-AGENT中间件代理类


class RandomUserAgent(object):
    agents = []

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

    def __init__(self):
        # self.proxies = self.get_ip_proxy()
        self.proxies = []
        if self.proxies:
            for proxy in self.proxies:
                proxy_item = ProxyInfo()
                proxy_item['proxy'] = str(json.dumps(dict(proxy), ensure_ascii=False))
                proxy_item['date_time'] = SqlUtil.gen_current_time()
                user_sql, user_params = ServiceCompanyOpt.get_sql_info_by_code(proxy_item, "proxy_info", 2)
                user_count = MysqlHelper.insert(user_sql, user_params)
                print("新增代理IP: %d" %user_count)
        else:
            proxies = MysqlHelper.get_all('select proxy from proxy_info', [])
            if proxies:
                for t in proxies:
                    self.proxies.append(json.loads(t[0]))

    # @classmethod
    # def from_crawler(cls):
    #     return cls(cls.proxies)

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
        url = 'https://dps.kdlapi.com/api/getdps/?orderid=995728565437721&num=3&area=%E5%B9%BF%E4%B8%9C%2C%E7%A6%8F%E5%BB%BA%2C%E6%B5%99%E6%B1%9F%2C%E6%B1%9F%E8%A5%BF%2C%E5%8C%97%E4%BA%AC%2C%E6%B9%96%E5%8D%97%2C%E9%A6%99%E6%B8%AF%2C%E4%BA%91%E5%8D%97%2C%E5%A4%A9%E6%B4%A5%2C%E6%B1%9F%E8%8B%8F%2C%E6%B9%96%E5%8C%97%2C%E6%B2%B3%E5%8D%97&pt=1&ut=2&dedup=1&format=json&sep=1&signature=sq5pzskhi33dmpt8h16ksm16br8xd45v'
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


class ProcessAllExceptionMiddleware(RetryMiddleware):

    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response

        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        if response.status != 200:
            print('状态码异常')
            reason = response_status_message(response.status)
            # self.proxy_opt(self, request)
            time.sleep(random.randint(3, 5))
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        # 设置同一个代理发生异常的次数
        # 捕获几乎所有的异常
        if isinstance(exception, self.ALL_EXCEPTIONS):
            # 在日志中打印异常类型
            print('Got exception: %s' % (exception))
            if re.findall(r'Connection was refused by other side', str(exception)) or \
                    re.findall(r'connection timed out', str(exception)) or \
                    re.findall(r'User timeout caused connection failure', str(exception)) or \
                    re.findall(r'Connection to the other side was lost', str(exception)) or \
                    re.findall(r'Could not open CONNECT tunnel', str(exception)):
                # 删除失效的代理
                self.del_proxy(request.meta.get('proxy', False))
            # 设置新的代理
            self.proxy_opt(request, spider)
            time.sleep(random.randint(3, 5))
            # 随意封装一个response，返回给spider
            response = HtmlResponse(url='exception')
            return self._retry(request, exception, spider) or response
            # return response
        # 打印出未捕获到的异常
        print('not contained exception: %s' % exception)

    '''1.获取代理'''
    def proxy_opt(self, request, spider):
        # 获取代理列表
        proxies = MysqlHelper.get_all('select proxy from proxy_info', [])
        _list = self.format_tuple2list(proxies)
        if len(_list) <= 5:
            # 生产一批代理新的入库
            proxies = self.get_ip_proxy()
            if proxies:
                self.batch_insert_proxy(proxies)
                # 设置代理
                self.set_proxy(request, spider, proxies)
        else:
            # 设置代理
            proxies_tmps = []
            for t in proxies:
                proxies_tmps.append(json.loads(t[0]))
            self.set_proxy(request, spider, proxies_tmps)

    '''将tuple转换为list'''
    def format_tuple2list(self, proxies):
        _list = []
        if proxies:
            for t in proxies:
                _list.append(json.loads(t[0]))
        return _list

    def batch_insert_proxy(self, proxies):
        for proxy in proxies:
            proxy_item = ProxyInfo()
            proxy_item['proxy'] = str(json.dumps(dict(proxy), ensure_ascii=False))
            proxy_item['date_time'] = SqlUtil.gen_current_time()
            user_sql, user_params = ServiceCompanyOpt.get_sql_info_by_code(proxy_item, "proxy_info", 2)
            user_count = MysqlHelper.insert(user_sql, user_params)
            print("新增代理IP: %d" % user_count)

    '''删除过期的代理'''
    def del_proxy(self, proxy, res=None):
        proxies = MysqlHelper.get_all('select proxy from proxy_info', [])
        if proxies:
            for proxy_item in proxies:
                ip_proxy = proxy_item[0]
                _proxy = json.loads(ip_proxy)['ip_port']
                _tmp = re.findall(_proxy, proxy)
                if _tmp:
                    print('已过期需要删除的代理: %s' % ip_proxy)
                    count = MysqlHelper.delete('delete from proxy_info where proxy= %s', [ip_proxy])
                    print('成功删除代理%s--------rows act: %d' % (proxy, count))

    '''功能：获取新的可用的代理list'''
    def get_proxies(self, proxies):
        _proxies = []
        if proxies:
            proxy_item = ProxyInfo()
            proxy_item['proxy'] = str(json.dumps(dict(proxies[0]), ensure_ascii=False))
            proxy_item['date_time'] = SqlUtil.gen_current_time()
            user_sql, user_params = ServiceCompanyOpt.get_sql_info_by_code(proxy_item, "proxy_info", 2)
            MysqlHelper.insert(user_sql, user_params)
            _proxies = proxies
        else:
            proxies = MysqlHelper.get_all('select proxy from proxy_info', [])
            if proxies:
                _proxies = proxies
        return _proxies

    def set_proxy(self, request, spider, proxies):
        if proxies:
            proxy = random.choice(proxies)
            if proxy['user_pass']:
                # 参数是bytes对象,要先将字符串转码成bytes对象
                encoded_user_pass = base64.b64encode(proxy['user_pass'].encode('utf-8'))
                request.headers['Proxy-Authorization'] = 'Basic ' + str(encoded_user_pass, 'utf-8')
                request.meta['proxy'] = "http://" + proxy['ip_port']
            else:
                request.meta['proxy'] = "http://" + proxy['ip_port']

    '''通过接口获取最新的代理'''
    def get_ip_proxy(self):
        proxy_list = []
        proxy_newlist = []
        url = 'https://dps.kdlapi.com/api/getdps/?orderid=995728565437721&num=3&area=%E5%B9%BF%E4%B8%9C%2C%E7%A6%8F%E5%BB%BA%2C%E6%B5%99%E6%B1%9F%2C%E6%B1%9F%E8%A5%BF%2C%E5%8C%97%E4%BA%AC%2C%E6%B9%96%E5%8D%97%2C%E9%A6%99%E6%B8%AF%2C%E4%BA%91%E5%8D%97%2C%E5%A4%A9%E6%B4%A5%2C%E6%B1%9F%E8%8B%8F%2C%E6%B9%96%E5%8C%97%2C%E6%B2%B3%E5%8D%97&pt=1&ut=2&dedup=1&format=json&sep=1&signature=sq5pzskhi33dmpt8h16ksm16br8xd45v'
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
                    proxy_newlist.append({"ip_port": ip_port, "user_pass": settings['USER_PASS']})
        except Exception as e:
            info = e
        return proxy_newlist
