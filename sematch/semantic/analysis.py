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

from gensim import corpora, models, similarities, matutils

class TextAnalysis:

    """This implements wrapper for gensim lsa and tfidf analysis of text collection"""

    def __init__(self, text_process, model, dictionary, tfidf, tfidf_index, lsa, lsa_index):
        self._text_process = text_process
        self._model = model
        self._dictionary = dictionary
        self._tfidf = tfidf
        self._tfidf_index = tfidf_index
        self._lsa = lsa
        self._lsa_index = lsa_index

    def text2model(self, text):
        t = self._text_process(text)
        bow = self._dictionary.doc2bow(t)
        tfidf = self._tfidf[bow]
        if self._model == 'tfidf':
            return tfidf
        else:
            return self._lsa[tfidf]

    def text_similarity(self, t1, t2):
        if self._model == 'tfidf':
            t1_vec = matutils.any2sparse(self.text2model(t1))
            t2_vec = matutils.any2sparse(self.text2model(t2))
            return matutils.cossim(t1_vec, t2_vec)
        else:
            t1_vec = matutils.any2sparse(self.text2model(t1))
            t2_vec = matutils.any2sparse(self.text2model(t2))
            return matutils.cossim(t1_vec, t2_vec)

    def search(self, text):
        query = self.text2model(text)
        if self._model == 'tfidf':
            return self._tfidf_index[query]
        else:
            return self._lsa_index[query]

    @classmethod
    def load(cls, text_process, model='tfidf', top_N=100, save_dir='data/'):
        import logging
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        dictionary = corpora.Dictionary.load(save_dir+'dictionary')
        tfidf = models.TfidfModel.load(save_dir+'tfidf.model')
        tfidf_index = similarities.Similarity.load(save_dir+'tfidf_index/tfidf.index')
        tfidf_index.num_best = top_N
        if model == 'lsa':
            lsa = models.LsiModel.load(save_dir+'lsa.model')
            lsa_index = similarities.Similarity.load(save_dir+'lsa_index/lsa.index')
            lsa_index.num_best = top_N
            return cls(text_process, model, dictionary, tfidf, tfidf_index, lsa, lsa_index)
        return cls(text_process, model, dictionary, tfidf, tfidf_index, None, None)

    @classmethod
    def train(cls, texts, text_process, model='lsa', topic_n=100, top_N=100, save_dir='data/'):
        import logging
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        corpus = [text_process(t) for t in texts]
        dictionary = corpora.Dictionary(corpus)
        print(dictionary)
        dictionary.save(save_dir+'dictionary')
        bow = [dictionary.doc2bow(t) for t in corpus]
        corpora.MmCorpus.serialize(save_dir+'bow', bow)
        bow_corpus = corpora.MmCorpus(save_dir+'bow')
        tfidf = models.TfidfModel(bow_corpus, id2word=dictionary)
        corpora.MmCorpus.serialize(save_dir+'tfidf', tfidf[bow_corpus])
        tfidf.save(save_dir+'tfidf.model')
        tfidf_corpus = corpora.MmCorpus(save_dir+'tfidf')
        tfidf_index = similarities.Similarity(save_dir+'tfidf_index/shard', tfidf_corpus, num_features=tfidf_corpus.num_terms)
        tfidf_index.num_best = top_N
        tfidf_index.save(save_dir+'tfidf_index/tfidf.index')
        if model == 'lsa':
            lsa = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=topic_n)
            lsa.save(save_dir+'lsa.model')
            lsa_index = similarities.Similarity(save_dir+'lsa_index/shard', lsa[tfidf_corpus], num_features=topic_n)
            lsa_index.num_best = top_N
            lsa_index.save(save_dir+'lsa_index/lsa.index')
            return cls(text_process, model, dictionary, tfidf, tfidf_index, lsa, lsa_index)
        return cls(text_process, model, dictionary, tfidf, tfidf_index, None, None)


