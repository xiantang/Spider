import requests
import json
import time
from lxml import etree
import re
import csv
import random
from multiprocessing import Pool
class Spider(object):

    header={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }

    proxy=[
    {"proxy": "http://61.178.238.122:63000", "proxy_scheme": "http"},
    {"proxy": "http://113.204.226.158:808", "proxy_scheme": "http"},
    {"proxy": "http://180.156.94.129:8118", "proxy_scheme": "http"},
    {"proxy": "http://118.114.77.47:8080", "proxy_scheme": "http"},
    {"proxy_scheme": "https", "proxy": "https://222.76.187.131:8118"},
    {"proxy_scheme": "http", "proxy": "http://61.178.238.122:63000"},
    {"proxy_scheme": "http", "proxy": "http://111.155.116.211:8123"},
    {"proxy_scheme": "http", "proxy": "http://222.76.187.238:8118"},
    {"proxy_scheme": "http", "proxy": "http://118.114.77.47:8080"}
    ]

    scraped_urls=set()

    csv_header=['title','runtime','ReleaseDate','attrs','stars','commits','type','actors','state','language']
    def __init__(self):
        with open('douban.csv','w') as  f:
            f_csv=csv.writer(f)
            f_csv.writerow(self.csv_header)

    def get_content(self,url):
        time.sleep(2)
        try:
            item=random.choice(self.proxy)
            proxy = {
                item['proxy_scheme']: item['proxy']
            }
            req = requests.get(url, headers=self.header,proxies=proxy,timeout=2)
            content = req.text
            if content==None:
                self.get_content(url)
            return content
        except:
            self.get_content(url)



    def json_to_dict(self,content):
        content_dict=json.loads(content)
        return content_dict

    def Analytic_content_get_url(self,dict):
        urllist=[]
        for item in dict['data']:
            if item['url'] in self.scraped_urls:
                pass
            else:
                urllist.append(item['url'])
        return urllist
    def Analytic_moive_page_content(self,content):
        # print(content)
        all=[]
        html=etree.HTML(content)
        for item in html.xpath('//*[@id="content"]'):
            title=item.xpath('./h1/span[1]/text()')#标题
            #//*[@id="info"]/span[11]
            all.append(''.join(title))
        for item in html.xpath('//div[@id="info"]'):
            runtime=item.xpath('./span[@property="v:runtime"]/text()')#片长
            ReleaseDate=item.xpath('./span[@property="v:initialReleaseDate"]/text()')#上映时间
            attrs=item.xpath('./span[1]/span[@class="attrs"]/a/text()')#导演
            all.append(''.join(runtime))
            all.append(','.join(ReleaseDate))
            all.append(''.join(attrs))
        stars=re.findall('property="v:average">(.*?)</strong>',content)#评分
        state = re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>', content)#国家
        actors=re.findall('rel="v:starring">(.*?)</a>',content)#主演
        type=re.findall('<span property="v:genre">(.*?)</span>',content)#类型
        language=re.findall('<span class="pl">语言:</span> (.*?)<br/>',content)#语言
        commits=re.findall('>(全部 \d+ 条)</a>',content)[0]
        all.append(''.join(stars))
        all.append(''.join(commits))
        all.append(''.join(type))
        all.append(','.join(actors))
        all.append(','.join(state))
        all.append(','.join(language))
        print('----------------------------------------')
        for item in all:
            print(item)
        return all

    def write_to_csv(self,items):
        with open('douban.csv','a') as  f:
            a = csv.writer(f)
            if items ==None:
                pass
            else:
                a.writerow(items)
                print(items[0],'write to csv')

def get_body(url):
    movie_page_content = S.get_content(url)
    movie_content=S.Analytic_moive_page_content(movie_page_content)
    S.write_to_csv(movie_content)

if __name__ == '__main__':
    S = Spider()
    for i in range(0, 100, 20):
        url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}'.format(i)
        content = S.get_content(url)
        content_dict = S.json_to_dict(content)
        urllist = S.Analytic_content_get_url(content_dict)
        pool = Pool(processes=4)
        for url in urllist:
            pool.apply_async(get_body, (url,))
        pool.close()
        pool.join()



