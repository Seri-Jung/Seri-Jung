from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.smu.ac.kr/ko/life/shuttle2.do")
soup = BeautifulSoup(html, "html.parser")

#li_shuttle = bsObject.find_all('ol',class_='hyphen' )
#shuttle = li_shuttle.text.strip()
#with open('shuttle.csv', 'w') as file:
#    for j in shuttle_data:
#        file.write('{0}\n'.format(j[0]))
#print(shuttle)

#for li_shuttle in bsObject.find_all('ol', class_="hyphen"):
#    shuttle = li_shuttle.text.strip()
#    shuttle_data.append([shuttle])
#    with open('shuttle.csv', 'w') as file:
#        for k in shuttle_data:
#            file.write('{0}\n'.format(k[0]))
#    print(shuttle)

shuttle_table_am = soup.find('table' , {'class': 'smu-table mt30'})
shuttle_data_am = []

for tbody in shuttle_table_am.find_all('tbody'):
    for tr in tbody.find_all('tr'):
        tds = list(tr.find_all('td'))
        #for td in tds:
            #    if tds.find(rowspan= "2"):
            #        etc = tds[4].text
        num = tds[0].text
        dujeong = tds[2].text
        cheon_station = tds[3].text

        shuttle_data_am.append([num, dujeong, cheon_station])

with open('amshuttle.csv', 'w') as file:
    file.write('num, dujeong, cheon_station \n')
    for i in shuttle_data_am:
        file.write('{0},{1},{2}\n'.format(i[0],i[1],i[2]))