import pandas as pd
import pymysql
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from plotly import graph_objs as go
from plotly.graph_objs import *


mysql_user='root'
mysql_pass='123456'
mysql_host='118.24.26.227'
mysql_port=3306
mysql_data='job'

colors = ["red","rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","green","rgb(138 ,43, 226)","rgb(47 ,79 ,79)",
          "#26CC58", "#28C86D", "#29C481", "#2AC093", "#2BBCA4","#613099","#F4EC15", "#DAF017", "#BBEC19", "9DE81B"]

my_db=pymysql.connect(user=mysql_user,password=mysql_pass,host=mysql_host,port=mysql_port,database=mysql_data)

job_data=pd.read_sql('select * from job_company',con=my_db)
# print(job_data.head(10))
# print(job_data.duplicated().sum())


a=job_data.groupby(by='city').size()
b=job_data['salary_1'].groupby(job_data['city']).mean()
c=job_data['salary_2'].groupby(job_data['city']).mean()
bar_data=pd.concat([a,b,c],axis=1)
print(bar_data)


def bar_figure(va=20):
    s1=go.Bar(x=bar_data[bar_data.iloc[0:]>va].index[0],
           y=bar_data['salary_1'][0:va],
           name='salary_low',
           marker=go.Marker(color='#66CC99')
           )
    s2=go.Bar(x=bar_data[bar_data.iloc[0:]>va].index[0],
           y=bar_data['salary_2'][0:va],
           name='salary_high',
           marker=go.Marker(color='#99CC00'))
    data=[s1,s2]
    layout=Layout(title='不同城市的薪水区间',
                  showlegend=True,
                  legend=go.Legend(x=0,y=1),
                  margin=go.Margin(l=0,d=0,r=0,t=0),
                  )
    return go.Figure(data,layout)

