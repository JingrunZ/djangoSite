from django.shortcuts import render
from django.templatetags.static import static
from collections import defaultdict
import pymysql.cursors
import pandas as pd

from typing import List

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='project',
                             cursorclass=pymysql.cursors.DictCursor)
with connection:
    with connection.cursor() as cursor:
        companyInd = "SELECT name,industry FROM `myapp_sector`"
        companyNewestPrice = "SELECT name,max FROM `myapp_wealth` WHERE date='2022-06-30'"
        companyGeo = "SELECT name,geo FROM `myapp_sector`"
        basicInfo = "SELECT * FROM `myapp_wealth`"
        companyInfo = "SELECT * FROM `myapp_info`"

        cursor.execute(companyInd)
        industry_company = cursor.fetchall()

        cursor.execute(companyNewestPrice)
        newestPrice_company = cursor.fetchall()

        cursor.execute(companyGeo)
        company_Geo = cursor.fetchall()

        cursor.execute(basicInfo)
        Basic_Info = cursor.fetchall()

        cursor.execute(companyInfo)
        company_Info = cursor.fetchall()

# Create your views here.
def charts(request):
    Requirement1 = defaultdict(int)
#    Requirement2 = defaultdict(int)
    Requirement3=defaultdict(int)

    mylist=[]
    CLOSEPRICE_company=[]
    COMPANY_closeprice=[]
    #Requirement 1
    for i in industry_company:
        for j in newestPrice_company:
            if i['name']==j['name']:
                Requirement1[i['industry']] += float(j['max'].replace(",", ""))
    
    for i in Requirement1.copy():
        if Requirement1[i] < 600:
            Requirement1['其他'] += Requirement1[i]
            del Requirement1[i]
    Requirement1 = sorted(Requirement1.items(), key=lambda item:item[1],reverse=True)
    
    run = 0
    res=[]
    for x,y in Requirement1:
        my_list={
        'value':y,
        'name':x
        }
        res.append(my_list)
        run +=1
        if run == 12:
            break

    #------------------------------------------------------------------------
    #Requirement 2

    #-----------------------------------------------------------------------
    #Requirement 3
    
    for i in newestPrice_company:
        Requirement3[i['name']] = float(i['max'].replace(",", ""))
    Requirement3 = sorted(Requirement3.items(), key=lambda item:item[1],reverse=True)
    run = 0
    for x,y in Requirement3:
        run+=1       
        COMPANY_closeprice.append(x)
        CLOSEPRICE_company.append(y)
        if run == 12:
            break
    COMPANY_closeprice.reverse()
    CLOSEPRICE_company.reverse()
    return render(request,'homePage.html',{'res':res,'mylist':mylist,'COMPANY_closeprice':COMPANY_closeprice,'CLOSEPRICE_company':CLOSEPRICE_company})

def search(request):
    if request.method == "GET":
        company_names=[]
        searched = request.GET["searched"]

        kmapwealth=[]
        dates=[]
        myname = "none"
        myaddress="none"
        myestablishment="none"
        mymarketTime="none"
        myopeningPrice="none"
        myclosingPrice="none"
        myInd="none"
        regex="none"
        for i in company_Geo:
            company_names.append(i['name'])

        if searched in company_names:
            for i in Basic_Info:
                if i['name'] == searched:
                    
                    temp=[]
                    dates.append(i['date'])
                    temp.append(float(i['close'].replace(",", "")))
                    temp.append(float(i['open'].replace(",", "")))
                    temp.append(float(i['min'].replace(",", "")))
                    temp.append(float(i['max'].replace(",", "")))

                    kmapwealth.append(temp)
        else:
            searched='error'

        if searched in company_names:
            for i in company_Info:
                if i['name'] == searched:
                    myname = i['name']
                    myaddress =i['address']
                    myestablishment=i['establishment']
                    mymarketTime=i['marketTime']
                    myopeningPrice=i['openingPrice']
                    myclosingPrice=i['closingPrice']

            for i in industry_company:
                if i['name'] == searched:
                    myInd = i['industry']
        
        url = static('tushare.csv')
        df = pd.read_csv(url)
        for i in range(0,4735):
            temp = df.loc[i][2]
            if temp == searched:
                regex=df.loc[i][0][0:6]
        print(searched)
        #encapsulation 
        data = {
            'searched':searched,
            'kmapwealth':kmapwealth,
            'dates':dates,
            'company_names':company_names,
            'myname': myname,
            'myaddress':myaddress,
            'myestablishment':myestablishment,
            'mymarketTime':mymarketTime,
            'myopeningPrice':myopeningPrice,
            'myclosingPrice':myclosingPrice,
            'myInd':myInd,
            'regex':regex
        }

        
        return render(request,'./detail.html',data)
    else:
        return render(request,'./detail.html',{})
