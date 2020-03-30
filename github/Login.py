import requests
from lxml import etree

try:
    import cookielib
except:
    import http.cookiejar as cookielib


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.profileUrl = 'https://github.com/settings/profile'
        self.session = requests.Session()

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')
        return token

    def login(self, email, password):
        token = self.token()[1]
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token':token ,
            'login': email,
            'password': password,
            'webauthn-support': 'supported'
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        # if response.status_code == 200:
        #     self.dynamics(response.text)
        if response.status_code != 200:
            raise Exception
        response = self.session.get(self.profileUrl, headers=self.headers)
        if response.status_code != 200:
            raise Exception
        return self.session

    def is_login(self):
        response = self.session.get(self.profileUrl, headers=self.headers)
        selector = etree.HTML(response.text)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')
        if(len(name) == 0):
            return False
        else:return True


    def profile(self, html):
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)



if __name__ == "__main__":
    login = Login()
    # 输入自己email账号和密码
    session = login.login(email='zhujingdi1998@gmail.com', password='')
    print(login.is_login())
