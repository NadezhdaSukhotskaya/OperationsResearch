import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, adjacency_node, weight):
        self.adjacency_node = adjacency_node
        self.weight = weight

    def __str__(self):
        return f'({self.adjacency_node}, {self.weight})'

    def __repr__(self):
        return f'({self.adjacency_node+1}, {self.weight})'


class Edge:
    def __init__(self, first_node, second_node, weight):
        self.first_node = first_node
        self.second_node = second_node
        self.weight = weight

    def __le__(self, other):
        return self.weight <= other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __str__(self):
        return f'({self.first_node}, {self.second_node}, {self.weight})'

    def __repr__(self):
        return f'({self.first_node}, {self.second_node}, {self.weight})'

    def __ne__(self, other):
        return self.first_node!=other.first_node or self.second_node!=other.second_node
    def __eq__(self, other):
        first = self.first_node==other.first_node and self.second_node==other.second_node
        second = self.first_node==other.second_node and self.second_node==other.first_node
        return first or second

    def is_incident(self, other):
        vertices = {self.first_node, self.second_node, other.first_node, other.second_node}
        return len(vertices)==3

class Graph:

    def __init__(self, n , **kwargs):
        if 'edge_list' in kwargs:
            self.edge_list = list(kwargs['edge_list'])
            self.edge_list.sort()
            self.edge_list = self.edge_list[::-1]
            self.adjacency_list = dict()
            self.graph_visualization = nx.Graph()
            for edge in self.edge_list:
                if edge.first_node not in self.adjacency_list:
                    self.adjacency_list[edge.first_node] = list()
                self.adjacency_list[edge.first_node].append(
                    Node(edge.second_node, edge.weight))


        if 'adjacency_list' in kwargs:
            self.adjacency_list = list(kwargs['adjacency_list'])
            self.edge_list = []
        for i in range(n):
            if i not in self.adjacency_list:
                continue
            for node in self.adjacency_list[i]:
                self.graph_visualization.add_edge(i, node.adjacency_node)
        self.n = n
        self.color_map = ['grey'] * self.n
        self.visit = [bool() for i in range(n)]
        self.d = []
        self.label = []
        self.is_cycle = False
        self.t = 0
        self.s = 0
        self.cmin = 0
        self.f = None

    def ford_falkerson(self, s, t):
        self.s = s
        self.t = t
        self.visit = [False for i in range(self.n)]
        self.f = [[0 for i in range(self.n)] for j in range(self.n)]
        self.color_map = ['grey'] * self.n
        added_flow = self.dfs_ford_falkerson(s, 2**32)
        max_flow = added_flow
        while added_flow > 0:
            self.visit = [False for i in range(self.n)]
            self.color_map = ['grey'] * self.n
            added_flow = self.dfs_ford_falkerson(s, 2**32)
            max_flow += added_flow
        print(f'Величина максимального потоак равна: {max_flow}')
        return max_flow

    def dfs_ford_falkerson(self, u, cmin):
        self.color_map = ['green' if node_visit else 'grey' for node_visit in self.visit]
        self.color_map[u] = 'blue'
        if u == self.t:
            self.color_map[u] = 'red'
            plt.subplot()
            nx.draw_shell(self.graph_visualization, node_color=self.color_map, node_size=900, with_labels=True, width=3)
            plt.show()
            return cmin
        self.visit[u] = True

        plt.subplot()
        nx.draw_shell(self.graph_visualization, node_color=self.color_map, node_size=900, with_labels=True, width=3)
        plt.show()
        for node in self.adjacency_list[u]:
            v = node.adjacency_node
            self.color_map[v] = 'yellow'
            nx.draw_shell(self.graph_visualization, node_color=self.color_map, node_size=900, with_labels=True, width=3)
            plt.show()
            self.color_map[v] = 'grey'
            if not self.visit[v] and self.f[u][v] < node.weight:
                delta = self.dfs_ford_falkerson(v, min(cmin, node.weight - self.f[u][v]))
                if delta > 0:
                    self.f[u][v] += delta
                    self.f[v][u] -= delta
                    return delta
        return 0


def main():
    edge_list = []
    n = 0
    with open('input.txt', 'r+') as f:
        line = f.readline()
        n, m = [int(i) for i in line.split(' ')]
        for line in f.readlines():
            a, b, w = [int(i) for i in line.split(' ')]
            edge = Edge(a-1, b - 1, w)
            edge_list.append(edge)

    graph = Graph(n, edge_list=edge_list)
    graph.ford_falkerson(0, 4)

main()