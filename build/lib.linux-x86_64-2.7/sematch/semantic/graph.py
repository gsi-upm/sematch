#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2017 Ganggao Zhu- Grupo de Sistemas Inteligentes
# gzhu[at]dit.upm.es
# DIT, UPM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from abc import ABCMeta, abstractmethod
from collections import deque
from itertools import combinations

import networkx as nx
import numpy as np

from sematch.semantic.ontology import DBpedia
from sematch.utility import FileIO


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

class DBpediaDataTransform(DataTransform):

    def __init__(self):
        self._ontology = DBpedia()

    def transform(self):
        nodes =  map(lambda x:x.toPython(), self._ontology.classes)
        node_id = {n:i for i,n in enumerate(nodes)}
        labels = [self._ontology.token(value) for i,value in enumerate(self._ontology.classes)]
        edges = []
        for i, node in enumerate(nodes):
            children = self._ontology.subClass(node)
            children = [child for child in children if child in nodes]
            children_ids = map(lambda x:node_id[x], children)
            for child_id in children_ids:
                edges.append((i, child_id))
        return nodes, labels, edges

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
        return self._hyponyms[node] if node in self._hyponyms else []

    def hypernyms(self, node):
        return self._hypernyms[node] if node in self._hypernyms else []

class SimGraph:
    '''
    General Purpose Similarity Graph which is used to perform graph analysis.

    The nodes in graph represent general purpose object such as concept, word, phrase,
    sentence, document, entity.

    The edges in graph represent semantic similarity between nodes. The similarity score between
    objects is ranged in [0,1] and computed by specific similarity measures.

    '''

    def __init__(self, nodes, sim_metric, threshold=0.0):
        self._nodes = nodes
        self._sim_metric = sim_metric
        self._threshold = threshold
        self._graph = self.similarity_graph(self.similarity_matrix())

    def similarity_matrix(self):
        """
        :return: a similarity matrix
        """
        N = len(self._nodes)
        M = np.zeros((N, N), dtype=np.float64)
        for i in range(N):
            M[i,i] = 1.0
        for x,y in combinations(range(N), 2):
            score = self._sim_metric(self._nodes[x], self._nodes[y])
            if score > self._threshold:
                M[x,y] = score
            else:
                M[x,y] = 0.0
        return M

    def similarity_graph(self, M):
        return nx.from_numpy_matrix(M)

    def page_rank(self):
        rank_scores = nx.pagerank(self._graph)
        return {self._nodes[key]: value for key, value in rank_scores.iteritems()}

    def hits(self):
        '''h, a = hits() hub and authority'''
        return nx.hits(self._graph)

    def minimum_spanning_tree(self):
        return nx.minimum_spanning_tree(self._graph)

from sematch.semantic.sparql import StatSPARQL
import math

class GraphIC:

    """
    This class is used to compute graph-based IC in knowledge graph, which is
    basically the proportion of instances tagged with a specific concept
    """

    def __init__(self, ic_file):
        self._ic_file = ic_file
        self._graph_ic = self.graph_ic_reader(ic_file)
        self._graph_stats = StatSPARQL()
        self._N = self._graph_stats.entity_N()

    def concept_ic(self, concept):
        """
        Compute the ic value of a concept using sparql query
        :param concept: a id of concept, here is the uri of concept
        :return: the ic value of the concept
        """
        if concept in self._graph_ic:
            return self._graph_ic[concept]
        else:
            freq = int(self._graph_stats.concept_freq(concept))
            if freq == 0:
                ic = 0.0
            else:
                prob = 1.0 * freq / self._N
                ic = -math.log(prob)
            self.graph_ic_writer(self._ic_file, [{'concept':concept, 'ic':str(ic)}])
            self._graph_ic[concept] = ic
            return ic

    def graph_ic_reader(self, filename):
        """
        Load the saved IC values
        :param filename: the file containing IC values of concepts
        :return: a dictionary concept:IC
        """
        data = FileIO.read_json_file(filename)
        return {d['concept']:float(d['ic']) for d in data}

    def graph_ic_writer(self, filename, data):
        """
        Save the ic values for a concept for faster access.
        :param filename:
        :param data:
        :return:
        """
        FileIO.append_json_file(filename, data)


