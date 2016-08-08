from nltk import FreqDist
from nltk.collocations import BigramAssocMeasures, TrigramAssocMeasures, BigramCollocationFinder


class TextStats:

    def __init__(self, data):
        self._fd = FreqDist(data)
        self._bigram = BigramAssocMeasures()
        self._trigram = TrigramAssocMeasures()
        self._finder = BigramCollocationFinder.from_words(data)

    def nbest_pmi(self, n=10):
        return self._finder.nbest(self._bigram.pmi, n)

