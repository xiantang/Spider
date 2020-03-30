import requests
import re
import execjs
import copyheaders
def get_521_content():
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    req=requests.get('https://www.seebug.org/vuldb/ssvid-92666',headers=headers)
    cookies=req.cookies

    cookies='; '.join(['='.join(item) for item in cookies.items()])
    txt_521=req.text
    txt_521=''.join(re.findall('<script>(.*?)</script>',txt_521))
    return (txt_521,cookies)

def fixed_fun(function):
    func_return=function.replace('eval','return')
    content=execjs.compile(func_return)
    evaled_func=content.call('f')
    # print(evaled_func)
    mode_func=evaled_func.replace('while(window._phantom||window.__phantomas){};','').\
        replace('document.cookie=','return').replace(';if((function(){try{return !!window.addEventListener;}','').\
        replace("catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',l,false);}",'').\
        replace("else{document.attachEvent('onreadystatechange',l);}",'').replace(r"setTimeout('location.href=location.href.replace(/[\?|&]captcha-challenge/,\'\')',1500);",'')
    content = execjs.compile(mode_func)
    cookies=content.call('l')
    __jsl_clearance=cookies.split(';')[0]
    return __jsl_clearance

def cookie_dict(js,id):
    dict={}
    js=js.split('=')
    id=id.split('=')
    dict[js[0]]=js[1]
    dict[id[0]] = id[1]
    return dict
if __name__ == '__main__':
    func=get_521_content()
    content=func[0]
    cookie_id=func[1]
    cookie_js=fixed_fun(func[0])
    dicted_cookie=cookie_dict(cookie_js,cookie_id)
    headers={
             'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
             'Cookie': cookie_id+';'+cookie_js}
    req=requests.get('https://www.seebug.org/vuldb/ssvid-92666',
                      headers=headers)
    print(req.status_code)
    print(len(req.text))


