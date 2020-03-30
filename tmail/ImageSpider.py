import requests
from lxml import etree
import time
import json
import re
import pymysql

import traceback

conn = pymysql.connect("url",
                                    "root", "", "product")
cursor = conn.cursor()
def download(img_name,img_url):
    try:
        img_content = requests.get(img_url).content
        with open("imgs/" + img_name + ".jpg", "wb") as f:
            f.write(img_content)
        print(img_name)
    except Exception as e:
        print(e)

cursor.execute("select * from `product`.`test_xquark_sku_img`  limit 1000,2000")
a = cursor.fetchall()
print(len(a))
for item in a:
    img_name = item[2]
    img_url  = item[1]
    download(img_name,img_url)