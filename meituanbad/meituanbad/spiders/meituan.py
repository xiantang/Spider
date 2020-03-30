# -*- coding: utf-8 -*-
import scrapy
from meituanbad.items import  MeituanbadItem

class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    # allowed_domains = ['xa.meituan.com']
    start_urls = ['http://sz.meituan.com/meishi/']


    def start_requests(self):

        for i in self.start_urls:
            yield  scrapy.Request(url=i,callback=self.parse)


    def parse(self, response):
        # print(response.text)
        sel=response.xpath('//*[@id="app"]/section/div/div[2]/div[1]/div/div[1]/ul/li')

        for i in sel:
            url=i.xpath("./a/@href").extract_first()

            url+="pn1/"
            yield scrapy.Request(url,callback=self.getid)


    def getid(self,response):

        # sel=response.xpath('//ul[@class="list-ul"]/li')
        #//*[@id="app"]/section/div/div[2]/div[2]/div[1]/ul/li[1]/div[2]/a
        import re

        id=re.findall('"poiId":(.*?),"frontImg"',response.text)

        for i in id:
            url="http://www.meituan.com/meishi/api/poi/getMerchantComment?&id="+str(i)+"&pageSize=200&tag=%E4%B8%8D%E6%8E%A8%E8%8D%90"
            yield  scrapy.Request(url,callback=self.getbad)

        # page=response.xpath("//div[@class='mt-pagination']/ul/li[last()-1]/span/text()")
        # print(page)
        page=int(re.findall("pn(\d)/",response.url)[0])+1
        if page>32:
            pass
        else:
            url=re.sub("pn(\d)/",str(page),response.url)
            scrapy.Request(url,callback=self.getid)


    def getbad(self,response):
        import json
        dictComment=json.loads(response.text)
        Comments=dictComment['data']['comments']

        for comment in Comments:
            item=MeituanbadItem()
            item['time']=comment['comment']
            item['comment']=comment["commentTime"]
            yield item