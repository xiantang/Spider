import random
import requests
from requests.models import Response
import time
class WebRequest(object):

    def __init__(self,*args,**kwargs):
        pass

    @property
    def user_agent(self):
        '''
        返回一个随机的属性
        :return:
        '''
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        return random.choice(ua_list)

    @property
    def hearder(self):
        '''
        标准的头部
        :return:
        '''
        return {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    def get(self,url,header=None,retry_time=2,timeout=5,retry_flag=list(),
            retry_interval=5,*args,**kwargs):

        '''
        :param url: 传入的url
        :param header: 传入的头部
        :param retry_time: 重试次数
        :param timeout:
        :param retry_flag:
        :param retry_interval: 重试秒数
        :param args:
        :param kwargs:
        :return:
        '''
        headers=self.hearder
        if header and isinstance(header,dict):
            #isinstance用来判断对象的类型
            headers.update(header)
        while True:
            try:
                html = requests.get(url,headers=headers,timeout=timeout)
                if any(f in html.content for f in retry_flag):
                    raise Exception
                return html
            except Exception as e:
                print(e)
                retry_time-=1
                if retry_time<=0:
                    resp=Response()
                    #实例化一个空的response
                    resp.status_code=200
                    return  resp
                time.sleep(retry_interval)
