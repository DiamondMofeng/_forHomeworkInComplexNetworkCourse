import os
from math import sin, asin, cos, radians, fabs, sqrt
import requests
import json
import pandas as pd

def Geodistance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000
    return dis / 1000  # 换算为千米

# code edited by mofeng
#0、在这里设置城市和线路名！(应确保有这条线路)
key=''
cityname=''
savepath="./export/export_new.csv"#以.csv结尾
ss=1    #从第多少路开始，一般为1
se=170   #到第多少路截止。程序不会自动识别该地区有多少路公交车，建议事先查询
rg=range(ss,se)
lst=[22,56,76]
for line in rg :

    try:
        url = 'https://restapi.amap.com/v3/bus/linename?s=rsv3&extensions=all&key={}&output=json&city={}&offset=1&keywords={}&platform=JS'.format(key,cityname,line)
        #1、获取数据
        r = requests.get(url).text
        rt = json.loads(r)
        #2、读取公交线路部分信息（可参考rt变量中的内容，按需获取）
        dt = {}
        dt['line_id'] = line #本次所获取的是哪条路
        dt['line_name'] = rt['buslines'][0]['name'] #公交线路名字

       #  3、获取沿途站点站名和对应坐标并保存在“公交基本信息”表格中


        Sources = []
        Deses = []
        Distance = []

        for i in range(len(rt['buslines'][0]['busstops'])-1):
            Sources.append(rt['buslines'][0]['busstops'][i]['name'])
            Deses.append(rt['buslines'][0]['busstops'][i+1]['name'])
            ## 获取距离
            distance_straight_site_start = rt['buslines'][0]['busstops'][i]['location']
            distance_straight_site_end = rt['buslines'][0]['busstops'][i + 1]['location']

            lat_s, lon_s = distance_straight_site_start.split(',', 1)
            lat_e, lon_e = distance_straight_site_end.split(',', 1)

            distance = Geodistance(float(lat_s), float(lon_s), float(lat_e), float(lon_e))
            Distance.append(distance)

        dt['Sources'] = Sources
        dt['Destinations'] = Deses


        dt['Distance'] = Distance  # 直线距离







        dm = pd.DataFrame(dt)

        dm.to_csv(savepath,mode="a",header=False,index=False,encoding='utf-8-sig')
        print("获取{}路数据成功！".format(line))

    except:

        if rt['status'] =="1":

            print("获取{}路数据出错了，很可能是没有该路。详情可以检查".format(line))
            print(url)
        else :
            print("获取{}路数据时发生重大错误。详情可以检查".format(line))
            print(url)
            print("已暂停，按任意键以继续运行")
            os.system('pause')






