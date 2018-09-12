import pandas as pd
import pymongo
import requests
from requests.adapters import DEFAULT_RETRIES
from urllib.parse import urlencode
import numpy as np
import sqlalchemy
from lxml.html import etree
from wow.phone_user_agent import PHONE_USER_ANGET
import random
import json
import time
mongo_host = '127.0.0.1'
mongo_port = 27017
mongo_user = 'Jess'
mongo_password = '12345678wu'

WEB_PROXY='http://127.0.0.1:5555/random'
base_url='https://m.tianyancha.com/search?'
url_key={}
#'user-agent' : random.choice(PHONE_USER_ANGET),

mongo=pymongo.MongoClient(host=mongo_host,port=mongo_port,username=mongo_user,password=mongo_password)
mongo_company=mongo['conpany']

headers_1={
       'accept':'ext/css,*/*;q=0.1',
       'accept-encoding':'gzip, deflate, br'
}

company_details=pd.read_csv('G:\\visualization\\visualization\wow\company.csv',header=None,usecols=[1])
print('kaqi1111111111111111111111111111111111111111111111111111111111111111111111111111111111')

ak='ezrEdpmVQ8EAvnUCGSLyPPiZxWXA1oqH'

baidu_base_url='http://api.map.baidu.com/geocoder/v2/?'
request_data={
    'output':'json',
    'ak':ak
}

uu=company_details.iloc[:,0].unique()
uu_compy=uu.tolist()
count=0
for c in uu_compy:
    request_data['address']=c
    url=baidu_base_url+urlencode(request_data)
    try:
        DEFAULT_RETRIES=5
        response=requests.get(url,headers=headers_1)
        if response.status_code ==200:
            k=json.loads(response.text)
            kk=k.get('result')
            if kk is not None:
                m = kk['location']
                z={}
                z['conpany_name']=c
                z['lng']=m["lng"]
                z['lat']=m["lat"]
                print(z)
                mongo_company['loca_company'].insert(z)
    except Exception:
        print(Exception)
        uu_compy.append(c)
        count+=1

print(count)














"""
#天眼查cookies一多就被封，需要建立cookies池
def parse1(cc_url):
    response=requests.get(cc_url,headers=headers_1)
    kk=etree.HTML(response.text)
    cj={
        'company_name':''.join(kk.xpath('//div[@class="f18 new-c3 float-left"]/text()')),
        'company_score':''.join(kk.xpath('//div[@class="c9 pt15 f14"]/span//text()')),
        'company_location':''.join(kk.xpath('//div[@class="content-container pb10"]//div[last()-1]//span[2]/text()'))
    }
    print(cj)
    mongo_company['comp'].insert(cj)

def get_proxy(WEB_PROXY):
    response=requests.get(WEB_PROXY)
    p=response.text
    proxy='https://' + p
    return p
cookiess={
    '_ga':'GA1.2.1623906762.1536475193',
    '_gat_gtag_UA_123487620_1':'1',
    '_gid':'GA1.2.641943932.1536475193',
    'auth_token':'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODU1MTYyODczMCIsImlhdCI6MTUzNjQ4MTI2MCwiZXhwIjoxNTUyMDMzMjYwfQ.SIbNPxvRHNp1643FRJAcXDUTK7pRaCzx1vKIGY6xA4N_PIv6WCC14ommhJ4hb-S-E6FetA6tO1yQwMsa_o7vTw',
    'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758':'1536475187',
    'Hm_lvt_e92c8d65d92d534b0fc290df538b4758':'1536475187',
    'ssuid':'3491556385',
    'tyc-user-info':'%7B%22token%22%3A%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODU1MTYyODczMCIsImlhdCI6MTUzNjQ4MTI2MCwiZXhwIjoxNTUyMDMzMjYwfQ.SIbNPxvRHNp1643FRJAcXDUTK7pRaCzx1vKIGY6xA4N_PIv6WCC14ommhJ4hb-S-E6FetA6tO1yQwMsa_o7vTw%22%2C%22integrity%22%3A%220%25%22%2C%22state%22%3A%220%22%2C%22redPoint%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22vnum%22%3A%220%22%2C%22monitorUnreadCount%22%3A%220%22%2C%22onum%22%3A%220%22%2C%22mobile%22%3A%2218551628730%22%7D',
    'TYCID':'229937f0b3fb11e884a4d725851a941e',
    'undefined':'229937f0b3fb11e884a4d725851a941e'
}

for c in company_details.iloc[:,0].unique():
    url_key['key']=c
    url=base_url + urlencode(url_key)
    print(url)
    time.sleep(2)
    p=get_proxy(WEB_PROXY)
    proxies={"https://":p}
    response=requests.get(url,headers=headers_1,proxies=proxies)
    if response.status_code ==200:
        k=etree.HTML(response.text)
        c_url=k.xpath('//a[@class="query_name in-block"]/@href')
        print(c_url)
        if len(c_url) >0:
          cc_url=c_url[0]
          parse1(cc_url)
"""
