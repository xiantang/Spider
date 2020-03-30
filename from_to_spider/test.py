from  selenium import webdriver
from multiprocessing import Pool
import time
from xlrd import open_workbook
from xlutils.copy import copy
import re
driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.distancefromto.net/')
from_=driver.find_element_by_id('distancefrom')
from_.send_keys('Pittsfield')
goto_ = driver.find_element_by_id('distanceto')
goto_.send_keys('Los Angeles')
submit=driver.find_element_by_id('hae')
submit.click()

time.sleep(5)
print(driver.find_element_by_id('totaldistancekm').get_attribute('value'))

# distance=re.findall('id="drvDistance">(.*?)</span>',driver.page_source)
# print(distance)
driver.quit()
