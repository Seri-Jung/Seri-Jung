from urllib.request import urlopen
from bs4 import BeautifulSoup
#import pandas as pd
import pymysql

html = urlopen("https://www.smu.ac.kr/ko/life/shuttle2.do")
soup = BeautifulSoup(html, "html.parser")

shuttle_table_pm = soup.find('table' , {'summary': '횟수, 차량, 학교출발, 터미널 애슐리 앞, 천안역 50m전방 빠리안경 앞, 비고로 구성된 셔틀버스 오후 운행을 볼 수 있는 표'})
shuttle_data_pm = []


for tbody in shuttle_table_pm.find_all('tbody'):
    for tr in tbody.find_all('tr'):
        tds = list(tr.find_all('td'))
        num = tds[0].text.strip()
        fromschool = tds[2].text.strip()
        terminal= tds[3].text.strip()
        cheon_station_pm = tds[4].text.strip()
        #db = pymysql.connect(host='eunmiri-rds-demo-mysql2.ckcrvyfxpuwm.ap-northeast-2.rds.amazonaws.com', user='eunmiri', passwd='eunmiri805!', db='eunmiridb')
        #cursor = db.cursor()
        #sql = '''INSERT INTO eunmiridb.shuttle_noon (num, fromschool, terminal, cheon_station_pm) VALUES ('%s', '%s', '%s', '%s')''' % (num, fromschool, terminal, cheon_station_pm)
        #cursor.execute(sql)
        #db.commit()

        shuttle_data_pm.append([num, fromschool, terminal, cheon_station_pm])

print(shuttle_data_pm)



