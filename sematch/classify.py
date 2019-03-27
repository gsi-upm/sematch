from gsitk.datasets.datasets import DatasetManager
from nltk.corpus import opinion_lexicon
from collections import Counter


def prepare_lexicon(process=True, dim=250, save=False):
    if process:
        dm = DatasetManager()
        data = dm.prepare_datasets()
        nega = set(opinion_lexicon.negative())
        posi = set(opinion_lexicon.positive())
        lexicon = opinion_lexicon.words()
        lexicon_dic = {x: 0 for x in lexicon}
        for t in data['vader']['text']:
            for w in t:
                if w in lexicon_dic:
                    lexicon_dic[w] += 1
        for t in data['sentiment140']['text']:
            for w in t:
                if w in lexicon_dic:
                    lexicon_dic[w] += 1
        L = Counter(lexicon_dic).most_common(4000)
        N = []
        P = []
        for w, _ in L:
            if w in nega:
                N.append(w)
            elif w in posi:
                P.append(w)
        l = P[:dim] + N[:dim]
        if save:
            with open('senti.lexicon', 'w') as f:
                for d in l:
                    f.write(d)
                    f.write('\n')
        return l
    else:
        with open('senti.lexicon', 'r') as f:
            data = [line.strip() for line in f]
        return data


from gensim.models import Word2Vec
from numpy import array, dot
from gensim import matutils
import collections
import functools


class memoized(object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


class WordRelatedness:
    def __init__(self, model):
        self._model = model
        self._words = set([w for w in self._model.vocab])

    def check_word(self, word):
        return True if word in self._words else False

    def check_words(self, words):
        return [w for w in words if self.check_word(w)]

    def similar_words(self, word):
        return self._model.most_similar(word) if self.check_word(word) else []

    @memoized
    def word_similarity(self, w1, w2):
        return self._model.similarity(w1, w2) if self.check_word(w1) and self.check_word(w2) else 0.0

    def words_similarity(self, words1, words2):
        w1 = self.check_words(words1)
        w2 = self.check_words(words2)
        return self._model.n_similarity(w1, w2) if w1 and w2 else 0.0

    def word_vector(self, w):
        return matutils.unitvec(self._model[w]) if self.check_word(w) else None

    def words_vector(self, words):
        v_words = [self._model[w] for w in self.check_words(words)]
        return matutils.unitvec(array(v_words).mean(axis=0)) if v_words else None

    def consine_similarity(self, v1, v2):
        return dot(v1, v2)


from gsitk.features.word2vec import Word2VecFeatures
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
import numpy as np
import nltk


class SimVectorizer:
    def __init__(self, senti_lexicon):
        w2v_feat = Word2VecFeatures(w2v_model_path='/data/w2vmodel_500d_5mc')
        sim_model = WordRelatedness(w2v_feat.model)
        self._sim = sim_model.word_similarity
        self._lexicon = senti_lexicon
        self._N = len(self._lexicon)
        # self._vectorizer = DictVectorizer(sparse=False)
        self._stopwords = set(nltk.corpus.stopwords.words('english'))

    def word_process(self, words):
        return [w for w in words if w not in self._stopwords and len(w) > 2]

    def similarity(self, words, feature):
        return max([self._sim(w, feature) for w in words] + [0.0])

    def transform(self, X):
        X_transformed = np.zeros((len(X), self._N))
        for i, x in enumerate(X):
            # if i % 10000 == 0:
            #    print(i)
            words = self.word_process(x)
            words = set(words)
            for j, f in enumerate(self._lexicon):
                X_transformed[i, j] = self.similarity(words, f)
        return X_transformed


from nltk.corpus import opinion_lexicon
from collections import Counter
import numpy as np
import nltk

Punc = [".", "!", "?", ",", ";", ":", "-", "'", "\"",
        "!!", "!!!", "??", "???", "?!?", "!?!", "?!?!", "!?!?"]
Negate = ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
          "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
          "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
          "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
          "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
          "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
          "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
          "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite"]
Booster = ["absolutely", "amazingly", "awfully", "completely", "considerably",
           "decidedly", "deeply", "effing", "enormously", "entirely", "especially", "exceptionally",
           "extremely", "fabulously", "flipping", "flippin", "fricking", "frickin", "frigging",
           "friggin", "fully", "fucking", "greatly", "hella", "highly", "hugely", "incredibly",
           "intensely", "majorly", "more", "most", "particularly", "purely", "quite", "really",
           "remarkably", "so", "substantially", "thoroughly", "totally", "tremendously",
           "uber", "unbelievably", "unusually", "utterly", "very", "almost", "barely", "hardly",
           "just enough", "kind of", "kinda", "kindof", "kind-of", "less", "little", "marginally",
           "occasionally", "partly", "scarcely", "slightly", "somewhat", "sort of", "sorta",
           "sortof", "sort-of"]

Extra_Lexicon = Punc + Negate + Booster


def create_lexicon(corpus, embedding, num=250):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    V = set([w for w in embedding.vocab])
    tags = corpus['polarity']
    texts = corpus['text']
    P = [t for i, t in texts.iteritems() if int(tags[i]) == 1]
    N = [t for i, t in texts.iteritems() if int(tags[i]) == -1]

    def word_count(X):
        d = {}
        for x in X:
            for w in x:
                if w not in stopwords and w in V and len(w) > 1:
                    d[w] = d[w] + 1 if w in d else 1
        return d

    P_dict = word_count(P)
    N_dict = word_count(N)
    L_p = Counter(P_dict).most_common(num)
    L_n = Counter(N_dict).most_common(num)
    Words_p, Counts_p = zip(*L_p)
    Words_n, Counts_n = zip(*L_n)
    P_sum = sum(Counts_p)
    N_sum = sum(Counts_n)
    P_score = [x * 1.0 / P_sum for x in Counts_p]
    N_score = [x * 1.0 / N_sum for x in Counts_n]
    return Words_p + Words_n, P_score + N_score


def prepare_lexicon(corpus, embedding, num=250, extra=False):
    V = set([w for w in embedding.vocab])
    neg = set(opinion_lexicon.negative())
    pos = set(opinion_lexicon.positive())
    senti_lexicon = opinion_lexicon.words()
    senti_lexicon = [w for w in senti_lexicon if w in V]
    lexicon_dic = {x: 0 for x in senti_lexicon}
    for sent in corpus:
        for w in sent:
            if w in lexicon_dic:
                lexicon_dic[w] += 1
    L = Counter(lexicon_dic).most_common(5000)
    N = []
    N_count = []
    P = []
    P_count = []
    for word, count in L:
        if word in neg:
            N.append(word)
            N_count.append(count)
        elif word in pos:
            P.append(word)
            P_count.append(count)
    Senti_L = P[:num] + N[:num]
    P_sum = sum(P_count[:num])
    P_score = [x * 1.0 / P_sum for x in P_count[:num]]
    N_sum = sum(N_count[:num])
    N_score = [x * 1.0 / N_sum for x in N_count[:num]]
    Senti_W = P_score + N_score
    if extra:
        Extra_L = [l for l in Extra_Lexicon if l in V]
        Extra_W = [1.0 for l in Extra_L]
        return Senti_L + Extra_L, Senti_W + Extra_W
    return Senti_L, Senti_W


class SimVectorizer:
    def __init__(self, lexicon, weight, embedding, stopword=True, weighted=False):
        self._stopwords = set(nltk.corpus.stopwords.words('english'))
        self._model = embedding
        self._W = weight
        self._V = set([w for w in self._model.vocab])
        self._L = self.word_vectors(lexicon).T
        self._filter = lambda x: self.vectorization(self.word_process(x))
        self.sim_vectorization = self._filter if stopword else self.vectorization
        self._weighter = lambda x: np.multiply(self.sim_vectorization(x), self._W)
        self.sim_vector = self._weighter if weighted else self.sim_vectorization

    def word_process(self, words):
        return [w for w in words if w not in self._stopwords and len(w) > 1]

    def word_vectors(self, x):
        return np.array([self._model[w] for _, w in enumerate(x) if w in self._V])

    def vectorization(self, x):
        v = self.word_vectors(x)
        if v.shape[0] == 0:
            return np.zeros(self._L.shape[1])
        s = np.dot(v, self._L)
        return s.max(axis=0)

    def transform(self, X):
        return np.array([self.sim_vector(x) for _, x in enumerate(X)])

