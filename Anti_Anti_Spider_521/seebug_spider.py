import requests
import copyheaders
import re
import execjs

def get_once():
    header={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    }
    url = 'https://www.seebug.org/vuldb/ssvid-92666'
    content=requests.get(url,headers=header)
    print(content.cookies)
    content=content.content

    js_content=''.join(re.findall('<script>(.*?)</script',content)).replace('eval','return')
    return js_content

def get_cookies(content):
    # js = r'''var x="dc@10@captcha@var@2@onreadystatechange@Path@__ph
    # antomas@reverse@for@@1519809366@@setTimeout@g8A@@if@_phantom@Array@8@document@charAt@Expires@zCzGRXXEn@457@06@location@Feb@KhSaKG@return@window@else@cookie@Wed@chips@attachEvent@replace@@function@l@3D@catch@false@addEventListener@0@while@try@@16@1500@i@length@@challenge@28@href@18@__jsl_clearance@cd@SQ2qW@DOMContentLoaded@GMT@join@e".replace(/@*$/,"").split("@"),y="4 22=21(){28(1c.i||1c.8){};4 32,1='31=c.16|27|';32=10(+[((-~[]+[(-~![]<<-~![])]>>(-~![]<<-~![]))-~~~[]-~-~{}-~~~[]-~-~{}+[]+[])]);4 1g=['f%23',[{}+[[], ~~!{}][~~{}]][27].13((-~~~[]+[]+[])+(5+[[], ~~!{}][~~{}])),'15',([-~[]-~[]-~[]-~[]][-~[]]+[]+[]).13(-~[-~~~[]-~(-~((-~[]+[(-~![]<<-~![])]>>(-~![]<<-~![]))))]),'1a',[{}+[]+[[]][~~[]]][27].13((-~[]+[(-~![]<<-~![])]>>(-~![]<<-~![]))),'33',[{}+[[]][~~!{}]][27].13(11)];a(4 2d=27;2d<1g.2e;2d++){32.9()[2d]=1g[2d]};32=32.36('');1+=32;e('18.2i=18.2i.1i(/[\\?|&]3-2g/,\\'\\')',2c);12.1e=(1+';14=1f, 2h-19-30 2:2b:17 35;7=/;');};h((21(){29{1b !!1c.26;}24(37){1b 25;}})()){12.26('34',22,25);}1d{12.1h('6',22);}",z=0,f=function(x,y){var a=0,b=0,c=0;x=x.split("");y=y||99;while((a=x.shift())&&(b=a.charCodeAt(0)-77.5))c=(Math.abs(b)<13?(b+48.5):parseInt(a,36))+y*c;return c},g=y.match(/\b\w+\b/g).sort(function(x,y){return f(x)-f(y)}).pop();while(f(g,++z)-x.length){};return(y.replace(/\b\w+\b/g, function(y){return x[f(y,z)-1]}));'''
    ctx = execjs.compile(content)
    # x = "dc@10@captcha@var@2@onreadystatechange@Path@__phantomas@reverse@for@@1519809366@@setTimeout@g8A@@if@_phantom@Array@8@document@charAt@Expires@zCzGRXXEn@457@06@location@Feb@KhSaKG@return@window@else@cookie@Wed@chips@attachEvent@replace@@function@l@3D@catch@false@addEventListener@0@while@try@@16@1500@i@length@@challenge@28@href@18@__jsl_clearance@cd@SQ2qW@DOMContentLoaded@GMT@join@e".replace(
    #     '/@*$/', "").split("@")
    new_fun = ctx.call('f')
    new_fun = new_fun.replace('document.cookie=', 'return')
    new_fun = new_fun.replace(
        "if((function(){try{return !!window.addEventListener;}catch(e){return false;}})()){document", '').replace(
        ".addEventListener('DOMContentLoaded',l,false);}else{document.attachEvent('onreadystatechange',l);}",
        '').replace(r"setTimeout('location.href=location.href.replace(/[\?|&]captcha-challenge/,\'\')',1500);",
                    '').replace('while(window._phantom||window.__phantomas){};', '')
    ctx = execjs.compile(new_fun)
    cookie=ctx.call('l')
    return cookie

def get_second(cookie):
    header_dict={}
    header_dict['User-Agent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    cookie=cookie.split(';')[0]
    # header_dict=copyheaders.headers_raw_to_dict(header)
    #Cookie:__jsluid=9536c75cdfa3e7e8c38d59bcbf4fc98b; csrftoken=YzAMB2QogF2YmzpruqWI5vdsfeH9PSx5; Hm_lvt_6b15558d6e6f640af728f65c4a5bf687=1519809319; __jsl_clearance=1519815987.506|0|4oUuV1OIf0a2NjV7i%2BWDH8%2FSw6w%3D; Hm_lpvt_6b15558d6e6f640af728f65c4a5bf687=1519816687
    header_dict['Cookie']='__jsluid=9536c75cdfa3e7e8c38d59bcbf4fc98b; '+cookie
    print(header_dict)
    code=requests.get('https://www.seebug.org/vuldb/ssvid-92666',header_dict).status_code
    print(code)
if __name__ == '__main__':
    con=get_once()
    cookie=get_cookies(con)
    get_second(cookie)