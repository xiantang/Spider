import requests
import copyheaders
from  lxml import etree
import re
import random
import time
from multiprocessing import Pool
# from anjuke import proxt
headers=b'''accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept-encoding:gzip, deflate, br
accept-language:zh,en-US;q=0.9,en;q=0.8
cache-control:max-age=0
upgrade-insecure-requests:1
user-agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'''


class anjuke(object):

    def get_list(self,city):#获取该城市的所有地区的url
        area_all_url=[]
        url='https://{}.anjuke.com/sale/?from=navigation'.format(city)
        while True:
            content=self.download_1(url)
            print('正在尝试连接')
            time.sleep(3)
            if content!= None:
                print("成功")
                break
        print("链接成功")
        selector=etree.HTML(content)
        area_list=selector.xpath('//*[@id="content"]/div[3]/div[1]/span[2]/a/@href')
        for area_url in area_list:
            next_content=self.download_1(area_url)
            if next_content==None:
                continue
            sel=etree.HTML(next_content)
            area_list_url=sel.xpath('//*[@id="content"]/div[3]/div[1]/span[2]/div/a/@href')
            for url in  area_list_url:
                area_all_url.append(url)
        print("---------获取所有的url成功-----------")
        return area_all_url

    def download(self,url,retry=0,timeout=5):
        try:
            sessions = requests.session()
            sessions.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            content = sessions.get(url,
                                   # proxies=proxt.proxy()
                                   timeout=timeout
                                   ).text

            if '访问验证' in content:
                self.download_1(url, retry)
                print('---------遭遇验证码---------')
                if retry > 10:
                    retry+=1
                    return None
            return content
        except :
            retry += 1
            self.download_1(url, retry)
            if retry > 3:
                return None
    def download_1(self,url,retry=0,timeout=5):
        time.sleep(1)
        try:
            sessions = requests.session()
            sessions.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            content = sessions.get(url,
                                   # proxies=proxt.proxy()
                                   timeout=timeout
                                   ).text
            return content
        except :
            retry+=1
            self.download_1(url,retry)
            if retry>3:
                return None



    def ever_page(self,urls):
        # print(urls)
        for url in  urls:#遍历每个城市的地区
            # print(url)
            for i in range(1,50):
                complete_url=url+'p{}/'.format(i)
                # print(complete_url)
                city=''.join(re.findall('//(.*?).anjuke',complete_url))
                area=''.join(re.findall('/sale/(.*?)/',complete_url))
                print('爬去'+city+'的'+area+'的第'+str(i)+'页')
                content_page=self.download(complete_url)
                if content_page==None:
                    print('爬取失败')
                    time.sleep(5)
                    continue
                selector=etree.HTML(content_page)
                ever_hotels=selector.xpath('//ul/li/div[2]/div[1]/a/@href')

                if len(ever_hotels)<10: #如果小于10跳出循环 跳到下个地区
                    print('----------不到50页跳出循环-----------')
                    time.sleep(5)
                    break
                self.scraped_ever_hotel(ever_hotels)

    def scraped_ever_hotel(self,hotel_page):
        # pool = Pool(processes=6)
        for item_url in hotel_page:#每个url遍历
            # pool.apply_async(self.ever_page_, (item_url,))
            self.ever_page_(item_url)
        # pool.close()
        # pool.join()
    def ever_page_(self,item_url):
        a=random.randint(1, 2)
        time.sleep(a)
        content = self.download(item_url)
        selector = etree.HTML(content)
        Subordinate_District = selector.xpath('//div[@class="houseInfo-wrap"]/div/div/dl/dd/a/text()')
        local = selector.xpath('//p[@class="loc-text"]/a/text()')
        bulid_time = selector.xpath('//div[@class="houseInfo-wrap"]/div/div[1]/dl[3]/dd/text()')
        type = selector.xpath('//div[@class="houseInfo-wrap"]/div/div/dl[4]/dd/text()')
        area = selector.xpath('//div[@class="houseInfo-wrap"]/div/div[2]/dl[2]/dd/text()')
        first_pay = selector.xpath('//div[@class="houseInfo-wrap"]/div/div[3]/dl[3]/dd/text()')
        house_info = selector.xpath('//p[@class="houseInfo"]/text()')
        house_info = ''.join(house_info)
        if len(house_info)<5:
            print("------------没有成功抓取-----------------")
            time.sleep(3)
        house_info = house_info.split('\n')
        print('-----------------------------------------')
        print(house_info[1].replace('\t', ''))
        print(house_info[3].replace('\t', ''))
        print(''.join(local))
        print(''.join(Subordinate_District))
        print(''.join(bulid_time))
        print(''.join(type))
        print(''.join(area))
        print(''.join(first_pay).replace('\n', '').replace('\t', ''))
        house_data = [house_info[1].replace('\t', '').replace(',', ''),
                      house_info[3].replace('\t', ''),
                      ''.join(local),
                      ''.join(Subordinate_District),
                      ''.join(bulid_time),
                      ''.join(type),
                      ''.join(area),
                      ''.join(first_pay).replace('\n', '').replace('\t', '')
                      ]
        self.write_to_csv(house_data)
    def write_to_csv(self,data):
        with open('ers.csv','a') as f:
            f.write(','.join(data)+'\n')



if __name__ == '__main__':
    citylist=['zh']
    S = anjuke()
    for citt in  citylist:
        area_all_url = S.get_list(citt)
        S.ever_page(area_all_url)


