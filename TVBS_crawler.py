#!/usr/bin/python
# #-*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pandas import Series,DataFrame
import pandas as pd
import numpy as np 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime
import re
import csv

df = pd.DataFrame() #創建空間
headerlist = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
           "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]

def supertaste3():

    hot = [24,22,23,26]

    for cate in hot:
        time.sleep(1)
        url = requests.get('https://supertaste.tvbs.com.tw/topic/'+str(cate)).text
        soup = BeautifulSoup(url, 'html.parser')

        for ele in soup.find('div', 'talk_article').find_all('li'):

            datelist = re.findall('(\d+)',ele.find('h5').text.strip()) #利用re正規式找出時間
            
            del datelist[3] #刪除時分秒
            del datelist[3]
            datestr = datelist[0] + datelist[1] + datelist[2] #接成字符串
        
            if datestr == time.strftime("%Y%m%d"): #如果為當日就存入
            
                a = pd.Series({"category":'熱門',"title":ele.find('div','txt').text.strip(),"href":'https://supertaste.tvbs.com.tw'+ele.find('a')['href']})
                global df
                df = df.append(a,ignore_index = True)
    print('食尚玩家 Done')

def TVBSeat5():

    #食尚玩家
    '''foodmap = ['台北','新北','桃園','新竹','苗栗','台中','彰化','雲林',
    '嘉義','台南','高雄','屏東','台東','花蓮','宜蘭','基隆','南投',
    '澎湖','金門','馬祖','綠島']'''
    
    foodmap = ['台北']

    for i in foodmap:

        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get('https://www.google.com')
        q  = driver.find_element_by_name('q')
        q.send_keys('site:supertaste.tvbs.com.tw '+i+' 美食')
        q.send_keys(Keys.RETURN)
    
        for p in range(3):

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for ele in soup.find('div', 'srg').find_all('div','r'):

                a = pd.Series({"category":'美食',"title":ele.find('h3').text.strip(),"href":ele.find('a')['href'],"category2":i})
                global df
                df = df.append(a,ignore_index = True)
        
            driver.find_element_by_link_text('下一頁').click()
        
            time.sleep(3)
    
        driver.close()
    print('食尚食物搜尋 Done')

def TVBStravel6():

    #食尚玩家
    '''sightmap = ['台北','新北','桃園','新竹','苗栗','台中','彰化','雲林',
    '嘉義','台南','高雄','屏東','台東','花蓮','宜蘭','基隆','南投',
    '澎湖','金門','馬祖','綠島']'''

    sightmap = ['台北']

    for i in sightmap:

        driver = webdriver.Chrome()
        driver.implicitly_wait(3)
        driver.get('https://www.google.com')
        q  = driver.find_element_by_name('q')
        q.send_keys('site:supertaste.tvbs.com.tw '+i+' 旅遊')
        q.send_keys(Keys.RETURN)
    
        for p in range(3):

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for ele in soup.find('div', 'srg').find_all('div','r'):
                if len(ele.find('h3').text.strip()) >13:
                    a = pd.Series({"category":'旅遊',"title":ele.find('h3').text.strip(),"href":ele.find('a')['href'],"category2":i})
                    global df
                    df = df.append(a,ignore_index = True)
        
            driver.find_element_by_link_text('下一頁').click()
        
            time.sleep(3)
    
        driver.close()
    print('食尚旅遊搜尋 Done')


if __name__ == '__main__':

  
       
    supertaste3()
    TVBSeat5()
    TVBStravel6()


    print(df) # 看看資料框的外觀

    df.to_csv('Result.txt')

	