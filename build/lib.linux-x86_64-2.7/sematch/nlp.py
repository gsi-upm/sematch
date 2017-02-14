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

from sematch.utility import FileIO

from nltk.stem import WordNetLemmatizer
import nltk

from collections import Counter
import itertools
import string
import re

stopwords = set(nltk.corpus.stopwords.words('english'))
wn_lemma = WordNetLemmatizer()
reg_tokenizer = nltk.RegexpTokenizer(r'\w+')
word_pattern = re.compile('[a-zA-Z]+')

def word_tokenize(text):
    tokens = reg_tokenizer.tokenize(text)
    return list(filter(lambda token: word_pattern.match(token) and len(token) >= 1, tokens))

def sent_tokenize(text):
    return re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s').split(text)

def word_process(words):
    words = [w.lower() for w in words]
    words = [w for w in words if w not in stopwords]
    words = [wn_lemma.lemmatize(w) for w in words]
    words = [wn_lemma.lemmatize(w, pos='v') for w in words]
    return words

chunk_grammar_phrases = """CHUNK: {<NNP><NNP><NNP><NNP>}
    {<NNP|NNPS><NNP|NNPS><NNP|NNPS>}
    {<NNP|NNPS><NNP|NNPS>}
    {<NNP|NNPS>+}"""

class Extraction:

    """This class is used to extract nouns, proper nouns, phrases from text, including descriptions and
    url links"""

    def __init__(self, w_tokenize=None, s_tokenize=None,
                 pos_tag=None, stop_words=None, punct=None,
                 grammar=chunk_grammar_phrases):
        self._word_tokenize = w_tokenize if w_tokenize else word_tokenize
        self._sent_tokenize = s_tokenize if s_tokenize else sent_tokenize
        self._tagger = pos_tag if pos_tag else nltk.pos_tag
        self._stop_words = stop_words if stop_words else stopwords
        self._punct = punct if punct else set(string.punctuation)
        self._chunk_grammar = grammar
        self._chunker = nltk.RegexpParser(self._chunk_grammar)

    def extract_chunks_sent(self, sent):
        """
         Extract chunk phrases from a sentence.
        :param sent: a sentence level text.
        :return: chunk phrases
        """
        tags = self._tagger(self._word_tokenize(sent))
        chunks = nltk.chunk.tree2conlltags(self._chunker.parse(tags))
        # join constituent chunk words into a single chunked phrase
        return [' '.join(word for word, pos, chunk in group)
                  for key, group in itertools.groupby(chunks, lambda (word, pos, chunk): chunk != 'O') if key]

    def extract_chunks_doc(self, text):
        """
        Extract chunk phrases from a document.
        :param text: a document level text
        :return: chunk phrases
        """
        sents = self._sent_tokenize(text)
        sents = [s for s in sents if s]
        return list(itertools.chain.from_iterable(map(self.extract_chunks_sent, sents)))

    def extract_words(self, text, good_tags=set(['NN','NNS','NNP','VBP', 'VBZ','VBG','VBN'])):
        pos_tags = self._tagger(self._word_tokenize(text))
        words = [word for word, tag in pos_tags if tag in good_tags
                 and not all(char in self._punct for char in word)]
        return word_process(words)

    def extract_nouns(self, text):
        return self.extract_words(text, set(['NN', 'NNS', 'NNP']))

    def extract_verbs(self, text):
        return self.extract_words(text, set(['VBP', 'VBZ','VBG','VBN']))

    def category_features(self, categories):
        return map(lambda x:x.replace('http://dbpedia.org/resource/Category:', ''), categories)

    def category2words(self, categories):
        words = []
        for cat in categories:
            cat_str = ' '.join(cat.split('_'))
            words.extend(self.extract_nouns(cat_str))
        return list(set(words))


class RAKE:

    """
    Implementation of RAKE -- Rapid Automatic Keywords Extraction From Individual Documents
    https://github.com/aneesha/RAKE/blob/master/rake.py

    To make a class for rake python implementation for easy incorporation in other modules.
    This class is used to extract keywords from textual document, such as description of entity from DBpedia.
    """

    def __init__(self, stopwords_file='models/FoxStoplist.txt', word_tokenize=None, sent_tokenize=None):
        self._stopwords_pattern = self.build_patterns(self.load_stopwords(stopwords_file))
        self._sent_tokenize = sent_tokenize if sent_tokenize else nltk.sent_tokenize
        self._word_tokenize = word_tokenize if word_tokenize else nltk.word_tokenize

    def load_stopwords(self, filename):
        data = FileIO.read_list_file(FileIO.filename(filename))
        data = [d.split() for d in data[1:]] # skip first line, in case more than one word per line
        data = list(itertools.chain.from_iterable(data))
        return data

    def build_patterns(self, stopwords):
        pattern = lambda x: r'\b' + x + r'(?![\w-])'  # added look ahead for hyphen
        stopword_patterns = map(pattern, stopwords)
        return re.compile('|'.join(stopword_patterns), re.IGNORECASE)

    def candidate_phrases(self, text):
        candidates = []
        for s in self._sent_tokenize(text):
            phrases = re.sub(self._stopwords_pattern, '|', s.strip()).split('|')
            for p in phrases:
                p = p.strip().lower()
                candidates.append(p) if p else None
        return candidates

    def ranking_phrases(self, phrases):
        word_frequency = {}
        word_degree = {}
        for p in phrases:
            words = self._word_tokenize(p)
            degree = len(words) - 1
            for w in words:
                word_frequency.setdefault(w, 0)
                word_frequency[w] += 1
                word_degree.setdefault(w, 0)
                word_degree[w] += degree

        for word in word_frequency:
            word_degree[word] += word_frequency[word]

        word_scorer = lambda x: word_degree[x] / 1.0 * word_frequency[x]
        word_score = {word:word_scorer(word) for word in word_frequency}

        phrase_scorer = lambda x: sum([word_score[word] for word in self._word_tokenize(x)])
        phrase_score = {p:phrase_scorer(p) for p in phrases}

        return phrase_score

    def extract(self, text, ratio=3):
        phrases = self.ranking_phrases(self.candidate_phrases(text))
        phrases = Counter(phrases).most_common(len(phrases.keys()) / ratio)
        phrases, _ = zip(*phrases)
        return phrases


