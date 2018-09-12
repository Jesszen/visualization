import requests
import pandas as pd
import numpy as np
import json
from urllib.parse import urlencode

ak='ezrEdpmVQ8EAvnUCGSLyPPiZxWXA1oqH'

baidu_base_url='http://api.map.baidu.com/geocoder/v2/?'
request_data={
    'output':'json',
    'ak':ak
}

#usecols指定读取列的范围
city_df=pd.read_csv('G:\\visualization\\visualization\wow\city.csv',header=None,usecols=[1])
print(city_df.head(10))
print(type(city_df))
city_unique=city_df.iloc[:,0].unique()
print(city_unique)

ci=[]
lng=[]
lat=[]
for c in city_unique:
    request_data['address']=c
    url=baidu_base_url+urlencode(request_data)
    response=requests.get(url)
    if response.status_code ==200:
        k=json.loads(response.text)
        kk=k.get('result')
        if kk is not None:
           m=kk['location']
           ci.append(c)
           lng.append(m["lng"])
           lat.append(m["lat"])
u=np.hstack((np.asarray(ci).reshape(len(ci),1),np.asarray(lng).reshape(len(lng),1),np.asarray(lat).reshape(len(lat),1)))
city_location=pd.DataFrame(u,columns=['city','lng','lat'])
print(city_location)
city_location.to_csv('city_location.csv',encoding='utf_8_sig')



company_details=pd.read_csv('G:\\visualization\\visualization\wow\company.csv',header=None,usecols=[1])
