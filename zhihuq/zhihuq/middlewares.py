# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from zhihuq.settings import PROXY
import random



class HttpProxyMiddleware(object):
    def __init__(self,ip=''):
        self.ip=ip
    def process_request(self,request,spider):
        thisip=random.choice(PROXY)
        print('this ip is :%s'%thisip['proxy'])
        request.meta['proxy']=thisip['proxy']
        request.meta['download_timeout']=3

