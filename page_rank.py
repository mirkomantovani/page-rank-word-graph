import sys
sys.setrecursionlimit(1500)


class PageRank:
    def __init__(self, word_graph, alpha=0.85):
        self.alpha = alpha
        self.word_graph = word_graph

    def s(self, i, p, previous_s):

        return self.alpha * sum(self.word_graph.get_edge(j, i) / sum(self.word_graph.get_edge(j, k)
                                                                     for k in self.word_graph.graph[j]) * previous_s[j]
                                for j in self.word_graph.graph[i]) + (1 - self.alpha) * p[i]

    def page_rank(self,  convergence):

        p = {}
        page_rank = {}
        last_page_rank = {}

        for node in self.word_graph.graph:
            p[node] = 1/len(self.word_graph.graph)
            page_rank[node] = 1/len(self.word_graph.graph)
            last_page_rank[node] = 1/len(self.word_graph.graph)
        for iteration in range(0, convergence):
            for i in self.word_graph.graph:
                page_rank[i] = self.s(i, p, last_page_rank)
            #normalization and updating steps
            total_weight = sum(page_rank[i]**2 for i in page_rank)**(1/2)
            for i in page_rank:
                # ??
                page_rank[i] = page_rank[i] / total_weight
                last_page_rank[i] = page_rank[i]
        return page_rank
