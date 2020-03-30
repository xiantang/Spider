# coding=UTF-8
# from copyheaders import headers_raw_to_dict
import requests
from lxml import etree
import time
import re
import csv
import random


class Spider(object):
    headers = b'''Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:zh,en-US;q=0.9,en;q=0.8
Cache-Control:max-age=0
Connection:keep-alive
Cookie:__jsluid=3f8b631de5544d404eb64a83577b457e; gr_user_id=fab8087e-e1b2-4286-b75d-476cfe078b66; UM_distinctid=161c794045e1b2-00fc3893a398bc-3a7f0e5a-100200-161c794045f74; qlm_username=15868759135; qlm_password=E8mmpu8fB87EC88jfj3up3BRp7oURjou; rem_login=1; seo_refUrl="https://www.baidu.com/link?url=FsipNhoi6Han8Bkuab63iDbL0i46cIytjoXKkAe5xvw7-zW_DZ7ie5TVjweCXnJl&wd=&eqid=c51c146600008c6d000000065a939528"; seo_curUrl="http://www.qianlima.com/common/area.jsp"; seo_intime="2018-02-26 13:03:51"; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1519655630; Hm_lvt_0a38bdb0467f2ce847386f381ff6c0e8=1519621457,1519651654,1519733653,1519794622; Hm_lvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1519622402,1519651654,1519733653,1519794622; gr_session_id_83e3b26ab9124002bae03256fc549065=606de9b4-ec5a-44ca-986b-1b96602de6e9; qlmll_his=",78986517,78986382,78688477,78688488,78688496,78772645,78773957,78774308,78774321,78774968,"; CNZZDATA1848524=cnzz_eid%3D286386678-1519468056-null%26ntime%3D1519797041; __jsl_clearance=1519798422.034|0|X2zCD9ltDnhxMpj9K1aUZ%2BoJ4zw%3D; Hm_lpvt_0a38bdb0467f2ce847386f381ff6c0e8=1519798453; Hm_lpvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1519798453
Host:www.qianlima.com
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'''

    header = ['title', 'time', 'content']
    header_us = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }

    def __init__(self):
        with open('zhaobiao(1).csv', 'w', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.header)

    def random(self):
        dely = random.uniform(0, 1)
        return round(dely, 2)

    def get_content(self, url):
        daly = self.random()
        time.sleep(daly)
        html = requests.get(url,
                            # headers=headers_raw_to_dict(self.headers),
                            headers=self.header_us
                            ).text

        return html

    def analysis_list_html(self, count, i=1):
        url = 'http://www.qianlima.com/zb/area_11_0_{}/'.format(count)
        html = self.get_content(url)
        selector = etree.HTML(html)
        if '黑龙江省招标网' in selector.xpath('//title/text()'):
            print('-----正在爬取第{}页------'.format(count))
            # /html/body/table[8]/tbody/tr/td[1]/table[4]/tbody/tr[2]/td/table/tbody/tr[39]/td[2]/a
            sel = selector.xpath('//table[@width="100%"]/tr')
            urls = []
            for item in sel:
                url = item.xpath('./td[2]/a[@class="list"]/@href')
                if url != []:
                    urls.append(''.join(url))
            return urls
        else:
            dely = self.random() + 2
            print('---------try-{}----sleep{}-------'.format(i, dely))
            time.sleep(dely)

            i += 1

            if i == 5:
                print('跳转至下一个页面')
                return None

            self.analysis_list_html(count, i)

    def analysis_content_html(self, url):
        # // *[ @ id = "print_dom"] / div[2] / h2
        html = self.get_content(url)
        selector = etree.HTML(html)
        title = selector.xpath('//*[@id ="print_dom"]/div[2]/h2/text()')
        # //*[@id="wen"]/div/div/div[1]
        if title == []:
            self.analysis_list_html(url)
        else:
            items = []
            all = []
            title = ''.join(title)
            time = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})",
                              ''.join(selector.xpath('//meta[@name="description"]/@content')))

            # //*[@id="wen"]/div/div/div[2]/div[2]/div
            text = selector.xpath('//*[@id="wen"]/div/div/div[2]/div[2]/div/text()')
            Coarse_content = ''.join(re.findall(r"<div> <div> <div>(.*?)</div> <br>", html))
            Coarse_content = Coarse_content.split("<tr style='background: #FBFDFE;' >")

            for item in Coarse_content:
                item = item.replace('</tr>', '\n').replace('</td>', ':', 1).replace('<td>', '').replace('<div>',
                                                                                                        '').replace(
                    '</div>', '').replace('</table>', '').replace('</td>', '').replace('<br>', '')
                item = re.sub('<td colspan="\d">', '', item).replace('<p>', '').replace('</p>', '').replace('<a.*?</a>',"")
                if 'target' in item:
                    pass
                elif '<table' in item:
                    pass
                else:
                    items.append(item)
            content = ''.join(items)
            all.append(title)
            all.append(''.join(time))
            all.append(content)
            return all

            # print(','.join(new_content))

    def write_to_excel(self, items):
        with open('zhaobiao.csv', 'a', encoding='utf-8') as f:
            a = csv.writer(f)
            if items == None:
                pass
            else:
                a.writerow(items)
                print(items[0], 'write to csv')


if __name__ == '__main__':
    s = Spider()
    for i in range(1, 20):
        urls = s.analysis_list_html(i)
        if urls == None:
            continue
        else:
            for url in urls:
                items = s.analysis_content_html(url)
                s.write_to_excel(items)

