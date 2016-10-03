from nltk.classify.api import ClassifierI
from sematch.semantic.similarity import WordNetSimilarity
from nltk.wsd import lesk as nltk_lesk
from sematch.nlp import word_tokenize, lemmatization
from collections import Counter
from itertools import combinations
import networkx as nx
import random


class WSD(ClassifierI):

    def __init__(self, method='maxsim', name='path'):
        '''
        method = ['random_sense','first','frequent','maxsim', 'graph', 'lesk', 'naive']
        name = ['path', 'lch', 'wup', 'li', 'res', 'lin', 'jcn', 'wpath']
        '''
        self._method = method
        self._sim_name = name
        self._wn_sim = WordNetSimilarity()

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
        context_words = self.context2words(context)
        return nltk_lesk(context_words, word, 'n')

# wsd = WSD()
# sentence = ' '.join(['I', 'went', 'to', 'the', 'bank', 'to', 'deposit', 'money', '.'])
# print sentence
# test = wsd.max_sim(sentence, 'bank')
# print test, test.definition()
# test2 = wsd.lesk(sentence, 'bank')
# print test, test.definition()


    # def disambiguate_pagerank(self, context_words, ambiguous_word, method):
    #     ambiguous_synsets = self.word2synset(ambiguous_word)
    #     if not ambiguous_synsets:
    #         return None
    #     if len(ambiguous_synsets) == 1:
    #         return ambiguous_synsets[0]
    #     context_words = list(set(context_words))
    #     context_synsets = []
    #     for word in context_words:
    #         if word != ambiguous_word:
    #             context = wn.synsets(word, pos=wn.NOUN)
    #             if context:
    #                for con in context:
    #                    context_synsets.append(con)
    #     context_synsets = list(set(context_synsets))
    #     all_synsets = [x for x in ambiguous_synsets]
    #     for x in context_synsets:
    #         if x not in ambiguous_synsets:
    #             all_synsets.append(x)
    #     synset_id_dic = {all_synsets[i]:i for i in range(len(all_synsets))}
    #     graph = nx.Graph()
    #     for pair in combinations(all_synsets, 2):
    #         x, y = pair
    #         sim_score = self.similarity(x, y, method)
    #         if sim_score > 0:
    #             graph.add_edge(synset_id_dic[x], synset_id_dic[y], weight=sim_score)
    #     ranks = nx.pagerank(graph)
    #     result = {x:ranks[synset_id_dic[x]] for x in ambiguous_synsets if synset_id_dic[x] in ranks}
    #     return Counter(result).most_common(1)[0][0]


class Combiner:

    def sim_normalization(self, simList):
        pass

    def sim2rank(self, simList):
        pass

    def comb_sum(self, simList):
        pass

    def comb_anz(self, simList):
        pass

    def comb_mnz(self, simList):
        pass

    def borda(self, rankList):
        pass

    def condorcet(self, rankList):
        pass

    def reciprocal(self, rankList):
        pass
