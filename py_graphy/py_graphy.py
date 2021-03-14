#!usr/bin/env python
"""
https://networkx.org/
https://github.com/networkx/networkx
https://www.osgeo.cn/networkx/tutorial.html
https://cloud.tencent.com/developer/article/1667290
https://www.cnblogs.com/kaituorensheng/p/5423131.html
"""
import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from networkx.readwrite import json_graph
from networkx.drawing.nx_agraph import read_dot
from networkx.drawing.nx_agraph import graphviz_layout
import os
import json 
from pprint import pprint
#G=nx.Graph()#创建空的简单图
#G=nx.Graph()#创建空的简单有向图
#G=nx.MultiGraph()#创建空的多图
#G=nx.MultiGraph()#创建空的有向多图

#.加点、加边
#G.add_node(1)#加1这个点
#G.add_node(1,1)#用(1,1)这个坐标加点
#G.add_nodes_from([2,3])#加列表中的点
 
#G.add_edge(1,2)#加边，起点是1终点是2
#G.add_weight_edge(1,2,3.0)#第三个是权值
#G.add_edges_from(list)#添加列表中的边
#G.add_weight_edges_from(list)

#
# G.remove_node()
# G.remove_nodes_from()
# G.remove_edge()
# G.remove_edges_from()
# G.clear()

#.遍历点和边
# G.add_nodes_from([1,2,3])
# for n in G.nodes():
#     print(n)
# G.add_edges_from([(1,2),(1,3)])
# for e in G.edges():
#     print(e)
# print(G.degree())


# G=nx.Graph()
# G.add_nodes_from([1,2,3,4,6,7,8,9,10])
# G.add_edges_from([(1,2),(2,3),(3,4),(4,5),(6,7),(7,8),(9,10),(7,10)])
# nx.draw_networkx(G)
# plt.show()

print(nx.__version__)
#dod = {0: {1: {"weight": 1}}}  # single edge (0,1)
#G = nx.from_dict_of_dicts(dod)
#dot_path  = os.path.abspath(os.path.join(os.path.dirname(__file__),"connection.dot"))
#dot =read_dot(dot_path)
json_path  = os.path.abspath(os.path.join(os.path.dirname(__file__),"connection_in.json"))
with open(json_path, "rt") as fp:
    data = json.load(fp)
G=json_graph.node_link_graph(data)

#G=nx.DiGraph(dot)
#G.add_nodes_from(["IO_I2S1_RX","SBC","AMP","SRC","IO_I2S1_TX"])
#G.add_edges_from([("IO_I2S1_RX","SBC"),("SBC","AMP"),("AMP","SRC"),("SRC","IO_I2S1_TX")])
options = {
    'node_color': 'red',
    'node_size': 500,
    'width': 1.5,
}


# pos = {
#   'IO_I2S1_RX':  ([1, 0]),
#   'SBC':    ([2, 0.1]),
#   'AMP':    ([3, 0.2]),
#   'SRC':    ([4, 0.2]),
#   'IO_I2S1_TX': ([5, 0.1]),
#   'IO_I2S0_RX':  ([1, -0.1]),
#   'SBC2':    ([2, -0.1]),
#   'IO_I2S0_TX': ([5, -0.2])
# }
#print(type(pos))
pos_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"pos_in.json"))
with open(pos_path, "rt") as fp:
    pos = json.load(fp)
pos_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"pos_out.json"))
with open(pos_path, "wt") as fp:
    json.dump(pos,fp,indent=4)
    pass

#pos = nx.spring_layout(G); 
#top = nx.bipartite.sets(G)[0]
#pos = nx.bipartite_layout(G, top)
#pos = nx.nx_agraph.graphviz_layout(G)
#pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
#pos = nx.kamada_kawai_layout(G)
#pos = nx.planar_layout(G)
#pos =  nx.random_layout(G)
#pos = nx.spectral_layout(G)
#pos = nx.spiral_layout(G)
#pos = nx.multipartite_layout(G)
pprint(pos)


nx.draw_networkx(G,pos=pos,**options)

#save the connection 
#connection_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"connection_out.txt"))
#write_dot(G,connection_path)
connection_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"connection_out.json"))
data1 = json_graph.node_link_data(G)
with open(connection_path, "wt") as fp:
    json.dump(data1,fp,indent=4)
    pass 

plt.title("Base-Topology")
plt.show()
#save the picture 
#png_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"G.png"))
#plt.savefig(png_path)

#list(nx.connected_components(G))

# degree(G[, nbunch, weight])：返回单个节点或nbunch节点的度数视图。 

# degree_histogram(G)：返回每个度值的频率列表。

# density(G)：返回图的密度。

# info(G[, n])：打印图G或节点n的简短信息摘要。

# create_empty_copy(G[, with_data])：返回图G删除所有的边的拷贝。

# is_directed(G)：如果图是有向的，返回true。

# add_star(G_to_add_to, nodes_for_star, **attr)：在图形G_to_add_to上添加一个星形。

# add_path(G_to_add_to, nodes_for_path, **attr)：在图G_to_add_to中添加一条路径。

# add_cycle(G_to_add_to, nodes_for_cycle, **attr)：向图形G_to_add_to添加一个循环。



# nodes(G)：在图节点上返回一个迭代器。

# number_of_nodes(G)：返回图中节点的数量。

# all_neighbors(graph, node)：返回图中节点的所有邻居。

# non_neighbors(graph, node)：返回图中没有邻居的节点。

# common_neighbors(G, u, v)：返回图中两个节点的公共邻居。