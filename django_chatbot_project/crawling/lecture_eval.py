from selenium import webdriver
from bs4 import BeautifulSoup
import pyautogui
import time
import pymysql
import math

FIND_NUM = 1
count = 0
sum_ = 0
std_deviation = 0
j = 0
lecture_link = list()
lecture_NO = list()
lecture_elearn = list()
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

driver.find_element_by_xpath('//*[@id="sheet"]/ul/li[3]/a').click()
driver.implicitly_wait(30)

pyautogui.moveTo(400, 650)
for i in range(1, 29):
    pyautogui.scroll(-30000)
    time.sleep(8)

for i in range(FIND_NUM):
    time.sleep(7)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for content in soup.find_all('td'):
        for star in content.find_all('a', attrs={'class', 'star'}):
            lectureID = star.get('href')
            lecture_link.append('https://everytime.kr' + lectureID) #강의별 강의평가 페이지 접속

    for lecture_list in soup.find_all('div', attrs={'class', 'list'}):
        for lecture_tbody in lecture_list.find_all('tbody'):
            for lecture_tr in lecture_tbody.find_all('tr'):
                #for lecture_td in lecture_tr.find_all('td'):
                lecture_num = lecture_tr.select('td')[0].text
                lecture_NO.append(lecture_num) #학수번호

    for elearning in soup.find_all('td', attrs={'class', 'small'}):
        elearn = elearning.get_text()
        if elearn == '원격수업(e-러닝)' or elearn == '원격수업(b-러닝)' or elearn == '서울권역대학 e-러닝 학점교류강좌':
           e_learning = 'YES'
           lecture_elearn.append(e_learning)
        else:
            e_learning = 'NO'
            lecture_elearn.append(e_learning)
print(lecture_elearn)
print(lecture_link)
print(lecture_NO)

for url in lecture_link:
    try:
        lecture = []
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #title = soup.find('div', attrs={'class', 'side head'}).get_text()
        #print(title)


        for side_head in soup.find_all('div', attrs={'class', 'side head'}):
            #lecture = []
            class_title = side_head.select('h2')[0].text
            professor = side_head.select('p')[1]
            class_professor = professor.select('span')[0].text
            lecture.append(class_title) #강의 이름
            lecture.append(class_professor) #교수명

            length = len(lecture_NO)
            while i < length :
                lecture_number = lecture_NO[i] #학수번호
                lecture.append(lecture_number)
                i+=1
                break

            e_length = len(lecture_elearn)
            while j < e_length :
                lecture_ELEARN = lecture_elearn[j]
                lecture.append(lecture_ELEARN)
                j+=1
                break


        for side_article in soup.find_all('div', attrs={'class', 'side article'}):
            detail_result = []
            lecture_eval = []
            for rating in side_article.find_all('div', attrs={'class', 'rating'}):
                #for lecture_rate in rating.find_all('div', attrs={'class', 'rate'}):
                star = rating.select('span')[0].text #총 별점
                star = float(star)
                lecture.append(star)
            #for empty in side_article.find_all('div', attrs={'class', 'empty'}):

            if side_article.find_all('div', attrs={'class', 'empty'}):
                print("강의평이 없습니다.")
                lecture_project = 'NONE'
                lecture_team = 'NONE'
                lecture_score = 'NONE'
                lecture_check = 'NONE'
                lecture_exam = 'NONE'
                detail_result.append(lecture_project)
                detail_result.append(lecture_team)
                detail_result.append(lecture_score)
                detail_result.append(lecture_check)
                detail_result.append(lecture_exam)

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

        for articles in soup.find_all('div', attrs={'class', 'articles'}):
            for article in articles.find_all('article'):
            #article = articles.select('article')[0]
                star_ = article.select('p')[0]
                for stars in star_.select('span')[0]:
                    starrate = stars.get('style')
                    #lecture.append(starrate) #개별별점
                    if starrate == 'width: 20%;':
                        real_rate = 5*0.2
                    elif starrate == 'width: 40%;':
                        real_rate = 5*0.4
                    elif starrate == 'width: 60%;':
                        real_rate = 5*0.6
                    elif starrate == 'width: 80%;':
                        real_rate = 5*0.8
                    else:
                        real_rate = 5
                    real_rate = float(real_rate)
                    #lecture.append(real_rate)

                    deviation = real_rate-star
                    deviation = math.fabs(deviation)
                    deviation = round(deviation, 2) #편차

                    variance = deviation*deviation
                    variance = round(variance, 4) #편차제곱

                    count += 1
                    sum_ += variance
                    sum_ = round(sum_, 4)
                    std_deviation = math.sqrt(sum_/count)
                    std_deviation = round(std_deviation, 4)
                    #variance = float(variance)
                    #sum_ = float(sum_)
                    #std_deviation = float(std_deviation)

                    if star == '0':
                        lecture_eval = []
                    text_ = article.select('p')[2].text #강의평
                    #lecture.append(text_)
                    lecture_eval.append(text_)

                #with open('lecture_eval.text', 'a', encoding='utf-8') as file:
                #    file.write('{0},{1}\n'.format(lecture[0], text_)) #강의평 파일 저장

                #db = pymysql.connect(host='eunmiri-rds-demo-mysql2.ckcrvyfxpuwm.ap-northeast-2.rds.amazonaws.com',
                #                     user='eunmiri', passwd='eunmiri805!', db='eunmiridb')
                #cursor = db.cursor()
                #sql = '''INSERT INTO eunmiridb.lecture_eval(lecture, star, eval) VALUES ('%s', '%s', '%s')''' % (
                #    lecture[0], real_rate, text_)
                #cursor.execute(sql)
                #db.commit()

        #print(std_deviation)
        if(std_deviation > 0.85):
            reputation = "BAD"
            print("이 강의는 호불호가 많이 갈립니다.")
        elif(std_deviation == 0):
            print("이 강의는 강의평이 없습니다.")
            reputation = "NONE"
        else:
            print("이 강의는 대체적으로 반응이 좋습니다.")
            reputation = "GOOD"

        db = pymysql.connect(host='eunmiri-rds-demo-mysql2.ckcrvyfxpuwm.ap-northeast-2.rds.amazonaws.com',
                             user='eunmiri', passwd='eunmiri805!', db='eunmiridb')
        cursor = db.cursor()
        sql = '''INSERT INTO eunmiridb.pyeong_lectureinfo1(lecture_number, lecture, professor, Total_star, project, team, score, lecture_check, lecture_exam, e_learning) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
            lecture[2], lecture[0], lecture[1], lecture[4], detail_result[0], detail_result[1], detail_result[2],
            detail_result[3], detail_result[4], lecture[3])
        cursor.execute(sql)
        db.commit()

        db = pymysql.connect(host='eunmiri-rds-demo-mysql2.ckcrvyfxpuwm.ap-northeast-2.rds.amazonaws.com',
                             user='eunmiri', passwd='eunmiri805!', db='eunmiridb')
        cursor = db.cursor()
        sql = '''INSERT INTO eunmiridb.pyeong_lectureinfo2(lecture_number, lecture, professor, Total_star, project, team, score, lecture_check, lecture_exam, e_learning) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
            lecture[2], lecture[0], lecture[1], lecture[4], detail_result[0], detail_result[1], detail_result[2],
            detail_result[3], detail_result[4], lecture[3])
        cursor.execute(sql)
        db.commit()


        db = pymysql.connect(host='eunmiri-rds-demo-mysql2.ckcrvyfxpuwm.ap-northeast-2.rds.amazonaws.com',
                             user='eunmiri', passwd='eunmiri805!', db='eunmiridb')
        cursor = db.cursor()
        sql = '''INSERT INTO eunmiridb.pyeong_reputation1(lecture_number, std_deviation, rep) VALUES ('%s', '%s', '%s')''' % (
            lecture[2], std_deviation, reputation)
        cursor.execute(sql)
        db.commit()

        db = pymysql.connect(host='eunmiri-rds-demo-mysql2.ckcrvyfxpuwm.ap-northeast-2.rds.amazonaws.com',
                             user='eunmiri', passwd='eunmiri805!', db='eunmiridb')
        cursor = db.cursor()
        sql = '''INSERT INTO eunmiridb.pyeong_reputation2(lecture_number, std_deviation, rep) VALUES ('%s', '%s', '%s')''' % (
            lecture[2], std_deviation, reputation)
        cursor.execute(sql)
        db.commit()

        #with open('lecture_eval.txt', 'a', encoding='utf-8') as file:
        #    file.write('{0}\n{1}\n{2}\n'.format(lecture[0], lecture[2], lecture_eval))  # 강의평 파일 저장
        #    file.write('=========================\n')
        #    file.close()

        std_deviation = 0
        sum_ = 0
        variance = 0
        count = 0
        print(lecture)
        print(detail_result)


    except Exception as e:
        print(e)
        fail_link.append(url)
        continue


driver.close()