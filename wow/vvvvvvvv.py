import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
from plotly.graph_objs import *
import pandas as pd

app =dash.Dash()

mapbox_access_token = '你的token'

df_job = pd.read_csv("job_to_map.csv")
del df_job["Unnamed: 0"]
df_job['text'] = df_job['name'] + '<br> ' + '公司：' +(df_job['company']).astype(str)+ '<br> ' +'评分'+ (df_job['final_score']).astype(int).astype(str)
colors = ["red","rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","green","rgb(138 ,43, 226)","rgb(47 ,79 ,79)",
          "#26CC58", "#28C86D", "#29C481", "#2AC093", "#2BBCA4","#613099","#F4EC15", "#DAF017", "#BBEC19", "9DE81B"]


#此为地图的主体部分，通过callback函数获得
def get_figure(values):
    datas = []
    #数据部分，以marker呈现，需要坐标数据
    job = Data([Scattermapbox(
        lon=df_job['lon'],
        lat=df_job['lat'],
        mode='markers',
        marker=Marker(
            size=df_job["final_score"] , #marker大小
            color=colors[4], #marker颜色
            # sizemode='area' #大小类型，会自动缩放
        ),
        text=df_job['text'], #marker上展示的内容
        name = "job"
    )
    ])
    house = job
    trans = {"job": job,"house":house}
    for item in values:
        datas.extend(trans[item])
    # 数据呈现部分
    layout = Layout(
        autosize=True,
        height=600,  #地图的长宽
        width=1100,
        margin=Margin(l=10, r=10, t=20, b=20),  #地图切边
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token, #这里的token要去mapbox申请
            bearing=0,
            center=dict(
                lat=39.908543,  #打开地图的中心方位
                lon=116.397389
            ),
            pitch=0,
            zoom=10,  #缩放大小
            style='mapbox://styles/mapbox/streets-v10'  #地图的类型
        ),
    )
    return go.Figure(data=datas, layout=layout)

NAME ='find job'
INFO ="找工作用的找工作程序——by 泛泛之素"

app.layout = html.Div([
    #建立个标题
    html.H1(
        children='找工作app',
        style={
            'textAlign': 'center',
            'color': colors[5],
            'fontSize':'30px'
        }
    ),
    #建立副标题
    html.Div(children='结合工作信息、房租信息、企业信息找到合适工作',
        style={
        'textAlign': 'center',
        'color': colors[5],
        'fontSize':'18px'
    }),
    #建立选项框
    html.Div([
         html.Div([
             dcc.Checklist(
                 id ='checkbox',
                 options=[
                     {'label': u'工作', 'value': 'job'},
                     {'label': u'房源', 'value': 'house'},
                 ],
                 values=['job','house'])
         ],className='twelve columns',style=dict( textAlign='center',columnCount=8,color=colors[6])),
    ]),
    #建立职位搜索内容展示


    html.Div([
        html.Div([
            html.Br(),
            # 工作名称
            html.A(NAME,
                  id='chem_name',
                  href="http://blog.csdn.net/tonydz0523",
                  target="_blank"),
            html.Br(),
            # 公司名称
            html.A(NAME,
                  id='company_name',
                  href="http://blog.csdn.net/tonydz0523",
                  target="_blank",
                  style = dict( maxWidth="350px")),
            # 工作详情
            html.Div(INFO,
                id ='chem_desc',
                style = dict( maxHeight='500px',maxWidth="350px", fontSize='13px' )),
            ],className ='three columns',style=dict(height='500px',textAlign='center')),
        #将信息call给函数
        html.Div([
            dcc.Graph(id="histogram",
                    style=dict(width='1100px'),
                    hoverData=dict( points=[dict(pointNumber=10)])
                    ),
        ], className='eight columns')
    ])
])
#获得地图
@app.callback(Output('histogram', "figure"),
              [Input("checkbox", "values")])
def update_graph(values):
    return get_figure(values)
#获取工作名
@app.callback(
    Output('chem_name', 'children'),
    [Input('histogram', 'hoverData')])
def get_hover_title(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        title = info["name"].tolist()[0]
        return title
    except :
        pass
#获取工作链接
@app.callback(
    dash.dependencies.Output('chem_name', 'href'),
    [dash.dependencies.Input('histogram', 'hoverData')])
def return_href(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        link = info['link'].tolist()[0]
        return link
    except Exception as e:
        print(e)
# 获取公司名
@app.callback(
    Output('company_name', 'children'),
    [Input('histogram', 'hoverData')])
def get_hover_title(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        title = info["company"].tolist()[0]
        return title
    except :
        pass
#获取公司链接
@app.callback(
    dash.dependencies.Output('company_name', 'href'),
    [dash.dependencies.Input('histogram', 'hoverData')])
def return_href(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        link = info['url'].tolist()[0]
        return link
    except Exception as e:
        print(e)
#获取工作明细
@app.callback(
    Output('chem_desc', 'children'),
    [Input('histogram', 'hoverData')])
def display_molecule(hoverData):
    try:
        name = str(hoverData).split("<")[0].split("'")[-1]
        company = str(hoverData).split("<")[1].split("：")[1]
        info = df_job[df_job['name'].isin([name])]
        info = info[info["company"].isin([company])]
        description = info["info"].tolist()[0]
        return description
    except:
        pass
#引用css
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium" ]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    # 运行
    app.run_server(debug=True)