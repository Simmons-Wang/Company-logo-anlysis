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

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}


for i in trange(363, len(stk_left)):
    stk = stk_left.iloc[-i, 0]
    stk_name = stk_left.iloc[-i, 1].replace('*', '')
    full_name = stk_left.iloc[-i, 2]
    if not full_name:
        print(full_name)
        continue
    url = 'https://baike.baidu.com/item/' + stk_name
    try:
        req = requests.get(url, headers=headers, timeout=20)
    except requests.exceptions.ReadTimeout:
        print(full_name)
        continue
    soup = BeautifulSoup(req.text, 'lxml')
    target = soup.find('a', attrs={'nslog-type': "10002401"})
    if not target:
        print(full_name)
        time.sleep(random.uniform(0.5, 0.6))
        continue

    img_src = target.img['src']
    time.sleep(random.uniform(0.5, 0.6))
    try:
        img_content = requests.get(img_src, timeout=20).content
    except requests.exceptions.ReadTimeout:
        print(img_src, full_name)
        continue
    try:
        os.mkdir('./img/{}'.format(stk))
    except FileExistsError:
        pass
    with open(r'./img/{0}/{1}.png'.format(stk, stk_name), 'wb') as f:
        f.write(img_content)

    time.sleep(random.uniform(1, 2))