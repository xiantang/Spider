import requests
import copyheaders
headers=b'''accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept-encoding:gzip, deflate, br
accept-language:zh,en-US;q=0.9,en;q=0.8
cache-control:max-age=0
upgrade-insecure-requests:1
user-agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'''

a=requests.get('https://shenzhen.anjuke.com/prop/view/A1151434098?from=filter-saleMetro&spread=commsearch_p&position=2&kwtype=filter',
               copyheaders.headers_raw_to_dict(headers)).text
print(a)