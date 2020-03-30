# -*- coding: utf-8 -*-
from scrapy.pipelines.files import FilesPipeline
from os.path import basename,dirname,join
#scrapy.crawler.Crawler
from scrapy.crawler import Crawler
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
#
# class LianjiaPipeline(object):
#     def __init__(self):
#         self.filename = open("lianjia.json", "w")
#     def process_item(self, item, spider):
#         text=json.dumps(dict(item),ensure_ascii=False)+"\n"
#         self.filename.write(text.encode("utf-8"))
#         return item
#     def closespider(self,spider):
#         self.filename.close()


# class MyFilesPipeline(FilesPipeline):
#
#     count=0
#     def file_path(self, request, response=None, info=None):
#         FILES_STORE = '指标平台简介及全流程案例分享'
#         MyFilesPipeline.count+=1
#         FILENAME="第{}节".format(MyFilesPipeline.count)
#         return join(basename(FILES_STORE),FILENAME)