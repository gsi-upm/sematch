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
from nltk.corpus import wordnet as wn
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
    tokens = reg_tokenizer.tokenize(text.encode('utf-8').translate(None, string.punctuation))
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

class SpaCyNLP:

    """This class provides a wrapper of SpaCy of tokenizer, pos tagger and named entity recognizer"""

    def __init__(self):
        try:
            import spacy #default english
            from numpy import dot
            from numpy.linalg import norm
            self._nlp = spacy.load('en')
            self._vocab = list(set([w.orth_ for w in self._nlp.vocab if w.orth_.islower()]))
            self._cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))
        except:
            print('Install SpaCy. https://spacy.io/docs/usage/')
            import sys
            sys.exit()

    def sent_tokenize(self, doc):
        parsedData = self._nlp(doc)
        sent2str = lambda x : ''.join(parsedData[i].string for i in range(x.start, x.end)).strip()
        return map(sent2str, parsedData.sents)

    def word_tokenize(self, text):
        return [token.orth_ for _, token in enumerate(self._nlp(text))]

    def pos_tag(self, text):
        parsedData = self._nlp(text)
        return [(token.orth_, token.pos_) for _, token in enumerate(parsedData)]

    def ner(self, text):
        parsedData = self._nlp(text)
        ents = list(parsedData.ents)
        return [(' '.join(t.orth_ for t in entity),entity.label_) for entity in ents]

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


class TFIDF:

    def __init__(self, docs,
                 LEMMA=True,
                 TOKENIZER=None):
        self._tokenize = TOKENIZER if TOKENIZER else word_tokenize
        self._process = lambda x: word_process(self._tokenize(x)) if LEMMA else self._tokenize
        from sklearn.feature_extraction.text import TfidfVectorizer
        self._vectorizer = TfidfVectorizer(tokenizer=self._process)
        self._vectorizer.fit_transform(docs)
        self._idf_dict = dict(zip(self._vectorizer.get_feature_names(), self._vectorizer.idf_))

    def idf(self, word):
        return self._idf_dict[word] if word in self._idf_dict else None

    def tfidf(self, doc):
        doc_rep = self._vectorizer.transform([doc])
        features = self._vectorizer.get_feature_names()
        return [(features[index], doc_rep[0, index]) for index in doc_rep.nonzero()[1]]

class NameDict:

    def __init__(self, name_dict):
        self._name_dict = name_dict

    def match(self, name):
        name_lower = name.lower()
        if name_lower in self._name_dict:
            return self._name_dict[name_lower]
        else:
            return []

    @classmethod
    def load(cls, name_dict_file='models/name.dict'):
        from sematch.utility import FileIO
        name = FileIO.read_json_file(name_dict_file)
        name = {n['name']: n['concepts'] for n in name}
        return cls(name)


class EntityFeature:

    def __init__(self, feature_dict):
        self._feature_dict = feature_dict

    def description(self, entity):
        if entity in self._feature_dict:
            return self._feature_dict[entity][0]
        else:
            return None

    def category(self, entity):
        if entity in self._feature_dict:
            return self._feature_dict[entity][1]
        else:
            return []

    @classmethod
    def candidate_features(cls, candidates, export_file='models/candidate_features.json',
                           feature_dict_file='models/entity_features.json'):
        from sematch.utility import FileIO
        entity_features = FileIO.read_json_file(feature_dict_file)
        entity_features = {e['dbr']: (e['desc'], e['cat']) for e in entity_features}
        features = []
        for i, can in enumerate(candidates):
            print i, " ", can
            data = {}
            data['dbr'] = can
            data['desc'] = entity_features[can][0] if can in entity_features else None
            data['cat'] = entity_features[can][1] if can in entity_features else []
            features.append(data)
        FileIO.save_json_file(export_file, features)
        return features


    @classmethod
    def load(cls, feature_dict_file='models/entity_features.json'):
        from sematch.utility import FileIO
        entity_features = FileIO.read_json_file(feature_dict_file)
        entity_features = {e['dbr']: (e['desc'], e['cat']) for e in entity_features}
        return cls(entity_features)


class FeatureExtractor:

    def __init__(self, features, pos=None):
        import nltk
        self._features = features
        self._pos = pos if pos else nltk.pos_tag
        self._lemma = nltk.stem.WordNetLemmatizer().lemmatize
        self._stop_words = set(nltk.corpus.stopwords.words('english'))

    def extract_words(self, pos_tags, good_tags=set(['NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV'])):
        return [(word, tag) for word, tag in pos_tags
                if tag in good_tags and word.lower() not in self._stop_words]

    def filter_character(self, w):
        for c in ['@', '.', '|', '/', ':', '#']:
            if c in w:
                return True
        return False

    def extract_nouns(self, pos_tags):
        nouns = self.extract_words(pos_tags, set(['NOUN']))

        def words_process():
            words, tag = zip(*nouns)
            words = map(lambda x: x.lower(), words)
            words = [w for w in words if not self.filter_character(w)]
            words = map(self._lemma, words)
            words = [w for w in words if len(w) > 2]
            words = [w for w in words if wn.synsets(w, pos=wn.NOUN)]
            return list(set(words))

        return words_process() if nouns else []

    def extract_verbs(self, pos_tags):
        verbs = self.extract_words(pos_tags, set(['VERB']))

        def words_process():
            words, tag = zip(*verbs)
            words = map(lambda x: x.lower(), words)

            words = [self._lemma(w, pos='v') for w in words]
            return list(set(words))

        return words_process() if verbs else []

    def context_features(self, text):
        pos_tags = self._pos(text)
        word_nouns = self.extract_nouns(pos_tags)
        return word_nouns

    def entity_categories(self, candidates):
        candidate_features = {}
        for candidate in candidates:
            f = self._features.category(candidate)
            f = ['http://dbpedia.org/resource/Category:%s' % c for c in f.split()]
            if f:
                candidate_features[candidate] = f
        return candidate_features

    def entity_descriptions(self, candidates):
        candidate_features = {}
        for candidate in candidates:
            f = self._features.description(candidate)
            if f:
                candidate_features[candidate] = f
        return candidate_features

    def entity_word_features(self, candidates):
        candidate_features = {}
        for candidate in candidates:
            f = self._features.category(candidate)
            f_words = self.category_features(f)
            if f_words:
                candidate_features[candidate] = f_words
        return candidate_features

    def category_features(self, categories):
        cats = ' '.join(categories.split('_'))
        return self.extract_nouns(self._pos(cats))


#
# class AhoCorasickNameDict:
#     """This class is used to match strings using aho corasick algorithm and Trie"""
#
#     def __init__(self, automaton, id2concepts):
#         self._automaton = automaton
#         self._id2concepts = id2concepts
#
#     def exact_match(self, text):
#         try:
#             t = text.encode('utf-8')
#         except:
#             print text
#         if t in self._automaton:
#             key, name = self._automaton.get(t)
#             return name, self._id2concepts[key]
#         else:
#             return None
#
#     def match(self, text):
#         return [(name, self._id2concepts[key]) for end_index, (key, name)
#                 in self._automaton.iter(text.encode('utf-8'))]
#
#     def longest_match(self, text):
#         concepts = {name: concepts for name, concepts in self.match(text)}
#         len_dict = {}
#         for name in concepts.keys():
#             len_dict.setdefault(len(name), []).append(name)
#         names = len_dict[max(len_dict.keys())]
#         return [(name, concepts[name]) for name in names]
#
#     @classmethod
#     def build(cls, name_concepts, automaton_file, id2concepts_file):
#         import cPickle as pickle
#         name_dict = AhoCorasickNameDict.build_memory(name_concepts)
#         # save automaton
#         with open(FileIO.filename(automaton_file), 'wb') as f:
#             pickle.dump(name_dict._automaton, f)
#         # save id2concepts
#         with open(FileIO.filename(id2concepts_file), 'wb') as f:
#             pickle.dump(name_dict._id2concepts, f)
#         return name_dict
#
#     @classmethod
#     def build_memory(cls, name_concepts):
#         from ahocorasick import Automaton
#         auto = Automaton()
#         names = name_concepts.keys()
#         id2concepts = {}
#         for i, name in enumerate(names):
#             id2concepts[i] = name_concepts[name]
#             auto.add_word(name.encode('utf8'), (i, name.encode('utf8')))
#         auto.make_automaton()
#         return cls(auto, id2concepts)
#
#     @classmethod
#     def load(cls, automaton_file, id2concepts_file):
#         import cPickle as pickle
#         with open(FileIO.filename(automaton_file), 'rb') as f:
#             auto = pickle.load(f)
#         with open(FileIO.filename(id2concepts_file), 'rb') as f:
#             id2concepts = pickle.load(f)
#         return cls(auto, id2concepts)
#


class HashtagMatch:

    def __init__(self, name_matcher):
        from nltk.tokenize import RegexpTokenizer
        self._name_matcher = name_matcher
        self._hashtag_extract = RegexpTokenizer('(#[A-Za-z][A-Za-z0-9-_]+)')
        self._at_extract = RegexpTokenizer('(@[A-Za-z][A-Za-z0-9-_]+)')

    def extract_hashtag(self, text):
        return self._hashtag_extract.tokenize(text)

    def extract_at(self, text):
        return self._at_extract.tokenize(text)

    def match(self, text):
        segs = [' '.join(seg) for seg in self.segment(text[1:])]
        entities = map(self._name_matcher.exact_match, segs)
        return [e for e in entities if e]

    def segment(self, text):
        n = len(text) - 1
        count = 2 ** n
        sequences = map(lambda x: bin(x)[2:].zfill(n), range(count))
        segmentations = []
        for s in sequences:
            segmentation = []
            begin = 0
            for i in range(n):
                end = i + 1
                if s[i] == '1':
                    segmentation.append(''.join(text[begin:end]))
                    begin = end
            segmentation.append(''.join(text[begin:end + 1]))
            segmentations.append(segmentation)
        return segmentations

