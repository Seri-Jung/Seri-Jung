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

pyautogui.moveTo(400, 600)

#time.sleep(10)
#for i in range(1, 29):
#    pyautogui.scroll(-30000)
#
time.sleep(8)