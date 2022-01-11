import time
import pandas as pd


def getNonRepeatList(data):
    # 去重
    return


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


def import_data(path: str):
    data = pd.read_csv(path, sep=',', engine='python', iterator=True, encoding='utf-8')
    df = pd.concat(data, ignore_index=True)
    lst = []
    for k in range(len(df)):
        train = df.iloc[k, 0]
        s = df.iloc[k, 1]
        t = df.iloc[k, 2]
        lst.append([train, s, t])
    print(lst)
    return lst


if __name__ == '__main__':
    cities = import_city('./data2/各市坐标.csv')
    lst = import_data('export_01-10-192456.csv')
    savepath_full = '总铁路_' + time.strftime("%m-%d-%H%M%S", time.localtime()) + ".csv"
    savepath_G = '高铁_' + time.strftime("%m-%d-%H%M%S", time.localtime()) + ".csv"
    savepath_other = '其他火车_' + time.strftime("%m-%d-%H%M%S", time.localtime()) + ".csv"
    to_save = []
    for b in cities:
        for i in range(len(cities)):

            if cities[i] == b:
                continue

            source = b
            target = cities[i]

            # weight = 0  # 总数
            weight_other = 0  # 其他车
            weight_G = 0  # 高铁

            for data in lst:
                if data[1].find(b) != -1 and data[2].find(cities[i]) != -1:
                    if data[0][0] == 'G':
                        weight_G = weight_G + 1
                    else:
                        weight_other = weight_other + 1
            weight = weight_G + weight_other  # 总数
            if weight != 0:
                to_save.append([source, target, weight, weight_G, weight_other])

    out = pd.DataFrame(to_save, columns=['source', 'target', 'weight', 'weight_G',
                                         'weight_other'])
    # out.columns = ['id', 'source', 'target', 'weight', 'weight_G',
    #               'weight_other']
    out.to_csv(savepath_full, mode='a', header=True, index=True, encoding='utf-8')

    # 分车型输出
    # 高铁
    to_save_G = []
    to_save_other = []
    for i in to_save:
        if i[3]!=0:
            to_save_G.append([i[0],i[1],i[3]])
    for i in to_save:
        if i[4]!=0:
            to_save_other.append([i[0],i[1],i[4]])
    out = pd.DataFrame(to_save_G, columns=['source', 'target', 'weight'])
    out.to_csv(savepath_G, mode='a', header=True, index=True, encoding='utf-8')

    out = pd.DataFrame(to_save_other, columns=['source', 'target', 'weight'])
    out.to_csv(savepath_other, mode='a', header=True, index=True, encoding='utf-8')

    print('done')
