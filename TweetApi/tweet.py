import tweepy
import json

consumer_key = "V8b7S88NhvsRiLX0krPRGEgEt"
consumer_secret = "n9kIfQ85s2zGOh1EyeT3oejjGGoINVbQn2ksHOy3Jt5jF0udr6"
access_token = "903279992796135427-uUYUCmRdtqOW16h3XQJX3IC2UaGdQNZ"
access_token_secret = "2LtD1YHywdmbeOZliOdslT5VxdRPPuA9Jd5KagOReK9p0"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, proxy='127.0.0.1:1080')
search_results = api.search(q='python', count=100)

# 对对象进行迭代

for tweet in search_results:
    # tweet还是一个对象,推特的相关信息在tweer._json里
    # 这里是检测消息是否含有'text'键,并不是所有TWitter返回的所有对象都是消息(有些可能是用来删除消息或者其他内容的动作--这个没有确认),区别就是消息对象中是否含有'text'键
    if 'text' in tweet._json:
        print(tweet._json['text'])

        print('-------------')
        # 这里是把内容给打印出来了,如果需要保存到文件需要用json库的dumps函数转换为字符串形式后写入到文件中
        # 例如 :output_file.write(json.dumps(tweet._json))