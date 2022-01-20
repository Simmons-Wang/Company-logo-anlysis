import time
import pandas as pd
import numpy as np
import requests
import os
import json
import re
import random
from tqdm import tqdm

os.chdir(r'C:\Users\Simmons\PycharmProjects\stocklogo')

url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'

headers={
 'Accept':'*/*',
 'Accept-Encoding':'gzip, deflate',
 'Accept-Language':'zh-CN,zh;q=0.9',
 'Connection':'keep-alive',
 'Content-Length':'232',
 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
 'Cookie':'JSESSIONID=AA88D20CA77FB70F8E45008A59D42B62; insert_cookie=45380249; routeId=.uc2; _sp_ses.2141=*; SID=cb91c1de-8484-4866-b7b9-cc60fd4f88e8; _sp_id.2141=427f7cee-b8d4-43f5-9db6-e780d86c8f0b.1633420912.2.1633449813.1633421038.6dd58cff-bef2-467e-a31d-a6f6325dfefc',
 'Host':'www.cninfo.com.cn',
 'Origin':'http://www.cninfo.com.cn',
 'Referer':'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index',
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
 'X-Requested-With':'XMLHttpRequest'
}

form_data = {
 'pageNum':'1',
 'pageSize':'30',
 'column':'szse',
 'tabName':'fulltext',
 'plate':'sz',
 'stock':'',
 'searchkey':'2020年年度报告',
 'secid':'',
 'category':'category_ndbg_szsh',
 'trade':'',
 'seDate':'2020-10-05~2021-10-06',
 'sortName':'',
 'sortType':'',
 'isHLtitle':'true'
}


for pnum in range(121):
    form_data['pageNum'] = str(pnum)
    try:
        req = requests.post(url=url, data=form_data, headers=headers)
    except :
        print(pnum)
        continue
    str_data = req.content

    json_data = json.loads(str_data)
    time.sleep(random.uniform(1, 1.5))
# stk_url = 'http://www.cninfo.com.cn/new/disclosure/detail?stockCode={0}&announcementId={1}&orgId={2}&announcementTime={3}'.format(scode, annid, orgid, anntime)

    for ann in tqdm(json_data.get('announcements'), desc=str(pnum)):
        scode = ann['secCode']
        annid = ann['adjunctUrl'].split('/')[-1].split('.')[0]
        orgid=ann['orgId']
        anntime = ann['adjunctUrl'].split('/')[-2]
        pdf_name = re.sub('[a-zA-Z’!"#$%&\'()*+,-./:;<=>?@，。?、《》？“”‘’！[\\]^_`{|}~\s]+', "", ann['announcementTitle'])
        if '摘要' in pdf_name:
            time.sleep(1)
            continue
        down_url = 'http://www.cninfo.com.cn/new/announcement/download?bulletinId={0}&announceTime={1}'.format(annid, anntime)
        try:
            pdf_content = requests.get(down_url).content
        except :
            print(pdf_name)
            continue
        with open(r'./output/{}.pdf'.format(pdf_name + '_' + scode + '_' + anntime), 'wb') as f:
            f.write(pdf_content)
        time.sleep(random.uniform(1, 1.5))

