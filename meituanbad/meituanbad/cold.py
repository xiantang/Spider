import csv
import matplotlib.pyplot as plt
import pickle
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
import jieba.analyse
csv_reader = csv.reader(open('D:\meituanbad\meituanbad\ductdetail.csv', encoding='utf-8'))
list_=[]
stopwords=['推荐']
for row in csv_reader:
    try:
        time=int(row[0].replace("\ufeff",""))
        if time>1514807085000 :

            list_.append(row[1])

    except Exception as e:
        print(e)

str_=''.join(list_)
print(str_)
# str_=''.join(list)
# new_str=""
# for i in jieba.cut(str_):
#     if i not in stopwords:
#         new_str+=i
# print(new_str)
try:
    # jieba.analyse.set_stop_words('你的停用词表路径')
    tags = jieba.analyse.extract_tags(str_, topK=100, withWeight=True)
    for v, n in tags:
        #权重是小数，为了凑整，乘了一万
        print (v + '\t' + str(int(n * 10000)))

except Exception as  e:
    print(e)



# backgroud_Image = plt.imread(r'下载.jpg')
# wc = WordCloud( background_color = 'white',    # 设置背景颜色
#                 mask = backgroud_Image,        # 设置背景图片
#                 max_words = 2000,            # 设置最大现实的字数
#                 stopwords = STOPWORDS,        # 设置停用词
#                 font_path = r'C:\Windows\Fonts\simkai.ttf',# 设置字体格式，如不设置显示不了中文
#                 max_font_size = 50,            # 设置字体最大值
#                 random_state = 30,            # 设置有多少种随机生成状态，即有多少种配色方案
#                 )
# wc.generate(
# )
# image_colors = ImageColorGenerator(backgroud_Image)
# wc.recolor(color_func = image_colors)
# plt.imshow(wc)
# plt.axis('off')
# plt.show()
# # plt.imsave("dd.jpg")
# img=wc.to_image()
# img.save("2018.jpg")
# fout = open('text.txt','wb')
# pickle.dump(text,fout)
# fout.close()