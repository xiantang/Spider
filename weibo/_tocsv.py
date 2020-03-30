import pymysql
import csv
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='weibo', charset='utf8')
cursor = conn.cursor()
cursor.execute("select * from `original`")
with open("test2.csv","w",encoding="utf-8") as csvfile:
    for i in cursor.fetchall():
        writer = csv.writer(csvfile)
        writer.writerow(list(i))