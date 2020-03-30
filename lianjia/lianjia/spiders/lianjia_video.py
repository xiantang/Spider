# -*- coding: utf-8 -*-
import scrapy
from lianjia.items import LianjiaItem
import sys
import os
import math
from urllib.request import urlretrieve

def report(count, blockSize, totalSize):
  percent = int(count*blockSize*100/totalSize)
  sys.stdout.write("\r%d%%" % percent + ' complete')
  sys.stdout.write('[%-50s] %s'%( '=' * int(math.floor(count*blockSize*50/totalSize)),percent))
  sys.stdout.flush()



def stringtoDict(cookie):
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        print(key)
        print(value)
        itemDict[key] = value
    return itemDict


class LianjiaVideoSpider(scrapy.Spider):
    name = 'lianjia_video'
    # allowed_domains = ['lianjia.com', 'http://www.ljabc.com.cn']
    start_urls = 'http://www.ljabc.com.cn/user/toCourseDetail.html?courseId=691604'
    net_cookie='phone=; password=; gr_user_id=bd56b5b9-3da0-49ea-aa05-bb84aabab3a4; gr_session_id_a0f0692c929ad91f=8da0f95c-5ba0-4981-9cfe-e7032c9cd1d1; JSESSIONID=F0BD0C528CC4911EF46456365B5C48EC'
    cookie=stringtoDict(net_cookie)
    BASE_PATH='指标平台简介及全流程案例分享'
    header = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0',
    }
    header_XHR = {
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Accept - Encoding': 'gzip, deflate',
        'Accept - Language': 'zh,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep - alive',
        'Content - Length': '15',
        'Content - Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X - Requested - With': 'XMLHttpRequest',
        'Cookie':'gr_user_id=bd56b5b9-3da0-49ea-aa05-bb84aabab3a4; JSESSIONID=7C898CB7A96A6B2AACFD66FEC8318EFF; gr_session_id_a0f0692c929ad91f=5b49071e-09c3-4579-b2a6-bb76313fb1cb; phone=; password=',
        'Host': 'www.ljabc.com.cn',
        'Origin': 'http: // www.ljabc.com.cn',
        'Referer': 'http: // www.ljabc.com.cn / jsp / index / videoPlay.jsp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0',
    }
    formdata={
        'courseId': '691604'
    }


    def start_requests(self):
        url='http://www.ljabc.com.cn/system/getPlayVideosByCourseId.html'
        # yield scrapy.Request(url,callback=self.content,headers=self.header_XHR)

        # yield scrapy.FormRequest(url,formdata=self.formdata,headers=self.header_XHR)
        return [scrapy.Request(self.start_urls,callback=self.parse_video,cookies=self.cookie,headers=self.header)]

    def parse_video(self, response):
        # print('---------------')
        # print(response.text)
        base_url = 'http://video.ljabc.com.cn/upload/cdn_video/file_000000808%.mp4?source=1&sessionId' \
                   '=704FE7FD4714C9E98FC4EDF0EED4C636 '
        new_string = 4
        CoursePageList = response.xpath("//div[@class='kcml_line']")
        # print(CoursePageList)
        urllist=['http://video.ljabc.com.cn/upload/cdn_video/file_0000008084.mp4?source=1&sessionId=F0E4D4E53D8F0174B553DB906EB46599',
                 'http://video.ljabc.com.cn/upload/cdn_video/file_0000008085.mp4?source=1&sessionId=F0E4D4E53D8F0174B553DB906EB46599'
                 ]
        item=LianjiaItem()

        self.download_by_requests(urllist)
        for url in urllist:
            item['VideoUrl']=urllist

        return item
    def download_by_requests(self,urllist):
        try:
            os.makedirs(self.BASE_PATH)
        except:
            print("file exist!")
            return
        i=1
        # for url in urllist:
        #     with open('{}/第{}节.mp4'.format(self.BASE_PATH,i),'wb') as f:
               # response=requests.get(url).content
               # f.write(response)
               # print("第{}节下载完成！".format(i))
               # i+=1
        for url in urllist:
            sys.stdout.write('\rFetching ' + '第{}节'.format(i) + '...\n')
            urlretrieve(url,'{}/第{}节.mp4'.format(self.BASE_PATH,i),reporthook=report)
            sys.stdout.flush()
            sys.stdout.write("\rDownload complete, saved as {}/第{}节.mp4".format(self.BASE_PATH,i) + '\n\n')
            i+=1
            #http://blog.csdn.net/Lingdongtianxia/article/details/76359555
            #http://www.jb51.net/article/63312.htm
