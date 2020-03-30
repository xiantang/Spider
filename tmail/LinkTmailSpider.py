from selenium import webdriver
from lxml import etree
import time
import json

class LinkTmailSpider():

    def __init__(self,start_url):
        self.driver = webdriver.Chrome()
        self.url_list = []
        self.start_url_list=start_url

    def get_page_roll_time(self) -> int:
        """
        根据页面高度获取滚动次数
        :return:
        """
        # 获取页面高度
        page_high = self.driver.execute_script("return document.body.clientHeight")
        roll_time = int(page_high / 1000)+1
        return roll_time

    def get_one_page_list(self, url: str) -> list:
        self.driver.get(url)
        roll_time = self.get_page_roll_time()
        for i in range(0, roll_time):
            # 根据页面高度滚动
            js = "var q=document.documentElement.scrollTop={}".format(i * 1000)
            self.driver.execute_script(js)
            time.sleep(1)
        selector = etree.HTML(self.driver.page_source)
        url_first = selector.xpath("//li[@data-mark='pit']/a/@href")
        url_second = selector.xpath("//a[@class='area-item']/@href")
        return url_first+url_second

    def all_url_list(self):
        for url in self.start_url_list:
            url_list = self.get_one_page_list(url)
            print(len(url_list))
            self.url_list =self.url_list+url_list
            print(len(self.url_list))

        json_url_list = json.dumps(self.url_list)

        with open("json/url_list.json", "w") as f:
            f.write(json_url_list)


    def run(self):
        self.all_url_list()

if __name__ == '__main__':
    stat_url = [
            "https://pages.tmall.com/wow/yao/17473/baojianzibu",
            "https://pages.tmall.com/wow/yao/act/711jf",
            "https://pages.tmall.com/wow/yao/act/999",
            "https://pages.tmall.com/wow/yao/act/aljkdyf-fuke",
            "https://miao.tmall.com/"
        ]
    ts = LinkTmailSpider(stat_url)
    ts.all_url_list()
# driver.quit()
