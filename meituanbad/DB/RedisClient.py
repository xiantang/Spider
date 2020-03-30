import redis
import json
import random
class RedisClient(object):

    def __init__(self,name,host,port):
        '''

        :param name:
        :param host:
        :param port:
        '''
        self.name=name
        self.__conn=redis.Redis(host=host,port=port,db=0)

    def get(self):
        '''
        随机返回一个值
        :return:
        '''
        key=self.__conn.hgetall(name=self.name)
        rkey=random.choice(list(key.keys())) if key else None
        if isinstance(rkey,bytes):
            return rkey.decode("utf-8")
        else:
            return key

    def put(self,key):

        '''

        :param key:
        :return:
        '''
        key=json.dumps(key) if isinstance(key,(dict,list)) else key
        return self.__conn.hincrby(self.name,key,1)

    def delete(self,key):
        '''
        删除
        :param key:
        :return:
        '''
        self.__conn.hdel(self.name,key)
    def getAll(self):
        return [key.decode("utf-8") for key in  self.__conn.hgetall(self.name).keys()]


    def getvalue(self,key):
        '''
        获取一个指定的键值
        :param key:
        :return:
        '''
        key=json.dumps(key)
        value=self.__conn.hget(self.name,key)
        return value if value else  None

    def changeTable(self,name):
        '''
        更换表
        :param name:
        :return:
        '''
        self.name=name

    def get_status(self):
        '''
        返回一个键的长度
        :return:
        '''
        return  self.__conn.hlen(self.name)

    def pop(self):
        '''
        pop a item
        :return:
        '''
        key=self.get()
        if key:
            self.__conn.hdel(self.name,key)
        return key

    def exists(self,key):
        '''
        检验是否存在
        :param key:
        :return:
        '''
        return self.__conn.hexists(self.name,key)

if __name__ == '__main__':
    test=RedisClient('useful_proxy_http','',6379)
    print(test.getAll())