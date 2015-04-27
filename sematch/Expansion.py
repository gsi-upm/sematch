from nltk.corpus import wordnet as wn
from Similarity import SemanticSimilarity

class SynsetExpansion:

    def __init__(self, th, sim):
        self.semsim = SemanticSimilarity()
        self.th = th
        self.sim = sim

    def expansion(self, seeds):
        result = []
        for s in seeds:
             self.expander(s, s, self.th, self.semsim.sim(self.sim), result)
        return result

    def expander(self, c, s, th, sim, lst):
        lst.append(c)
        for x in c.hypernyms():
            if x not in lst and sim(s,x) >= th:
                self.expander(x, s, th, sim, lst)
        for y in c.hyponyms():
            if y not in lst and sim(s,y) >= th:
                self.expander(y, s, th, sim, lst)

    def synsets(self, term):
        seeds = wn.synsets(term, pos=wn.NOUN)
        return self.expansion(seeds)



