# coding=utf-8
import random
import networkx as nx
import pandas as pd
from networkx import Graph
import matplotlib.pyplot as plt

# code by mofeng
def import_node(path: str, nxGraph):
    """
    :param path: 输入csv文件的路径
    :param nxGraph: 导入至的netWorkX Graph
    :return: nothing
    """
    # 读取csv文件
    data = pd.read_csv(path, sep=',', engine='python', iterator=True, encoding='utf-8')
    df = pd.concat(data, ignore_index=True)
    for k in range(len(df)):
        # 提前把节点名称放在第二列
        nxGraph.add_node(df.iloc[k, 1])


def import_edge(path: str, nxGraph):
    # 读取csv文件
    data = pd.read_csv(path, sep=',', engine='python', iterator=True, encoding='utf-8')
    df = pd.concat(data, ignore_index=True)
    for k in range(len(df)):
        # 提前把边的起点放在第二列，终点放在第三列，权重放在第四列
        # print(df.iloc[k, 1], df.iloc[k, 2], df.iloc[k, 3])
        # nxGraph.add_edge(df.iloc[k, 1], df.iloc[k, 2], df.iloc[k, 3])
        nxGraph.add_edge(df.iloc[k, 1], df.iloc[k, 2])


def import_data(node_path: str, edge_path: str, nxGraph):
    import_node(node_path, nxGraph)
    print("node import done")
    import_edge(edge_path, nxGraph)
    print("edge import done")


def static_data(G):
    """输出图的统计数据
    
    :param G: 导入至的netWorkX Graph
    :return: nothing
    """

    print('------网络统计数据------')
    # 节点数
    stat_nodes = len(G.nodes())
    print("节点数,", stat_nodes)
    # 边数
    print("边数,", len(G.edges()))
    # 平均度
    print('度',G.degree())
    stat_degrees = [v for k, v in G.degree()]
    stat_avg_degree = sum(stat_degrees) / len(stat_degrees)
    print("平均度,", stat_avg_degree)

    # 网络直径（最长最短路径的长度）
    # 这个n方级算法太慢了，但是现在没有优化的需求
    # https://stackoverflow.com/questions/33114746/why-does-networkx-say-my-directed-graph-is-disconnected-when-finding-diameter

    stat_shortest_paths = [max(j.values()) for (i, j) in nx.shortest_path_length(G)]
    print("网络直径,", max(stat_shortest_paths))

    # 所有节点间平均最短路径长度。
    # 无向图没法用
    # nx.shortest_path_length(G)

    sum_shortest_path = sum(stat_shortest_paths)
    avg_shortest_path = sum_shortest_path / stat_nodes
    print("平均最短路径长度,", avg_shortest_path)

    # 介数
    stat_betweenness_s = [v for k, v in nx.betweenness_centrality(G).items()]
    # print(stat_betweenness_s)
    stat_avg_betweenness = sum(stat_betweenness_s) / len(stat_betweenness_s)
    print("平均介数,", stat_avg_betweenness)

    print("最大介数,", max(stat_betweenness_s))

    # 网络全局效率
    print("网络全局效率,", nx.global_efficiency(G))

    # 连接度
    ####### 不算了，这个算法数量级太大了跑不完
    # print("连接度,", nx.average_node_connectivity(G))

    # 平均集聚系数
    print("平均集聚系数,", nx.average_clustering(G))
    #  各个节点的集聚系数
    print("各个节点的集聚系数,", nx.clustering(G))

    ###
    # 最大度、介数的节点名称

    def find_max_degree(G):
        degrees = [v for k, v in G.degree()]
        for k, v in G.degree():
            if max(degrees) == v:
                print(k, '是最先找到的度最大的节点')
                return k

    def find_max_bet(G):
        # stat_betweenness_s
        # nx.betweenness_centrality(G).items()
        for k, v in nx.betweenness_centrality(G).items():
            if max(stat_betweenness_s) == v:
                print(k, '是最先找到的介数最大的节点')
                return k

    find_max_degree(G)
    find_max_bet(G)

    ##################

    # # 输出图表
    # fig = plt.figure("度、介分布")
    # # axgrid = fig.add_gridspec(2, 2)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    #
    # ax0 = fig.add_subplot(121)
    # #
    # ax0.plot(sorted(stat_betweenness_s, reverse=True), "b-", marker="o")
    # ax0.set_title("累计介数分布")
    # ax0.set_ylabel("累积概率")
    # ax0.set_xlabel("介数")
    #
    # # ax2.bar(*np.unique(sorted(stat_degrees,reverse=True), return_counts=True))
    # ax1 = fig.add_subplot(122)
    # ax1.plot(
    #     sorted(stat_degrees, reverse=True), "b-", marker="o")
    # ax1.set_title("累计度分布")
    # ax1.set_ylabel("累计度")
    # ax1.set_xlabel("度")
    #
    # plt.suptitle("度、介分布")
    #
    # fig.tight_layout()
    # plt.show()
    # plt.close(fig)

    # 输出图表  最短路径
    fig = plt.figure("最短路径")
    plt.rcParams['font.sans-serif'] = ['SimHei']

    ax0 = fig.add_subplot(122)
    #
    ax0.plot(sorted(stat_shortest_paths, reverse=True))
    ax0.set_title("累计最短路径分布")
    ax0.set_ylabel("累积概率")
    ax0.set_xlabel("最短路径")

    ax1 = fig.add_subplot(121)
    # ax1.plot(
    #     sorted(stat_degrees, reverse=True), "b-", marker="o")
    ax1.hist(stat_shortest_paths, bins=20, facecolor="blue", edgecolor="black", alpha=0.7)
    ax1.set_title("最短路径分布直方图")
    ax1.set_ylabel("频数")
    ax1.set_xlabel("最短路径")

    plt.suptitle("最短路径")

    fig.tight_layout()
    plt.show()
    plt.close(fig)

    # 输出图表  度
    fig = plt.figure("度")
    plt.rcParams['font.sans-serif'] = ['SimHei']

    ax0 = fig.add_subplot(122)
    #
    ax0.plot(sorted(stat_degrees, reverse=True))
    ax0.set_title("累计度分布")
    ax0.set_ylabel("累积概率")
    ax0.set_xlabel("度")

    ax1 = fig.add_subplot(121)
    ax1.hist(stat_degrees, bins=20, facecolor="blue", edgecolor="black", alpha=0.7)
    ax1.set_title("度分布直方图")
    ax1.set_ylabel("频数")
    ax1.set_xlabel("度")

    plt.suptitle("度")

    fig.tight_layout()
    plt.show()
    plt.close(fig)

    # 输出图表  介数
    fig = plt.figure("介数")
    plt.rcParams['font.sans-serif'] = ['SimHei']

    ax0 = fig.add_subplot(122)
    #
    ax0.plot(sorted(stat_betweenness_s, reverse=True))
    ax0.set_title("累计介数分布")
    ax0.set_ylabel("累积概率")
    ax0.set_xlabel("介数")

    ax1 = fig.add_subplot(121)
    ax1.hist(stat_betweenness_s, bins=20, facecolor="blue", edgecolor="black", alpha=0.7)
    ax1.set_title("介数分布直方图")
    ax1.set_ylabel("频数")
    ax1.set_xlabel("介数")

    plt.suptitle("介数")

    fig.tight_layout()
    plt.show()
    plt.close(fig)


def random_attack(G: Graph, t: int):
    """对目标进行单次的随机攻击

    :param G:
    :param t:攻击次数
    :return:
    """

    def atk(G):
        # 随机删除G中的1个点
        nodes = [i for i in G.nodes()]
        # print(nodes)
        rd = random.randint(0, len(nodes) - 1)
        G.remove_node(nodes[rd])
        print(nodes[rd], '被随机选中，进行移除')
        return nodes[rd]

    # 思路：对atk循环t次，然后输出两个图表，横坐标为攻击次数，纵坐标为全局效率、最大连通子图大小
    # 对G进行复制，对复制体进行操作而不是本体。

    print('------开始进行随机攻击------')

    g = G.copy()
    # 计算初始全局效率、最大连通子图大小
    eff = []
    lgc = []
    init_eff = nx.global_efficiency(g)
    init_lgc = len(max(nx.connected_components(g), key=len))
    eff.append(1.00)
    lgc.append(1.00)

    atk_path = []
    for i in range(0, t):
        print('---攻击进度：', i + 1, "/", t, '---')
        # 记录攻击路径
        atk_path.append(atk(g))
        # 记录攻击后的全局效率、最大连通子图大小
        cur_eff = nx.global_efficiency(g) / init_eff
        cur_lgc = len(max(nx.connected_components(g), key=len)) / init_lgc
        print('剩余全局效率：', cur_eff)
        print('剩余最大连通子图相对大小：', cur_lgc)
        eff.append(cur_eff)
        lgc.append(cur_lgc)
    # 攻击路径
    print('攻击路径：', atk_path)

    # 输出图表
    fig = plt.figure("随机攻击")
    # axgrid = fig.add_gridspec(2, 2)
    plt.rcParams['font.sans-serif'] = ['SimHei']

    ax0 = fig.add_subplot(121)
    #
    ax0.plot(sorted(eff, reverse=True), "b-", marker="o")
    ax0.set_title("随机攻击下的全局效率值")
    ax0.set_ylabel("全局效率")
    ax0.set_xlabel("失效节点个数")

    ax1 = fig.add_subplot(122)
    ax1.plot(lgc, "b-", marker="o")
    ax1.set_title("随机攻击下的最大连通子图相对大小")
    ax1.set_ylabel("最大连通子图相对大小")
    ax1.set_xlabel("失效节点个数")

    plt.suptitle("随机攻击")

    fig.tight_layout()
    plt.show()
    plt.close(fig)


def deliberately_attack(G: Graph, t: int):
    """删除G中度数最大的点

    :param G:
    :param t:攻击次数
    :return:
    """

    # 我这写的算法太烂了，能用就行
    def atk(G):
        degrees = [v for k, v in G.degree()]
        for k, v in G.degree():
            if max(degrees) == v:
                G.remove_node(k)
                print(k, '是当前最先找到的度最大的节点，进行移除')
                return k

    # 思路：对atk循环t次，然后输出两个图表，横坐标为攻击次数，纵坐标为全局效率、最大连通子图大小
    # 对G进行复制，对复制体进行操作而不是本体。
    print('------开始进行蓄意攻击------')

    g = G.copy()
    # 计算初始全局效率、最大连通子图大小
    eff = []
    lgc = []
    init_eff = nx.global_efficiency(g)
    init_lgc = len(max(nx.connected_components(g), key=len))
    eff.append(1.00)
    lgc.append(1.00)

    atk_path = []
    for i in range(0, t):
        print('---攻击进度：', i + 1, "/", t, '---')
        # 记录攻击路径
        atk_path.append(atk(g))
        # 记录攻击后的全局效率、最大连通子图大小
        cur_eff = nx.global_efficiency(g) / init_eff
        cur_lgc = len(max(nx.connected_components(g), key=len)) / init_lgc
        print('剩余全局效率：', cur_eff)
        print('剩余最大连通子图相对大小：', cur_lgc)
        eff.append(cur_eff)
        lgc.append(cur_lgc)
    # 攻击路径
    print('攻击路径：', atk_path)

    # 输出图表
    fig = plt.figure("蓄意攻击")
    # axgrid = fig.add_gridspec(2, 2)
    plt.rcParams['font.sans-serif'] = ['SimHei']

    ax0 = fig.add_subplot(121)
    ax0.plot(eff, "b-", marker="o")
    ax0.set_title("蓄意攻击下的全局效率值")
    ax0.set_ylabel("全局效率")
    ax0.set_xlabel("失效节点个数")

    ax1 = fig.add_subplot(122)
    ax1.plot(lgc, "b-", marker="o")
    ax1.set_title("蓄意攻击下的最大连通子图相对大小")
    ax1.set_ylabel("最大连通子图相对大小")
    ax1.set_xlabel("失效节点个数")

    plt.suptitle("蓄意攻击")

    fig.tight_layout()
    plt.show()
    plt.close(fig)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # 创建无向图G
    G: Graph = nx.Graph()
    import_data("../data/城市名及经纬度.csv", "../高铁_01-10-182636.csv", G)

    static_data(G)

    random_attack(G, 200)
    deliberately_attack(G, 200)

    # generate_degree(G)
    print("done")
