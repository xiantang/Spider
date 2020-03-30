from excel_local.base_spider.spider import base_spider
import xlrd,xlwt
from lxml import etree
import re
from xlrd import open_workbook
from xlutils.copy import copy
class local_spider(base_spider):
    def __init__(self, delay, retry=1):
        super().__init__(delay, retry)
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.list=[]
        self.path = r"C:\Users\战神皮皮迪\Documents\GitHub\Spider\excel_local\country.xls"
        rb = open_workbook(self.path)
        # 通过sheet_by_index()获取的sheet没有write()方法
        rs = rb.sheet_by_index(0)
        self.wb = copy(rb)
        # 通过get_sheet()获取的sheet有write()方法
        self.ws = self.wb.get_sheet(0)


    def get_from_excel(self):
        xlsfile = r"C:\Users\战神皮皮迪\Documents\GitHub\Spider\excel_local\country.xls"  # 打开指定路径中的xls文件
        book = xlrd.open_workbook(xlsfile)  # 得到Excel文件的book对象，实例化对象
        # sheet0 = book.sheet_by_index(0)  # 通过sheet索引获得sheet对象
        sheet_name = book.sheet_names()[0]
        sheet_1=book.sheet_by_name(sheet_name)
        rows=sheet_1.nrows

        for i in range(0  ,rows):
            # print(sheet_1.row_values(i)) #每一列

            self.serach_conent(sheet_1.row_values(i)[0],str(sheet_1.row_values(i)[1]).replace('.0',''),','.join([sheet_1.row_values(i)[2],sheet_1.row_values(i)[3]]))

    def serach_conent(self,id,keyword,ad):
        if '-' in keyword:
            a=keyword.split('-')
            url='https://www.unitedstateszipcodes.org/{}/'.format(a[0])
            resp=self.get_content(url,header=self.header)
            if resp:
                if len(resp.text)>40000:
                    self.logger.info('current id is {}'.format(id))
                    self.analysis_page_content(id,resp.text)
                else:

                    self.list.append([id,ad])
                    print(self.list)
            else:
                self.list.append([id,ad])
                # print(self.list)



    def analysis_page_content(self,id,content):
        selector=etree.HTML(content)

        sel=selector.xpath('//*[@id="map-info"]/table/tbody')[0]
        a=sel.xpath('string(.)')
        # print(a)
        Neighborhood=re.findall('Neighborhood: (.*?)Manha',a)
        country=re.findall('County: (.*?)Time',a)
        timezone=re.findall('CountyTimezone: (.*?)Area',a)
        areacode=re.findall('Area code: (.*?)Coor',a)

        data=[int(id),Neighborhood,country,timezone,areacode]
        self.write_to_excel(data)
    def write_to_excel(self,data):

        self.ws.write(data[0],4,data[2]) #country
        self.ws.write(data[0], 5, data[1]) #nb
        self.ws.write(data[0], 6, data[3])#time
        self.ws.write(data[0], 7, data[4])
        self.logger.info('write_to_excel')
        self.wb.save(self.path)





if __name__ == '__main__':

    S=local_spider(0)
    S.get_from_excel()

