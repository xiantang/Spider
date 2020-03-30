# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider,Request
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
from zhihuq.items import  ZhihuqItem
import json


class QuestSpider(scrapy.Spider):
    name = 'quest'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    start_user='zhi-liao-85-19'
    quest_include='data[*].created,answer_count,follower_count,author,admin_closed_comment'
    quest_url='https://www.zhihu.com/api/v4/members/{user}/questions?include={include}&offset={offset}&limit={limit}'
    fellowers_url='https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    fellowers_include='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    def start_requests(self):
        yield Request(self.fellowers_url.format(user=self.start_user,include=self.fellowers_include,offset=0,limit=20),callback=self.parse_fellowers)#粉丝页面
        yield Request(self.quest_url.format(user=self.start_user,include=self.quest_include,offset=0,limit=20),callback=self.parse_question)
        # yield Request(self.quest_include.format(user=self.start_user,include=self.quest_include,offset=0,limit=20),callback=self.parse_question)
        # yield Requ est(self.fellowers_url.format(user=self.start_user,),callback=self.parse_fellowers)  # 粉丝页面
    #     yield Request('http://www.zhihu.com/api/v4/questions/265762204')
    #     # yield Request('http://www.zhihu.com/api/v4/questions/265734502/recommend-readings?include=data%5B%2A%5D.follower_count%2Canswer_count%3Bdata%5B%2A%5D.question.follower_count%2Canswer_count%3Bdata%5B%2A%5D.voteup_count%2Ccomment_count%3B&limit=3&offset=3')
    def parse_fellowers(self,response):
        results=json.loads(response.text)
        # print(result)

        if 'data' in results.keys():
            for result in  results.get('data'):
                meta = {
                    'user': result.get('url_token')
                }
                yield Request(self.quest_url.format(user=result.get('url_token'),include=self.quest_include,offset=0,limit=20),callback=self.parse_question,meta=meta)
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            nextpage=results.get('paging').get('next')
            yield Request(nextpage,callback=self.parse_fellowers)


    def parse_question(self, response):
        results = json.loads(response.text)
        question = ZhihuqItem()
        user_token=response.meta['user']

        if 'data' in results.keys():
            for result in  results.get('data'):
                if int(result.get('created'))>1464752710:

                    question['title']=result.get('title')
                    question['answer_count'] =result.get('answer_count')
                    question['follower_count'] =result.get('follower_count')
                    yield question
        if 'paging' in results.keys() and results.get('paging').get('is_end')==False:
            nextpage=results.get('paging').get('next')
            yield Request(nextpage,callback=self.parse_question)

        yield Request(self.fellowers_url.format(user=user_token,include=self.fellowers_include,offset=0,limit=20),callback=self.parse_fellowers)



    # rule={
    #     Rule(LinkExtractor(allow=('/question/'),deny=('/answer/')))
    # }
    # def parse(self, response):
    #     print(len(response.text))
