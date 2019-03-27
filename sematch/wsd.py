# !/usr/bin/python
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


import networkx as nx
from itertools import combinations
import numpy as np


class LexRank:
    def __init__(self, synsets, sim_metric, threshold=0.0):
        self._synsets = synsets
        self._nodes = list(itertools.chain.from_iterable(synsets))
        self._node2id = {n: i for i, n in enumerate(self._nodes)}
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
            M[i, i] = 1.0
        K = len(self._synsets)
        pairs = [(i, j) for i in range(K - 1) for j in range(i + 1, K)]
        for i, j in pairs:
            x = self._synsets[i]
            y = self._synsets[j]
            for s_x in x:
                for s_y in y:
                    score = self._sim_metric(s_x, s_y)
                    n_x = self._node2id[s_x]
                    n_y = self._node2id[s_y]
                    if score > self._threshold:
                        M[n_x, n_y] = score
                    else:
                        M[n_x, n_y] = 0.0
        return M

    def similarity_graph(self, M):
        return nx.from_numpy_matrix(M)

    def page_rank(self):
        rank_scores = nx.pagerank(self._graph)
        return {self._nodes[key]: value for key, value in rank_scores.items()}


from similarity import WordNetSimilarity
from collections import Counter
import itertools


class WordNetSimWSD():

    def __init__(self, metric_name):
        self._wns = WordNetSimilarity()
        self._similarity = lambda x, y: self._wns.similarity(x, y, metric_name)

    def word_sense_similarity(self, word, sense):
        word_senses = self._wns.word2synset(word)
        scorer = lambda x: self._similarity(x, sense)
        sim_scores = list(map(scorer, word_senses)) + [0.0]
        return max(sim_scores)

    def synset_from_context(self, target, context, target_syns=None,
                            context_syns=None):
        senses = self._wns.word2synset(target)
        if len(senses) == 1:
            return senses[0]
        result = {}
        for ss in senses:
            scorer = lambda x: self.word_sense_similarity(x, ss)
            sim_score = sum(list(map(scorer, context)))
            result[ss] = sim_score
        return Counter(result).most_common(1)[0][0]

    def synset_from_graph(self, target, context, target_syns=None,
                          context_syns=None):
        senses = self._wns.word2synset(target)
        if len(senses) == 1:
            return senses[0]
        words = [target] + context
        words = list(set(words))
        words_synsets = [self._wns.word2synset(w) for w in words]
        # construct similarity graphs
        sim_graph = LexRank(words_synsets, self._similarity)
        # get pagerank scores of synsets
        rank_scores = sim_graph.page_rank()
        candidate_scores = {s: rank_scores[s] for s in senses}
        return Counter(candidate_scores).most_common(1)[0][0]


##This is old code for word sense disambiguation based on WordNet semantic similarity metrics.
import itertools
import random


class WSD:
    def __init__(self, wsd_method='maxsim', sim_name='wpath'):
        '''
        wsd_methods = ['random_sense','first','frequent','maxsim', 'graph', 'lesk', 'naive']
        sim_name = ['path', 'lch', 'wup', 'li', 'res', 'lin', 'jcn', 'wpath']
        '''
        self._method = wsd_method
        self._sim_name = sim_name
        self._wn_sim = WordNetSimilarity()

    def disambiguate_graph(self, sentence):
        words_origin = word_tokenize(sentence)
        # extract words that have a synset in WordNet, currently support NOUN.
        words = [w for w in words_origin if self._wn_sim.word2synset(w)]
        # map words to synsets
        words_synsets = {w: self._wn_sim.word2synset(w) for w in words}
        # construct sets list
        synsets = list(itertools.chain.from_iterable([words_synsets[w] for w in words]))
        # remove duplicate synsets
        synsets = list(set(synsets))
        # define semantic similarity metric
        sim_metric = lambda x, y: self._wn_sim.similarity(x, y, self._sim_name)
        # construct similarity graphs
        sim_graph = SimGraph(synsets, sim_metric)
        # get pagerank scores of synsets
        rank_scores = sim_graph.page_rank()
        results = []
        for w in words_origin:
            if w in words:
                candidate_scores = {s: rank_scores[s] for s in words_synsets[w]}
                results.append((w, Counter(candidate_scores).most_common(1)[0][0]))
            else:
                results.append((w, None))
        return results

    def classify(self, featureset):
        context = featureset['context']
        senses = featureset['senses']
        return self.max_senses(context, senses)

    def context2words(self, sent):
        words = word_tokenize(sent.lower())
        words = [w for w in words if len(w) > 2]
        return lemmatization(words)

    def random_sense(self, word):
        senses = self._wn_sim.word2synset(word)
        return random.choice(senses)

    def first_sense(self, word):
        senses = self._wn_sim.word2synset(word)
        return senses[0]

    def word_sense_similarity(self, word, sense):
        word_senses = self._wn_sim.word2synset(word)
        scorer = lambda x: self._wn_sim.similarity(x, sense, self._sim_name)
        sim_scores = map(scorer, word_senses) + [0.0]
        return max(sim_scores)

    def max_senses(self, context, senses):
        if len(senses) == 1:
            return senses[0]
        context_words = self.context2words(context)
        result = {}
        for ss in senses:
            scorer = lambda x: self.word_sense_similarity(x, ss)
            sim_score = sum(map(scorer, context_words))
            result[ss] = sim_score
        return Counter(result).most_common(1)[0][0]

    def max_sim(self, context, word):
        senses = self._wn_sim.word2synset(word)
        return self.max_senses(context, senses)

    def lesk(self, context, word):
        from nltk.wsd import lesk as nltk_lesk
        context_words = self.context2words(context)
        return nltk_lesk(context_words, word, 'n')


from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize

from similarity import WordNetSimilarity

from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim import matutils
from numpy import array, dot

import networkx as nx
import numpy as np

from string import punctuation
from collections import Counter
import itertools
import multiprocessing

import os
import glob
from lxml import etree


class SynsetRank:
    def __init__(self, synsets, sim_metric, threshold=0.0):
        self._synsets = synsets
        self._nodes = list(itertools.chain.from_iterable(synsets))
        self._node2id = {n: i for i, n in enumerate(self._nodes)}
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
            M[i, i] = 1.0
        K = len(self._synsets)
        pairs = [(i, j) for i in range(K - 1) for j in range(i + 1, K)]
        for i, j in pairs:
            x = self._synsets[i]
            y = self._synsets[j]
            for s_x in x:
                for s_y in y:
                    score = self._sim_metric(s_x, s_y)
                    n_x = self._node2id[s_x]
                    n_y = self._node2id[s_y]
                    # M[n_x,n_y] = score
                    if score > self._threshold:
                        M[n_x, n_y] = score
                    else:
                        M[n_x, n_y] = 0.0
        return M

    def similarity_graph(self, M):
        return nx.from_numpy_matrix(M)

    def page_rank(self):
        rank_scores = nx.pagerank(self._graph)
        return {self._nodes[key]: value for key, value in rank_scores.items()}


STOPWORD = stopwords.words('english')
STOPWORD = set(STOPWORD)
wn_lemma = WordNetLemmatizer()

PUNT = set(["'", '`'])


def check_punt(word):
    for c in word:
        if c in PUNT:
            return False
    return True


def word_process(words):
    words = list(filter(lambda t: len(t) > 1, words))
    words = [w.lower() for w in words]
    words = [w for w in words if w not in STOPWORD]
    words = [w for w in words if check_punt(w)]
    words = [wn_lemma.lemmatize(w) for w in words]
    words = [wn_lemma.lemmatize(w, pos='v') for w in words]
    return words


def text_process(text):
    result = []
    for t in text:
        words = word_tokenize(t)
        words = [w.split('_') for w in words]
        words = list(itertools.chain.from_iterable(words))
        words = word_process(words)
        result.extend(words)
    return result


def parse_corpus(path_name='Training_Corpora/SemCor/'):
    """This function parse the training data"""
    keys_path = glob.glob(os.path.join(path_name, '*gold.key.txt'))[0]
    sentences_path = glob.glob(os.path.join(path_name, '*data.xml'))[0]

    keys = dict()
    with open(keys_path, 'r') as f:
        for line in f:
            line = line.strip().split(' ')
            id_ = line[0]
            synset_keys = line[1:]
            synsets = [wn.lemma_from_key(k).synset() for k in synset_keys]
            keys[id_] = synsets

    with open(sentences_path, 'r') as f:
        tree = etree.parse(f)

    training = []

    for sentence in tree.xpath('//sentence'):
        sent_id = sentence.attrib['id']
        tags = []
        words = []
        for chunck in sentence[:]:
            type_ = chunck.tag
            if type_ == 'instance':
                tags.append(keys[chunck.attrib['id']])
            if chunck.attrib['pos'] != '.' and chunck.attrib['lemma'] not in STOPWORD:
                words.append(chunck.attrib['lemma'])
        training.append((words, list(set(itertools.chain.from_iterable(tags)))))
    return training


class SynsetProfile(object):
    def __init__(self, corpus=None, expand=True):
        self._corpus = corpus
        self._expand = expand

    def synset_expansion(self, synset):
        super_concepts = list(set(itertools.chain.from_iterable(synset.hypernym_paths())))
        related = list(set(itertools.chain.from_iterable([synset.part_meronyms(), synset.part_holonyms()])))
        return [s.name() for s in list(set(itertools.chain.from_iterable([super_concepts, related, [synset]])))]

    def descriptions(self, synset):
        text = text_process([synset._definition])
        example = text_process(synset._examples)
        names = text_process(synset._lemma_names)
        return list(itertools.chain.from_iterable([text, example, names]))

    def __iter__(self):
        for synset in wn.all_synsets():
            if self._expand:
                synsets = [self.synset_expansion(s) for s in synsets]
                synsets = list(set(itertools.chain.from_iterable(synsets)))
                yield TaggedDocument(words=self.descriptions(synset), tags=synsets)
            else:
                yield TaggedDocument(words=self.descriptions(synset), tags=[synset.name()])
        if self._corpus:
            for words, synsets in self._corpus:
                if self._expand:
                    synsets = [self.synset_expansion(s) for s in synsets]
                    synsets = list(set(itertools.chain.from_iterable(synsets)))
                yield TaggedDocument(words=words, tags=synsets)


class Synset2Vec:
    def __init__(self, model):
        self._model = model
        self._concepts = set([c for c in self._model.docvecs.doctags])
        self._words = set([w for w in self._model.vocab])

    def check_word(self, word):
        return True if word in self._words else False

    def check_words(self, words):
        return [w for w in words if self.check_word(w)]

    def similar_words(self, word):
        return self._model.most_similar(word) if self.check_word(word) else []

    def word_similarity(self, w1, w2):
        return self._model.similarity(w1, w2) if self.check_word(w1) and self.check_word(w2) else 0.0

    def words_similarity(self, words1, words2):
        w1 = self.check_words(words1)
        w2 = self.check_words(words2)
        return self._model.n_similarity(w1, w2) if w1 and w2 else 0.0

    def word_vector(self, w):
        return matutils.unitvec(self._model[w]) if self.check_word(w) else None

    def words_vector(self, words):
        v_words = [self._model[w] for w in self.check_words(words)]
        return matutils.unitvec(array(v_words).mean(axis=0)) if v_words else None

    def consine_similarity(self, v1, v2):
        return dot(v1, v2)

    def check_concept(self, concept):
        """
         Check if a concept is contained in the embedding model
        :param doc: a concept
        :return:
        """
        return True if concept in self._concepts else False

    def check_concepts(self, concepts):
        return [c for c in concepts if self.check_concept(c)]

    def similar_concepts(self, concept):
        return self._model.docvecs.most_similar(concept) if self.check_concept(concept) else []

    def similar_words(self, word):
        return self._model.most_similar(word) if self.check_word(word) else []

    def concept_similarity(self, c1, c2):
        return self._model.docvecs.similarity(c1, c2) if self.check_concept(c1) and self.check_concept(c2) else 0.0

    def concepts_similarity(self, concepts1, concepts2):
        c1 = self.check_concepts(concepts1)
        c2 = self.check_concepts(concepts2)
        return self._model.docvecs.n_similarity(c1, c2) if c1 and c2 else 0.0

    # return vector of a concept
    def concept_vector(self, c):
        return matutils.unitvec(self._model.docvecs[c]) if self.check_concept(c) else None

    # return mean vector of a set of concepts
    def concepts_vector(self, concepts):
        v_concepts = [self._model.docvecs[c] for c in self.check_concepts(concepts)]
        return matutils.unitvec(array(v_concepts).mean(axis=0)) if v_concepts else None

    def concept_word_similarity(self, concept, word):
        v_word = self.word_vector(word)
        v_concept = self.concept_vector(concept)
        return self.consine_similarity(v_word, v_concept) if v_word is not None and v_concept is not None else 0.0

    def concept_text_similarity(self, concept, text):
        v_words = self.words_vector(text)
        v_concept = self.concept_vector(concept)
        return self.consine_similarity(v_concept, v_words) if v_words is not None and v_concept is not None else 0.0

    @classmethod
    def load(cls, model_file='synset2vec'):
        model = Doc2Vec.load(model_file)
        return cls(model)

    @classmethod
    def train(cls, corpus, dimention=100, min_count=5, window_size=10, model_file='synset2vec'):
        cores = multiprocessing.cpu_count()
        model = Doc2Vec(corpus, size=dimention, min_count=min_count, window=window_size, workers=cores)
        # model.save(model_file)
        return cls(model)


wn_pos_map = {'ADJ': wn.ADJ,
              'ADV': wn.ADV,
              'N': wn.NOUN,
              'NE': wn.NOUN,
              'NN': wn.NOUN,
              'NNS': wn.NOUN,
              'NOUN': wn.NOUN,
              'NP': wn.NOUN,
              'NPS': wn.NOUN,
              'VERB': wn.VERB,
              'a': wn.ADJ,
              'n': wn.NOUN,
              'r': wn.ADV,
              'v': wn.VERB}


class SenseDisambiguation():
    def __init__(self, model, wsd='word', wns_metric='jcn', th=0.5):
        self._wns = WordNetSimilarity()
        self._wns_metric = wns_metric
        self._model = model
        self._wsd = wsd
        self._th = th

    def topN_words(self, word_scores, top_N=5):
        tops = Counter(word_scores).most_common(top_N)
        if tops:
            w, score = zip(*tops)
            score = [s for s in score if s > 0.2]
            if score:
                N = len(score)
                return sum(score) / N
            else:
                return 0.0
        else:
            return 0.0

    def wn_word_sense_similarity(self, word, sense):
        word_senses = wn.synsets(word, pos=wn.NOUN)
        scorer = lambda x: self._wns.similarity(x, sense, self._wns_metric)
        sim_scores = list(map(scorer, word_senses)) + [0.0]
        return max(sim_scores)

    def word_sense_similarity(self, word, sense):
        word_senses = wn.synsets(word)
        word_senses = [s.name() for s in word_senses]
        scorer = lambda x: self._model.concept_similarity(x, sense.name())
        sim_scores = list(map(scorer, word_senses)) + [0.0]
        return max(sim_scores)

    def word_similarity(self, targets, context, model='WordEmbed'):
        result = {}
        for t in targets:
            word_sim = {}
            for w in context:
                if model == 'WordEmbed':
                    word_sim[w] = self._model.concept_word_similarity(t.name(), w)
                elif model == 'SenseEmbed':
                    word_sim[w] = self.word_sense_similarity(w, t)
                elif model == 'WordNet':
                    word_sim[w] = self.wn_word_sense_similarity(w, t)
            result[t] = self.topN_words(word_sim)
        t, score = Counter(result).most_common(1)[0]
        if score > self._th:
            return [t]
        else:
            return [targets[0]]

    def text_similarity(self, targets, context):
        result = {}
        for t in targets:
            words = [w for w in context if self._model.concept_word_similarity(t.name(), w) > 0.2]
            result[t] = self._model.concept_text_similarity(t.name(), words)
        c, score = Counter(result).most_common(1)[0]
        # print(c, score)
        if score > self._th:
            # print(c,score)
            return [c]
        else:
            return [targets[0]]

    def synset_candidates(self, target, synsets):
        candidates = [s for s in synsets if target in s.name()]
        if not candidates:
            return synsets
        else:
            return candidates

    def synset_from_context(self, target, target_pos, context, target_syns=None,
                            context_syns=None):
        candidates = wn.synsets(target, wn_pos_map[target_pos])
        if len(candidates) == 1:
            return [candidates[0]]
        candidates = self.synset_candidates(target, candidates)
        words = [w for w, pos in context if pos not in set(['.', 'NUM', 'DET'])]
        words = word_process(words)
        if self._wsd == 'sense':
            return self.word_similarity(candidates, words, 'SenseEmbed')
        elif self._wsd == 'word':
            return self.word_similarity(candidates, words, 'WordEmbed')
        elif self._wsd == 'wordnet':
            if wn_pos_map[target_pos] != wn.NOUN:
                return [candidates[0]]
            return self.word_similarity(candidates, words, 'WordNet')
        elif self._wsd == 'text':
            return self.text_similarity(candidates, words)

    def synset_from_graph(self, target, target_pos, context, target_syns=None,
                          context_syns=None):
        candidates = wn.synsets(target, wn_pos_map[target_pos])
        if len(candidates) == 1:
            return [candidates[0]]
        candidates = self.synset_candidates(target, candidates)
        if self._wsd == 'wordnet':
            if wn_pos_map[target_pos] != wn.NOUN:
                return [candidates[0]]
            words = [(w, pos) for w, pos in context if pos in set(['N', 'NN', 'NNS', 'NOUN'])]
            words = [(w, pos) for w, pos in words if w not in STOPWORD]
            words = [(w, pos) for w, pos in words if wn.synsets(w, wn.NOUN)]
            words_synsets = [[s for s in wn.synsets(w, wn.NOUN)] for w, pos in words]
            words_synsets.append(candidates)
            metric = lambda x, y: self._wns.similarity(x, y, self._wns_metric)
            sim_graph = SynsetRank(words_synsets, metric)
            # get pagerank scores of synsets
            rank_scores = sim_graph.page_rank()
            candidate_scores = {c: rank_scores[c] for c in candidates if c in rank_scores}
        else:
            words = [(w, pos) for w, pos in context if pos in set(['N', 'NN', 'NNS', 'NOUN', 'VERB'])]
            words = [(w, pos) for w, pos in words if w not in STOPWORD]
            words = [(w, pos) for w, pos in words if wn.synsets(w, wn_pos_map[pos])]
            words_synsets = [[s.name() for s in wn.synsets(w, wn_pos_map[pos])] for w, pos in words]
            words_synsets.append([s.name() for s in candidates])
            # construct similarity graphs
            sim_graph = SynsetRank(words_synsets, self._model.concept_similarity)
            # get pagerank scores of synsets
            rank_scores = sim_graph.page_rank()
            candidate_scores = {c: rank_scores[c.name()] for c in candidates if c.name() in rank_scores}
        if candidate_scores:
            c, score = Counter(candidate_scores).most_common(1)[0]
            if score > 0.0:
                return [c]
            else:
                return [candidates[0]]
        else:
            return [candidates[0]]
