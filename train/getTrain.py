# 静态的数据一般在elements中（复制文字到sources按ctrl+f搜索。找到的为静态），而动态去network中去寻找相关的信息
import requests
import re


def send_request():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        ,
        'Cookie': 'JSESSIONID=0CB8BE3546F963E0235C9D72DE823E3F; RAIL_EXPIRATION=1642036670442; RAIL_DEVICEID=py1mmkhVLvxym3CKSqimUk4-PgSXGLF1U1kbBd7Osj6A8B_wQNh5_WVD-15Dw5bvPvgWKlAK-s320lU9QfjA91gu4hh45NfvPGZXp4v303SmAlhGQyaKalhFO01RsPnHMe4ksFsP2_C4ml_oA1Fxyq-9FSUOdyO7; _jc_save_fromStation=%u9752%u5DDE%u5E02%u5317%2CQOK; _jc_save_toStation=%u5408%u80A5%u5357%2CENH; _jc_save_fromDate=2022-01-10; _jc_save_toDate=2022-01-10; _jc_save_wfdc_flag=dc; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; BIGipServerotn=149946890.24610.0000; BIGipServerpool_passport=233046538.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; current_captcha_type=C'}  # 创建头部信息
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=2022-01-20&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=TJP&purpose_codes=ADULT'
    # 设置编码格式。防止乱码
    #    https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=2022-01-10&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=TJP&purpose_codes=ADULT
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
    lst = parse_json(send_request(), get_city())
    print(lst)
    # 进行数据的筛选(得到有效的数据)
    for i in lst:
        # if i[3]!='无' and i[3]!='':#只显示有余票的
        print(i)


if __name__ == '__main__':
    start()  # 开始
