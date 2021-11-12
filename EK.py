from copy import deepcopy

import networkx as nx
import queue


# use bfs to find the shortest path of the unweighted graph
# return the records of the shortest path.
def shortest(G: nx.DiGraph, src):
    q = queue.Queue(len(G.nodes))
    records = dict()
    for i in G.nodes:
        records[i] = {
            'visited': False,
            'dist': 0,
            'path': [],
        }

    q.put(src)
    records[src]['visited'] = True
    records[src]['dist'] = 0
    # records[src]['path'].append(src)
    while q.empty() is False:
        q_head = q.get()
        q_nb = list(G.neighbors(q_head))
        for i in q_nb:
            if records[i]['visited'] is not True:
                q.put(i)
                records[i]['visited'] = True
                records[i]['dist'] = records[q_head]['dist'] + 1
                records[i]['path'].append((q_head, i))
                records[i]['path'] = records[q_head]['path'] + records[i]['path']

    return records


def bfs_for_ek(g: nx.DiGraph, s: int, t: int):
    """
    :param g: residual Graph
    :param s: source
    :param t: destination
    :return: if find the path from s to t. return true
    """
    q = queue.Queue(len(g.nodes))
    records = dict()
    # 初始化记录表
    for i in g.nodes:
        records[i] = {
            'visited': False,
            'dist': 0,
            'path': [],
        }

    q.put(s)
    # 因为计算的是从源点 s 到各个点包括 t 的最短路径,records 节点记录的 path 当前节点的前一个节点.距离为 s 到各个点的总距离,所以
    # 循环内总是设置当前节点的邻居和当前节点的关系,当前节点的关系应在上一轮循环中完成
    records[s]['visited'] = True
    records[s]['dist'] = 0

    while q.empty() is False:
        front = q.get()
        nb = list(g.neighbors(front))
        for i in nb:
            if records[i]['visited'] is False:
                records[i]['visited'] = True
                records[i]['dist'] = records[front]['dist'] + 1
                records[i]['path'].append((front, i))
                records[i]['path'] = records[front]['path'] + records[i]['path']
                if i == t:
                    return True, records[i]['path']
                q.put(i)

    return False, None


def EK(g: nx.DiGraph, s: int, t: int):
    """
    Edmonds-Karp, to get the Maximum Flow

    If want to use this EK algorithm, you should add 3 attributes to the edges in a k-v way.
    The attributes are: capacity, residual and flow.

    :param g: residual graph
    :param s: source
    :param t: destination
    :return: the maximum flow
    """

    original_graph = deepcopy(g)

    ok, path = bfs_for_ek(g, s, t)
    while ok:
        bottleneck = 100
        for p in path:
            if g.edges[p]['residual'] < bottleneck:
                bottleneck = g.edges[p]['residual']

        for p in path:
            g.edges[p]['flow'] = bottleneck
            g.edges[p]['residual'] -= bottleneck
            reverse_edge = p[::-1]
            # if the reversed edge exist, merge the residual
            if g.has_edge(*reverse_edge):
                g.edges[reverse_edge]['residual'] += bottleneck
            # if the reversed edge not exist, add it
            else:
                g.add_edge(*p[::-1], residual=bottleneck)
            if g.edges[p]['residual'] == 0:
                g.remove_edge(*p)

        ok, path = bfs_for_ek(g, s, t)

    for i in original_graph.edges:
        if i not in g.edges:
            g.add_edge(*i, residual=0, capacity=original_graph.edges[i]['capacity'])

    maximum = 0
    for i in g.in_edges('t'):
        maximum += g.edges[i]['capacity'] - g.edges[i]['residual']

    return maximum
