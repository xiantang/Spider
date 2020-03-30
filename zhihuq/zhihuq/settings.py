# -*- coding: utf-8 -*-

# Scrapy settings for zhihuq project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihuq'

SPIDER_MODULES = ['zhihuq.spiders']
NEWSPIDER_MODULE = 'zhihuq.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihuq (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 45

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
    "authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'
}
DOWNLOAD_DELAY=0.5
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihuq.middlewares.ZhihuqSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'zhihuq.middlewares.HttpProxyMiddleware': 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'zhihuq.pipelines.ZhihuqPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
PROXY=[
{"proxy": "http://175.171.155.244:80", "proxy_scheme": "http"},
{"proxy": "https://106.42.97.138:808", "proxy_scheme": "https"},
{"proxy": "http://112.114.96.189:8118", "proxy_scheme": "http"},
{"proxy": "https://124.133.74.58:8118", "proxy_scheme": "https"},
{"proxy": "http://59.173.55.5:8118", "proxy_scheme": "http"},
{"proxy": "https://221.215.169.40:8118", "proxy_scheme": "https"},
{"proxy": "http://183.23.72.87:808", "proxy_scheme": "http"},
{"proxy": "https://114.234.99.69:8118", "proxy_scheme": "https"},
{"proxy": "http://139.208.187.142:8118", "proxy_scheme": "http"},
{"proxy": "https://180.156.94.177:8118", "proxy_scheme": "https"},
{"proxy": "http://123.114.57.102:8118", "proxy_scheme": "http"},
{"proxy": "https://49.81.32.187:808", "proxy_scheme": "https"},
{"proxy": "https://114.228.208.177:8118", "proxy_scheme": "https"},
{"proxy": "http://106.56.102.63:808", "proxy_scheme": "http"},
{"proxy": "http://113.215.194.51:8118", "proxy_scheme": "http"}
]