from nltk.corpus import wordnet as wn
from scipy.stats import spearmanr
from scipy.stats import pearsonr
from scipy.stats import kendalltau
from sematch.semantic.similarity import Similarity
from sematch.semantic.relatedness import Relatedness
from sematch.utility import FileIO
import networkx as nx
import numpy as np
import random
import math
import csv

class Result:

    def __init__(self, name):
        self.name = name
        self.data = FileIO.read_list_file('eval/results/%s' % self.name)

    def ratings(self):
        methods = self.data[0].split()[2:]
        scores = {m:[] for m in methods}
        for r in self.data[1:]:
            items = r.split()[2:]
            for i in range(len(items)):
                scores[methods[i]].append(float(items[i]))
        return scores

class Dataset:

    def __init__(self, name):
        self.name = name
        self.data = FileIO.read_list_file('eval/lexical/%s' % self.name)
        self.dataset_info()

    def dataset_info(self):
        print 'name ', self.name
        print 'size', len(self.data)

    def pairs(self):
        return map(lambda x: (x.split()[0], x.split()[1]), self.data)

    def human(self):
        h = map(lambda x: x.split()[2], self.data)
        return map(float, h)


class Evaluation:

    def __init__(self):
        self.sim = Similarity()

    def has_type(self, lst):
        for l in lst:
            if l != 0:
                return True
        return False

    def check_word_graph(self, w1, w2):
        s1 = wn.synsets(w1, pos=wn.NOUN)
        s2 = wn.synsets(w2, pos=wn.NOUN)
        lcs= [self.sim.concept_graph_freq(self.sim.least_common_subsumer(c1,c2)) for c1 in s1 for c2 in s2]
        return self.has_type(lcs)

    def check_word_type(self, w1, w2):
        s1 = wn.synsets(w1, pos=wn.NOUN)
        s2 = wn.synsets(w2, pos=wn.NOUN)
        s1_count = [self.sim.concept_graph_freq(s) for s in s1]
        s2_count = [self.sim.concept_graph_freq(s) for s in s2]
        return self.has_type(s1_count) and self.has_type(s2_count)

    def check_word_noun(self, w1, w2):
        s1 = wn.synsets(w1, pos=wn.NOUN)
        s2 = wn.synsets(w2, pos=wn.NOUN)
        if s1 and s2:
            return True
        return False

    def create_sub_dataset(self, dataset, check_words, filename):
        data = []
        pairs = dataset.pairs()
        human = dataset.human()
        for i in range(len(pairs)):
            w1,w2 = pairs[i]
            h = human[i]
            if check_words(w1,w2):
                data.append(' '.join([w1,w2,str(h)]))
        FileIO.save_list_file('eval/lexical/%s'% filename, data)

    def sim_eval_wpath_k(self, cor_measure, method, dataset):
        print dataset.name
        for k in range(1, 11):
            sim = [self.sim.word_similarity_wpath(w1,w2,method, k/10.0) for w1,w2 in dataset.pairs()]
            sim = map(lambda x:round(x,3), sim)
            cor = self.correlation(cor_measure)(sim, dataset.human())[0]
            cor = "%.3f" % round(cor,3)
            print k, ' ', cor

    def sim_eval_memory(self, cor_measure, methods, dataset):
        print dataset.name
        for m in methods:
            sim = [self.sim.word_similarity(w1,w2,m) for w1,w2 in dataset.pairs()]
            sim = map(lambda x:round(x,3), sim)
            cor = self.correlation(cor_measure)(sim, dataset.human())[0]
            cor = "%.3f" % round(cor,3)
            print m, ' ', cor

    def sim_eval_file(self, methods, dataset):
        result = []
        result.append(' '.join(['word1','word2']+methods))
        for w1,w2 in dataset.pairs():
            scores = [self.sim.word_similarity(w1,w2,m) for m in methods]
            scores = map(lambda x:"%.3f" % round(x,3),scores)
            result.append(' '.join([w1,w2]+scores))
        FileIO.save_list_file('eval/results/%s'% dataset.name, result)

    def sim_eval_analysis_file(self, cor_measure, filename):
        print filename
        dataset = Dataset(filename)
        result = Result(filename)
        ratings = result.ratings()
        for key in ratings:
            cor = self.correlation(cor_measure)(ratings[key], dataset.human())[0]
            cor = "%.3f" % round(cor,3)
            print key, ' ', cor

    def correlation(self, name):
        def function(x, y):
            return getattr(self, name)(x,y)
        return function

    def spearman(self,x,y):
        return spearmanr(x,y)

    def pearson(self,x,y):
        return pearsonr(x,y)

    def kendal(self,x,y):
        return kendalltau(x,y)



# data = FileIO.read_list_file('eval/lexical/SimLex-999.txt')
# data = data[1:]
# data_p = []
# for d in data:
#     l = d.split()
#     if l[2] == 'N':
#         data_p.append(' '.join([l[0],l[1],l[3]]))
# FileIO.save_list_file('eval/lexical/simlex_n.txt',data_p)

#   word similarity of noun
#   noun_rg.txt
#   noun_mc.txt
#   noun_ws353.txt
#   noun_ws353-sim.txt
#   noun_simlex.txt

#   the lcs is in graph
#   graph_rg.txt
#   graph_mc.txt
#   graph_ws353.txt
#   graph_ws353-sim.txt
#   graph_simlex.txt

#   both words are in graph
#   type_rg.txt
#   type_mc.txt
#   type_ws353.txt
#   type_ws353-sim.txt
#   type_simlex.txt

eval = Evaluation()
sim_methods_noun = ['path','lch','wup','li','res','lin','jcn','wpath']
sim_methods_graph = ['path','lch','wup','li','res','res_graph','lin','jcn','wpath','wpath_graph']
sim_methods_type = ['path','lch','wup','li','res','res_graph','lin','lin_graph','jcn','jcn_graph','wpath','wpath_graph']
word_noun = ['noun_rg.txt','noun_mc.txt','noun_ws353.txt','noun_ws353-sim.txt','noun_simlex.txt']
word_graph = ['graph_rg.txt','graph_mc.txt','graph_ws353.txt','graph_ws353-sim.txt','graph_simlex.txt']
word_type = ['type_rg.txt','type_mc.txt','type_ws353.txt','type_ws353-sim.txt','type_simlex.txt']
datasets = [Dataset(f) for f in word_type]
# for d in datasets:
#     eval.sim_eval_file(sim_methods_type, d)
# for f in word_type:
#     eval.sim_eval_analysis_file('spearman', f)
#datasets = ['noun_rg.txt']
#datasets = [Dataset(d) for d in datasets]
#for d in datasets:
#    eval.sim_eval_file(sim_methods,d)
#for d in datasets:
#    check_words = eval.check_word_graph
    #check_words = eval.check_word_type
    #check_words = eval.check_word_noun
#    eval.create_sub_dataset(d, check_words, 'graph_simlex.txt')
#eval.sim_eval_analysis_file('spearman','noun_rg.txt')
for d in datasets:
    eval.sim_eval_wpath_k('spearman', 'wpath_graph', d)