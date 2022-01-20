import time
import pandas as pd
import numpy as np
import requests
import os
import json
import re
import random
from tqdm import tqdm, trange
import tushare as ts
from bs4 import BeautifulSoup


os.chdir(r'C:\Users\Simmons\PycharmProjects\stocklogo')

pro = ts.pro_api('c671b0e2d1161704817540482f52701730ae70600fde0501fe4bf8f0')

data = pro.stock_basic(exchange='', list_status='L', fields='symbol,name,fullname')

dirs = os.listdir('./img')
stk_left = data.query('symbol not in @dirs')

for i in trange(195, len(stk_left)):
    stk = stk_left.iloc[i, 0 ]
    stk_name = stk_left.iloc[i, 1 ].replace('*', '')
    full_name = stk_left.iloc[i, 2 ]

    url1 = 'https://www.kanzhun.com/search/comprehensive.json?query=' + full_name

    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    req1 = requests.get(url1, headers=head)
    try:
        encid = json.loads(req1.content)[ 'resdata' ][ 'companys' ][ 0 ][ 'encId' ]
    except:
        print(full_name)
        continue

    url2 = 'https://www.kanzhun.com/firm/info/{0}.html'.format(encid)
    time.sleep(random.uniform(1, 2))
    req2 = requests.get(url2, headers=head)
    soup = BeautifulSoup(req2.text, 'lxml')
    div1 = soup.find('div', attrs={'class': 'logo'})
    if div1:
        img_src = div1.img[ 'src' ]
    else:
        try:
            div1 = soup.find('div', attrs={'class': 'company-head-logo'})
            img_src = div1.img[ 'src' ]
        except AttributeError:
            print(full_name)
            continue

    try:
        time.sleep(random.uniform(4, 6))
        img_content = requests.get(img_src, timeout=30).content
    except Exception as e:
        print(e, img_src, full_name)
        continue
    try:
        os.mkdir('./img/{}'.format(stk))
    except FileExistsError:
        pass
    with open(r'./img/{0}/{1}.png'.format(stk, stk_name), 'wb') as f:
        f.write(img_content)

    time.sleep(random.uniform(1, 2))

# div2 = soup.find('div', attrs={'class': 'company-info'})
