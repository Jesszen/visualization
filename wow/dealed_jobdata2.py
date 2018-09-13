import pandas as pd
import pymysql
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
from plotly import graph_objs as go
from plotly.graph_objs import *
import matplotlib.pyplot as plt


mysql_user='root'
mysql_pass='123456'
mysql_host='118.24.26.227'
mysql_port=3306
mysql_data='job'


my_db=pymysql.connect(user=mysql_user,password=mysql_pass,host=mysql_host,port=mysql_port,database=mysql_data)

job_data=pd.read_sql('select * from job_company',con=my_db)

a=job_data.groupby(by='city').size()
b=job_data['salary_1'].groupby(job_data['city']).mean()
c=job_data['salary_2'].groupby(job_data['city']).mean()
bar_data=pd.concat([a,b,c],axis=1)
#print(bar_data)
bar_data['city']=bar_data.index
#print(bar_data)
print(bar_data.iloc[:,0])
# x1=bar_data['city'][bar_data.iloc[0,:]>20].values
# y1=bar_data['salary_1'][bar_data.iloc[0,:]>20].values
# x2=bar_data['city'][bar_data.iloc[0,:]>20].values
# y2=bar_data['salary_2'][bar_data.iloc[0,:]>20].values
# print(type(x1))
# print(type(y1))

def bar_figure(va=20):
    x1=bar_data['city'][bar_data.iloc[:,0]>va].values
    y1=bar_data['salary_1'][bar_data.iloc[:,0]>va].values
    x2=bar_data['city'][bar_data.iloc[:,0]>va].values
    y2=bar_data['salary_2'][bar_data.iloc[:,0]>va].values
    s1=go.Bar(x=x1,
           y=y1,
           name='salary_low',
           marker=go.Marker(color='#66CC99')
           )
    s2=go.Bar(x=x2,
           y=y2,
           name='salary_high',
           marker=go.Marker(color='#99CC00'))
    data=[s1,s2]
    layout=Layout(title='不同城市的薪水区间',
                  showlegend=True,
                  legend=go.Legend(x=0,y=1),
                xaxis=dict(tickangle=-45),
                barmode='group'
                  )
    return go.Figure(data=data,layout=layout)
app=dash.Dash()



app.layout=html.Div([
    #建立一级标题
    #HTML标签对里的内容是通过children关键字参数指定的
    html.H1(children='数据分析工作',
            style={
            'textAlign': 'center',
            'fontSize':'30px'
        }),
    html.Div(children='查看全国是数据分析工作',
             style={
        'textAlign': 'center',
        'fontSize':'18px'
    }),
    html.Div([
        dcc.Slider(
            min=10,
            max=500,
            step=20,
            value=20,
            id='slider_jobs'),
        html.Div(
           dcc.Graph(
              id='bar_salary'),className='bar_salary',style={'height': 300}),
    html.Div(children=20,id='kkkkk')]),])

#获取城市数量
@app.callback(Output('bar_salary','figure'),[Input('kkkkk','children')])
def bar_update(children):
   return bar_figure(children)

if __name__=='__main__':
    app.run_server(debug=True,use_reloader=False,port=8000)






