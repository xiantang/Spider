import requests
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
print(requests.get('https://www.jinfuzi.com/simu/list_w1_p10.html',headers=header).text)