import requests
import re
import pymysql
from fake_useragent import UserAgent
import lxml
from lxml import etree
import proxy
header_shop = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
}#浏览器头
ua=UserAgent()




# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='dazhong', charset='utf8')
# cursor = conn.cursor()
# cursor.execute('USE dazhong')#链接数据库


# def connect_to_my_sql():。


def get_content():
    list=['g105','g110','g132','g111']#遍历四个标签
    for j in  list:
        for i in range(1, 51):#遍历每一页
            content = requests.get('http://www.dianping.com/guiyang/ch10/{}p{}'.format(j,i), headers=header_shop).text
            parse_content(content)


def parse_content(content):
    selector=etree.HTML(content)#树状HTML
    sel=selector.xpath('//*[@id="shop-all-list"]/ul/li')
    for item in sel:
        # time.sleep(1)
        url=''.join(item.xpath('./div[@class="txt"]/div[@class="tit"]/a[1]/@href'))
        name=''.join(item.xpath('./div[2]/div[1]/a/h4/text()'))
        amount=''.join(item.xpath('./div[2]/div[2]/a[1]/b/text()'))
        if amount=='':
            amount=0
        adress=''.join(item.xpath('./div[2]/div[3]/span/text()'))
        per=''.join(item.xpath('./div[2]/div[2]/a[2]/b/text()'))
        # print(name)
        sql="INSERT INTO shop VALUES ('{url}', '{name}', {amount}, '{adress}', '{per}')".format(
                                            url=url,name=name,
                                            amount=amount,adress=adress,per=per
        )#sql语句
        # instert_to_bd(sql)
        ID=''.join(re.findall("(\d+)",url))
        print(ID)
        commit_content(ID,name)


def commit_content(ID,name): #获取评论的函数
        for i in range(1,20):
            print(name)
            url = 'http://www.dianping.com/shop/{}/review_all/p{}'.format(ID,i)
            # print(url)
            header_comment = {
                'User-Agent': ua.random,
                'Cookie':'_lxsdk_cuid=163057e2d4fc8-03370d242f56b8-7c117d7e-1fa400-163057e2d4fc8; _lxsdk=163057e2d4fc8-03370d242f56b8-7c117d7e-1fa400-163057e2d4fc8; _hc.v=8cd08b53-f19b-6289-b239-4ef97a2b76b5.1524805545; dper=e5b5aa8cba5ad90edcbd56145582c4ee31ed97e633d1b8cb40a1a946cb2549d7; ll=7fd06e815b796be3df069dec7836c3df; ua=%E5%92%B8%E7%B3%96_8951; ctu=12a017cea659512d0c8b94961d2e13e41cca89bd5be8c472b9f196ec6d9a228b; uamo=15868759135; cy=101; cye=wenzhou; s_ViewType=10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=163057e2d54-8c1-82e-dfe%7C%7C1975'
            }
            # print(header_comment)
            content = requests.get(url, headers=header_comment,proxies=proxy.return_()).text
            if(len(content)==0):
                continue
            selector= etree.HTML(content)

            sel = selector.xpath('//div[@class="reviews-items"]/ul/li')
            if (len(sel)>2):
                for item in sel:
                    user_id=''.join(item.xpath('./a/@data-user-id'))
                    print(user_id)
            else:
                print(name,"跳出循环")
                break

        # if len(sel)>10:
        #     for item in sel:
        #         ID_user = item.xpath("./a/@data-user-id")
        #         print(ID_user)


    # print(content)


        # time=''.join(item.xpath('./div[@class="content"]/div[@class="misc-info"]/span[@class="time"]/text()'))
        #
        # data=''.join(item.xpath('./div')[0].xpath('string(.)'))
        #
        # taste=''.join(re.findall("口味：(.*?) 环境",data))
        # enviroment = ''.join(re.findall("环境：(.*?) 服务", data))
        # service=''.join(re.findall("服务：(.*?) ",data))
        #
        # overall_rating =(''.join(re.findall('\d+', ''.join(item.xpath('./div/p[1]/span[1]/@class')))).replace('0',''))
        # try:
        #     coment =re.sub('：(.*?)  ','',re.findall("服务(.*?) 赞",data)[0])
        # except:
        #     coment=''

        # sql = "INSERT INTO comment VALUES ('{ID}', '{time}', '{coment}', '{service}', '{enviroment}','{taste}','{overall_rating}')".format(
        #     ID=id, time=time,
        #     coment=coment, service=service, enviroment=enviroment,
        #     taste=taste,overall_rating=overall_rating
        # )#sql语句
        # # instert_to_bd(sql)#插入数据库
        # print(sql)


#
# def instert_to_bd(sql): #插入数据库
#         try:
#             cursor.execute(sql)
#             conn.commit()
#         except pymysql.err.IntegrityError as e:
#             pass
#         except pymysql.err.ProgrammingError as  ex:
#             pass
#         else:
#             print("写入成功")



get_content()
# conn.close()
