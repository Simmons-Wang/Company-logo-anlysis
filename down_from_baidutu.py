import random
import re
import sys
import time
import urllib
import os
import shutil
import pandas as pd
import requests
from tqdm import trange
import tushare as ts
from bs4 import BeautifulSoup


os.chdir(r'C:\Users\Simmons\PycharmProjects\stocklogo')

pro = ts.pro_api('c671b0e2d1161704817540482f52701730ae70600fde0501fe4bf8f0')

data = pro.stock_basic(exchange='', list_status='L', fields='symbol,name,fullname')

dirs = os.listdir('./img')

with open('./output/stk_check.csv', 'r') as f:
    check_need = [i.replace('\n', '') for i in f.readlines()]

for i in check_need:
    try:
        shutil.rmtree('./img/'+ i)
    except FileNotFoundError:
        continue


stk_left = data.query('symbol not in @dirs',)
stk_left = data.query('symbol in @check_need')


def geturl(keyword):
    keyword = urllib.parse.quote(keyword, safe='/')
    url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&cl=2&lm=-1&st=-1&word='+keyword+'logo'
    return url


headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Cookie':'BIDUPSID=E43159961D154B035826914AF768C291; PSTM=1568907172; BAIDUID=870663869F7A2C7BF49F0796EAB7FF6F:FG=1; __yjs_duid=1_fa33c9a808d4108cb907a0f111b484e61619358340813; BCLID_BFESS=7922568375041084408; BDSFRCVID_BFESS=hLuOJexroG3VOzRHOTUtZjTQ4mKKHPoTDYLtOwXPsp3LGJLVg8_JEG0PtjOBDqu-oxCnogKK5mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tRk8oK_XtIvDqTrP-trf5DCShUFsaU7tB2Q-XPoO3KO48Pc-yMnx3J0lMROItPriW2bTWMbgylRM8P3y0bb2DUA1y4vpK5vdWeTxoUJ22q7Is-jGqtnWLPCebPRit4r9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHj8bj5JL3f; MCITY=-%3A; BAIDUID_BFESS=870663869F7A2C7BF49F0796EAB7FF6F:FG=1; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; cleanHistoryStatus=0; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; indexPageSugList=%5B%22%E8%B4%B5%E5%B7%9E%E8%8C%85%E5%8F%B0logo%22%2C%22%E4%B8%8A%E6%B5%B7%E9%9C%8D%E8%8E%B1%E6%B2%83%E7%94%B5%E5%AD%90%E7%B3%BB%E7%BB%9F%E6%8A%80%E6%9C%AF%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8logo%22%2C%22%E6%B9%96%E5%8D%97%E6%AD%A3%E8%99%B9%E7%A7%91%E6%8A%80%E5%8F%91%E5%B1%95%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8logo%22%2C%22%E5%B9%BF%E4%B8%9C%E5%AE%9D%E4%B8%BD%E5%8D%8E%E6%96%B0%E8%83%BD%E6%BA%90%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8logo%22%2C%22%E8%A7%86%E8%A7%89(%E4%B8%AD%E5%9B%BD)%E6%96%87%E5%8C%96%E5%8F%91%E5%B1%95%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8logo%22%2C%22%E6%B5%99%E6%B1%9F%E5%8D%8E%E5%AA%92%E6%8E%A7%E8%82%A1%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22%E5%B9%BF%E4%B8%9C%E9%9F%B6%E8%83%BD%E9%9B%86%E5%9B%A2%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22%E6%B2%B3%E5%8C%97%E5%BB%BA%E6%8A%95%E8%83%BD%E6%BA%90%E6%8A%95%E8%B5%84%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8logo%22%2C%22%E5%AE%89%E5%BE%BD%E5%8F%A4%E4%BA%95%E8%B4%A1%E9%85%92%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8logo%22%5D; userFrom=null; BDORZ=FAE1F8CFA4E8841CC28A015FEAEE495D; ab_sr=1.0.1_ZjI1YWYxNzA4OTEwYjdmMjEzNDYyZDU5OGU1NGYzYjUwMGI4ZDIwNjEwZDVkY2JkOWIyYjY1M2ExYTQwYjhjYjNiODY5OWZjODhjNzYyMjk4NzljMmUyOWI0NmVlZWU1NjJkZTY4Njg2MmMwYmVjMTM4ZjU0YjNjMTAwNDFkOTUwOTQyN2VjYTc3MWZmMWYwZjY2MTA5MzI1MGVkNzEzMw==',
    'Host':'image.baidu.com',
    'Referer':'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&cl=2&lm=-1&st=-1&word=%E8%B4%B5%E5%B7%9E%E8%8C%85%E5%8F%B0logo',
    'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile':'?0',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
}


def get_onepage_first(onepageurl):
    try:
        html = requests.get(onepageurl, headers=headers).text
    except Exception as e:
        print(e)
        return []
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    return pic_urls[0]


for i in trange(len(stk_left)):
    stk = stk_left.iloc[i, 0 ]
    stk_name = stk_left.iloc[i, 1 ].replace('*', '')
    full_name = stk_left.iloc[i, 2 ]
    onepageurl = geturl(stk_name)
    img_src = get_onepage_first(onepageurl)
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

    time.sleep(random.uniform(4, 6))
