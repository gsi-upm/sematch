from nltk.corpus import wordnet as wn
from itertools import combinations
from sematch.semantic.similarity import WordNetSimilarity
from sematch.utility import FileIO
import numpy as np

class Tax2Vec:

    def __init__(self):
        self.concepts = list(wn.all_synsets('n'))[:10000]
        self.threshold = 0.2
        self.id2concept = {i:self.concepts[i] for i in range(len(self.concepts))}
        self.tax_sim = WordNetSimilarity()

    def sim_matrix(self):
        N = len(self.concepts)
        M = np.zeros((N, N), dtype=np.float64)
        for i in range(N):
            M[i, i] = 1.0
        for x, y in combinations(range(N), 2):
            score = self.tax_sim.similarity(self.id2concept[x], self.id2concept[y])
            if score > self.threshold:
                M[x, y] = score
                M[y, x] = score
        return M

tax = Tax2Vec()
model = tax.sim_matrix()
np.save(FileIO.filename('db/tax2vec/wordnet2vec'), model)
model = np.load(FileIO.filename('db/tax2vec/wordnet2vec.npy'))
print model