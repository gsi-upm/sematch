from nltk.corpus import wordnet_ic

class SemanticSimilarity:

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
