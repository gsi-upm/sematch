from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic

class SynsetExpansion:

    def __init__(self):
        self.ic_corpus = wordnet_ic.ic('ic-brown.dat')

    def path(self, syn1, syn2):
        return syn1.wup_similarity(syn2)

    def wup(self, syn1, syn2):
        return syn1.wup_similarity(syn2)

    def lch(self, syn1, syn2):
        return syn1.lch_similarity(syn2,) / syn1.lch_similarity(syn1)

    def res(self, syn1,syn2):
        return syn1.res_similarity(syn2, self.ic_corpus) / syn1.res_similarity(syn1, self.ic_corpus)

    def jcn(self, syn1,syn2):
        return syn1.jcn_similarity(syn2, self.ic_corpus)

    def lin(self, syn1,syn2):
        return syn1.lin_similarity(syn2, self.ic_corpus)

    def sim(self, name):
        def function(syn1, syn2):
            return getattr(self, name)(syn1,syn2)
        return function

    def expansion(self, seeds, th, sim):
        result = []
        for s in seeds:
             self.expander(s, s, th, sim, result)
        return result

    def expander(self, c, s, th, sim, lst):
        lst.append(c)
        for x in c.hypernyms():
            if x not in lst and sim(s,x) >= th:
                self.expander(x, s, th, sim, lst)
        for y in c.hyponyms():
            if y not in lst and sim(s,y) >= th:
                self.expander(y, s, th, sim, lst)

    def synsets(self, term, sim, th):
        seeds = wn.synsets(term, pos=wn.NOUN)
        expanding = self.expansion(seeds, th, self.sim(sim))
        return expanding

    def explain(self, lst):
        return [{'name':str(s),'definition':s.definition} for s in lst]
