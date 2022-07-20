from django.db import models
import requests
from bs4 import BeautifulSoup

# Create your models here.
class info(models.Model):
    name = models.CharField('中文简称', max_length=100)
    address = models.CharField('地址', max_length=100)
    establishment = models.CharField('成立时间', max_length=100)
    marketTime = models.CharField('上市时间', max_length=100)
    openingPrice = models.CharField('开盘价', max_length=100)
    closingPrice = models.CharField('开盘价', max_length=100)
    
    def __str__(self):
        return self.name

class wealth(models.Model):
    name = models.CharField('中文简称', max_length=100)
    date = models.CharField('日期', max_length=100)
    open = models.CharField('开盘价', max_length=100)
    min = models.CharField('最低价', max_length=100)
    max = models.CharField('收盘价', max_length=100)
    upDown = models.CharField('涨跌额', max_length=100)
    Quote = models.CharField('涨跌幅', max_length=100)
    volume = models.CharField('成交量', max_length=100)
    Turnover = models.CharField('成交金额', max_length=100)
    amplitude = models.CharField('振幅', max_length=100)
    TurnoverRate = models.CharField('换手率', max_length=100)

    def __str__(self):
        return self.name

url1 = 'http://quotes.money.163.com/f10/gszl_000002.html#01f01'
text=requests.get(url1)
text.encoding=text.apparent_encoding
text=text.text
bs4 = BeautifulSoup(text,'html.parser')
#get company name
CompanyName = bs4.find('a',href="/1000002.html").text

rows=bs4.find_all('td')
#find opening price
i=0
for price in rows:
    if price.text == "上市首日开盘价":
        openIndex = i
    i += 1
openPrice = rows[openIndex+1].text
#find closing price
j=0
for price in rows:
    if price.text == "上市首日收盘价":
        closeIndex = j
    j += 1
closePrice = rows[closeIndex+1].text

#find address
a=0
for address in rows:
    if address.text == "办公地址":
        addressIndex = a
    a+=1
companyAddress = rows[addressIndex+1].text

#find establishment date
b=0
for est in rows:
    if est.text == "成立日期":
        estIndex = b
    b+=1
estdate = rows[estIndex+1].text

c=0
for marDate in rows:
    if marDate.text == "上市日期":
        marketIndex = c
    c+=1
marketDate = rows[marketIndex+1].text


for i in info.objects.all():
    if i.name != CompanyName:
        b = info(name=CompanyName, openingPrice=openPrice, closingPrice=closePrice, address=companyAddress,establishment=estdate,marketTime=marketDate)
        b.save()

#------------------------------------------------------------------

wealth_list= "http://quotes.money.163.com/trade/lsjysj_000001.html?year=2022&season=2"
temp=requests.get(wealth_list)
temp.encoding=temp.apparent_encoding
new=temp.text
res = BeautifulSoup(new,'html.parser')

result = res.find_all('tr')
tempName = res.find('a',href="/1000001.html").text
for i in range(5,64):
    tempDate = result[i].find_all('td')[0].text
    tempOpen =  result[i].find_all('td')[1].text
    tempMax = result[i].find_all('td')[2].text
    tempMin = result[i].find_all('td')[3].text
    tempClose = result[i].find_all('td')[4].text
    tempUpDown = result[i].find_all('td')[5].text
    tempQuote = result[i].find_all('td')[6].text
    tempVol = result[i].find_all('td')[7].text
    tempTurnover = result[i].find_all('td')[8].text
    tempAmplitude = result[i].find_all('td')[9].text
    tempTurnoverRate = result[i].find_all('td')[10].text
    for i in wealth.objects.all():
        if i.name != tempName and i.date != tempDate:
            b = wealth(name=tempName,date=tempDate,open=tempOpen,max=tempMax,min=tempMax,upDown=tempUpDown,Quote=tempQuote,volume=tempVol,Turnover=tempTurnover,amplitude=tempAmplitude,TurnoverRate=tempTurnoverRate)
            b.save()