# http://weixin.sogou.com/
import re
import urllib.request
import time
import urllib.error
import urllib.request
import json
from lxml import etree
import csv
import logging

# 自定义函数，功能为使用代理服务器爬一个网址
def use_proxy(url):
    # 建立异常处理机制
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400')
        # proxy=urllib.request.ProxyHandler({'http':proxy_addr})
        # opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
        data = urllib.request.urlopen(req).read().decode("utf-8", "ignore")
        return data
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        # 若为URLErroe异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        # 若为Exception异常，延时1秒执行
        time.sleep(1)


def write_to_txt(data):
    with open('C:/Users/dadaguo/Desktop/豆瓣电影/豆瓣电影.txt', 'a') as f:
        f.write(data[0] + '\n')
        f.write(data[1] + '\n')
        f.write(data[2] + '\n')
        f.write("---------------------")
        f.write("\n")


def replaceAll(old, new, str):
    while str.find(old) > -1:
        str = str.replace(old, new)
    return str

def write_to_csv(data):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    with open("租房.csv", "a") as f:
        f.write(','.join(data)+'\n')
        logger = logging.getLogger(__name__)

        logger.info("write to csv")


# 设置关键词
key = "郭浩"
# 设置代理服务器
# proxy="120.79.217.139:6666"
# 爬多少页
city_list=['https://fs.zu.anjuke.com/?from=navigation','https://zh.zu.anjuke.com/?from=navigation']
for m in range(0,3):
    city_url=city_list[m]
    city_data=use_proxy(city_url)
    seletor = etree.HTML(city_data)
    smallurl=seletor.xpath('//span[@class="elems-l"]//a/@href')
    print(city_url)
    for n in range (3,7):
        newnew_url=smallurl[n]
        for i in range(1, 51):
            # key=urllib.request.quote(key)
            # print (key)
            thispageurl = newnew_url+"p" + str(i)
            thispagedata = use_proxy(thispageurl)
            seletor = etree.HTML(thispagedata)
            url = seletor.xpath('//div[@class="zu-itemmod  "]/a[@class="img"]/@href')
            for j in range(0, len(url)):
                thisurl = url[j]
                thisdata = use_proxy(thisurl)
                seletor = etree.HTML(thisdata)
                moneyRent = seletor.xpath('//ul[@class="house-info-zufang cf"]')
                info = moneyRent[0].xpath('string(.)').strip().replace("\n", "")
                info=replaceAll('  ',' ',info)
                info=info.replace('查看租金走势','').replace('户型：','').replace('面积：','').replace('朝向： ','').replace('楼层： ','').replace('装修：','').replace('类型：','').replace('小区：','').replace('\xa0','')
                list = info.split('  ')
                write_to_csv(list)
                time.sleep(1)