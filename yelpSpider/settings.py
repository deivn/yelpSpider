# -*- coding: utf-8 -*-

# Scrapy settings for yelpSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'yelpSpider'

# 数据保存路径
DATA_PATH_PREFIX = "D:/yelp/data"

SPIDER_MODULES = ['yelpSpider.spiders']
NEWSPIDER_MODULE = 'yelpSpider.spiders'

MYSQL_HOST = "184.181.11.233"
MYSQL_PORT = 3306
MYSQL_USER = "ebuyhouse"
MYSQL_PASSWD = "ebuyhouse135"
MYSQL_DB = "crawl_data"


# 默认情况下,RFPDupeFilter只记录第一个重复请求。将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
DUPEFILTER_DEBUG = True
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 关掉重定向, 不会重定向到新的地址
REDIRECT_ENABLED = False
# 返回301, 302时, 按正常返回对待, 可以正常写入cookie
# HTTPERROR_ALLOWED_CODES = [301, 302]

# PHANTOMJS_PATH = 'D:\\devtools\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 40
# CONCURRENT_REQUESTS_PER_IP = 16
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

CLOSESPIDER_ITEMCOUNT = 50
DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS = 40
DOWNLOAD_TIMEOUT = 30

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept-Encoding': 'gzip',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'realtorSpider.middlewares.RealtorspiderSpiderMiddleware': 543,
#}

# 下载中间件配置User-Agent池
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
USER_PASS = "wh429004:ylsvtvu1"
# 代理
PROXIES = [
    {'ip_port': '110.85.155.248:15363', 'user_pass': 'wh429004:ylsvtvu1'},
    {'ip_port': '60.179.238.167:15702', 'user_pass': 'wh429004:ylsvtvu1'},
    {'ip_port': '115.221.125.143:15197', 'user_pass': 'wh429004:ylsvtvu1'},
    {'ip_port': '120.78.127.134:23815', 'user_pass': 'wh429004:ylsvtvu1'},
    {'ip_port': '113.222.80.117:22873', 'user_pass': 'wh429004:ylsvtvu1'},
    # {'ip_port': '60.179.232.197:16063', 'user_pass': 'wh429004:ylsvtvu1'},
    # {'ip_port': '59.63.65.209:23298', 'user_pass': 'wh429004:ylsvtvu1'},
    # {'ip_port': '220.186.144.135:23052', 'user_pass': 'wh429004:ylsvtvu1'},
    # {'ip_port': '36.106.166.40:20278', 'user_pass': 'wh429004:ylsvtvu1'},
    # {'ip_port': '113.221.15.101:22702', 'user_pass': 'wh429004:ylsvtvu1'},
]
# 代理服务器
# proxyServer = "http://http-dyn.abuyun.com:9020"
# PROXY_SERVER = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
# proxyUser = "H012345678901zyx"
# proxyPass = "0123456789012xyz"
# PROXY_USER= "H012345678901zyx"
# PROXY_PASS= "0123456789012xyz"

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
    # 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'yelpSpider.middlewares.RandomUserAgent': 400,
    'yelpSpider.middlewares.RandomProxy': 600,
    'yelpSpider.middlewares.ProcessAllExceptionMiddleware': 750,

}

RETRY_TIMES = 10
RETRY_ENABLED: True

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'yelpSpider.pipelines.YelpspiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# 如果要保证纵向爬取的时候，数据漏爬，可以打开此配置
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
