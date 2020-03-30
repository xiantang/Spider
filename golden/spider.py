from  Spider.base_spider.spider import base_spider
import time
class spider(base_spider):
    def get(self):
        a=time.time()
        for i in range(1,10):
            con = self.get_content('https://www.jinfuzi.com/simu/list_d4_w1_p{}.html'.format(i))['html']
            print(len(con))
        print(time.time()-a)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
if __name__ == '__main__':
    S=spider(header=header)
    aaaaaa
    S.get()