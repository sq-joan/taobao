# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 09:46:05 2018

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import jieba                      #分词库
from wordcloud import WordCloud   #词云库
import collections                # 词频统计库

# 存储销售量
saleVolumn_1,saleVolumn_2,saleVolumn_3,saleVolumn_4,saleVolumn_5,saleVolumn_6,saleVolumn_7=0,0,0,0,0,0,0
# 存储男、女西装销售量总集合，用于箱型图绘制
saleTotal_1,saleTotal_2,saleTotal_3,saleTotal_4,saleTotal_5,saleTotal_6,saleTotal_7=[],[],[],[],[],[],[]
# 存储标题，用于绘制词云
titles = ''

#########################################################################  
#                           读取数据
def saleCalculate(csvpath):
    #在python的函数中和全局同名的变量，如果你有修改变量的值就会变成局部变量，
    #在修改之前对该变量的引用就会出现没定义这样的错误，如果确定要引用全局变量，
    #并且要对它修改，必须加上global关键字。
    global saleVolumn_1,saleVolumn_2,saleVolumn_3,saleVolumn_4,saleVolumn_5,saleVolumn_6,saleVolumn_7
    global titles
    
    #读取csv文件内容
    file_men = open(csvpath,'r')
    lines = file_men.readlines()
    file_men.close()
    
    for line in lines:
        ziduan = line.split(',')
        price = float(ziduan[1])
        sale = int(ziduan[3])
        titles += ziduan[0]
        if price >= 0 and price <= 100: # 判断价格范围
            saleVolumn_1 = saleVolumn_1 + sale
            if sale == 0:
                saleTotal_1.append(sale) #不能对0取对数
            else:
                saleTotal_1.append(math.log(sale)) # 对销售量取对数，用于箱型图的显示
        elif price > 100 and price <= 200:
            saleVolumn_2 = saleVolumn_2 +sale
            if sale == 0:
                saleTotal_2.append(sale)
            else:
                saleTotal_2.append(math.log(sale))
        elif price > 200 and price <= 300:
            saleVolumn_3 = saleVolumn_3 +sale
            if sale == 0:
                saleTotal_3.append(sale)
            else:
                saleTotal_3.append(math.log(sale))
        elif price > 300 and price <= 400:
            saleVolumn_4 = saleVolumn_4 +sale
            if sale == 0:
                saleTotal_4.append(sale)
            else:
                saleTotal_4.append(math.log(sale))
        elif price > 400 and price <= 500:
            saleVolumn_5 = saleVolumn_5 +sale
            if sale == 0:
                saleTotal_5.append(sale)
            else:
                saleTotal_5.append(math.log(sale))
        elif price > 500 and price <= 1000:
            saleVolumn_6 = saleVolumn_6 +sale
            if sale == 0:
                saleTotal_6.append(sale)
            else:
                saleTotal_6.append(math.log(sale))
        else:
            saleVolumn_7 = saleVolumn_7 +sale
            if sale == 0:
                saleTotal_7.append(sale)
            else:
                saleTotal_7.append(math.log(sale))
    
saleCalculate('.\\data\\xizhuang_men.csv')
sale_men = [saleVolumn_1,saleVolumn_2,saleVolumn_3,saleVolumn_4,saleVolumn_5,saleVolumn_6,saleVolumn_7]
# 置空
saleVolumn_1,saleVolumn_2,saleVolumn_3,saleVolumn_4,saleVolumn_5,saleVolumn_6,saleVolumn_7=0,0,0,0,0,0,0
titles_men = titles # 男西装标题集合
titles = ''
saleCalculate('.\\data\\xizhuang_women.csv')
sale_women = [saleVolumn_1,saleVolumn_2,saleVolumn_3,saleVolumn_4,saleVolumn_5,saleVolumn_6,saleVolumn_7]
titles_women = titles # 女西装标题集合

#########################################################################  
#                           价格-销售量条形图
# x轴坐标标度
scope = ('0-100','100-200','200-300','300-400','400-500','500-1000','>1000')
index = np.arange(7)
# 设置柱形图宽度
bar_width = 0.4
# 绘制男西装销售量
rects_men = plt.bar(index , sale_men, width=0.4 , color='y', label = 'men')
# 绘制女西装销售量
rects_women = plt.bar(index +  bar_width, sale_women, width=0.4 , color='b', label = 'women')
# X轴标题
plt.xticks(index + bar_width,scope)
# Y轴范围
plt.ylim(ymax=250000, ymin=0)
# 图例显示在图表下方
plt.legend(loc = 1, ncol = 1)
# 添加数据标签
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
        # 柱形图边缘用白色填充，纯粹为了美观
        rect.set_edgecolor('white')
        
add_labels(rects_men)
add_labels(rects_women)
# 设置横轴、纵轴名称
plt.xlabel('price')
plt.ylabel('sale')

plt.savefig('.\\output\\sale_bar.png') # 图表输出到本地
plt.show()

#########################################################################  
#                           价格-销售量箱形图
fig = plt.figure()  # 创建画布
ax = plt.subplot()  # 创建作图区域
# 蓝色矩形的红线：50%分位点是4.5,上边沿：25%分位点是2.25,下边沿：75%分位点是6.75
ax.boxplot([saleTotal_1, saleTotal_2, saleTotal_3,saleTotal_4,saleTotal_5,saleTotal_6,saleTotal_7])
# 修改x轴下标
ax.set_xticklabels(['0-100', '100-200', '200-300', '300-400', '400-500', '500-1000', '>1000'])
# 设置横轴、纵轴名称
plt.xlabel('price')
plt.ylabel('sale(log)')

plt.savefig('.\\output\\sale_box.png')
plt.show()

#########################################################################  
#                           按标题词频作词云图
def wcTitle(title,picName):
    cut_text = jieba.cut(title) # 分词
    object_list = []
    remove_words = [u'的', u'，',u'和', u'是', u'随着', u'对于', u'对',u'等',u'能',u'都',u'。',u' ',u'、',u'中',u'在',u'了',
                    u'通常',u'如果',u'我们',u'005d',u'西装',u'外套'] # 自定义去除词库
    for word in cut_text: # 循环读出每个分词
        if word not in remove_words: # 如果不在去除词库中
            object_list.append(word) # 分词追加到列表
#    result = "/".join(object_list) # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
    # 词频统计
    word_counts = collections.Counter(object_list) # 对分词做词频统计
    # 需要定义font_path，否则出现乱码
    wc = WordCloud(font_path=r"F:\MyDownloads\Download\spyder_code\taobaoxizhuang\Monaco Yahei.ttf",background_color='white',width=800,height=600,max_font_size=50,
                   max_words=200)
#    wc.generate(result)
    wc.generate_from_frequencies(word_counts) # 从字典生成词云
    wc.to_file(picName) # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰
    # 显示图片
#    plt.figure("词云图") # 指定所绘图名称
    plt.imshow(wc)       # 以图片的形式显示词云
    plt.axis("off")      # 关闭图像坐标系
    plt.show()
wcTitle(titles_men,'.\\output\\wc_men.png')
wcTitle(titles_women,'.\\output\\wc_women.png')