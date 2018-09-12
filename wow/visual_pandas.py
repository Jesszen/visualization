import pandas as pd
import pymongo
import matplotlib
import matplotlib.pyplot  as plt
import seaborn
import numpy as np
import re
import sqlalchemy
import pymysql
seaborn.set_style(rc={'font.sans-serif':['simhei','Arial']})

m_client=pymongo.MongoClient(host='127.0.0.1',port=27017,username='Jess',password='12345678wu')
job=m_client['JOB_VISUALIZATION']
df_job=pd.DataFrame(list(job['51job'].find()))

mysql_user='root'
mysql_pass='123456'
mysql_host='118.24.26.227'
mysql_port=3306
mysql_data='job'
mysql_engine=sqlalchemy.create_engine\
    ('mysql+mysqlconnector://{user}:{pass1}@{host}:{port}/{databse}?charset=utf8'.
     format(user=mysql_user,pass1=mysql_pass, host=mysql_host,port=mysql_port,databse=mysql_data))
# 随机查看10行
print(df_job.sample(10))


#计算重复的公司
print(df_job['company'].duplicated().sum())
df_job_comp_duplicated=df_job[df_job['company'].duplicated()]
print(df_job_comp_duplicated.shape)
print(df_job_comp_duplicated.head(10))

#查看缺失值
print(df_job.isnull().any())
rows_Nan=df_job.isnull().any(axis=1).sum()
print('{:-^80}'.format('rows has nan {r_n}').format(r_n=rows_Nan))
print(df_job['location'].isnull().sum())
#print(df_job[df_job['location'].isnull()==True])

print(df_job[df_job.isnull().values==True])
#print(df_job[df_job.isnull().any(axis=1)==True])
#发现67行数据空，我们删除它

df_job=df_job.dropna()



#删除无意义的job
def ban_job(job_name):
    ban = ['无经验', '免费', '培训', '操盘', '股票', '期货']
    if any(m in job_name for m in ban):###########################any()的用法，判断是否在ban中是否字段是否存在于job name
        job_name=np.nan
        return job_name
    else:
        return job_name
df_job['job']=df_job['job'].apply(lambda x:ban_job(x))
print(df_job['job'].isnull().sum())
df_job.dropna()

#提取薪资
def salary_1(salary):
    """
    区间1
    :param salary:
    :return:
    """
    if '-' in salary:
        if '千' in salary:
            m=salary.split('-')[0]
            m=np.float(m) * 1000
            return m
        if '万' in salary:
            n=salary.split('-')[0]
            n=np.float(n) * 10000
            return n
    else:
        return np.nan


def salary_2(salary):
    """
    区间1
    :param salary:
    :return:
    """
    re_rule = re.compile(r'(^[1-9]\.[1-9])|(^[0-9]*)')#*表示匹配0次以上，不可以和？连用，因为？表示匹配0/1次
    if '-' in salary:
        if '千' in salary:
            m=salary.split('-')[1]
            s=re.search(re_rule,m).group()
            m=np.float(s) * 1000
            return m
        if '万' in salary:
            n=salary.split('-')[1]
            s=re.search(re_rule,n).group()
            n=np.float(s) * 10000
            return n
    else:
        return np.nan

#没有在apply中引用lamda，所以直接函数不需要括号
df_job['salary_1']=df_job['salary'].apply(salary_1)
df_job['salary_2']=df_job['salary'].apply(salary_2)

print(df_job)
print(df_job.isnull().any(axis=1).sum())
df_job.dropna()

#拆分学历
def college(x):
    """
    学历拆分
    :param x:
    :return:
    """
    if '大专' in x:
        return '大专'
    if '本科' in x:
        return '本科'
    if '硕士' in x:
        return '硕士'
    else:
        return '其他'

df_job['education_new']=df_job['education'].apply(lambda x:college(x) )
print(df_job.sample(10))

#拆分城市
def location_1(x):
    """
    拆分城市
    :param x:
    :return:
    """
    m=x.split('-')[0]
    return m
df_job['city']=df_job['location'].apply(lambda x:location_1(x))

#拓展新的特征列，在于transform前，要由列名，否则报错
df_job['city_count']=df_job.groupby(df_job['city'])['city'].transform('count').astype(np.int64)
print(df_job.head(5))

df_job=df_job.dropna()
#导出城市名，和公司名
# df_job['city'].to_csv('city.csv',encoding='utf_8_sig')
# df_job['company'].to_csv('company.csv',encoding='utf_8_sig')


#----------------------------------------------------导入城市/公司的经纬度--------------------------------
city_lnglat=pd.read_csv('G:\\visualization\\visualization\wow\city_location.csv',usecols=[1,2,3])
ccc_lng=m_client['conpany']
company_lnglat=pd.DataFrame(list(ccc_lng['loca_company'].find()))
company_lnglat=company_lnglat.iloc[:,1:]
# print(city_lnglat)
# print(company_lnglat)
print(df_job.shape)
#how =left  以左边为依据合并，没有匹配的Nan值替代
df_job_lnglat=pd.merge(df_job,city_lnglat,on='city',how='left')
print(df_job_lnglat.shape)
print(df_job_lnglat.isnull().any(axis=1).sum())
df_job_lnglat=pd.merge(df_job_lnglat,company_lnglat,left_on='company',right_on='conpany_name',how='left')
#print(df_job_lnglat.sample(10))
print(df_job_lnglat.shape)
print(df_job_lnglat.isnull().any(axis=1).sum())
#print(df_job_lnglat[df_job_lnglat.isnull().any(axis=1)==True])
df_job_lnglat=df_job_lnglat.dropna()

print(df_job_lnglat.columns)
print(df_job_lnglat.dtypes)
pd.io.sql.to_sql(frame=df_job_lnglat.iloc[:,1:],name='job_company',con=mysql_engine,index=False,if_exists='replace')
"""
好多区没有，所以就不提取了
def location_2(x):
    if '-'in x:
        n=x.split('-')[1]
        return n
df_job['district']=df_job['location'].apply(lambda x:location_2(x))
"""

# print(df_job.shape)
# print(df_job.sample(10))

# 重点都是画图，添加坐标轴ax参数
# 画两张图方法一
# 先建立画布，在添加子图
fig=plt.figure()
axes1=fig.add_subplot(121)#前两位数，表示行列，后一位数，表示第几幅图
axes2=fig.add_subplot(122)
seaborn.countplot(x='education_new',data=df_job,ax=axes1)
seaborn.countplot(x='city',data=df_job[df_job['city_count']>50],ax=axes2)
plt.show()

#画两张图方法二
#直接画布，子图一起建立
fig,axes=plt.subplots(1,2)
seaborn.countplot(x='education_new',data=df_job,ax=axes[0])
seaborn.countplot(x='city',data=df_job[df_job['city_count']>50],ax=axes[1])
plt.show()


