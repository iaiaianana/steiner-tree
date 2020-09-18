import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as ax

N = int(input("Введите число точек на плоскости: "))
max_size = int(input("Введите максимальное значение координаты точки: "))

# список имен точек
list_nodes = [str(x) for x in range(N)]
# список координат всех сгенерированных точек
coords_of_nodes = [(random.randrange(0, max_size), random.randrange(0, max_size)) for i in range(N)]
# словарь, сопоставляющий каждой точке ее кординаты на плоскости
pos = dict(zip(list_nodes, coords_of_nodes))


def distance_between_nodes(x1, y1, x2, y2):
    dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


G = nx.Graph()
G.add_nodes_from(pos.keys())
for n, p in pos.items():
    G.nodes[n]['pos'] = p
G_nodes = G.nodes()

# вес ребер совпадает с расстояними между соответствующими вершинами. Тогда задача о минимальной сумме длин ребер
# сводится к задаче о поиске подграфа с минимальной суммой весов.
edges = [(u, v, distance_between_nodes(pos[u][0], pos[u][1], pos[v][0], pos[v][1])) for u, v in
         nx.complete_graph(pos.keys()).edges()]
G.add_weighted_edges_from(edges)

# Создали граф, где каждая вершина соединена с каждой
nx.draw_networkx(G, pos, node_color=range(N), node_size=300, cmap=plt.cm.Purples)
plt.show()

# Построим приближенное минимальное дерево Штейнера для нашего набора вершин
st_tree_for_G = ax.steinertree.steiner_tree(G=G, terminal_nodes=G_nodes, weight='weight')
# Выведем список смежности в виде словаря, где каждой точке соответствует набор связанных с ней вершин для случая
# кратчайшего пути
adjlist_for_G = dict(zip(list_nodes, [x for x in nx.generate_adjlist(st_tree_for_G)]))
print(f'Список смежности: {adjlist_for_G}')

# Визуализируем получившееся дерево Штейнера в графе
nx.draw_networkx(st_tree_for_G, pos, node_color=range(N), node_size=300, cmap=plt.cm.Purples)
plt.show()

# Ту же иллюстрацию получим, используя алгоритм поиска минимального остовного дерева
nx.draw_networkx(nx.minimum_spanning_tree(G), pos, node_color=range(N), node_size=300, cmap=plt.cm.Reds)
plt.show()