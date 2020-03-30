import requests
from lxml import etree
import pymysql
import re
header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='weibo', charset='utf8')
cursor = conn.cursor()
data = requests.get('https://weibo.cn/u/1223178222?oid=3995999519800276').text #下载用户页面
name=re.findall('<span class="ctt">(.*?)<img src=',data)[0] #获取姓名
content=re.findall('(.*?)</span><br />',data)[1]#获取详细信息
following_count=re.findall('关注\[(.*?)\]</a>',data)[0] #关注
weibo_count=re.findall('微博\[(.*?)\]</span>',data)[0] #微博数目
follower=re.findall('粉丝\[(.*?)\]</',data)[0]#被关注数
#获取性别和地址 存在数组中
#------------------------------------------------------
new=re.findall('alt="M"/></a>(.*?)<a href=',data)[0] #-
news = re.findall(r'[\u4e00-\u9fa5]+',new)           #-
#------------------------------------------------------
sex=news[0]#性别
local=news[1]#地址
print(name)
print(content)
print(following_count)
print(weibo_count)
print(follower)
print(local)
print(sex)
sql = "INSERT user (name,content,weibo_count,follower,sex,local,following_count) VALUES('%s','%s',%d,%d,'%s','%s','%d')" % (name,content,int(weibo_count),int(follower),sex,local,int(following_count))
print("插入成功")#字符串带单引号才能插入
cursor.execute(sql)#执行插入语句
conn.commit()
cursor.close()#关闭游标
conn.close()#关闭连接