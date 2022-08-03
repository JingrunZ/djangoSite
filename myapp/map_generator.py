
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts import options as opts 
import pymysql.cursors
from collections import defaultdict

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='project',
                             cursorclass=pymysql.cursors.DictCursor)
with connection:
    with connection.cursor() as cursor:
        
        companyGeo = "SELECT name,geo FROM `myapp_sector`"

        cursor.execute(companyGeo)
        company_Geo = cursor.fetchall()




mylist=[]
data = defaultdict(int)
for i in company_Geo:
    data[i['geo']]+=1
data = sorted(data.items(), key=lambda item:item[1])
print(data)
    
for x,y in data:       
    mylist.append({
        'value':y,
        'name':x
    })






geo = (
Geo()
	.add_schema(maptype="china")
	.add("",
        data
        )
	.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
	.set_global_opts(
		visualmap_opts=opts.VisualMapOpts(),
		title_opts=opts.TitleOpts(title="公司区域(Geo Map for Company)"),
	)
)
geo.render("homePage.html")
geo.render_notebook()



#geo = Geo("全国主要城市空气质量", "data from pm2.5", title_color="#fff", title_pos="center",
#width=1200, height=600, background_color='#404a59')
#attr, value = geo.cast(data)
#geo.add("", attr, value, visual_range=[0, 200], visual_text_color="#fff", symbol_size=15, is_visualmap=True)
#geo.render("map_visualmap.html")


