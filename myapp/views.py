from django.shortcuts import render
from .models import info
from .models import sector
from .models import wealth
from collections import defaultdict
import pymysql.cursors

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

        cursor.execute(companyInd)
        industry_company = cursor.fetchall()

        cursor.execute(companyNewestPrice)
        newestPrice_company = cursor.fetchall()

        cursor.execute(companyGeo)
        company_Geo = cursor.fetchall()


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









#connect b and c