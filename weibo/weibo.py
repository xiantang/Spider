import requests
import re
import time
import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='weibo', charset='utf8')
cursor = conn.cursor()
#链接数据库
def download(url,retry=0):  #下载函数
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

        # proxies=proxy.retun_proxy()
    try: #try异常处理
        html_json = requests.get(url,
                                 # proxies=proxy.return_(),
                                 headers=header, timeout=2
                                 ).json()
        return html_json
    except:
        retry+=1
        time.sleep(1)
        download(url,retry) #如果失败递归
        if retry==10:
            return None  #返回空



def get_weibo_id():
    for i in range(1, 500):
        print("第",i,"页")
        html_json = download(
            "https://m.weibo.cn/api/container/getIndex?type=uid&value=1223178222&containerid=1076031223178222&page={}".format(
                i))
        if html_json == None:
            print("第"+str(i)+"条微博爬取失败")
            continue

        id_list = html_json["data"]['cards']
        # print(html_json)
        for id_count in id_list:
            # print(id["itemid"])
            id = id_count["itemid"][-16:] #id获取  构造url


            try:
                like_count=id_count['mblog']['attitudes_count']
                text=id_count['mblog']['text']
                comments_count=id_count['mblog']['comments_count']
                reposts_count = id_count['mblog']["reposts_count"]
                created_at=id_count['mblog']["created_at"]
                text = ''.join(re.findall(r'[\u4e00-\u9fa5]+', text))#微博内容 #正则提取汉字
            except:
                comments_count=0
                like_count=0
                text=""
                created_at=""
                reposts_count=0
            print("---------------------------------")
            print(text)
            print("---------------------------------")

            url = "https://m.weibo.cn/api/comments/show?id={}&page=".format(id) #根据ID 构建url
            sql="INSERT original VALUES('%s','%d','%d','%d','%s')"%(text,int(like_count),int(reposts_count),int(comments_count),created_at)
            insert_to_db(sql)#插入数据库
            get_comments(url,text)


def get_comments(url,text):#获取评论
    # pool = Pool(processes=1)
    #
    # for i in range(1, 51):
    #     pool.apply_async(print_, (url, i,text,))
    for i in range(1,51):
        print_(url, i,text)


def print_(url, i,text):

        format_url = url + str(i)
        commit_json = download(format_url)
        if commit_json == None:
            print("没有评论")
            pass
        else:
            try:    #获取评论信息
                commit_list = commit_json['data']['data']
                for commit in commit_list:
                    created_at = commit["created_at"]
                    screen_name = commit['user']['screen_name']
                    like_counts = commit["like_counts"]
                    commit = commit["text"]

                    frist = re.sub("<span.*?</span>", "", commit)
                    commit_text = re.sub("<a.*?</a>", "", frist)#去除无关的信息

                    print(screen_name)  # 名字
                    print(commit_text)  # 评论内容

                    sql = "INSERT comment VALUES('%s','%s','%s','%d','%s')" % (
                        text, screen_name, commit_text, int(like_counts), created_at)
                    insert_to_db(sql)
            except KeyError as e:
                print(e)


def insert_to_db(sql): #插入数据库
    try:
        cursor.execute(sql)
        conn.commit()
    except pymysql.err.ProgrammingError as e:
        print(e)
    except:
        pass
if __name__ == '__main__':
    get_weibo_id()
