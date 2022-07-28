from django.shortcuts import render

from collections import defaultdict
import pymysql.cursors
import pandas as pd

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
    Requirement2 = defaultdict(int)
    Requirement3=defaultdict(int)
    x_data=[]
    y_data=[]
    mylist=[]
    CLOSEPRICE_company=[]
    COMPANY_closeprice=[]
    #Requirement 1
    for i in industry_company:
        for j in newestPrice_company:
            if i['name']==j['name']:
                Requirement1[i['industry']] += float(j['max'].replace(",", ""))
    Requirement1 = sorted(Requirement1.items(), key=lambda item:item[1])

    for x,y in Requirement1:       
        x_data.append(x)
        y_data.append(y)
    #------------------------------------------------------------------------
    #Requirement 2
    for i in company_Geo:
        Requirement2[i['geo']]+=1
    Requirement2 = sorted(Requirement2.items(), key=lambda item:item[1])
    
    for x,y in Requirement2:       
        mylist.append({
            'value':y,
            'name':x
        })
    #-----------------------------------------------------------------------
    #Requirement 3
    for i in newestPrice_company:
        Requirement3[i['name']] = float(i['max'].replace(",", ""))
    Requirement3 = sorted(Requirement3.items(), key=lambda item:item[1])
    
    for x,y in Requirement3:       
        COMPANY_closeprice.append(x)
        CLOSEPRICE_company.append(y)

    return render(request,'index.html',{'x_data':x_data,'y_data':y_data,'mylist':mylist,'COMPANY_closeprice':COMPANY_closeprice,'CLOSEPRICE_company':CLOSEPRICE_company})



def search(request):
    if request.method == "GET":
        company_names=[]
        searched = request.GET["searched"]

        kmapwealth=[]
        dates=[]

        for i in company_Geo:
            company_names.append(i['name'])

        if searched in company_names:
            for i in Basic_Info:
                if i['name'] == searched:
                    temp=[]
                    dates.append(i['date'])
                    
                    temp.append(float(i['close']))
                    temp.append(float(i['open']))
                    temp.append(float(i['min']))
                    temp.append(float(i['max']))

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

        df = pd.read_csv(r'C:\Users\stanf\OneDrive\Desktop\project\mysite\myapp\tushare.csv')
        for i in range(0,4735):
            temp = df.loc[i][2]
            if temp == searched:
                regex=df.loc[i][0][0:6]

        #encapsulation 
        data = {
            'searched':searched,
            'kmapwealth':kmapwealth,
            'dates':dates,
            'company_names':company_names,
            'myname':myname,
            'myaddress':myaddress,
            'myestablishment':myestablishment,
            'mymarketTime':mymarketTime,
            'myopeningPrice':myopeningPrice,
            'myclosingPrice':myclosingPrice,
            'myInd':myInd,
            'regex':regex
        }

        print(regex)
        

        
        
        return render(request,'./detail.html',data)
    else:
        return render(request,'./detail.html',{})




#connect b and c