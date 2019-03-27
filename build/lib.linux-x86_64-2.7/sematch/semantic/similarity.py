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
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content

from sematch.semantic.sparql import EntityFeatures, StatSPARQL
from sematch.semantic.graph import GraphIC
from sematch.utility import FileIO, memoized


import math
from collections import Counter

class ConceptSimilarity:
    """
    This class is used to compute taxonomical semantic similarity scores between
    concepts that are located in a concept taxonomy. A taxonomy object needs to be passed into
    this class in order to find the structural information of concepts such as depth, path length,
    and so on. The graph-based IC is needed for semantic similarity measures wpath, res, lin, jcn.
    """
    def __init__(self, taxonomy, ic_file):
        self._taxonomy = taxonomy
        self._concepts = taxonomy._nodes
        self._concept2node = taxonomy._node2id
        self._label2concepts = {label:self._concepts[i] for i, label in enumerate(taxonomy._labels)}
        self._graph_ic = GraphIC(ic_file)

    def hyponyms(self, concept):
        if concept in self._concept2node:
            nodes = self._taxonomy.hyponyms(self._concept2node[concept])
            return [self._concepts[n] for n in nodes]
        return []

    def hypernyms(self, concept):
        if concept in self._concept2node:
            nodes = self._taxonomy.hypernyms(self._concept2node[concept])
            return [self._concepts[n] for n in nodes]
        return []

    def shortest_path_length(self, concept1, concept2):
        n1 = self._concept2node[concept1]
        n2 = self._concept2node[concept2]
        return self._taxonomy.shortest_path_length(n1, n2)

    def depth(self, concept):
        if concept == 'root':
            return 1
        n = self._concept2node[concept]
        return self._taxonomy.depth(n)

    def least_common_subsumer(self, concept1, concept2):
        n1 = self._concept2node[concept1]
        n2 = self._concept2node[concept2]
        n = self._taxonomy.least_common_subsumer(n1, n2)
        if n > len(self._concepts):
            return 'root'
        return self._concepts[n]

    def method(self, name):
        def function(c1, c2):
            score = getattr(self, name)(c1, c2)
            return abs(score)
        return function

    def name2concept(self, name):
        return self._label2concepts[name] if name in self._label2concepts else []

    def concept_ic(self, concept):
        """
        Get the graph-based IC of a concept. the ic of virtual root is 0
        :param concept: the node id of concept
        :return: the ic value of concept
        """
        if concept == 'root':
            return 0.0
        else:
            return self._graph_ic.concept_ic(concept)

    @memoized
    def similarity(self, c1, c2, name='wpath'):
        """
        Compute semantic similarity between two concepts
        :param c1:
        :param c2:
        :param name:
        :return:
        """
        if c1 not in self._concept2node or c2 not in self._concept2node:
            return 'link error'
        return self.method(name)(c1, c2)

    def path(self, c1, c2):
        """
        Rada's shortest path based similarity metric
        :param c1:
        :param c2:
        :return: similarity score in [0,1]
        """
        return 1.0/ self.shortest_path_length(c1, c2)

    def wup(self, c1, c2):
        """
        Wu and Palm's similarity metric
        :param c1:
        :param c2:
        :return:
        """
        lcs = self.least_common_subsumer(c1, c2)
        depth_c1 = self.depth(c1)
        depth_c2 = self.depth(c2)
        depth_lcs = self.depth(lcs)
        return 2.0*depth_lcs / (depth_c1 + depth_c2)

    def li(self, c1, c2, alpha=0.2, beta=0.6):
        path = self.shortest_path_length(c1, c2) - 1
        lcs = self.least_common_subsumer(c1, c2)
        depth = self.depth(lcs)
        # print path, lcs, depth
        x = math.exp(-alpha * path)
        y = math.exp(beta * depth)
        # print y
        z = math.exp(-beta * depth)
        a = y - z
        b = y + z
        return x * (a / b)

    def res(self, c1, c2):
        lcs = self.least_common_subsumer(c1, c2)
        return self.concept_ic(lcs)

    def lin(self, c1, c2):
        lcs = self.least_common_subsumer(c1, c2)
        lcs_ic = self.concept_ic(lcs)
        c1_ic = self.concept_ic(c1)
        c2_ic = self.concept_ic(c2)
        combine = c1_ic + c2_ic
        if c1_ic == 0.0 or c2_ic == 0.0:
            return 0.0
        return 2.0 * lcs_ic / combine

    def jcn(self, c1, c2):
        lcs = self.least_common_subsumer(c1, c2)
        lcs_ic = self.concept_ic(lcs)
        c1_ic = self.concept_ic(c1)
        c2_ic = self.concept_ic(c2)
        lcs_ic = 2.0 * lcs_ic
        if c1_ic == 0.0 or c2_ic == 0.0:
            return 0.0
        return 1.0 / 1 + (c1_ic + c2_ic - lcs_ic)

    def wpath(self, c1, c2, k=0.8):
        lcs = self.least_common_subsumer(c1, c2)
        path = self.shortest_path_length(c1, c2) - 1
        weight = k ** self.concept_ic(lcs)
        return 1.0 / (1 + path * weight)



class WordNetSimilarity:

    """Extend the NLTK's WordNet with more similarity metrics, word lemmatization, and multilingual."""

    def __init__(self, ic_corpus='brown'):
        self._ic_corpus = wordnet_ic.ic('ic-brown.dat') if ic_corpus == 'brown' else wordnet_ic.ic('ic-semcor.dat')
        self._wn_max_depth = 19
        self._default_metrics = ['path','lch','wup','li','res','lin','jcn','wpath']
        self._wn_lemma = WordNetLemmatizer()

    def method(self, name):
        def function(syn1, syn2):
            score = getattr(self, name)(syn1, syn2)
            return abs(score)
        return function

    def synset_expand(self, s):
        result = [s]
        hypos = s.hyponyms()
        if not hypos:
            return result
        for h in hypos:
            result.extend(self.synset_expand(h))
        return result

    #return all the noun synsets in wordnet
    def get_all_synsets(self):
        return wn.all_synsets('n')

    def get_all_lemma_names(self):
        return wn.all_lemma_names('n')

    def offset2synset(self, offset):
        '''
        offset2synset('06268567-n')
        Synset('live.v.02')
        '''
        return wn._synset_from_pos_and_offset(str(offset[-1:]), int(offset[:8]))

    def synset2offset(self, ss):
        return '%08d-%s' % (ss.offset(), ss.pos())

    #semcor live%2:43:06::
    def semcor2synset(self, sense):
        return wn.lemma_from_key(sense).synset()

    def semcor2offset(self, sense):
        '''
        semcor2synset('editorial%1:10:00::')
        06268567-n
        '''
        return self.synset2offset(self.semcor2synset(sense))

    def word2synset(self, word, pos=wn.NOUN):
        word = self._wn_lemma.lemmatize(word)
        return wn.synsets(word, pos)

    def multilingual2synset(self, word, lang='spa'):
        """
        Map words in different language to wordnet synsets
        ['als', 'arb', 'cat', 'cmn', 'dan', 'eng', 'eus', 'fas', 'fin', 'fra', 'fre',
         'glg', 'heb', 'ind', 'ita', 'jpn', 'nno','nob', 'pol', 'por', 'spa', 'tha', 'zsm']
        :param word: a word in different language that has been defined in
         Open Multilingual WordNet, using ISO-639 language codes.
        :param lang: the language code defined
        :return: wordnet synsets.
        """
        return wn.synsets(word.decode('utf-8'), lang=lang, pos=wn.NOUN)


    @memoized
    def similarity(self, c1, c2, name='wpath'):
        """
        Compute semantic similarity between two concepts
        :param c1:
        :param c2:
        :param name:
        :return:
        """
        return self.method(name)(c1, c2)

    def max_synset_similarity(self, syns1, syns2, sim_metric):
        """
        Compute the maximum similarity score between two list of synsets
        :param syns1: synset list
        :param syns2: synset list
        :param sim_metric: similarity function
        :return: maximum semantic similarity score
        """
        return max([sim_metric(c1, c2) for c1 in syns1 for c2 in syns2] + [0])

    @memoized
    def word_similarity(self, w1, w2, name='wpath'):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        sim_metric = lambda x, y: self.similarity(x, y, name)
        return self.max_synset_similarity(s1, s2, sim_metric)

    @memoized
    def best_synset_pair(self, w1, w2, name='wpath'):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        sims = Counter({(c1, c2):self.similarity(c1, c2, name) for c1 in s1 for c2 in s2})
        return sims.most_common(1)[0][0]

    def word_similarity_all_metrics(self, w1, w2):
        return {m:self.word_similarity(w1, w2, name=m) for m in self._default_metrics}

    @memoized
    def word_similarity_wpath(self, w1, w2, k):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        sim_metric = lambda x, y: self.wpath(x, y, k)
        return self.max_synset_similarity(s1, s2, sim_metric)

    @memoized
    def monol_word_similarity(self, w1, w2, lang='spa', name='wpath'):
        """
         Compute mono-lingual word similarity, two words are in same language.
        :param w1: word
        :param w2: word
        :param lang: language code
        :param name: name of similarity metric
        :return: semantic similarity score
        """
        s1 = self.multilingual2synset(w1, lang)
        s2 = self.multilingual2synset(w2, lang)
        sim_metric = lambda x, y: self.similarity(x, y, name)
        return self.max_synset_similarity(s1, s2, sim_metric)

    @memoized
    def crossl_word_similarity(self, w1, w2, lang1='spa', lang2='eng', name='wpath'):
        """
         Compute cross-lingual word similarity, two words are in different language.
        :param w1: word
        :param w2: word
        :param lang1: language code for word1
        :param lang2: language code for word2
        :param name: name of similarity metric
        :return: semantic similarity score
        """
        s1 = self.multilingual2synset(w1, lang1)
        s2 = self.multilingual2synset(w2, lang2)
        sim_metric = lambda x, y: self.similarity(x, y, name)
        return self.max_synset_similarity(s1, s2, sim_metric)

    def least_common_subsumer(self, c1, c2):
        return c1.lowest_common_hypernyms(c2)[0]

    def synset_ic(self, c):
        return information_content(c, self._ic_corpus)

    def dpath(self, c1, c2, alpha=1.0, beta=1.0):
        lcs = self.least_common_subsumer(c1, c2)
        path = c1.shortest_path_distance(c2)
        path = 1.0 / (1 + path)
        path = path**alpha
        depth = lcs.max_depth() + 1
        depth = depth*1.0/(1 + self._wn_max_depth)
        depth = depth**beta
        return math.log(1+path*depth,2)

    def wpath(self, c1, c2, k=0.8):
        lcs = self.least_common_subsumer(c1,c2)
        path = c1.shortest_path_distance(c2)
        weight = k ** self.synset_ic(lcs)
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
        return c1.res_similarity(c2, self._ic_corpus)

    def jcn(self, c1, c2):
        lcs = self.least_common_subsumer(c1, c2)
        c1_ic = self.synset_ic(c1)
        c2_ic = self.synset_ic(c2)
        lcs_ic = self.synset_ic(lcs)
        diff = c1_ic + c2_ic - 2*lcs_ic
        return 1.0/(1 + diff)

    def lin(self, c1, c2):
        return c1.lin_similarity(c2, self._ic_corpus)



class YagoTypeSimilarity(WordNetSimilarity):

    """Extend the WordNet synset to linked data through YAGO mappings"""

    def __init__(self, graph_ic='models/yago_type_ic.txt', mappings="models/type-linkings.txt"):
        WordNetSimilarity.__init__(self)
        self._graph_ic = GraphIC(graph_ic)
        self._mappings = FileIO.read_json_file(mappings)
        self._id2mappings = {data['offset']: data for data in self._mappings}
        self._yago2id = {data['yago_dbpedia']: data['offset'] for data in self._mappings}

    def synset2id(self, synset):
        return str(synset.offset() + 100000000)

    def id2synset(self, offset):
        x = offset[1:]
        return wn._synset_from_pos_and_offset('n', int(x))

    def synset2mapping(self, synset, key):
        mapping_id = self.synset2id(synset)
        if mapping_id in self._id2mappings:
            mapping = self._id2mappings[mapping_id]
            return mapping[key] if key in mapping else None
        else:
            return None

    def synset2yago(self, synset):
        return self.synset2mapping(synset,'yago_dbpedia')

    def synset2dbpedia(self, synset):
        return self.synset2mapping(synset, 'dbpedia')

    def yago2synset(self, yago):
        if yago in self._yago2id:
            return self.id2synset(self._yago2id[yago])
        return None

    def word2dbpedia(self, word):
        return [self.synset2dbpedia(s) for s in self.word2synset(word) if self.synset2dbpedia(s)]

    def word2yago(self, word):
        return [self.synset2yago(s) for s in self.word2synset(word) if self.synset2yago(s)]

    def yago_similarity(self, yago1, yago2, name='wpath'):
        """
        Compute semantic similarity of two yago concepts by mapping concept uri to wordnet synset.
        :param yago1: yago concept uri
        :param yago2: yago concept uri
        :param name: name of semantic similarity metric
        :return: semantic similarity score if both uri can be mapped to synsets, otherwise 0.
        """
        s1 = self.yago2synset(yago1)
        s2 = self.yago2synset(yago2)
        if s1 and s2:
            return self.similarity(s1, s2, name)
        return 0.0

    def word_similarity_wpath_graph(self, w1, w2, k):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        return max([self.wpath_graph(c1, c2, k) for c1 in s1 for c2 in s2] + [0])

    def res_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        yago = self.synset2yago(lcs)
        return self._graph_ic.concept_ic(yago)

    def lin_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        yago_c1 = self.synset2yago(c1)
        yago_c2 = self.synset2yago(c2)
        yago_lcs = self.synset2yago(lcs)
        lcs_ic = self._graph_ic.concept_ic(yago_lcs)
        c1_ic = self._graph_ic.concept_ic(yago_c1)
        c2_ic = self._graph_ic.concept_ic(yago_c2)
        combine = c1_ic + c2_ic
        if c1_ic == 0.0 or c2_ic == 0.0:
            return 0.0
        return 2.0 * lcs_ic / combine

    def jcn_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        yago_c1 = self.synset2yago(c1)
        yago_c2 = self.synset2yago(c2)
        yago_lcs = self.synset2yago(lcs)
        lcs_ic = self._graph_ic.concept_ic(yago_lcs)
        c1_ic = self._graph_ic.concept_ic(yago_c1)
        c2_ic = self._graph_ic.concept_ic(yago_c2)
        lcs_ic = 2.0 * lcs_ic
        if c1_ic == 0.0 or c2_ic == 0.0:
            return 0.0
        return 1.0 / 1+(c1_ic + c2_ic - lcs_ic)

    def wpath_graph(self, c1, c2, k=0.9):
        lcs = self.least_common_subsumer(c1, c2)
        path = c1.shortest_path_distance(c2)
        yago_lcs = self.synset2yago(lcs)
        weight = k ** self._graph_ic.concept_ic(yago_lcs)
        return 1.0 / (1 + path*weight)


class EntitySimilarity:

    """This class implements entity relatedness using DBpedia links and entity concepts"""

    def __init__(self):
        self._features = EntityFeatures()
        self._stats = StatSPARQL()
        self._yago = YagoTypeSimilarity()

    def similarity(self, entity1, entity2):
        concepts_1 = self._features.type(entity1)
        concepts_1 = [c for c in concepts_1 if c.__contains__('class/yago')]
        concepts_2 = self._features.type(entity2)
        concepts_2 = [c for c in concepts_2 if c.__contains__('class/yago')]
        synsets_1 = [self._yago.yago2synset(c) for c in concepts_1 if self._yago.yago2synset(c)]
        synsets_2 = [self._yago.yago2synset(c) for c in concepts_2 if self._yago.yago2synset(c)]
        if not synsets_1 or not synsets_2:
            return 0.0
        s1,_ = zip(*Counter({s:self._yago.synset_ic(s) for s in synsets_1}).most_common(5))
        s2,_ = zip(*Counter({s:self._yago.synset_ic(s) for s in synsets_2}).most_common(5))
        N1 = len(s1)
        N2 = len(s2)
        score1 = sum([max([self._yago.similarity(syn1, syn2) for syn2 in s2]) for syn1 in s1]) / N1
        score2 = sum([max([self._yago.similarity(syn1, syn2) for syn1 in s1]) for syn2 in s2]) / N2
        return (score1 + score2) / 2.0

    def relatedness(self, entity1, entity2):
        ab = self._stats.entity_share(entity1, entity2)
        if ab == 0:
            return 0
        a = self._stats.entity_relation(entity1)
        b = self._stats.entity_relation(entity2)
        x = math.log(max([a,b])) - math.log(ab)
        y = math.log(self._stats.entity_N()) - math.log(min([a,b]))
        return x / y

