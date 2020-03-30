import xlwt
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
from time import sleep
dcap = dict(DesiredCapabilities.PHANTOMJS)
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet=book.add_sheet('sell')
dcap["phantomjs.page.settings.userAgent"] = (
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
driver=webdriver.PhantomJS(r'C:\Users\战神皮皮迪\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
url=input("输入你需要爬取的网址:")
endpage=input("输入向后爬取的数量:")
CurrentPage=re.findall("&s=(\d+)",url)
CurrentPage=int(''.join(CurrentPage))
#https://shopsearch.taobao.com/search?app=shopsearch&q=%E6%B5%B4&imgfile=&commend=all&ssid=s5-e&search_type=shop&sourceId=tb.index&spm=a21bo.1000386.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&isb=0&shop_type=&ratesum=&qq-pf-to=pcqq.c2c&sort=sale-desc&s=40
def get_content(i):
    driver.get(url.replace("&s="+str(CurrentPage),'&s=')+str(i))
    content=driver.page_source
    if len(driver.page_source)<500:
        sleep(1) #在这里改时间间隔
        get_content(i)
    else:
        nick=re.findall('"nick":"(.*?)","provcity',content)
        write_to_excel(i,nick)
def write_to_excel(star,data):
    # print(star ,'   ',star+len(data))
    excel_start=star-CurrentPage
    excel_end=star+len(data)-CurrentPage
    for i in range(excel_start,excel_end):
        if i<20:
            sheet.write(i,0,data[i])
            print(data[i] + "写入execl成功!")
        else:
            List_Down=i-excel_start
            sheet.write(i,0,data[List_Down])
            print(data[List_Down]+ "写入execl成功!")


for i in range(CurrentPage,CurrentPage+int(endpage)*20+1,20):
    get_content(i)
    book.save("test1.xls")