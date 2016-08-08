from sklearn.svm import LinearSVC
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sematch.nlp import feature_words_of_category, word_tokenize, lemmatization
from sematch.semantic.similarity import Word2VecSimilarity, WordNetSimilarity
from sematch.utility import generate_report
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
    def __init__(self, corpus, feature_num=10, model='onehot', wn_method='path'):
        """
        :param corpus: use a corpus to train a vector representation
        :param feature_num: number of dimensions
        :param model: onehot or wordnet or word2vec or both
        """
        self._model = model
        self._wn_method = wn_method
        self._features = self.extract_features(corpus, feature_num)
        self._wns = WordNetSimilarity() if model == 'wordnet' or model == 'both' else None
        self._wvs = Word2VecSimilarity() if model == 'word2vec' or model == 'both' else None

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return X

    def extract_features(self, corpus, feature_num=10):
        all_words = feature_words_of_category(corpus)
        feature_words = []
        for key in all_words:
            words, counts = zip(*all_words[key].most_common(feature_num))
            feature_words.extend(list(words))
        feature_words = set(feature_words)
        print 'feature number', len(feature_words)
        return feature_words

    def similarity(self, tokens, feature, method='wordnet',):
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


class SemanticClassification:

    def __init__(self, labels, model):
        self._labels = labels
        self._model = model

    @classmethod
    def train(cls, X, y, classifier=LinearSVC, feature_num=10, feature='onehot', wn_method='path', verbose=True):

        if isinstance(classifier, type):
            classifier = classifier()

        labels = LabelEncoder()
        y_train = labels.fit_transform(y)

        @timeit
        def build():

            corpus = zip(X, y)
            model = Pipeline([
                ('preprocessor', TextPreprocessor(corpus, feature_num, feature, wn_method)),
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

    def evaluate(self, X, y):
        pred = self.classify(X)
        print("Classification Report:\n")
        generate_report(list(y), list(pred), list(set(y)))


class SimpleClassification:

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

    def evaluate(self, X, y):
        pred = self.classify(X)
        print("Classification Report:\n")
        generate_report(list(y), list(pred), list(set(y)))












