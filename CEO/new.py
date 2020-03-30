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
    excel_path = r"zipvode court district.xls"
    rb = open_workbook(excel_path)
    sheet_name = rb.sheet_names()[0]
    sheet_1 = rb.sheet_by_name(sheet_name)
    rows = sheet_1.nrows
    code_array = []

    for i in range(1000, rows):
        element = sheet_1.row_values(i)[1]
        if element != "":
            if type(element) is str:
                pass
            else:
                element = str(int(element))
            code_array.append([element,i])
    return code_array




def insert_to_excel(target_url, index):
    excel_path = r"zipvode court district.xls"
    rb = open_workbook(excel_path)
    rd = copy(rb)
    ws = rd.get_sheet(0)
    ws.write(index,2,target_url)
    print(index,target_url)
    rd.save(excel_path)



def get_url(code_array):
    """
    get url by code_array
    :param code_array:
    :return:
    """
    # for code in code_array:
    # "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=s-1&dateb=&owner=exclude&count=40".format(code)
    # for index in range(1,len(code_array)):
    #     url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=s-1&dateb=&owner=exclude&count=40".format(
    #         code_array[index])
    #     resp = get_response(url)
    #     if not resp:
    #         continue
    #     next_link = parse_response(resp)
    #     if next_link:
    #         resp_of_target = get_response(next_link)
    #         target_url = parse_target_response(resp_of_target)
    #         if target_url:
    #             insert_to_excel(target_url,index)
    for ele in code_array:
        url = "http://www.uscourts.gov/court-locator/zip/{}/court/district".format(ele[0])
        resp =get_response(url)
        if not  resp:
            continue
        else:
            selector=etree.HTML(resp.text)
            if selector:
                resp=selector.xpath("//p[@class='grouped-court']/a/text()")
                if resp:
                    result=resp[0].strip()
                    insert_to_excel(result,ele[1])
                else:
                    continue
def get_response(url):
    resp = WebRequest().get(url)
    return resp





def main():
    code_array = read_excel()


    get_url(code_array)


if __name__ == '__main__':
    main()
