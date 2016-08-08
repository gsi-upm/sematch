from itertools import combinations
import networkx as nx
import numpy as np

class SimGraph:
    '''
    General Purpose Similarity Net

    The nodes in graph represent general purpose object such as synset, word, phrase,
    sentence, document, entity.

    The edges in graph represent general purpose object similarity. The similarity score between
    objects is ranged in [0,1] and computed by specific similarity measures. It can measuring
    taxonomical similarity, general purpose similarity or hybrid similarity.
    '''

    def __init__(self, object_list, similarity, threshold):
        self.sim = similarity
        self.object_list = object_list
        self.threshold = threshold
        self.id2object = {i:self.object_list[i] for i in range(len(self.object_list))}
        self.graph = self.sim_graph(self.sim_matrix())

    def sim_matrix(self):
        N = len(self.object_list)
        M = np.zeros((N, N), dtype=np.float64)
        for i in range(N):
            M[i,i] = 1.0
        for x,y in combinations(range(N), 2):
            score = self.sim(self.id2object[x], self.id2object[y])
            if score > self.threshold:
                M[x,y] = score
        return M

    def sim_graph(self, M):
        return nx.from_numpy_matrix(M)

    def page_rank(self):
        return nx.pagerank(self.graph)

    def hits(self):
        '''h, a = hits() hub and authority'''
        return nx.hits(self.graph)

    def minimum_spanning_tree(self):
        return nx.minimum_spanning_tree(self.graph)



#
# entity_list = ['Steve Jobs', 'Steve Wozniak', 'Jonathan Ivex', 'Mac Pro']
#
# sim = lambda x, y: len(x) + len(y)
#
# sim_graph = SimGraph(entity_list, sim, 0)
# print sim_graph.page_rank()
# print sim_graph.hits()
# sim_graph.draw2file(sim_graph.minimum_spanning_tree())

