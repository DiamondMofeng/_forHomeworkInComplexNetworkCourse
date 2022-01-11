import os
from time import sleep
import time
import pandas as pd
import re
import requests


# 0.读取字典
#
def import_dict(path: str):
    data = pd.read_csv(path, sep=',', engine='python', iterator=True, encoding='utf-8')
    df = pd.concat(data, ignore_index=True)
    d = {}
    for k in range(len(df)):
        d.update({df.iloc[k, 1]: df.iloc[k, 2]})
    return d


# 1.读取城市列表

def import_city(path: str):
    """
    :param path: 输入csv文件的路径
    :return: nothing
    """
    # 读取csv文件
    data = pd.read_csv(path, sep=',', engine='python', iterator=True, encoding='utf-8')
    df = pd.concat(data, ignore_index=True)
    cities = []
    for k in range(len(df)):
        # 提前把城市节点名称放在第一列
        cities.append(df.iloc[k, 1])
    return cities


# 2. 用城市列表从字典中获取信息：
#   输入城市名，用正则表达式(先用find了)########改为用==了，因为不需要xx东站,输入xx站会包含xx东站的结果
#   进行比较，返回符合条件的[车站名：车站ID]存入新字典

def search_stations(cities: list, dict: dict):
    """

    :param cities: 导入的城市列表
    :param dict: 字典
    :return:
    """
    stations = {}

    keys = [k for k, v in dict.items()]
    for c in cities:
        for k in keys:
            if k == c:
                stations.update({k: dict[k]})
    return stations


# 3.用新的stations字典去12306查询
def query_trains(station_dict: dict):
    def send_request(url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            ,
            'Cookie': 'JSESSIONID=0CB8BE3546F963E0235C9D72DE823E3F; RAIL_EXPIRATION=1642036670442; RAIL_DEVICEID=py1mmkhVLvxym3CKSqimUk4-PgSXGLF1U1kbBd7Osj6A8B_wQNh5_WVD-15Dw5bvPvgWKlAK-s320lU9QfjA91gu4hh45NfvPGZXp4v303SmAlhGQyaKalhFO01RsPnHMe4ksFsP2_C4ml_oA1Fxyq-9FSUOdyO7; _jc_save_fromStation=%u9752%u5DDE%u5E02%u5317%2CQOK; _jc_save_toStation=%u5408%u80A5%u5357%2CENH; _jc_save_fromDate=2022-01-10; _jc_save_toDate=2022-01-10; _jc_save_wfdc_flag=dc; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; BIGipServerotn=149946890.24610.0000; BIGipServerpool_passport=233046538.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; current_captcha_type=C'}  # 创建头部信息

        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        return resp

    # 解析数据
    # {}是字典。根据key获取值。
    def parse_json(resp, city):
        json_ticket = resp.json()  # 将相应的数据转换为json
        data_list = json_ticket['data']['result']  # 得到车次的列表
        lst = []  # 列表
        for item in data_list:
            # 遍历车次信息进行分割
            d = item.split('|')
            lst.append([d[3], city[d[6]], city[d[7]], d[31], d[30], d[13]])
        return lst

    '''
    d[3]从列表中获取索引为3的表示车次
    d[6]查询起始站
    d[7]查询到达站
    d[31]一等座
    d[30]表示二等座
    d[13]表示出行时间'''

    # 获得station_name的信息
    def get_city():
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9151'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        # 进行数据的提取(只要一部分)
        stations = re.findall('([\u4e00-\u9fa5]+)\|([A-Z]+)', resp.text)
        # 将列表进行转换为字典
        stations_data = dict(stations)
        # key与value进行互换
        station_d = {}  # 空字典。用于完成上述操作
        for item in stations_data:
            station_d[stations_data[item]] = item
        # print(station_d)
        return station_d

    def start():
        path = "export_" + time.strftime("%m-%d-%H%M%S", time.localtime()) + ".csv"
        sts = [k for k, v in station_dict.items()]
        for b in sts:  # b 是出发站点
            for i in range(len(sts)):
                try:
                    sleep(0.5)
                    beg = station_dict[b]
                    end = station_dict[sts[i]]

                    url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=2022-01-20&leftTicketDTO.from_station=' + beg + '&leftTicketDTO.to_station=' + end + '&purpose_codes=ADULT'
                    print(url)
                    lst = parse_json(send_request(url), get_city())
                    print(lst)
                    out = pd.DataFrame(lst)
                    out.to_csv(path, mode='a', header=False, index=False, encoding='utf-8')
                except KeyError:
                    print()
                    print("出现KeyError，但应该没有什么问题，继续运行")
                    # os.system('pause')

    start()


if __name__ == '__main__':
    # 导入字典
    d = import_dict('station.csv')
    cities = import_city('./data2/各市坐标.csv')
    stations = search_stations(cities, d)
    query_trains(stations)

    print('done')