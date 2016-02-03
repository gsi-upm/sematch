from nltk.corpus import wordnet as wn
from similarity import SemanticSimilarity

class SynsetExpansion:

    def __init__(self, th, sim):
        self.semsim = SemanticSimilarity()
        self.th = th
        self.sim = sim

    def expansion(self, seeds):
        result_tuple = []
        result_lst = []
        for s in seeds:
             self.expander((s,1.0), s, self.th, self.semsim.sim(self.sim), result_lst, result_tuple)
        return result_lst, result_tuple

    def expander(self, c, s, th, sim, result_lst, result_tuple):
        concept, score = c
        result_tuple.append(c)
        result_lst.append(concept)
        for x in concept.hypernyms():
            sim_score = sim(s,x)
            if x not in result_lst and sim_score >= th:
                self.expander((x, sim_score), s, th, sim, result_lst, result_tuple)
        for y in concept.hyponyms():
            sim_score = sim(s,y)
            if y not in result_lst and sim_score >= th:
                self.expander((y, sim_score), s, th, sim, result_lst, result_tuple)

    def synsets_exapnsion(self, term):
        seeds = self.synsets_mapping(term)
        return self.expansion(seeds)

    def synsets_mapping(self, term):
        return wn.synsets(term, pos=wn.NOUN)




