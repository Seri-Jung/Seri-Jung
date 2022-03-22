from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.smu.ac.kr/ko/life/circles2.do#tab6580")
soup = BeautifulSoup(html, "html.parser")

club = soup.find('table',{'class' : 'smu-table tb-w150'})
club_data = []

for tbody in club.find_all('tbody'):
    for tr in tbody.find_all('tr'):
        tds = list(tr.find_all('td'))
        num = tds[0].text.strip()
        name = tds[1].text.strip()
        purpose = tds[2].text.strip()
        contents = tds[3].text.strip()
        foundation = tds[4].text.strip()


        club_data.append([num, name, purpose, contents, foundation])

print(club_data)
with open('club.xlsx', 'w', encoding= 'UTF-8', newline='') as file:
    file.write('num, name, purpose, contents, foundation \n')
    for i in club_data:
        file.write('{0},{1},{2},{3},{4}\n'.format(i[0],i[1],i[2],i[3],i[4]))