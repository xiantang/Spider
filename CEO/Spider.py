import requests
from xlrd import open_workbook
from xlutils.copy import copy
from WebRequest import WebRequest
from lxml import etree


def read_excel():
    """
    read data from excel
    :return:
    """
    excel_path = r"CEO names hand collect from S_1.xls"
    rb = open_workbook(excel_path)
    sheet_name = rb.sheet_names()[0]
    sheet_1 = rb.sheet_by_name(sheet_name)
    rows = sheet_1.nrows
    code_array = []

    for i in range(1, rows):
        element = sheet_1.row_values(i)[7]
        if element != "":
            code_array.append(int(element))
    return code_array


def parse_target_response(resp_of_target):
    selector = etree.HTML(resp_of_target.text)
    first_url = selector.xpath("//table[@class='tableFile']/tr[2]/td/a/@href")
    second_url = selector.xpath("//table[@class='tableFile']/tr[last()]/td[3]/a/@href")
    if first_url:
        if ".htm" in first_url[0]:
            # print(first_url[0])
            return "https://www.sec.gov" + first_url[0]
        else:
            if second_url:
                # print(second_url[0])
                return "https://www.sec.gov" + second_url[0]
            else:
                return None
    return None


def insert_to_excel(target_url, index):
    excel_path = r"CEO names hand collect from S_1.xls"
    rb = open_workbook(excel_path)
    rd = copy(rb)
    ws = rd.get_sheet(0)
    ws.write(index+1,8,target_url)
    print(target_url)
    rd.save(excel_path)



def get_url(code_array):
    """
    get url by code_array
    :param code_array:
    :return:
    """
    # for code in code_array:
    # "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=s-1&dateb=&owner=exclude&count=40".format(code)
    for index in range(1,len(code_array)):
        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=s-1&dateb=&owner=exclude&count=40".format(
            code_array[index])
        resp = get_response(url)
        if not resp:
            continue
        next_link = parse_response(resp)
        if next_link:
            resp_of_target = get_response(next_link)
            target_url = parse_target_response(resp_of_target)
            if target_url:
                insert_to_excel(target_url,index)



def get_response(url):
    resp = WebRequest().get(url)
    return resp


def parse_response(resp):
    # print(resp.url)
    selector = etree.HTML(resp.text)

    filings = selector.xpath("//table[@class='tableFile2']/tr[last()]/td[1]/text()")
    if filings:
        if filings[0] == 'S-1' or filings[0] == 'S-1/A':
            next_link = selector.xpath("//table[@class='tableFile2']/tr[last()]/td[2]/a/@href")
            if next_link:
                next_link = "https://www.sec.gov" + next_link[0]
            else:
                next_link = None
            return next_link
    return None


def main():
    code_array = read_excel()
    get_url(code_array)


if __name__ == '__main__':
    main()
