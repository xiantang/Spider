# -*- coding: utf-8 -*-
from scrapy import Request
import scrapy
import json


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['www.xicidaili.com']
    def start_requests(self):

        for i in  range(1,5):
            # print('http://www.xicidaili.com/nn/{page}'.format(page=i))
            # yield Request('http://www.xicidaili.com/nn/{page}'.format(page=i))
            yield  Request('http://www.xicidaili.com/nn/%s'%i)
    def parse(self, response):
        # print(response.text)
        for sel in response.xpath('//table[@id="ip_list"]/tr[position()>1]'):
            # ip=sel.css('./td[1]/text()').extract_first()
            ip = sel.xpath('./td[2]/text()').extract_first()
            port= sel.xpath('./td[3]/text()').extract_first()
            scheme=sel.xpath('./td[6]/text()').extract_first().lower()
            url='%s://httpbin.org/ip'%scheme
            proxy='%s://%s:%s'%(scheme,ip,port)

            meta={
                'proxy':proxy,
                'dont_retry':True,
                'download_timeout':3,

                '_proxy_ip':ip,
                '_scheme_':scheme
            }
            yield  Request(url,callback=self.check,meta=meta,dont_filter=True)
    def check(self,response):
        proxy_ip=response.meta['_proxy_ip']
        if proxy_ip==json.loads(response.text)["origin"]:
            yield {
                'proxy_scheme':response.meta['_scheme_'],
                'proxy':response.meta['proxy']
            }

