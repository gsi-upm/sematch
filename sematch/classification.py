
from sematch.nlp import word_tokenize, lemmatization
from sematch.semantic.similarity import WordVecSimilarity, WordNetSimilarity
from sematch.utility import memoized
from collections import Counter

import numpy as np


class SimCatClassifier:
    """
    This class implements similarity based category classifiers.
    """

    def __init__(self, labels, cat_features, feature_weights, sim_metric, sim_model='weighted'):
        """
         Class initialization.
        :param labels: predefined categories
        :param cat_features: features to represent each category
        :param sim_metric: word similarity function
        """
        self._categories = labels
        self._cat_features = cat_features
        self._feature_weights = feature_weights
        self._sim_metric = sim_metric
        self._sim_model = self.pick_sim_model(sim_model)

    def pick_sim_model(self, sim_model):
        weighted = lambda x, y: self.weighted_similarity(x, y)
        max_sim = lambda x, y: self.max_similarity(x, y)
        average = lambda x, y: self.average_similarity(x, y)
        model_dic = {'weighted':weighted, 'max':max_sim, 'average':average}
        return model_dic[sim_model]

    @classmethod
    def train(cls, corpus, sim_metric, feature_num=5, sim_model='weighted'):
        '''
        Extract categories, features, feature weights, from corpus.
        Compute the weight for each feature token in each category
        The weight is computed as token_count / total_feature_count
        '''
        cat_word = {}
        for sent, cat in corpus:
            cat_word.setdefault(cat, []).extend(lemmatization(word_tokenize(sent)))
        features = {cat: Counter(cat_word[cat]) for cat in cat_word}
        labels = features.keys()
        cat_features = {}
        feature_weights = {}
        for c, f in features.iteritems():
            w_c_pairs = f.most_common(feature_num)
            words, counts = zip(*w_c_pairs)
            cat_features[c] = words
            total_count = float(sum(counts))
            word_weights = []
            for w, count in w_c_pairs:
                word_weights.append((w, count / total_count))
            feature_weights[c] = word_weights
        return cls(labels, cat_features, feature_weights, sim_metric, sim_model)

    def weighted_similarity(self, word, category):
        """
        Input word is compared to each feature word using semantic similarity. The whole similarity
        score is computed as weighted sum.
        :param word: feature word
        :param category: a predefined category
        :return: weighted word similarity score between word and category
        """
        features, weights = zip(*self._feature_weights[category])
        scores = map(lambda x: self._sim_metric(word, x), features)
        return np.dot(np.array(scores), np.array(weights).transpose())

    def max_similarity(self, word, category):
        """
        Compute similarity between word and category, where
        category is represented by several feature words
        :param word: feature word
        :param category: a predefined category
        :return: max word similarity score between word and category
        """
        return max(map(lambda x: self._sim_metric(word, x), self._cat_features[category]) + [0.0])

    def average_similarity(self, word, category):
        """
        Compute similarity between word and category, where
        category is represented by several feature words
        :param word: feature word
        :param category: a predefined category
        :return: average word similarity score between word and category
        """
        sum_score = sum(map(lambda x: self._sim_metric(word, x), self._cat_features[category]) + [0.0])
        N = len(self._cat_features[category])
        return sum_score / N

    @memoized
    def category_similarity(self, word, category):
        """
        Compute the semantic similarity between a word and a category.
        :param word: a feature word
        :param category: predefined category
        :param method: the name of semantic similarity metric
        :return: similarity score between word and category
        """
        return self._sim_model(word, category)

    def classify_single(self, sent, feature_model='max'):
        """
        The input feature words are compared to each category based on category similarity.
        Sum the semantic similarity score between features and category.
        The category having highest similarity score is the correct category.

        :param featuresets: feature sets such as word list
        :param method: specify the semantic similarity metric
        :param model: similarity combination model 'max', 'sum'. Default is 'max'
        :return: the correct category label.
        """
        feature_words = list(set(lemmatization(word_tokenize(sent))))
        score = {}
        for c in self._categories:
            if feature_model == 'max':
                score[c] = max([self.category_similarity(w, c) for w in feature_words] + [0.0])
            else:
                score[c] = sum([self.category_similarity(w, c) for w in feature_words] + [0.0])
        return Counter(score).most_common(1)[0][0]

    def classify(self, X, feature_model='max'):
        return [self.classify_single(x, feature_model) for x in X]


from sklearn.svm import LinearSVC
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer

import time

def timeit(func):

    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        delta  = time.time() - start
        return result, delta
    return wrapper


class TextPreprocessor(BaseEstimator, TransformerMixin):
    """
    Transform input text into feature representation
    """
    def __init__(self, corpus, feature_num=10, model='onehot',
                 wn_method='path',
                 vec_file='models/GoogleNews-vectors-negative300.bin',
                 binary=True):
        """
        :param corpus: use a corpus to train a vector representation
        :param feature_num: number of dimensions
        :param model: onehot or wordnet or word2vec or both
        """
        self._model = model
        self._wn_method = wn_method
        self._features = self.extract_features(corpus, feature_num)
        self._wns = WordNetSimilarity() if model == 'wordnet' or model == 'both' else None
        self._wvs = WordVecSimilarity(vec_file, binary) if model == 'word2vec' or model == 'both' else None

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return X

    def extract_features(self, corpus, feature_num=10):
        cat_word = {}
        for sent, cat in corpus:
            cat_word.setdefault(cat, []).extend(lemmatization(word_tokenize(sent)))
        features = {cat: Counter(cat_word[cat]) for cat in cat_word}
        feature_words = []
        for c, f in features.iteritems():
            words, counts = zip(*f.most_common(feature_num))
            feature_words.extend(list(words))
        feature_words = set(feature_words)
        return feature_words

    def similarity(self, tokens, feature, method='wordnet'):
        if method == 'wordnet':
            sim = lambda x: self._wns.word_similarity(feature, x, self._wn_method)
        else:
            sim = lambda x: self._wvs.word_similarity(feature, x)
        return max(map(sim, tokens) + [0.0])

    def unigram_features(self, tokens):
        words = set(tokens)
        features = {}
        for f in self._features:
            features['contains({})'.format(f)] = (f in words)
        return features

    def wordnet_features(self, tokens):
        words = set(tokens)
        features = {}
        for f in self._features:
            features['wns({})'.format(f)] = self.similarity(words, f)
        return features

    def word2vec_features(self, tokens):
        words = set(tokens)
        features = {}
        for f in self._features:
            features['w2v({})'.format(f)] = self.similarity(words, f, method='word2vec')
        return features

    def semantic_features(self, tokens):
        words = set(tokens)
        features = {}
        for f in self._features:
            features['wns({})'.format(f)] = self.similarity(words, f)
            features['w2v({})'.format(f)] = self.similarity(words, f, method='word2vec')
        return features

    def transform(self, X):
        tokenize = lambda x: lemmatization(word_tokenize(x))
        X_tokens = map(tokenize, X)
        if self._model == 'onehot':
            return map(self.unigram_features, X_tokens)
        elif self._model == 'wordnet':
            return map(self.wordnet_features, X_tokens)
        elif self._model == 'word2vec':
            return map(self.word2vec_features, X_tokens)
        elif self._model == 'both':
            return map(self.semantic_features, X_tokens)


class SimCatSVMClassifier:

    def __init__(self, labels, model):
        self._labels = labels
        self._model = model

    @classmethod
    def train(cls, X, y, classifier=LinearSVC,
              feature_num=10,
              feature='onehot',
              wn_method='path',
              vec_file='models/GoogleNews-vectors-negative300.bin',
              binary=True,
              verbose=True):

        if isinstance(classifier, type):
            classifier = classifier()

        labels = LabelEncoder()
        y_train = labels.fit_transform(y)

        @timeit
        def build():

            corpus = zip(X, y)
            model = Pipeline([
                ('preprocessor', TextPreprocessor(corpus, feature_num, feature, wn_method, vec_file, binary)),
                ('vectorizer', DictVectorizer()),
                ('classifier', classifier),
            ])

            model.fit(X, y_train)
            return model

        if verbose: print("Building the model")
        model, secs = build()
        if verbose: print("Complete model building in {:0.3f} seconds".format(secs))

        return cls(labels, model)

    def classify(self, X):
        predicted = self._model.predict(X)
        return list(self._labels.inverse_transform(predicted))



class SimpleSVMClassifier:

    def __init__(self, labels, vectorizer, classifier):
        self._labels = labels
        self._vectorizer = vectorizer
        self._classifier = classifier

    @classmethod
    def train(cls, X, y, classifier=LinearSVC, model='bow'):
        """
        :param X:
        :param y:
        :param classifier:
        :param model: bow or tfidf
        :return:
        """
        tokenize = lambda x: lemmatization(word_tokenize(x))
        labels = LabelEncoder()
        y_train = labels.fit_transform(y)
        vectorizer = CountVectorizer(tokenizer=tokenize) \
            if model == 'bow' else TfidfVectorizer(tokenizer=tokenize)
        X_train = vectorizer.fit_transform(X)
        if isinstance(classifier, type):
            classifier = classifier()
        classifier.fit_transform(X_train, y_train)
        return cls(labels, vectorizer, classifier)

    def classify(self, X):
        X_test = self._vectorizer.transform(X)
        predicted = self._classifier.predict(X_test)
        return list(self._labels.inverse_transform(predicted))







