from  selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from  lxml import etree
driver=webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
driver.get("https://weibo.com/login.php?spm=a2107.1.0.0.392d11d9QLVdh5&entry=taobao&goto=https%3A%2F%2Flogin.taobao.com%2Faso%2Ftvs%3Fdomain%3Dweibo%26sid%3D4681f6e1d3c164c432e7a026129e4329%26target%3D68747470733A2F2F616C697A732E74616F62616F2E636F6D2F6C6F67696E2F63616C6C6261636B&goto2=https%3A%2F%2Falizs.taobao.com%2Flogin%2Fcallback")
time.sleep(3)
driver.find_element_by_name("username").send_keys("username")
driver.find_element_by_name("password").send_keys("password")
driver.find_element_by_xpath('//*[@id="pl_login_logged"]/div/div[7]/div[1]/a/span').click()
time.sleep(2)
element=WebDriverWait(driver,60).until(lambda driver :driver.find_element_by_xpath("//*[@id='J_Quick2Static']")).click()
driver.find_element_by_xpath('//*[@id="J_OtherLogin"]/a[1]').click()
driver.find_element_by_xpath('//*[@id="pl_login_logged"]/div[1]/div[2]/div[3]/div[1]/a/span').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="slider-container"]/div[1]/div/a').click()
html=driver.page_source
content=etree.HTML(html)
sel=content.xpath('//*[@id="app"]/div/div[4]/div[1]/div/div[2]/div/div[2]/div[2]/div/ul/li')
for i in sel:
    print(i.xpath('./p[2]/text()'))
    print(i.xpath('./p[3]/span[1]/text()'))
    #//*[@id="app"]/div/div[4]/div[1]/div/div[2]/div/div[2]/div[2]/div/ul/li[1]/p[4]
    print(i.xpath('./p[4]/text()'))
