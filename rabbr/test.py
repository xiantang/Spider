import requests
import proxy
from lxml import etree
from fake_useragent import UserAgent
ua=UserAgent()
header_comment = {
    'User-Agent': ua.random,
    'Cookie':'_lxsdk_cuid=163057e2d4fc8-03370d242f56b8-7c117d7e-1fa400-163057e2d4fc8; _lxsdk=163057e2d4fc8-03370d242f56b8-7c117d7e-1fa400-163057e2d4fc8; _hc.v=8cd08b53-f19b-6289-b239-4ef97a2b76b5.1524805545; dper=e5b5aa8cba5ad90edcbd56145582c4ee31ed97e633d1b8cb40a1a946cb2549d7; ll=7fd06e815b796be3df069dec7836c3df; ua=%E5%92%B8%E7%B3%96_8951; ctu=12a017cea659512d0c8b94961d2e13e41cca89bd5be8c472b9f196ec6d9a228b; uamo=15868759135; cy=101; cye=wenzhou; s_ViewType=10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=163057e2d54-8c1-82e-dfe%7C%7C2365'
}

# //850753109
# []
# 33522959
# []
# 49804747
# []
# # 14957682
html=requests.get("http://www.dianping.com/shop/14957682/review_all",headers=header_comment,proxies=proxy.return_()).text
# selector = etree.HTML(html)
# sel = selector.xpath('//div[@class="reviews-items"]/ul/li')
# print(len(sel))
# print(len(html))

print(html)