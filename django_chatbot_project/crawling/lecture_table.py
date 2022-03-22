from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json
from bs4 import BeautifulSoup
import datetime
import time

FIND_NUM = 1
lecture_link = list()
fail_link = list()
comment_text = list()
page_number = 1
BOARD_URL = 'https://everytime.kr/timetable'
#def tree():
#    return defaultdict(tree)

driver = webdriver.Chrome('/Users/USER/Downloads/chromedriver_win32/chromedriver')
#driver = webdriver.PhantomJS()

driver.implicitly_wait(3)
driver.get('https://everytime.kr/login')
driver.find_element_by_name('userid').send_keys('vicrudal')
driver.find_element_by_name('password').send_keys('rudal6360!!')

driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()
driver.find_element_by_xpath('//*[@id="menu"]/li[2]/a').click()

driver.find_element_by_xpath('//*[@id="container"]/ul/li[1]').click()





for i in range(FIND_NUM):
    time.sleep(7)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for url in soup.findAll('td'):
        for find_url in url.findAll('a', attrs={'class', 'star'}):

            content = find_url.get('href')

            lecture_link.append('https://everytime.kr' + content)

            #print(lecture_link)

for url in lecture_link:
    #time_now = datetime.datetime.now()
    #json_data = dict()

    #json_data['comment_text'] = list()
    try :
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')


        for articles in soup.find_all('div', attrs={'class','articles'}):
            lecture_eval = []
            article = articles.select('article')[0]
            star_ = article.select('p')[0]
            star = star_.select('span')[0]
            #starrate = star.selcet('span')[0]

            re = star.find('span')

            text_ = article.select('p')[2].text
            lecture_eval.append([star,text_])
        print(lecture_eval)



        #for comment in soup.find_all('div', attrs = {'class','side article'}):
        #    for article in comment.find_all('div', attrs = {'class', 'article'}):
        #        text = article.find_all('p', attrs = {'class','text'}).get_text()
        #        print(text)
        #        #for text in article.findALL('p', attrs = {'class','text'}):
        #            #print(text.get.text)


    except Exception as e:
        print(e)
        fail_link.append(url)
        continue


