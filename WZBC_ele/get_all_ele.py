import requests
import pymysql
F_zone = [51,52,53,1013,1014,1015]
New_zone = [2076,2077,2078]
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='electric',
charset="utf8"

)
coursor = connect.cursor()
# for i in New_zone:
#
#     content = requests.get("http://pay.wzbc.edu.cn/api/pay/wzbc/query/room/buildid?zoneId=1&buildId={}".format(i)).json()
#     for i in content:
#         id = i['id']
#         roomid = i['roomId']
#         roomName = i['roomName']
#         build_id = i['buildId']
#         buildName = i['buildName']
#         sql = """
#         INSERT INTO `room` (`id`, `roomId`, `roomName`, `buildId`, `buildName`)
#          VALUES ('{id}', '{roomId}', '{roomName}', '{buildId}', '{buildName}')
#         """.format(id = id,roomId = roomid,roomName=roomName,buildId=build_id,buildName =buildName)
#         coursor.execute(sql)
# connect.commit()
# print(content)
# for i in New_zone:
#
#     content = requests.get("http://pay.wzbc.edu.cn/api/pay/wzbc/query/room/buildid?zoneId=1&buildId={}".format(i)).json()
#     for i in content:
#         print(i)


        #http://pay.wzbc.edu.cn/api/pay/wzbc/query/bill?zoneId=1&buildId=2077&roomId=2725 HTTP/1.1
c = requests.get("http://pay.wzbc.edu.cn/api/pay/wzbc/query/bill?zoneId=1&buildId=51&roomId=81").content
print(c)