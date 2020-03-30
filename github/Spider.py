from lxml import etree

from Login import Login


class Spider(object):

    def __init__(self,email,password):

        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.email = email
        self.password = password
        self.foller_url = 'https://github.com/{name}?tab=followers'
        self.login = Login()
        self.session = self.login.login(email, password)
        self.set = set()


    def re_login(self):
        self.session = self.login.login(self.email,self.password)

    def is_login(self):
        return self.login.is_login()

    def get_follers(self,name):
        if name not in self.set:
            print("find user! "+name)
            self.set.add(name)
        else:
            return
        url =self.foller_url.format(name=name)
        response =self.session.get(url,headers=self.headers)
        selector = etree.HTML(response.text)
        list_ = selector.xpath('//a[@data-hovercard-type="user"]/@href')
        ll = []
        for li in list_:
            ll.append(li.replace("/",''))
        list_ = list(set(ll))
        print("user name :" +name +" followers nums :"+str(len(list_)))
        for ll in list_:
            self.get_follers(ll)





    def run(self):
        self.get_follers("xiantang")

if __name__ == '__main__':
    spider = Spider(email='zhujingdi1998@gmail.com', password='')
    # print(spider.is_login())
    spider.run()
