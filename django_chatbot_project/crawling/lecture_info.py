from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json
import pymysql
from bs4 import BeautifulSoup
import time

FIND_NUM = 1
lecture_link = list()
fail_link = list()
lecture_NO = list()
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
            lecture_link.append('https://everytime.kr' + lectureID) #강의별 강의평가 페이지 접속
print(lecture_link)
for lecture_list in soup.find_all('div', attrs={'class', 'list'}):
        for lecture_tbody in lecture_list.find_all('tbody'):
            for lecture_tr in lecture_tbody.find_all('tr'):
                #for lecture_td in lecture_tr.find_all('td'):
                lecture_num = lecture_tr.select('td')[0].text
                lecture_NO.append(lecture_num)
            print(lecture_NO)



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
            professor = side_head.select('p')[1]
            class_professor = professor.select('span')[0].text
            lecture.append(class_title) #강의 이름
            lecture.append(class_professor) #교수명

            length = len(lecture_NO)
            while i < length :
                lecture_number = lecture_NO[i]
                lecture.append(lecture_number)
                i+=1
                break


        for side_article in soup.find_all('div', attrs={'class', 'side article'}):
            detail_result = []
            for rating in side_article.find_all('div', attrs={'class', 'rating'}):
                #for lecture_rate in rating.find_all('div', attrs={'class', 'rate'}):
                star = rating.select('span')[0].text #총 별점
                lecture.append(star)
            #for empty in side_article.find_all('div', attrs={'class', 'empty'}):

            if side_article.find_all('div', attrs={'class', 'empty'}):
                print("강의평이 없습니다.")

            elif side_article.find_all('div', attrs={'class', 'details'}):
                print("강의평이 있습니다.")
                for details in side_article.find_all('div', attrs={'class', 'details'}):
                    project = details.select('p')[0]
                    lecture_project = project.select('span')[0].text

                    team = details.select('p')[1]
                    lecture_team = team.select('span')[0].text

                    score_rate = details.select('p')[2]
                    lecture_score = score_rate.select('span')[0].text

                    check = details.select('p')[3]
                    lecture_check = check.select('span')[0].text

                    exam = details.select('p')[4]
                    lecture_exam = exam.select('span')[0].text

                    detail_result.append(lecture_project)
                    detail_result.append(lecture_team)
                    detail_result.append(lecture_score)
                    detail_result.append(lecture_check)
                    detail_result.append(lecture_exam)
                    db = pymysql.connect(host='eunmiri-rds-demo-mysql2.ckcrvyfxpuwm.ap-northeast-2.rds.amazonaws.com', user='eunmiri', passwd='eunmiri805!', db='eunmiridb')
                    cursor = db.cursor()
                    sql = '''INSERT INTO eunmiridb.lecture_info(lecture_number, lecture, professor, project, team, score, lecture_check, lecture_exam) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (lecture[2], lecture[0], lecture[1], detail_result[0], detail_result[1], detail_result[2], detail_result[3], detail_result[4])
                    cursor.execute(sql)
                    db.commit()

                    #print(detail_result)


        for articles in soup.find_all('div', attrs={'class', 'articles'}):
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
        print(detail_result)

    except Exception as e:
        print(e)
        fail_link.append(url)
        continue


driver.close()