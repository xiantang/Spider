from excel_local.base_spider.spider import base_spider
import xlrd,xlwt
from lxml import etree
import re
from xlrd import open_workbook
from xlutils.copy import copy
import requests
class local_spider(base_spider):

    def __init__(self, delay, retry=1):
        super().__init__(delay, retry)
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.path = r"C:\Users\战神皮皮迪\Documents\GitHub\Spider\excel_local\County.xls"
        rb = open_workbook(self.path)
        # 通过sheet_by_index()获取的sheet没有write()方法
        rs = rb.sheet_by_index(0)
        self.wb = copy(rb)
        # 通过get_sheet()获取的sheet有write()方法
        self.ws = self.wb.get_sheet(0)

    def get_from_excel(self):
        xlsfile = r"C:\Users\战神皮皮迪\Documents\GitHub\Spider\excel_local\County.xls"  # 打开指定路径中的xls文件
        book = xlrd.open_workbook(xlsfile)  # 得到Excel文件的book对象，实例化对象
        # sheet0 = book.sheet_by_index(0)  # 通过sheet索引获得sheet对象
        sheet_name = book.sheet_names()[0]
        sheet_1 = book.sheet_by_name(sheet_name)
        rows = sheet_1.nrows
        for i in range(rows):
            if sheet_1.row_values(i)[4] == '':
                print(sheet_1.row_values(i)[0])
                self.search_content(
                    sheet_1.row_values(i)[0],
                    str(sheet_1.row_values(i)[1]).replace('.0', ''),
                )
    def search_content(self,id,keyword):
        url = 'https://www.unitedstateszipcodes.org/{}/'.format(keyword)
        header={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        content = requests.get(url,headers=header).content
        print(len(content))
        if len(content)>36262:
            selector = etree.HTML(content)
            try:
                sel = selector.xpath('//*[@id="map-info"]/table/tbody')[0]
                a = sel.xpath('string(.)')
                Neighborhood = re.findall('Neighborhood: (.*?)Manha', a)
                country = re.findall('County: (.*?)Time', a)
                areacode = re.findall('Area code: (.*?)Coor', a)
                data = [int(id), Neighborhood, country, areacode]
                self.write_to_excel(data)
                print(id)
            except:
                pass
        else:
            print('len(content)<36262: pass ')
    def write_to_excel(self,data):

        self.ws.write(data[0],4,data[2])
        self.ws.write(data[0], 5, data[1])
        self.ws.write(data[0], 6, data[3])
        self.logger.info('write_to_excel')
        self.wb.save(self.path)


S=local_spider(0)
S.get_from_excel()