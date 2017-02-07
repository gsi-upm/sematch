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

from sematch.semantic.sparql import NameSPARQL, QueryGraph
from sematch.semantic.similarity import YagoTypeSimilarity
from sematch.utility import memoized
from sematch.nlp import word_tokenize, word_process, Extraction

import numpy as np
import itertools
from collections import Counter


class Matcher:

    """This class is used for concept based entity match in DBpedia"""

    def __init__(self, result_limit=5000, expansion=True, show_query=False):
        self._expansion = expansion
        self._show_query = show_query
        self._linker = NameSPARQL()
        self._extracter = Extraction()
        self._yago = YagoTypeSimilarity()
        self._query_graph = QueryGraph(result_limit)

    def type_links(self, word, lang='eng'):
        synsets = self._yago.multilingual2synset(word, lang=lang)
        if self._expansion:
            synsets = list(set(itertools.chain.from_iterable([self._yago.synset_expand(s) for s in synsets])))
        links = []
        for s in synsets:
            link_dic = {}
            link_dic['name'] = s.name()
            link_dic['gloss'] = s._definition
            link_dic['lemma'] = ' '.join(s._lemma_names)
            concept_link = []
            yago_link = self._yago.synset2yago(s)
            dbpedia_link = self._yago.synset2dbpedia(s)
            concept_link.append(yago_link) if yago_link else None
            concept_link.append(dbpedia_link) if dbpedia_link else None
            link_dic['lod'] = concept_link
            if link_dic['lod']:
                links.append(link_dic)
        return links

    def query_process(self, query):
        """
        Process query into concept (common noun) and entity (proper noun). Link them
        to Knowledge Graph uri links respectively.
        :param query: short text query
        :return: tuple of concepts and entities in uris.
        """
        entities = self._extracter.extract_chunks_sent(query)
        entity_filter = list(itertools.chain.from_iterable([e.lower().split() for e in entities]))
        entity_filter = set(entity_filter)
        concepts = list(set(self._extracter.extract_nouns(query)))
        concepts = [c for c in concepts if c not in entity_filter]
        concept_uris = [list(itertools.chain.from_iterable([s['lod'] for s in self.type_links(c)])) for c in concepts]
        concept_uris = list(itertools.chain.from_iterable(concept_uris))
        entity_uris = list(itertools.chain.from_iterable(map(self._linker.name2entities, entities)))
        return list(set(concept_uris)), list(set(entity_uris))

    def match_concepts(self, concepts, lang='en'):
        results = []
        for i in xrange(0, len(concepts), 5):
            results.extend(self._query_graph.type_query(concepts[i:i + 5], lang, self._show_query))
        result_dic = {}
        for res in results:
            if res['uri'] not in result_dic:
                result_dic[res['uri']] = res
        return [result_dic[key] for key in result_dic.keys()]

    def match_type(self, query, lang='eng'):
        lang_map = {'eng':'en','spa':'es', 'cmn':'zh'}
        result_lang = lang_map[lang]
        words = query.split()
        concept_uris = []
        for w in words:
            concepts = list(itertools.chain.from_iterable([s['lod'] for s in self.type_links(w,lang)]))
            concept_uris.extend(concepts)
        concept_uris = list(set(concept_uris))
        return self.match_concepts(concept_uris, result_lang)

    def match_entity_type(self, query):
        results = []
        concepts, entities = self.query_process(query)
        print concepts, entities
        for e in entities:
            for i in xrange(0, len(concepts), 5):
                results.extend(self._query_graph.type_entity_query(concepts[i:i + 5], e, self._show_query))
        result_dic = {}
        for res in results:
            if res['uri'] not in result_dic:
                result_dic[res['uri']] = res
        result = [result_dic[key] for key in result_dic.keys()]
        return result


class SimClassifier:
    """
    This class implements similarity based category classifiers.
    """

    def __init__(self, labels, cat_features, feature_weights, sim_metric, sim_model='weighted'):
        """
         Class initialization.
        :param labels: predefined categories
        :param cat_features: features to represent each category
        :param sim_metric: word similarity function
        """
        self._categories = labels
        self._cat_features = cat_features
        self._feature_weights = feature_weights
        self._sim_metric = sim_metric
        self._sim_model = self.pick_sim_model(sim_model)

    def pick_sim_model(self, sim_model):
        weighted = lambda x, y: self.weighted_similarity(x, y)
        max_sim = lambda x, y: self.max_similarity(x, y)
        average = lambda x, y: self.average_similarity(x, y)
        model_dic = {'weighted':weighted, 'max':max_sim, 'average':average}
        return model_dic[sim_model]

    @classmethod
    def train(cls, corpus, sim_metric, feature_num=5, sim_model='weighted'):
        '''
        Extract categories, features, feature weights, from corpus.
        Compute the weight for each feature token in each category
        The weight is computed as token_count / total_feature_count
        '''
        print "Training..."
        cat_word = {}
        for sent, cat in corpus:
            cat_word.setdefault(cat, []).extend(word_process(word_tokenize(sent)))
        features = {cat: Counter(cat_word[cat]) for cat in cat_word}
        labels = features.keys()
        cat_features = {}
        feature_weights = {}
        for c, f in features.iteritems():
            w_c_pairs = f.most_common(feature_num)
            words, counts = zip(*w_c_pairs)
            cat_features[c] = words
            total_count = float(sum(counts))
            word_weights = []
            for w, count in w_c_pairs:
                word_weights.append((w, count / total_count))
            feature_weights[c] = word_weights
        return cls(labels, cat_features, feature_weights, sim_metric, sim_model)

    def weighted_similarity(self, word, category):
        """
        Input word is compared to each feature word using semantic similarity. The whole similarity
        score is computed as weighted sum.
        :param word: feature word
        :param category: a predefined category
        :return: weighted word similarity score between word and category
        """
        features, weights = zip(*self._feature_weights[category])
        scores = map(lambda x: self._sim_metric(word, x), features)
        return np.dot(np.array(scores), np.array(weights).transpose())

    def max_similarity(self, word, category):
        """
        Compute similarity between word and category, where
        category is represented by several feature words
        :param word: feature word
        :param category: a predefined category
        :return: max word similarity score between word and category
        """
        return max(map(lambda x: self._sim_metric(word, x), self._cat_features[category]) + [0.0])

    def average_similarity(self, word, category):
        """
        Compute similarity between word and category, where
        category is represented by several feature words
        :param word: feature word
        :param category: a predefined category
        :return: average word similarity score between word and category
        """
        sum_score = sum(map(lambda x: self._sim_metric(word, x), self._cat_features[category]) + [0.0])
        N = len(self._cat_features[category])
        return sum_score / N

    @memoized
    def category_similarity(self, word, category):
        """
        Compute the semantic similarity between a word and a category.
        :param word: a feature word
        :param category: predefined category
        :param method: the name of semantic similarity metric
        :return: similarity score between word and category
        """
        return self._sim_model(word, category)

    def classify_single(self, sent, feature_model='max'):
        """
        The input feature words are compared to each category based on category similarity.
        Sum the semantic similarity score between features and category.
        The category having highest similarity score is the correct category.

        :param featuresets: feature sets such as word list
        :param method: specify the semantic similarity metric
        :param model: similarity combination model 'max', 'sum'. Default is 'max'
        :return: the correct category label.
        """
        feature_words = list(set(word_process(word_tokenize(sent))))
        score = {}
        for c in self._categories:
            if feature_model == 'max':
                score[c] = max([self.category_similarity(w, c) for w in feature_words] + [0.0])
            else:
                score[c] = sum([self.category_similarity(w, c) for w in feature_words] + [0.0])
        return Counter(score).most_common(1)[0][0]

    def classify(self, X, feature_model='max'):
        return [self.classify_single(x, feature_model) for x in X]



from sklearn.svm import LinearSVC
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer

import time

def timeit(func):

    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        delta  = time.time() - start
        return result, delta
    return wrapper


class TextPreprocessor(BaseEstimator, TransformerMixin):
    """
    Transform input text into feature representation
    """
    def __init__(self, corpus, word_sim_metric, feature_num=10, model='sim'):
        """
        :param corpus: use a corpus to train a vector representation
        :param feature_num: number of dimensions
        :param model: onehot or sim
        """
        self._model = model
        self._word_sim = word_sim_metric
        self._features = self.extract_features(corpus, feature_num)

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return X

    def extract_features(self, corpus, feature_num=10):
        cat_word = {}
        for sent, cat in corpus:
            cat_word.setdefault(cat, []).extend(word_process(word_tokenize(sent)))
        features = {cat: Counter(cat_word[cat]) for cat in cat_word}
        feature_words = []
        for c, f in features.iteritems():
            words, counts = zip(*f.most_common(feature_num))
            feature_words.extend(list(words))
        feature_words = set(feature_words)
        return feature_words

    def similarity(self, tokens, feature):
        sim = lambda x: self._word_sim(feature, x)
        return max(map(sim, tokens) + [0.0])

    def unigram_features(self, tokens):
        words = set(tokens)
        features = {}
        for f in self._features:
            features['contains({})'.format(f)] = (f in words)
        return features

    def sim_features(self, tokens):
        words = set(tokens)
        features = {}
        for f in self._features:
            features['sim({})'.format(f)] = self.similarity(words, f)
        return features

    def transform(self, X):
        tokenize = lambda x: word_process(word_tokenize(x))
        X_tokens = map(tokenize, X)
        if self._model == 'onehot':
            return map(self.unigram_features, X_tokens)
        else:
            return map(self.sim_features, X_tokens)


class SimSVMClassifier:

    def __init__(self, labels, model):
        self._labels = labels
        self._model = model

    @classmethod
    def train(cls, X, y, word_sim_metric, classifier=LinearSVC,
              feature_num=10, feature_type='sim', verbose=True):

        if isinstance(classifier, type):
            classifier = classifier()

        labels = LabelEncoder()
        y_train = labels.fit_transform(y)

        @timeit
        def build():

            corpus = zip(X, y)
            model = Pipeline([
                ('preprocessor', TextPreprocessor(corpus, word_sim_metric, feature_num, feature_type)),
                ('vectorizer', DictVectorizer()),
                ('classifier', classifier),
            ])

            model.fit(X, y_train)
            return model

        if verbose: print("Building the model")
        model, secs = build()
        if verbose: print("Complete model building in {:0.3f} seconds".format(secs))

        return cls(labels, model)

    def classify(self, X):
        predicted = self._model.predict(X)
        return list(self._labels.inverse_transform(predicted))
