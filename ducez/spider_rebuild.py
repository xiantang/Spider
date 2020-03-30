import re
from urllib.parse import parse_qs

import requests
from lxml import etree

URL = "http://114.112.74.138/"



def get_html_text(url: str):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            if "抱歉，指定的主题不存在或已被删除或正在被审核" in response.text:
                return False
            else:
                return response.text
        else:
            return False
    except:
        return False


def get_sections_url_list(url: str) -> list:
    response = get_html_text(url)
    if response:
        selector = etree.HTML(response)
        url_element = selector.xpath("//td[@class='fl_icn']")
        sections_url = []
        for element in url_element:
            section_url = element.xpath("./a/@href")[0]
            sections_url.append(section_url)
        return sections_url


# 获取板块中的post
def get_post_url_list(sections_url: list) -> list:
    url_list = []
    # print(sections_url)
    for section_url in sections_url:
        complete_url = URL + section_url
        for page in range(1, 4):
            url = complete_url + "&page=" + str(page)
            response = get_html_text(url)
            if response:
                selector = etree.HTML(response)
                url_crawl_list = selector.xpath('//a[@class="s xst"]/@href')
                url_list += url_crawl_list
    return url_list


def get_post_content(selector):
    content_info  = selector.xpath("//td[@class='t_f']")
    content_list = []
    for content in content_info:
        content_id = content.xpath("./@id")[0].split("_")[1]
        content_res = content.xpath("./text()")
        content_list.append({"content_id":content_id,"content":content_res})
    return content_list

def get_post_data(post_url):
    complete_url = URL + post_url
    response = get_html_text(complete_url)
    if response:
        selector = etree.HTML(response)
        title = selector.xpath("//title/text()")[0]
        link = selector.xpath("//link/@href")[0]
        t_id = parse_qs(link)['tid'][0]
        # 获取post中的用户数据
        post_user_list = get_post_user_list(selector)
        # 获取内容数据
        post_content_list = get_post_content(selector)
        for i in range(len(post_content_list)):
            post_content_list[i]["user_name"] = post_user_list[i]["user_name"]
            post_content_list[i]["user_id"] = post_user_list[i]["user_id"]
        post_content_info={
            "title":title,
            "link":link,
            "t_id":t_id,
            "author":post_content_list[0]["user_name"],
            "content":post_content_list[0]["content"],
            "comments":post_content_list[:]
        }
        return post_content_info

def get_post_user_list(selector):
    user_info = selector.xpath('//div[@class="pi"]/div[@class="authi"]')
    user_list = []
    for user_sel in user_info:
        user_name = user_sel.xpath("./a/text()")[0]
        user_id = parse_qs(user_sel.xpath("./a/@href")[0])["uid"][0]
        user_list.append({'user_id': user_id, 'user_name': user_name})
    return user_list


def main():
    # 获取post_data["title"]板块的地址列表
    sections_url = get_sections_url_list(URL)
    post_url_list = get_post_url_list(sections_url)
    for post_url in post_url_list:
        post_data = get_post_data(post_url)
        if post_data:

            # print( "{title}\t{link}\t{t_id}\t{author}".format(
            #     title = post_data["title"],
            #     link = post_data["link"],
            #     t_id = post_data["t_id"],
            #     author = post_data["author"],
            #     # content = post_data['content']
            # ))

            for comment in post_data["comments"]:
                comment_str = "{content_id}@{user_id}@{user_name}"\
                    .format(content_id = comment["content_id"],
                            user_name = comment["user_name"],
                            user_id = comment["user_id"])
                print(comment_str)

if __name__ == '__main__':
    main()
