# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 09:39:00 2018

@author: Administrator
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import re

titles,prices,shops,sales = [],[],[],[]

#csvFile = open("xizhuang_women.csv","w",newline='') # newline=''解决空白行问题
csvFile = open("xizhuang_men.csv","w",newline='')
writer = csv.writer(csvFile)
writer.writerow(('title','price','shop','sale'))

def getInfo(page):
#    url_women = "https://re.taobao.com/search?&extra=&refpid=420435_1006&keyword=%E8%A5%BF%E8%A3%85%20%E5%A5%B3&_input_charset=utf-8&page="+str(page)+"&isinner=0&rewriteKeyword"
    url_men = "https://re.taobao.com/search?&extra=&refpid=420435_1006&keyword=%E8%A5%BF%E8%A3%85%20%E7%94%B7&_input_charset=utf-8&page="+str(page)+"&isinner=0&rewriteKeyword"
    
    #配置headless
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless() #设置为headless模式
    driver = webdriver.Firefox(firefox_options=fireFoxOptions)
    time.sleep(2)
#    driver.get(url_women)
    driver.get(url_men)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    titles = soup.findAll('span',class_='title')
    prices = soup.findAll('span',class_='pricedetail')
    shops = soup.findAll('span',class_='shopNick')
    sales = soup.findAll('span',class_='payNum')
    print(len(titles))
    for i in range(len(titles)):
        saleNum = re.findall(r"\d+\.?\d*",sales[i].get_text()) #提取销售数量数值
        writer.writerow((titles[i].get_text(),prices[i].find('strong').get_text(),shops[i].get_text(),''.join(saleNum)))
        
    driver.quit() # 表示关闭浏览器

for page in range(0,10): # 爬取前10页
    print ("正在爬取第{}页".format(page))
    getInfo(page)

csvFile.close() # 关闭文件
print("完成！")