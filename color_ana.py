import cv2
import numpy as np
import src.colorlist as sc
import os
import pandas as pd
from tqdm import tqdm
import scipy
from scipy.spatial.distance import cdist


os.chdir(r'C:\Users\Simmons\PycharmProjects\stocklogo\img')

dirs = os.listdir()

for i in dirs:
    for root, d, files in os.walk("./" + i):
        pass
    os.rename('./' + i + '/' + files[0], './' + i + '/' + i + '.png')


# 处理图片
def get_color(frame):
    print('go in get_color')
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = sc.getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[ d ][ 0 ], color_dict[ d ][ 1 ])
        cv2.imwrite(d + '.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[ 1 ]
        binary = cv2.dilate(binary, None, iterations=2)
        contours, hierarchy = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in contours:
            sum += cv2.contourArea(c)
        if sum > maxsum:
            maxsum = sum
            color = d

    return color


def get_color_distribution(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color = None
    color_dict = sc.getColorList()
    result_dict = {}
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[ d ][ 0 ], color_dict[ d ][ 1 ])
        cv2.imwrite(d + '.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[ 1 ]
        binary = cv2.dilate(binary, None, iterations=2)
        contours, hierarchy = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in contours:
            sum += cv2.contourArea(c)
        result_dict[d] = sum
    return pd.Series(result_dict)


result_list = []

wrong_list = []

for i in tqdm(dirs):
    for root, d, files in os.walk("./" + i):
        pass
    filename = './' + i + '/' + files[0]
    frame = cv2.imread(filename)
    if frame is None:
        wrong_list.append(i)
        continue
    dist_i = get_color_distribution(frame)
    dist_i.name = i
    result_list.append(dist_i)


dist_df = pd.DataFrame(result_list).drop_duplicates()

for i in dist_df.index:
    if dist_df.loc[i, 'black'] == dist_df.loc[i].max():
        dist_df.loc[ i, 'white' ] += dist_df.loc[i, 'black']
        dist_df.loc[ i, 'black' ] == 0


dist_df['red'] = dist_df['red'] + dist_df['red2']
dist_df.drop(columns=['red2'], inplace=True)

dist_df_pct = dist_df.div(dist_df.sum(axis=1), axis=0)
dist_df_pct_ww = dist_df_pct.drop(columns=['white'])
dist_df_pct_ww = dist_df_pct_ww.div(dist_df_pct_ww.sum(axis=1), axis=0)
dist_df_pct_ww_max = dist_df_pct_ww.idxmax(axis=1)
max_dum = pd.get_dummies(dist_df_pct_ww_max)
max_dum.columns = [c+'_is_most' for c in max_dum.columns]


red = np.array([[0, 0, 255]])
blue = np.array([[255, 0, 0]])
green = np.array([[0, 128, 0]])


def color_distance(frame, target, white_remove=True):
    axis1 = frame.shape[0] * frame.shape[1]
    x = cdist(frame.reshape(axis1, 3), target)**2
    if white_remove:
        white = np.array([[255, 255, 255]])
        if_white = (cdist(white, red)**2)[0,0]
        x[x == if_white] = 0
    return np.mean(x)


color_distance(frame, green)


distance_list = []

wrong_distance_list = []
for i in tqdm(dirs):
    for root, d, files in os.walk("./" + i):
        pass
    filename = './' + i + '/' + files[0]
    frame = cv2.imread(filename)
    if frame is None:
        wrong_distance_list.append(i)
        continue
    i_dis = pd.Series([color_distance(frame, c) for c in [red, blue, green]], index=['red', 'blue', 'green'])
    i_dis.name = i
    distance_list.append(i_dis)

distance_df = pd.DataFrame(distance_list)
distance_df.columns = ['distance_from_'+i for i in distance_df.columns]


result = pd.concat([dist_df_pct_ww, max_dum, distance_df], axis=1)

result.to_csv(r'C:\Users\Simmons\PycharmProjects\stocklogo\output\factors.csv')

