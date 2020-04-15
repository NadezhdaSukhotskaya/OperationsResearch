import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, adjacency_node, weight):
        self.adjacency_node = adjacency_node
        self.weight = weight

    def __str__(self):
        return f'{self.adjacency_node}, {self.weight}'

    def __repr__(self):
        return f'{self.adjacency_node}, {self.weight}'


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


n = 0
visit = []
is_cycle = False


def get_induced_adjacency_list(edge_list):
    induced_adjacency_list = dict()
    for edge in edge_list:
        first_node = edge.first_node
        second_node = edge.second_node
        weight = edge.weight

        node1 = Node(first_node, weight)
        node2 = Node(second_node, weight)
        if first_node not in induced_adjacency_list:
            induced_adjacency_list[first_node] = list()
        if second_node not in induced_adjacency_list:
            induced_adjacency_list[second_node] = list()
        induced_adjacency_list[first_node].append(node2)
        induced_adjacency_list[second_node].append(node1)
    return induced_adjacency_list


def dfs(v, parent_node, adjacency_list):
    global visit
    visit[v] = True
    global is_cycle
    for node in adjacency_list[v]:
        if node.adjacency_node == parent_node:
            continue
        if not visit[node.adjacency_node]:
            dfs(node.adjacency_node, v, adjacency_list)
        else:
            is_cycle = True
            return
        if is_cycle:
            return
    is_cycle = False


def kruskals_algorithm(adjacency_list):
    sort_edge_list = [Edge(index_, node.adjacency_node, node.weight) for index_, nodes in enumerate(adjacency_list) for
                      node in nodes]
    sort_edge_list.sort()

    global n

    I_j = []

    global visit, is_cycle
    visit = [False] * n

    j = 0

    while len(I_j) < n - 1:
        if j >= len(sort_edge_list):
            j = 0
        edge = sort_edge_list[j]
        temp_I_j = list(I_j)
        temp_I_j.append(edge)
        temp_adjacency_I_j = get_induced_adjacency_list(temp_I_j)
        is_cycle = False
        visit = [False] * n
        for key, value in temp_adjacency_I_j.items():
            if not visit[key]:
                visit[key] = True
                dfs(key, -1, temp_adjacency_I_j)
                if is_cycle:
                    break
        if not is_cycle:
            I_j.append(edge)

        j += 1
        graph_ = nx.Graph()

        for edge in I_j:
            first_node = edge.first_node
            second_node = edge.second_node
            w = edge.weight
            graph_.add_edge(first_node + 1, second_node + 1)

        plt.subplot()
        nx.draw_shell(graph_, node_color='deepskyblue', node_size=900, with_labels=True, width=3, edge_color='navy')
        plt.show()


    graph_ = nx.Graph()

    for edge in I_j:
        first_node = edge.first_node
        second_node= edge.second_node
        w= edge.weight
        graph_.add_edge(first_node+1, second_node+1)

    plt.subplot()
    nx.draw_shell(graph_, node_color='deepskyblue', node_size=900, with_labels=True, width=3, edge_color='navy')
    plt.show()
    print("u_i, v_i, w_, где u_i, v_i - концы ребра, w_i - его вес")
    for edge in I_j:
        first_node = edge.first_node
        second_node = edge.second_node
        weight = edge.weight
        print(first_node + 1, second_node + 1, weight)

def main():
    adjacency_list = []
    global n
    with open('input.txt', 'r+') as f:
        line = f.readline()
        n, m = [int(i) for i in line.split(' ')]
        adjacency_list = [list() for i in range(n)]
        for line in f.readlines():
            a, b, w = [int(i) for i in line.split(' ')]
            node = Node(b - 1, w)
            adjacency_list[a - 1].append(node)

    kruskals_algorithm(adjacency_list)


main()
