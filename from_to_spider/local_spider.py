from  selenium import webdriver
from multiprocessing import Pool
import time
from xlrd import open_workbook
from xlutils.copy import copy
import re



def get_from_excel():
    path = r'C:\Users\dd\Documents\GitHub\Spider\from_to_spider\location and distance.xls'
    rb = open_workbook(path)
    sheet_name = rb.sheet_names()[0]
    sheet_1 = rb.sheet_by_name(sheet_name)
    rows = sheet_1.nrows
    fromlist = sheet_1.row_values(0)
    not_found_list=[]
    for i in range(11, rows):#列

        # print(sheet_1.row_values(i))
        for j in range(1,len(sheet_1.row_values(i))):#行
            # print(sheet_1.row_values(i)[j])
            if sheet_1.row_values(i)[j] =='':
                tocity = sheet_1.row_values(i)[1]
                form_city=sheet_1.row_values(0)[j]
                not_found_list.append([i,j,tocity,form_city])

    # print(not_found_list)
    print(len(not_found_list))
    pool=Pool(processes=8)
    for i in not_found_list:
        pool.apply_async(get_content, (i[0], i[1], i[2], i[3],))
    pool.close()
    pool.join()
    # for i in range(1081, rows):
    #     tocity = sheet_1.row_values(i)[1]
    #     pool = Pool(processes=8)
    #     for j in range(2,len(fromlist)):
    #         pool.apply_async(get_content, ( i,j,fromlist[j], tocity,))
    #     pool.close()
    #     pool.join()
def get_content(i,j,from_city,tocity):
=======
    for dd in not_found_list:
        print(dd)
        # pool = Pool(processes=8)
        # for j in range(2,len(fromlist)):
        #     # pool.apply_async(get_content, ( i,j,fromlist[j], tocity,))
        # pool.close()
        # pool.join()
def get_content(i,j,from_city,tocity):


        driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.set_page_load_timeout(40)
        # driver.get('http://www.distancebetweencities.us/result.php?fromplace={}&toplace={}'.format(from_city,tocity))

        # driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.get('https://www.distancefromto.net/')
        from_ = driver.find_element_by_id('distancefrom')
        from_.send_keys(from_city)
        goto_ = driver.find_element_by_id('distanceto')
        goto_.send_keys(tocity)
        submit = driver.find_element_by_id('hae')
        submit.click()

        # driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.get('https://www.distancefromto.net/')
        from_ = driver.find_element_by_id('distancefrom')
        from_.send_keys(from_city)
        goto_ = driver.find_element_by_id('distanceto')
        goto_.send_keys(tocity)
        submit = driver.find_element_by_id('hae')
        submit.click()
        time.sleep(3)
        distance=driver.find_element_by_id('totaldistancekm').get_attribute('value')
        print(distance)
        driver.quit()
        write_to_excel(i,j,''.join(distance))

def write_to_excel(x,y,distance):
    rb=open_workbook(r'C:\Users\战神皮皮迪\Documents\GitHub\Spider\from_to_spider\location and distance.xls')
    wb = copy(rb)
    ws=wb.get_sheet(0)
    ws.write(x,y,distance)
    wb.save(r'C:\Users\战神皮皮迪\Documents\GitHub\Spider\from_to_spider\location and distance.xls')
    print('write_to_excel')
    # driver.quit()
if __name__ == '__main__':

    get_from_excel()
    # write_to_excel(di)
#     pool = Pool(processes=8)
#     for i in range(10):
#         pool.apply_async(get_content, (i,))
#     pool.close()
#     pool.join()
# i=1
# get_content(i)



