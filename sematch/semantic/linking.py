from sematch.nlp import tokenization
from sematch.nlp import StopWords
from sematch.nlp import google_search_for_wiki




class EntityLinking:

    def __init__(self):
        self.window = 5

    def fragment(self, t):
        tokens = tokenization(t)
        n = len(tokens)
        segments = [' '.join(tokens[j:j+i]) for i in range(1, self.window + 1) for j in range(n - i + 1)]
        tokens, L = self.lexicon(tokens, segments)
        return tokens, L

    def viterbi_segmentation(self, query):
        """Find the best segmentation of the query based on viterbi algorithm using maximun span"""
        tokens, lexicon = self.fragment(query)
        n = len(tokens)
        segments = [' '] + tokens
        best = [1.0] + [0.0] * n
        for i in range(n+1):
            for j in range(0, i):
                s = tokens[j:i]
                k = ' '.join(s)
                if lexicon.get(k):
                    w = lexicon[k]['weight']
                    if w + best[i - len(s)] >= best[i]:
                        best[i] = w + best[i - len(s)]
                        segments[i] = s
        sequence = []
        i = len(segments)-1
        while i > 0:
            sequence[0:0] = [segments[i]]
            i = i - len(segments[i])
        sequence = map(lambda x:' '.join(x), sequence)
        return sequence, lexicon, best[-1]

    def segmentation(self, query):
        sequence, lexicon, score = self.viterbi_segmentation(query)
        resources = {}
        for seq in sequence:
            resources[seq] = lexicon[seq]['resources']
        return sequence, resources


print google_search_for_wiki('')