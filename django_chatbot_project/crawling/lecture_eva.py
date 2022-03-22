from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json
from bs4 import BeautifulSoup
import time

FIND_NUM = 1
lecture_link = list()
fail_link = list()
TABLE_URL = 'https://everytime.kr/timetable'

driver = webdriver.Chrome('/Users/USER/Downloads/chromedriver_win32/chromedriver')
driver.implicitly_wait(3)
driver.get('https://everytime.kr/login')
driver.find_element_by_name('userid').send_keys('vicrudal')
driver.find_element_by_name('password').send_keys('rudal6360!!')
driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()
driver.find_element_by_xpath('//*[@id="menu"]/li[2]/a').click() #시간표 들어가기
driver.find_element_by_xpath('//*[@id="container"]/ul/li[1]').click() #강의목록 조회

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(0.5)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height


for i in range(FIND_NUM):
    time.sleep(7)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for content in soup.find_all('td'):
        for star in content.find_all('a', attrs={'class', 'star'}):
            lectureID = star.get('href')
            lecture_link.append('https://everytime.kr' + lectureID)
print(lecture_link)


for url in lecture_link:
    try:
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #title = soup.find('div', attrs={'class', 'side head'}).get_text()
        #print(title)

        for side_head in soup.find_all('div', attrs={'class', 'side head'}):
            lecture = []
            class_title = side_head.select('h2')[0].text
            lecture.append(class_title)


        for articles in soup.find_all('div', attrs={'class', 'articles'}):
            lecture_eval = []
            for article in articles.find_all('article'):
            #article = articles.select('article')[0]
                star_ = article.select('p')[0]
                for star in star_.select('span')[0]:
                    starrate = star.get('style')
                    lecture.append(starrate) #개별별점
                    #print(starrate)
                text_ = article.select('p')[2].text #강의평
                lecture.append(text_)
        print(lecture)

    except Exception as e:
        print(e)
        fail_link.append(url)
        continue


driver.close()