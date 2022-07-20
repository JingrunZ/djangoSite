import requests
from bs4 import BeautifulSoup
from models import wealth

wealth_list= "http://quotes.money.163.com/trade/lsjysj_000001.html?year=2022&season=2"
temp=requests.get(wealth_list)
temp.encoding=temp.apparent_encoding
new=temp.text
res = BeautifulSoup(new,'html.parser')

result = res.find_all('tr')
tempName = res.find('a',href="/1000001.html").text

for i in range(5,64):
    tempDate = result[i].find_all('td')[0].text

    for i in wealth.objects.all():
        if i.name != tempName and i.date != tempDate:
            print("ok")
    