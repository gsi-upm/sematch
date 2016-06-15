from nltk.corpus import wordnet as wn
from sematch.semantic.similarity import Similarity
from sematch.nlp import word_tokenize, lemmatization
from collections import Counter
from itertools import combinations
import networkx as nx
import random

class WSD:
    '''
        wsd = WSD()
        print wsd.semcor2synset('editorial%1:10:00::')
        Synset('column.n.05')
        print wsd.offset2synset('06268567-n')
        Synset('live.v.02')
        print wsd.semcor2offset('editorial%1:10:00::')
        06268567-n
        context = ['editorial', 'homeless','research', 'colleague', 'issue', 'journal']
        wsd.disambiguate_max_similarity(context_words, 'research', 'wup')
        print wsd.disambiguate_baseline_first('research')
        print wsd.disambiguate_baseline_random('research')

    '''

    def __init__(self):
        self.sim = Similarity()
        self.sim_methods = ['path', 'lch', 'wup', 'li', 'res', 'jcn', 'lin', 'wpath']

    def offset2synset(self, offset):
        return wn._synset_from_pos_and_offset(str(offset[-1:]), int(offset[:8]))

    def semcor2synset(self, sense):
        return wn.lemma_from_key(sense).synset()

    def semcor2offset(self, sense):
        synset = self.semcor2synset(sense)
        return '%08d-%s' % (synset.offset(), synset.pos())

    def similarity(self, c1, c2, name='path'):
        return self.sim.method(name)(c1, c2)

    def word2synset(self, ambiguous_word):
        return wn.synsets(ambiguous_word, pos=wn.NOUN)

    def context2words(self, sent):
        words = word_tokenize(sent.lower())
        words = [w for w in words if len(w) > 2]
        words = lemmatization(words)
        return [w for w in words if self.word2synset(w)]

    def disambiguate_baseline_random(self, ambiguous_word):
        ambiguous_synsets = self.word2synset(ambiguous_word)
        if not ambiguous_synsets:
            return None
        return random.choice(ambiguous_synsets)

    def disambiguate_baseline_first(self, ambiguous_word):
        ambiguous_synsets = self.word2synset(ambiguous_word)
        if not ambiguous_synsets:
            return None
        return ambiguous_synsets[0]

    def disambiguate_pagerank(self, context_words, ambiguous_word, method):
        ambiguous_synsets = self.word2synset(ambiguous_word)
        if not ambiguous_synsets:
            return None
        if len(ambiguous_synsets) == 1:
            return ambiguous_synsets[0]
        context_words = list(set(context_words))
        context_synsets = []
        for word in context_words:
            if word != ambiguous_word:
                context = wn.synsets(word, pos=wn.NOUN)
                if context:
                   for con in context:
                       context_synsets.append(con)
        context_synsets = list(set(context_synsets))
        all_synsets = [x for x in ambiguous_synsets]
        for x in context_synsets:
            if x not in ambiguous_synsets:
                all_synsets.append(x)
        synset_id_dic = {all_synsets[i]:i for i in range(len(all_synsets))}
        graph = nx.Graph()
        for pair in combinations(all_synsets, 2):
            x, y = pair
            sim_score = self.similarity(x, y, method)
            if sim_score > 0:
                graph.add_edge(synset_id_dic[x], synset_id_dic[y], weight=sim_score)
        ranks = nx.pagerank(graph)
        result = {x:ranks[synset_id_dic[x]] for x in ambiguous_synsets if synset_id_dic[x] in ranks}
        return Counter(result).most_common(1)[0][0]


    def disambiguate_max_similarity(self, context_words, ambiguous_word, method):
        ambiguous_synsets = self.word2synset(ambiguous_word)
        if not ambiguous_synsets:
            return None
        if len(ambiguous_synsets) == 1:
            return ambiguous_synsets[0]
        context_words = list(set(context_words))
        context_synsets = []
        for word in context_words:
            if word != ambiguous_word:
                context = wn.synsets(word, pos=wn.NOUN)
                if context:
                    context_synsets.append(context)
        result = {}
        for syn in ambiguous_synsets:
            scores = []
            for context in context_synsets:
                score = max([self.similarity(syn, x, method) for x in context])
                scores.append(score)
            result[syn] = sum(scores)
        return Counter(result).most_common(1)[0][0]


