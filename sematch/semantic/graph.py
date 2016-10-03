from abc import ABCMeta, abstractmethod
from collections import deque
import networkx as nx
from itertools import combinations
import numpy as np

class DataTransform:
    """
    The interface of taxonomy data transformation. From skos, rdfs or any format, to
    nodes, edges, and labels.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def transform(self):
        """return nodes, labels, and edges"""
        pass

class Taxonomy:

    def __init__(self, dt):
        self._nodes, self._labels, self._edges = dt.transform()
        self._node2id = {value:i for i,value in enumerate(self._nodes)}
        self._label2id = {value:i for i, value in enumerate(self._labels)}
        #virtual root
        self._root = len(self._nodes) + 1
        self._taxonomy = nx.Graph()
        self._hyponyms = {}
        self._hypernyms = {}
        self.build_graph()

    def tree_encoder(self):
        # breadth first tree traverse to encode nodes
        # root is encoded as '#', a subnode of root is '#01' if code_length is 2
        # then a 3rd level node is '#01#01'
        # we can use string to encode tree strcuture for those trees without multiple inherences.
        id2code = {}
        id2code[self._root] = 'root'
        children_lengths = map(lambda x: len(self._hyponyms[x]), self._hyponyms.keys())
        n = max(children_lengths)
        code_length = 1
        for i in range(1, 8):
            if i * 10 - n > 0:
                break
            code_length = i
        coder = lambda x: "#%0*d" % (code_length, x)
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            if node in self._hyponyms:
                node_code = id2code[node]
                hypos = self._hyponyms[node]
                for i, child in enumerate(hypos):
                    queue.append(child)
                    id2code[child] = node_code + coder(i)
        return id2code


    def build_graph(self):
        map(self._taxonomy.add_node, range(self._root))
        parents, children = zip(*self._edges)
        parents_set = set(parents)
        children_set = set(children)
        root_children = []
        #to find out those node has no edges
        for i, n in enumerate(self._nodes):
            if i not in parents_set and i not in children_set:
                root_children.append(i)
        #find out those parents that are not appeared in children set
        for p in parents_set:
            if p not in children_set:
                root_children.append(p)
        for node in root_children:
            self._taxonomy.add_edge(self._root, node)
        for parent, child in self._edges:
            self._taxonomy.add_edge(parent, child)
        for parent, child in self._edges:
            self._hyponyms.setdefault(parent,[]).append(child)
        self._hyponyms[self._root] = root_children
        for parent, child in self._edges:
            self._hypernyms.setdefault(child, []).append(parent)
        for n in root_children:
            self._hypernyms[n] = [self._root]

    def shortest_path_length(self, node1, node2):
        return len(nx.shortest_path(self._taxonomy, node1, node2))

    def depth(self, node):
        return self.shortest_path_length(self._root, node)

    def least_common_subsumer(self, node1, node2):
        path1 = nx.shortest_path(self._taxonomy, node1, self._root)
        path2 = nx.shortest_path(self._taxonomy, node2, self._root)
        i = 1
        lcs = self._root
        while i <= len(path1) and i <= len(path2):
            if path1[-i] == path2[-i]:
                lcs = path1[-i]
            i = i + 1
        return lcs

    def hyponyms(self, node):
        return self._hyponyms[node] if self._hyponyms.get(node) else []

    def hypernyms(self, node):
        return self._hypernyms[node] if self._hypernyms.get(node) else []

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


