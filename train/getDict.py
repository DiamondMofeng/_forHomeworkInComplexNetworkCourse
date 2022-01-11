import re
import xlwt
import requests

# https://blog.csdn.net/qq_34608451/article/details/100561019
def search_station(station_names):
    # 得到的数据为：火车站名的首字母，火车站名，火车站id
    # 从12306获取的数据中，通过正则匹配过滤数据
    # data用来存放数据
    station_names_data = []
    # 从s中通过正则匹配得到"@bjb|北京北|"这样的数据形式所有符合的数据
    it = re.finditer(r"@((\w){3})\|((.){2,5})\|((\w){3})", station_names)
    for match in it:
        # 从"@bjb|北京北|VAP"过滤数据，得到"bjb|北京北|VAP"这样形式的数据
        num = re.sub(r'@', "", match.group())
        # 从"bjb|北京北|VAP"过滤数据，得到"bjb 北京北 VAP"这样形式的数据
        num = re.sub(r'\|', " ", num)
        # 初始化d列表
        d = []
        # 将"bjb 北京北 "这个数据中的非空格的字符串取出
        num = re.finditer(r"(\S){2,5}", num)
        for num1 in num:
            # 把筛选处理符合要求的数据放到d列表中
            d.append(num1.group())
        station_names_data.append(d)
    return station_names_data


# 将数据写入excel文件
# file_path为excel的文件路劲
# datas为要写入excel的数据，这里的数据为2列多行的数据
def data_write(file_path, datas):
    f = xlwt.Workbook()
    # 创建sheet
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    # 将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        for j in range(len(data)):
            sheet1.write(i, j, data[j])
        i = i + 1

    f.save(file_path)  # 保存文件


# 12306火车站数据的url
utl_12306 = 'https://www.12306.cn/index/script/core/common/station_name_v10037.js'
# 获取全国火车的的数据
r = requests.get(url=utl_12306)
# 筛选数据
station_data = search_station(r.text)
print(station_data)
# 写入excel
data_write("station.xls", station_data)