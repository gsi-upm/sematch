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

from numpy import array
from gensim import matutils


class WordRelatedness:
    def __init__(self, model):
        self._model = model
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
        return matutils.cossim(matutils.any2sparse(v1), matutils.any2sparse(v2))


class ConceptRelatedness(WordRelatedness):
    """This class is used for concept embedding (knowledge graph types (ontology classes, wiki categories)"""

    def __init__(self, model):
        WordRelatedness.__init__(self, model)
        self._concepts = set([c for c in self._model.docvecs.doctags])
        self._words = set([w for w in self._model.vocab])

    def check_concept(self, concept):
        """
         Check if a concept is contained in the embedding model
        :param doc: a concept
        :return:
        """
        return True if concept in self._concepts else False

    def check_concepts(self, concepts):
        return [c for c in concepts if self.check_concept(c)]

    def similar_concepts(self, concept, topn=20):
        """
        return most similar concept
        :param concept:
        :return:
        """
        return self._model.docvecs.most_similar(concept, topn=topn) if self.check_concept(concept) else []

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

    def word_concept_similarity(self, word, concept):
        v_word = self.word_vector(word)
        v_concept = self.concept_vector(concept)
        return self.consine_similarity(v_word, v_concept) if v_word is not None and v_concept is not None else 0.0

    def words_concepts_similarity(self, words, concepts):
        v_words = self.words_vector(words)
        v_concepts = self.concepts_vector(concepts)
        return self.consine_similarity(v_words, v_concepts) if v_words is not None and v_concepts is not None else 0.0


class TextRelatedness:
    """This class contains TF-IDF model and LSA model of text-text similarity."""

    def __init__(self, DICT='models/abstract/abstracts.dict',
                 TFIDF_MODEL='models/abstract/abstracts_tfidf.model',
                 LSA_MODEL='models/abstract/abstracts_lsi.model'):
        try:
            from nltk.tokenize import RegexpTokenizer
            from nltk.stem import WordNetLemmatizer
            import nltk
            self._tokenizer = RegexpTokenizer(r'[a-z]+')
            self._lemma = WordNetLemmatizer()
            self._stopwords = set(nltk.corpus.stopwords.words('english'))
        except:
            print('Install NLTK and download WordNet!')
            import sys
            sys.exit()
        try:
            from gensim import corpora, models
            from sematch.utility import FileIO
            self._dict = corpora.Dictionary.load(FileIO.filename(DICT))
            self._tfidf = models.TfidfModel.load(FileIO.filename(TFIDF_MODEL))
            self._lsa = models.LsiModel.load(FileIO.filename(LSA_MODEL))
        except Exception as ex:
            print('Error loading gensim: ', ex)
            print('Install gensim and prepare models data!')
            import sys
            sys.exit()

    def word_tokenize(self, text):
        tokens = self._tokenizer.tokenize(text.lower())
        tokens = [t for t in tokens if len(t) > 2]
        tokens = [w.lower() for w in tokens]
        tokens = [w for w in tokens if w not in self._stopwords]
        return tokens

    def lemmatization(self, tokens):
        tokens = [self._lemma.lemmatize(w) for w in tokens]
        tokens = [self._lemma.lemmatize(w, pos='v') for w in tokens]
        return tokens

    def text_process(self, text):
        return self.lemmatization(self.word_tokenize(text))

    def text2tfidf(self, text):
        tokens = self.text_process(text)
        bow = self._dict.doc2bow(tokens)
        return self._tfidf[bow]

    def text2lsa(self, text):
        tfidf = self.text2tfidf(text)
        return self._lsa[tfidf]

    # text similarity
    def text_similarity(self, t1, t2, model='tfidf'):
        if model == 'tfidf':
            t1_vec = matutils.any2sparse(self.text2tfidf(t1))
            t2_vec = matutils.any2sparse(self.text2tfidf(t2))
            return matutils.cossim(t1_vec, t2_vec)
        else:
            t1_vec = matutils.any2sparse(self.text2lsa(t1))
            t2_vec = matutils.any2sparse(self.text2lsa(t2))
            return matutils.cossim(t1_vec, t2_vec)

