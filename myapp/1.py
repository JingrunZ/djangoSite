import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv
import glob


#2610,2636




#rows = tbody.find_all('tr', recursive=False)


    #print(row.find_all('td')[0])

#result = res.find_all('table',{"class": "table_bg001 border_box limit_sale"})
#for i in result:
#    print(i)
    
#x = re.findall(".\d{7}[.]html", str(res))
#tempName = res.find('a',href=x[0]).text
#for i in result.find_all('td')[0].text:
#print(res.find_all('td')[0].text)
        

# tempDate = result[i].find_all('td')[0].text
# tempOpen =  result[i].find_all('td')[1].text
# tempMax = result[i].find_all('td')[2].text
# tempMin = result[i].find_all('td')[3].text
# tempClose = result[i].find_all('td')[4].text
# tempUpDown = result[i].find_all('td')[5].text
# tempQuote = result[i].find_all('td')[6].text
# tempVol = result[i].find_all('td')[7].text
# tempTurnover = result[i].find_all('td')[8].text
# tempAmplitude = result[i].find_all('td')[9].text
# tempTurnoverRate = result[i].find_all('td')[10].text

#df = pd.read_csv(r'C:\Users\stanf\OneDrive\Desktop\project\mysite\myapp\tushare.csv')
#for i in range(2643,4735):
#    wealth_list= "http://quotes.money.163.com/trade/lsjysj_600519.html?year=2022&season=2"
#    will_replace = df.loc[i][0][0:6]
    

#    wealth_list = re.sub("[0-9][0-9][0-9][0-9][0-9][0-9]", will_replace , wealth_list)
#    print(wealth_list)
    
    
wealth_list = "http://quotes.money.163.com/trade/lsjysj_600519.html?year=2022&season=2"
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
    print(tempOpen)
        
        
