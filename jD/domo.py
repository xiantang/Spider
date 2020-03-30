import requests
from  lxml import etree
header={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}
content=requests.get("https://www.jd.com/allSort.aspx",
                   headers=header).text
selector=etree.HTML(content)
count=0
lis=[]
for i in selector.xpath("/html/body/div[5]/div[2]/div[1]/div[2]/div[1]/div"):
    for j in i.xpath("./div[2]/div[3]/dl/dd/a"):
        url=j.xpath("./@href")[0]

        if 'html?cat=' in url:
            lis.append(url)
            print(url)
            print(j.xpath("./text()"))
        count+=1
print(len(lis))
    #/html/body/div[5]/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]
    #/html/body/div[5]/div[2]/div[1]/div[2]/div[1]/div[11]/div[2]/div[3]
# print(content)