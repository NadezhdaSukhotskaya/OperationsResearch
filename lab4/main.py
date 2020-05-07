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
        return len(vertices) == 3


class Graph:
    def __init__(self, n , **kwargs):
        if 'edge_list' in kwargs:
            self.edge_list = list(kwargs['edge_list'])
            self.edge_list.sort()
            self.adjacency_list = dict()
            for edge in self.edge_list:
                if edge.first_node not in self.adjacency_list:
                    self.adjacency_list[edge.first_node] = list()
                if edge.second_node not in self.adjacency_list:
                    self.adjacency_list[edge.second_node] = list()
                self.adjacency_list[edge.first_node].append(
                    Node(edge.second_node, edge.weight))
                self.adjacency_list[edge.second_node].append(
                    Node(edge.first_node, edge.weight))
        if 'adjacency_list' in kwargs:
            self.adjacency_list = list(kwargs['adjacency_list'])
            self.edge_list = []
        self.n = n
        self.visit = [bool() for i in range(n)]
        self.d = []
        self.label = []
        self.is_cycle = False

    def has_cycle(self):
        self.visit = [False] * self.n
        self.is_cycle = False
        for key, value in self.adjacency_list.items():
            if not self.visit[key]:
                self.visit[key] = True
                self.dfs(key, -1)
                if self.is_cycle:
                    break
        return self.is_cycle

    def dfs(self, v, parent_node):
        self.visit[v] = True
        for node in self.adjacency_list[v]:
            if node.adjacency_node == parent_node:
                continue
            if not self.visit[node.adjacency_node]:
                self.dfs(node.adjacency_node, v)
            else:
                self.is_cycle = True
                return

    def get_incident_edges(self, edge_list):
        if not edge_list:
            return self.edge_list
        incident_edges = list()
        vertices_set = set()
        for edge in edge_list:
            vertices_set.add(edge.first_node)
            vertices_set.add(edge.second_node)
        for self_edge in self.edge_list:
            if self_edge in edge_list:
                continue
            if self_edge.first_node in vertices_set or self_edge.second_node in vertices_set:
                incident_edges.append(self_edge)
        return incident_edges

    def ford_bellman(self):
        d = [[2**32 for i in range(self.n)] for i in range(self.n)]
        for i in range(self.n):
            d[i][i] = 0

        graph_ = nx.Graph()
        color_map = ['grey']*self.n
        plt.subplot()
        for edge in self.edge_list:
            d[edge.first_node][edge.second_node] = edge.weight
            d[edge.second_node][edge.first_node] = edge.weight
            graph_.add_edge(edge.first_node, edge.second_node, weight=edge.weight, color="red")

        nx.draw_shell(graph_, node_color=color_map, node_size=900, with_labels=True, width=3)
        plt.show()
        labels = [Node(i, d[0][i]) for i in range(self.n)]
        k = 1

        while k <= self.n:
            next_step = False
            for i in range(self.n):
                min_route = 2**32
                for j in range(self.n):
                    color_map[i] = "blue"
                    color_map[j] = "yellow"
                    nx.draw_shell(graph_, node_color=color_map, node_size=900, with_labels=True, width=3)
                    plt.show()
                    if (labels[j].weight + d[j][i]) < min_route:
                        color_map[j] = "green"
                        nx.draw_shell(graph_, node_color=color_map, node_size=900, with_labels=True, width=3)
                        plt.show()
                        min_route = labels[j].weight + d[i][j]
                    color_map[j] = "grey"
                if min_route < labels[i].weight:
                    labels[i].weight = min_route
                    k=k+1
                    if k == self.n:
                        print(f'Граф имеет контур отрицательной длины. Задача не имеет решение.')
                        return None
                    break
                else:
                    if i == self.n - 1:
                        print(labels)
                        return labels
                color_map[i] = "grey"


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

    graph_ = nx.Graph()
    color_map = ['grey'] * n
    plt.subplot()
    for edge in edge_list:
        graph_.add_edge(edge.first_node, edge.second_node, weight=edge.weight, color="red")
    nx.draw_shell(graph_, node_color=color_map, node_size=900, with_labels=True, width=3)
    plt.show()

    graph = Graph(n, edge_list=edge_list)
    graph.ford_bellman()

main()