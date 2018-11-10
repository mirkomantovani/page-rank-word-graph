# Mirko Mantovani


class UndirectedGraph:
    def __init__(self):
        self.graph = {}

    def __repr__(self):
        return 'Graph:'+ str(self.graph)

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, i, j, weight):
        if i not in self.graph:
            self.add_node(i)
        if j not in self.graph:
            self.add_node(j)
        self.graph[i][j] = weight
        self.graph[j][i] = weight

    def get_edge(self, i, j):
        if i in self.graph:
            if j in self.graph[i]:
                return self.graph[i][j]
        return -1