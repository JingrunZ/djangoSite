from django.shortcuts import render
from .models import info
from .models import sector
from .models import wealth
from collections import defaultdict
import pymysql.cursors


# Create your views here.
def industry_with_marketprice(request):
    result = defaultdict(int)
    x_data=[]
    y_data=[]
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='project',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            companyInd = "SELECT name,industry FROM `myapp_sector`"
            companyNewestPrice = "SELECT name,max FROM `myapp_wealth` WHERE date='2022-06-30'"
            cursor.execute(companyInd)
            industry_company = cursor.fetchall()
            cursor.execute(companyNewestPrice)
            newestPrice_company = cursor.fetchall()
    for i in industry_company:
        for j in newestPrice_company:
            if i['name']==j['name']:
                result[i['industry']] += float(j['max'].replace(",", ""))
    result = sorted(result.items(), key=lambda item:item[1])

    for x,y in result:       
        x_data.append(x)
        y_data.append(y)

    return render(request,'index.html',{'x_data':x_data,'y_data':y_data})

def geo_with_company(request):
    pass

def company_with_marketPrice(request):
    pass

def show_company_detail(request):
    pass

#connect b and c