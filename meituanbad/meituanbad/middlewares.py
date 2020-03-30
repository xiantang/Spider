# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class MeituanbadSpiderMiddleware(object):
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


import base64

""" 阿布云ip代理配置，包括账号密码 """
proxyServer = "http://http-dyn.abuyun.com:9020"
proxyUser = "H8OL9EO7M2N0M47D"
proxyPass = "125B6A2692BF831F"
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


class ABProxyMiddleware(object):
    """ 阿布云ip代理配置 """

    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        print(proxyServer)
        request.headers["Proxy-Authorization"] = proxyAuth


from DB.RedisClient import RedisClient


class RandomHttpsProxyMiddleware(object):

    def __init__(self):
        '''
        设置代理ip池
        '''
        self.db = RedisClient('useful_proxy', '', 6379)

    def process_request(self, request, spider):
        '''
        判断是否是http 或者https选择对应的
        :param request:
        :param spider:
        :return:
        '''
        if request.url.startswith('https'):
            self.db.changeTable('useful_proxy_https')
            request.meta['proxy'] = self.db.get()
        else:
            self.db.changeTable('useful_proxy')
            request.meta['proxy'] = self.db.get()


import random


class CookiesMiddleware(object):
    def process_request(self, request, spider):
        cookies = [{'uuid': 'efebec518ab44b67b67a.1528984059.1.0.0','_lxsdk_cuid': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8','__mta': '41660829.1528984063407.1528984063407.1528984069161.2', 'ci': '42', 'rvct': '42','_lxsdk': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8','_lxsdk_s': '163fe8d4c87-c4a-12a-613%7C%7C10'},
                   {'uuid': 'efebec518ab44b67b67a.1528984059.1.0.0',
                    '_lxsdk_cuid': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8',
                    '__mta': '99965529.1528984063407.1528984063407.1528984069161.2', 'ci': '42', 'rvct': '42',
                    '_lxsdk': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8',
                    '_lxsdk_s': '163fe8d4c87-c4a-12a-613%7C%7C10'},
                   {'uuid': 'efebec518ab44b67b67a.1528984059.1.0.0',
                    '_lxsdk_cuid': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8',
                    '__mta': '88860829.1528984063407.1528984063407.1528984069161.2', 'ci': '42', 'rvct': '42',
                    '_lxsdk': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8',
                    '_lxsdk_s': '163fe8d4c87-c4a-12a-613%7C%7C10'},
                   {'uuid': 'efebec518ab44b67b67a.1528984059.1.0.0',
                    '_lxsdk_cuid': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8',
                    '__mta': '77760833.1528984063407.1528984063407.1528984069161.2', 'ci': '42', 'rvct': '42',
                    '_lxsdk': '163fe8d4c821c-084e87f27a3e3a-601a167a-1fa400-163fe8d4c84c8',
                    '_lxsdk_s': '163fe8d4c87-c4a-12a-613%7C%7C10'}]
        import random
        request.cookies = random.choice(cookies)
# _lxsdk_cuid=1fb32820fc8-00a9ab228bf87f-3b60450b-1fa400-161fb328210c8; IJSESSIONID=19tpq92x3s5jei89pses7k5rr; iuuid=4038A299313C775DA013C8F14011EC1E2206FD2F5EE620BA51530F6E6FEFC411; latlng=27.919006%2C120.679321%2C1528965648281; cityname=%E6%B8%A9%E5%B7%9E; backurl=http://i.waimai.meituan.com/home?lat=37.434075&lng=122.196679; _lxsdk=4038A299313C775DA013C8F14011EC1E2206FD2F5EE620BA51530F6E6FEFC411; mtcdn=K; i_extend=H__a100040__b1; webp=1; __utma=74597006.1718431032.1528965650.1528965650.1528965650.1; __utmc=74597006; __utmz=74597006.1528965650.1.1.utmcsr=i.waimai.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/home; uuid=0bce4872f9da485a9b2c.1528965831.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; oc=htr2pPILbWb9eELz51ntXeqMKa2QWHGHO4Y3n4KG9RdzMVkFkML1BqMV_V57VUsXjarzLUmnJrt58jaGStIdJ9hy4m6dxzgJNgZD9j4yPwGDKr1TGeIsikUOW3MPyixZvLozKpSJgvW5a6vRUYmglIezR6fmAUQvqvZsgFX3N_A; ci=42; rvct=42; client-id=76f80503-ec8d-4e5e-99ad-e2b13a5efdd4; __mta=41660829.1520337847095.1528966786836.1528967920670.3; __mta=41660829.1520337847095.1528969852084.1528969907790.4; lat=34.261228; lng=108.94652; _lxsdk_s=163fe6302ff-17-66c-066%7C%7C1816
#http://www.meituan.com/meishi/api/poi/getMerchantComment?uuid=deb8d78e96194b97b7d0.1529039687.1.0.0&platform=1&partner=126&originUrl=http%3A%2F%2Fwww.meituan.com%2Fmeishi%2F1503238%2F&riskLevel=1&optimusCode=1&id=1503238&userId=&offset=0&pageSize=10&sortType=1&tag=%E4%B8%8D%E6%8E%A8%E8%8D%90