from selenium import webdriver
from lxml import etree
import time
import json
import re
import pymysql

import traceback
class DetailTmailSpider():

    def __init__(self, json_path):
        self.driver = webdriver.Chrome()
        self.load_url_list(json_path)
        self.conn = pymysql.connect("",
                                    "root", "123456", "product")
        self.cursor = self.conn.cursor()
        self.driver.set_page_load_timeout(15)


    def load_url_list(self:object, json_path: str):
        """
        从path中的json获取url列表
        :param json_path:
        :return:
        """
        with open(json_path, "r") as f:
            url_list = f.read()
        url_list = json.loads(url_list)
        self.url_list = []
        for url in url_list:
            # 过滤两张图片
            if url.startswith("//img.alicdn.com/bao/uploaded/"):
                pass
            else:
                self.url_list.append("https:" + url)
        # with open("uncrawl.text","r") as f:
        #     list_img=f.readlines()
        # for url in list_img:
        #     url=url.replace("\n","")
        #     self.url_list.append(url)
    def get_all_detail_page(self):
        """
        获取全部的内容页面
        :return:
        """
        for url in self.url_list:
            time.sleep(6)


            try:
                self.driver.get(url)
                row_html = self.driver.page_source
                print("Crawled page :" + url)
            except Exception as  e:
                continue
            self.parse_html(row_html,url)

    def list_to_str(self,field_list:list)->str:
        return "" if len(field_list) == 0 \
            else field_list[0]

    @property
    def created(self):

        return time.strftime('%Y-%m-%d',time.localtime())


    def parse_html(self, raw_html: str,url:str):
        """
        解析页面
        :param raw_html:
        :return:
        """
        selector = etree.HTML(raw_html)
        categoryid_list=re.findall('"categoryId":"(\d+)"',raw_html)
        # print(raw_html)
        title_list = selector.xpath('//meta[@name ="keywords"]/@content')
        shop_name_list = selector.xpath('//input[@name\
        ="seller_nickname"]/@value')
        comment_num = selector.xpath('//li[@class="tm-ind-item tm-ind-revi'
                                     'ewCount canClick tm-line3"]/div/span['
                                     '2]/text()')
        comment_num = self.list_to_str(comment_num)
        shop_name = self.list_to_str(shop_name_list)
        categoryId = self.list_to_str(categoryid_list)
        title = self.list_to_str(title_list)
        price_list = selector.xpath('//span[@class="tm-price"]/text()')
        item_id_list = re.findall("itemId=(\d+)",raw_html)
        item_id = self.list_to_str(item_id_list)
        low_price = None
        high_price = None
        low_counter_price = None
        high_counter_price = None
        monthly_sale  = selector.xpath('//li[@class="tm-ind-item tm-ind-sellCount"]'
                                       '/div/span[@class="tm-count"]/text()')
        monthly_sale = self.list_to_str(monthly_sale)
        created = self.created
        if len(price_list) == 2:
            counter_price = price_list[0].split("-")
            price = price_list[1].split("-")
            if(len(counter_price)>1):
                low_counter_price =counter_price[0]
                high_counter_price = counter_price[0]
            if(len(price)>1):
                low_price = price[0]
                high_price = price[1]
            if(len(price)==1):
                low_price = price[0]
                high_price = price[0]
            if(len(counter_price)==1):
                low_counter_price = counter_price[0]
                high_counter_price = counter_price[0]
        if(len(price_list)== 1):
            price = price_list[0].split("-")

            if (len(price) > 1):
                low_price = price[0]
                high_price = price[1]
                low_counter_price = -1
                high_counter_price = -1
            else:
                low_price = price[0]
                high_price = price[0]
                low_counter_price = -1
                high_counter_price = -1
        img_list = selector.xpath('//ul[@id="J_UlThumb"]/li/a/img/@src')

        prop_list = selector.xpath('//*[@id="J_AttrUL"]/li/text()')
        # print(prop_list)

        if monthly_sale is None or monthly_sale=="":
            monthly_sale = -1
        if comment_num  is None or comment_num=="":
            comment_num  = -1

        sql  ="""
        insert into `product`.`test_xquark_product` 
        ( `high_counter_price`, `created`, `high_price`, `title`, 
        `categoryId`, `low_price`, `monthly_sale`, `shop_name`, `comment_num`, 
        `item_id`, `low_counter_price`) values
        ( '{high_counter_price}', '{created}', '{high_price}', '{title}', '{categoryId}', 
        '{low_price}', '{monthly_sale}', '{shop_name}', '{comment_num}', '{item_id}', 
        '{low_counter_price}') ON DUPLICATE KEY UPDATE  `created`='{created}'
        """.format(high_counter_price=high_counter_price,created=created,high_price=high_price
                   ,title=title,categoryId=categoryId,low_price=low_price,monthly_sale=monthly_sale,
                   shop_name=shop_name,comment_num=comment_num,item_id=item_id,
                   low_counter_price=low_counter_price)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(high_counter_price)
            with open("uncrawl.text","a+") as f:
                f.writelines(url+"\n")
            traceback.print_exc()
        self.insert_img_list(img_list,item_id)
        self.insert_prop(prop_list,item_id)

    def insert_img_list(self,img_list:list,item_id:str):
        #insert into `product`.`test_xquark_sku_img` ( `img_name`, `created`, `img`, `item_id`) values ( '123', '2018-09-16', '3123', '123')
        i= 1
        for img_url in img_list:
            img_url = "https:"+img_url.replace("60x60","800x800")
            img_name = "id_"+item_id+"_{}".format(i)
            i+=1
            sql  = """
            insert into `product`.`test_xquark_sku_img` 
            ( `img_name`, `created`, `img`, `item_id`) 
            values ( '{img_name}', '{created}', '{img}',
             '{item_id}')  ON DUPLICATE KEY UPDATE  `created`='{created}'""".format(img_name=img_name,created=self.created,
                                    img=img_url,item_id=item_id)
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
    def insert_prop(self,prop_list:list,item_id:str):
        for prop in prop_list:
            prop_key_value = prop.split(':',1)
            if len(prop_key_value)>1:
                value = prop_key_value[1]
                prop = prop_key_value[0]
                sql  = """
                insert into `product`.`test_xquark_sku_prop` 
                ( `value`, `created`, `item_id`, `prop`)
                 values ( '{value}', '{created}', '{item_id}', '{prop}') ON DUPLICATE KEY UPDATE  `created`='{created}'"""
                sql = sql.format(value=value,created=self.created,item_id=item_id,prop=prop)
                try:
                    self.cursor.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    print(e)
    def run(self):
        self.get_all_detail_page()
        # url ="https://detail.tmall.com/item.htm?acm=lb-zebra-290127-2903430.1003.4.2564927&id=546003083194&scm=1003.4.lb-zebra-290127-2903430.ITEM_546003083194_2564927"
        # self.driver.get(url)
        # self.parse_html(self.driver.page_source)
if __name__ == '__main__':
    dts = DetailTmailSpider("json/url_list.json")
    dts.run()
