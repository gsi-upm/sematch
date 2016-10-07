from sematch.semantic.similarity import WordNetSimilarity
from sematch.semantic.graph import SimGraph
from sematch.nlp import word_tokenize, lemmatization

from collections import Counter
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
        #extract words that have a synset in WordNet, currently support NOUN.
        words = [w for w in words_origin if self._wn_sim.word2synset(w)]
        # map words to synsets
        words_synsets = {w:self._wn_sim.word2synset(w) for w in words}
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
                candidate_scores = {s:rank_scores[s] for s in words_synsets[w]}
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
        scorer = lambda x:self._wn_sim.similarity(x, sense, self._sim_name)
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


