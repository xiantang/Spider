# coding=gbk

import urllib
from urllib import request
import json
import time

for i in range(0,201,20):
    time.sleep(2)
    string='data_json=%7B%22city%22%3A%22%22%2C%22orderGrab%22%3A1%2C%22tags%22%3A%220%22%7D&common_json=%7B%22c_id%22%3A%22baidu%22%2C%22d_bd%22%3A%22Meizu%22%2C%22d_id%22%3A%22861069034104441%22%2C%22d_ml%22%3A%22MX6%22%2C%22from%22%3A%22com.huijiemanager%22%2C%22lat%22%3A%2229.898358999999999241481418721377849578857421875%22%2C%22lng%22%3A%22121.640027000000003454260877333581447601318359375%22%2C%22location%22%3A%22%E5%AE%81%E6%B3%A2%E5%B8%82%22%2C%22p%22%3A%22android%22%2C%22sensors%22%3A%7B%22anonymous_id%22%3A%229a25e1b786b4a4d%22%2C%22carrier%22%3A%22CMCC%22%2C%22module%22%3A%22%22%2C%22network_type%22%3A%22wifi%22%2C%22os%22%3A%22android%22%2C%22os_version%22%3A%226.0%22%2C%22product%22%3A%22%E4%BF%A1%E8%B4%B7%E5%AE%B6%22%2C%22screen_height%22%3A1920%2C%22screen_width%22%3A1080%2C%22utm_source%22%3A%22baidu%22%2C%22wifi%22%3Atrue%7D%2C%22specific_address%22%3A%22%E5%AE%81%E6%B3%A2%E5%B8%82%E9%95%87%E6%B5%B7%E5%8C%BA%E6%A2%85%E6%B1%9F%E8%B7%AF8118%E5%8F%B7%22%2C%22timestemp%22%3A%221519905508417%22%2C%22token%22%3A%229738e220774ef04897e38d89d1ff01e5%22%2C%22u_id%22%3A%2295d13540bbc5e493718ac24ad09d3d4e%22%2C%22ver%22%3A%223.3.0%22%7D&page_json=%7B%22last_record_id%22%3A%224834957%22%2C%22last_record_time%22%3A%221519809001000%22%2C%22page_size%22%3A20%2C%22start_row%22%3A{}%7D&'.format(i)
    # 改变的是提交表单的row%22%3A{}%7D&
    data=bytes(string,encoding ='utf8')
    url='http://api.huijieapp.com/iou-site/api/loanManager/find_orders_by_tags_cities.json?ver=3.3.0'
    #URL不会发生改变 主要改变的是data
    header={
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; MX6 Build/MRA58K)',
        'Host': 'api.huijieapp.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    req=request.Request(url=url,data=data,headers=header)
    json_content=urllib.request.urlopen(req).read().decode('utf-8')
    content_to_dict=json.loads(json_content)
    users=content_to_dict['data']['detail']['orders']
    for user in users:
        print(user['locationInfo'])
        print(user['province'])
        print(user['userDesc'])
        print(user['assetsInfo'])
        print(user['id'])
        print(user['incomeInfo'])
        print(user['loan_amount'])
        print('------------------------------')
# a=r'''{"code":"1","data":{"flag":"1","detail":{"orders":[{"orderType":"1",