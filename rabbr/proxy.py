def return_():
    # 要访问的目标页面
    targetUrl = "http://test.abuyun.com/proxy.php"
    # targetUrl = "http://proxy.abuyun.com/switch-ip"
    # targetUrl = "http://proxy.abuyun.com/current-ip"

    # 代理服务器

    proxyHost = "http-pro.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息
    proxyUser = "HD2V7LPM57I930UP"
    proxyPass = "D729689756557530"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies
# resp = requests.get(targetUrl, proxies=proxies)
#
# print(resp.status_code)
# print(resp.text  )
