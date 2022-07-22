from MySQLdb import IntegrityError
from django.db import models
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'date'],name='unique_booking')
        ]

    def __str__(self):
        return self.name
#----------------------------------------------------------------------------
url1 = 'http://quotes.money.163.com/f10/gszl_000001.html#01f01'
posts = []
for i in info.objects.all():
    posts.append(i.name)



df = pd.read_csv(r'C:\Users\stanf\OneDrive\Desktop\project\mysite\myapp\tushare.csv')
for i in range(2643,len(df)):
    url1 = re.sub("[0-9][0-9][0-9][0-9][0-9][0-9]", df.loc[i][0][0:6] , url1)
    text=requests.get(url1)
    print(url1)
    text.encoding=text.apparent_encoding
    text=text.text
    bs4 = BeautifulSoup(text,'html.parser')

    x = re.findall(".\d{7}[.]html", str(bs4))
    CompanyName = bs4.find('a',href=x[0]).text

    rows = bs4.find_all('tr')

    companyAddress=rows[5].find_all('td')[3].text
    openPrice=rows[28].find_all('td')[1].text
    closePrice=rows[29].find_all('td')[1].text
    marketDate=rows[17].find_all('td')[1].text
    estdate=rows[16].find_all('td')[1].text
    
    

    if CompanyName not in posts:
        b = info(name=CompanyName, openingPrice=openPrice, closingPrice=closePrice, address=companyAddress,establishment=estdate,marketTime=marketDate)
        b.save()
        posts.append(CompanyName)


# #------------------------------------------------------------------
# 
df = pd.read_csv(r'C:\Users\stanf\OneDrive\Desktop\project\mysite\myapp\tushare.csv')
for i in range(4684,4735):
    wealth_list= "http://quotes.money.163.com/trade/lsjysj_000001.html?year=2022&season=2"
    will_replace = df.loc[i][0][0:6]
    

    wealth_list = re.sub("[0-9][0-9][0-9][0-9][0-9][0-9]", will_replace , wealth_list)
    temp=requests.get(wealth_list)
    print(wealth_list)
    temp.encoding=temp.apparent_encoding
    new=temp.text
    res = BeautifulSoup(new,'html.parser')

    result = res.find_all('tr')
    
    x = re.findall(".\d{7}[.]html", str(res))
    tempName = res.find('a',href=x[0]).text

    for row in res.find_all('table',{"class":'table_bg001 border_box limit_sale'})[0].find_all('tr')[1:]:
        tempDate = row.find_all('td')[0].text
        tempOpen =  row.find_all('td')[1].text
        tempMax = row.find_all('td')[2].text
        tempMin = row.find_all('td')[3].text
        tempClose = row.find_all('td')[4].text
        tempUpDown = row.find_all('td')[5].text
        tempQuote = row.find_all('td')[6].text
        tempVol = row.find_all('td')[7].text
        tempTurnover = row.find_all('td')[8].text
        tempAmplitude = row.find_all('td')[9].text
        tempTurnoverRate = row.find_all('td')[10].text
        
        if not wealth.objects.filter(name=tempName,date=tempDate).exists():
            b = wealth(name=tempName,date=tempDate,open=tempOpen,max=tempMax,min=tempMin,upDown=tempUpDown,Quote=tempQuote,volume=tempVol,Turnover=tempTurnover,amplitude=tempAmplitude,TurnoverRate=tempTurnoverRate)  
            b.save()


            

