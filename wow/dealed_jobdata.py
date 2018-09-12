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

# NAME ='find job'
# INFO ="找工作用的找工作程序——by 泛泛之素"
colors = ["red","rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","green","rgb(138 ,43, 226)","rgb(47 ,79 ,79)",
          "#26CC58", "#28C86D", "#29C481", "#2AC093", "#2BBCA4","#613099","#F4EC15", "#DAF017", "#BBEC19", "9DE81B"]

my_db=pymysql.connect(user=mysql_user,password=mysql_pass,host=mysql_host,port=mysql_port,database=mysql_data)

job_data=pd.read_sql('select * from job_company',con=my_db)
print(job_data.head(10))
print(job_data.duplicated().sum())
#+ job_data['education']+job_data['salary']+ '<br>'+job_data['applicate_person']
job_data['makers_show_text']=(job_data['job']).astype(str) +'<br>'+(job_data['company']).astype(str)+'<br>' +job_data['education']+ '<br>'+job_data['salary']+\
                             '<br>'+job_data['job_url']+'<br>'+job_data['company_url']

app=dash.Dash()
mapbox_accesstoken='pk.eyJ1IjoiamVzc3hsbCIsImEiOiJjamx3NnQya2cxMzBpM2ttZWZmNjRzcnR1In0.aTango7PURwrPEHRpl9liQ'
def get_figure(values):
    """
    plotly中已经封装了mapbox
    :param values:
    :return:
    """
    #第一：数据部分
    datas=[]
    #此Data\scattermapbox\maker是plotly.graph_objs中的类
    #地图标签，经纬度设置，也即标签点的展示的相关信息
    job=Data([Scattermapbox(lon=job_data['lng_y'],
                            lat=job_data['lat_y'],
                            hoverinfo="text",#设置标签悬停展示的内容【"lon", "lat", "text", "name", "name"】https://plot.ly/python/reference/#scattermapbox-hoverinfo
                            mode='markers',
                            #size大小对应像素，不宜过大；sizeref按照size大小比例缩放，sizemode，按照面积/直径
                            marker=Marker(size=job_data['salary_1'].astype(int)/1000,color=colors[4],sizemin=5,sizeref=0.8,sizemode='area'),#设置标签大小依赖，和颜色
                            text=job_data['makers_show_text'],#标签展示的内容
                            name='jess'
                            )])
    house=job
    trans={'job':job,'house':house}#在一张地图上，放两份数据的选择项【一份工作地图，一份房租地图】
    #我们这里，暂时没有房租的数据，所以两份数据完全一致即house=job
    for item in values:
      datas.extend(trans[item])
    #第二：数据呈现部分
    layout=Layout(
        autosize=True,
        height=750,#地图长宽
        width=1100,
        #margin=Margin(l=10,b=10,r=20,t=20),#外边框
        hovermode='closest',#环绕方式，紧密
        #mapbox，填写mapbox的相关信息，以字典形式，包括token，style都要重mapbox网站获取
        mapbox=dict(
            accesstoken=mapbox_accesstoken,#mapbox公司的token
            bearing=0,
            center=dict(lat=30.4,  #打开地图的中心方位
                lon=120.5),
            pitch=0,
            zoom=5,
            style='mapbox://styles/jessxll/cjlw7j1lo1p472sqr89bdlz76'
        ),
    )
    return go.Figure(data=datas,layout=layout)#返回地图对象

NAME='find job'
INFO="visual gongzuo"



app.layout=html.Div([
    #建立一级标题
    #HTML标签对里的内容是通过children关键字参数指定的
    html.H1(children='数据分析工作',
            style={
            'textAlign': 'center',
            'color': colors[5],
            'fontSize':'30px'
        }),
    html.Div(children='查看全国是数据分析工作',
             style={
        'textAlign': 'center',
        'color': colors[5],
        'fontSize':'18px'
    }),
    #建立复选框
    html.Div([
      dcc.Checklist(
          id='checkbox',
          options=[{'label':'工作','value':'job'},
                   {'label':'其他','value':'house'}],
          #options中的值必须在values中
          values=['job','house'])],
          className='twelve columns',style={'textAlign':'center','color':colors[6]}),
    html.Div([
        html.Div([
                html.Div([
                    html.Br(),
                    # 工作名
                    html.A(NAME, id='job_name_1', href='https://blog.csdn.net/Jesszen', target='_blank'),
                    # 网页html中的连接a元素，target=black，总是在新窗口打开链接
                    html.Br(),
                    html.A(NAME, id='company_name', href='https://blog.csdn.net/Jesszen', target='_blank'),
                    html.Div(INFO, id='job_desc',
                                )
                ],className='right_detail'),
        #建立结果展示内容
            html.Div([
                    dcc.Graph(id='histogram')],# hoverData={'points': [{'customdata': 'Japan'}]}    ,hoverData=dict(points=dict(pointNumber=10))
                    #{'points': [{'curveNumber': 1, 'pointNumber': 1473, 'pointIndex': 1473, 'lon': 116.31666898184959, 'lat': 40.04370648452434, 'text': '数据分析师(海淀）
                   className='letf_map',style={'textAlign': 'right'})
        ],className='tablerow')],className='tablecontainer')
])

@app.callback(Output('histogram','figure'),[Input('checkbox','values')])#figure是一个Dash关键字，表明它将是一个plot，
# values是输入nputI中的Checklist的一个参数values名，IO put的参数，必须按照要求来
def update_graph(values):
    """
    第一步：我们从网页动态交互的checklist中，取得values
    第二步：拿到values值，传入这个被装饰器装饰的函数中，又经过get figure处理，
    刚好返回了我们Oouput装饰器中第二个参数，也就是Dash的关键字，这里plot的类
    :param values:
    :return:
    """
    return get_figure(values)


#获取工作名
@app.callback(Output('job_name_1','children'),[Input('histogram','hoverData')])
def get_hover_title(hoverData):
    """
    1  直接hoverData或者，hoverData['points']，无任何返回值，因为格式是列表/字典格式，网页无法显示
    2、hoverData['points'][0]['text']可以拿到
    3、拿到类别的索引hoverData['points'][0]['pointIndex'] 既然由索引了，那么通过列表索引取值即可
    :param hoverData:
    :return:
    """
    try:
        job_name=job_data['job'][hoverData['points'][0]['pointIndex']]
        return job_name
    except:
        pass
#获取公司名
@app.callback(Output('company_name','children'),[Input('histogram','hoverData')])
def get_hover_title(hoverData):
    try:
        job_company=job_data['company'][hoverData['points'][0]['pointIndex']]
        return job_company
    except:
        pass

#获取工作链接
@app.callback(Output('job_name_1','href'),[Input('histogram','hoverData')])
def get_hover_title(hoverData):
    try:
        job_url=job_data['job_url'][hoverData['points'][0]['pointIndex']]
        return job_url
    except:
        pass

#获取公司链接
@app.callback(Output('company_name','href'),[Input('histogram','hoverData')])
def get_hover_title(hoverData):
    try:
        job_company_url=job_data['company_url'][hoverData['points'][0]['pointIndex']]
        return job_company_url
    except:
        pass

#获取工作描述
@app.callback(Output('job_desc','children'),[Input('histogram','hoverData')])
def get_hover_title(hoverData):
    try:
        job_ds=job_data['applicate_person'][hoverData['points'][0]['pointIndex']]
        return job_ds
    except:
        pass



# external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
#                 "//fonts.googleapis.com/css?family=Raleway:400,300,600",
#                 "//fonts.googleapis.com/css?family=Dosis:Medium" ]
# for css in external_css:
#     app.css.append_css({"external_url": css})

#获得地图
#@app.callback(dash.dependencies.Output('graph01','figure'),#定义回调输出依赖关系：第一个参数是。graph的id，第二个参数输出的组件属性
              #[dash.dependencies.Input('slider_a1','value')])#定义回调函数的输入依赖关系：第一个参数是。slider的id，第二个是属性
#@装饰器就是用来提供调用的
#app.callback函数的参数(output, inputs=[], state=[], events=[])
#注意第一个是output是值，第二个inputs是列表
#dash.dependencies.Output('SOME_ID', 'figure')表示与此关联的对象ID将通过此函数调用进行更新。figure是一个Dash关键字，表明它将是一个plot
#[dash.dependencies.Input('SLIDER_ID', 'value')]提供来自与之相关的对象的输入值ID。我们可以参考value这个调用下的函数。
# 在我们的例子中，我们使用slider 来选择一个新的hard-prediction截止点来重新生成我们的地块。
#app.callback这个装饰器，输入由input来确定，output输出
#app.callback装饰器通过声明描述应用界面的“输入”与“输出”项

if __name__=='__main__':
    app.run_server(debug=True,use_reloader=False)






