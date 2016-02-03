from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content
from sematch.knowledge import graph
from sematch.semantic.score import Score
from sematch.utility import FileIO
import math

def graph_ic_reader(filename):
    data = FileIO.read_list_file(filename)
    ic_dic = {}
    for d in data:
        item = d.split()
        offset = int(item[0])
        count = int(item[1])
        ic_dic[offset] = count
    return ic_dic

def graph_ic_writer(filename, items):
    data = []
    for key in items.keys():
        data.append(' '.join([str(key),str(items[key])]))
    FileIO.append_list_file(filename, data)


class Similarity(Score):

    def __init__(self):
        self.ic_corpus = wordnet_ic.ic('ic-brown.dat')
        self.ic_graph = graph_ic_reader('db/graph-ic.txt')
        self.wn_max_depth = 19
        self.graph = graph.KnowledgeGraph()
        self.entity_N = self.graph.entity_N()

    def word_similarity_wpath(self, w1, w2, m, k):
        s1 = wn.synsets(w1, pos=wn.NOUN)
        s2 = wn.synsets(w2, pos=wn.NOUN)
        scores = [self.k_method(m)(c1, c2, k) for c1 in s1 for c2 in s2]
        return max(scores)

    def word_similarity(self, w1, w2, name='wup'):
        sim = self.method(name)
        s1 = wn.synsets(w1, pos=wn.NOUN)
        s2 = wn.synsets(w2, pos=wn.NOUN)
        scores = [sim(c1, c2) for c1 in s1 for c2 in s2]
        return max(scores)

    def pmi(self, c1, c2):
        freq_1 = self.graph.synset_entity_count(c1)
        freq_2 = self.graph.synset_entity_count(c2)
        freq_common = self.graph.synset_coocurrence(c1,c2)
        p_1 = 1.0 * freq_1 / self.entity_N
        p_2 = 1.0 * freq_2 / self.entity_N
        p_12 = 1.0 * freq_common / self.entity_N
        if p_1 == 0 or p_2 == 0:
            return 0
        prob = p_12/(p_1*p_2)
        if prob < 0.0001:
            return 0
        return math.log(prob)

    def least_common_subsumer(self, c1, c2):
        return c1.lowest_common_hypernyms(c2)[0]

    def synset_ic(self, c):
        return information_content(c, self.ic_corpus)

    def concept_graph_freq(self, c):
        key = c.offset()
        if key in self.ic_graph:
            return self.ic_graph[key]
        count = self.graph.synset_entity_count(c)
        graph_ic_writer('db/graph-ic.txt',{key:count})
        self.ic_graph[key] = count
        return count

    def entity_ic(self, c):
        freq = self.concept_graph_freq(c)
        if freq == 0:
            return 0
        prob = 1.0 * freq / self.entity_N
        return -math.log(prob)

    def res_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        return self.entity_ic(lcs)

    def lin_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        lcs_ic = self.entity_ic(lcs)
        c1_ic = self.entity_ic(c1)
        c2_ic = self.entity_ic(c2)
        combine = c1_ic + c2_ic
        if c1_ic == 0 or c2_ic == 0:
            return 0
        return 2.0 * lcs_ic / combine

    def jcn_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        lcs_ic = self.entity_ic(lcs)
        c1_ic = self.entity_ic(c1)
        c2_ic = self.entity_ic(c2)
        lcs_ic = 2.0 * lcs_ic
        if c1_ic == 0 or c2_ic == 0:
            return 0
        return 1.0/1+(c1_ic + c2_ic - lcs_ic)

    def dpath(self, c1, c2, alpha=1.0, beta=1.0):
        lcs = self.least_common_subsumer(c1, c2)
        path = c1.shortest_path_distance(c2)
        path = 1.0 / (1 + path)
        path = path**alpha
        depth = lcs.max_depth() + 1
        depth = depth*1.0/(1 + self.wn_max_depth)
        depth = depth**beta
        return math.log(1+path*depth,2)

    def wpath(self, c1, c2, k=0.8):
        lcs = self.least_common_subsumer(c1,c2)
        path = c1.shortest_path_distance(c2)
        weight = k ** self.synset_ic(lcs)
        return 1.0 / (1 + path*weight)

    def wpath_graph(self, c1,c2, k=0.8):
        lcs = self.least_common_subsumer(c1,c2)
        path = c1.shortest_path_distance(c2)
        weight = k ** self.entity_ic(lcs)
        return 1.0 / (1 + path*weight)

    def li(self, c1, c2, alpha=0.2,beta=0.6):
        path = c1.shortest_path_distance(c2)
        lcs = self.least_common_subsumer(c1, c2)
        depth = lcs.max_depth()
        x = math.exp(-alpha*path)
        y = math.exp(beta*depth)
        z = math.exp(-beta*depth)
        a = y - z
        b = y + z
        return x * (a/b)

    def path(self, c1, c2):
        return c1.path_similarity(c2)

    def wup(self, c1, c2):
        return c1.wup_similarity(c2)

    def lch(self, c1, c2):
        return c1.lch_similarity(c2)

    def res(self, c1, c2):
        return c1.res_similarity(c2, self.ic_corpus)

    def jcn(self, c1, c2):
        lcs = self.least_common_subsumer(c1, c2)
        c1_ic = self.synset_ic(c1)
        c2_ic = self.synset_ic(c2)
        lcs_ic = self.synset_ic(lcs)
        diff = c1_ic + c2_ic - 2*lcs_ic
        return 1.0/(1 + diff)

    def lin(self, c1, c2):
        return c1.lin_similarity(c2, self.ic_corpus)
