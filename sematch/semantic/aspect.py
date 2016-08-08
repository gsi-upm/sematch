from sematch.nlp import word_tokenize, lemmatization
from sematch.semantic.similarity import WordNetSimilarity, Word2VecSimilarity
from sematch.utility import FileIO
from BeautifulSoup import BeautifulSOAP as bs
from sematch.utility import memoized
from collections import Counter
import numpy as np
import abc

#http://textminingonline.com/dive-into-nltk-part-ix-from-text-classification-to-sentiment-analysis

class SimAspect(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, labels):
        self._wns = WordNetSimilarity()
        self._aspects = labels

    @abc.abstractmethod
    def feature_aspect_similarity(self, word, aspect, method='path'):
        pass

    def classify(self, targets, method='path'):
        '''
        The input target words are compared to each category based on feature aspect similarity.
        The final semantic similarity score between input words with category is sum.
        The category having highest score become the category for target words.
        '''
        target_words = list(set(lemmatization(word_tokenize(targets))))
        score = {}
        for aspect in self._aspects:
            #score[aspect] = sum([self.feature_aspect_similarity(w, aspect, method) for w in target_words])
            score[aspect] = max([self.feature_aspect_similarity(w, aspect, method) for w in target_words] + [0.0])
        return Counter(score).most_common(1)[0][0]



class MaxSimAspect(SimAspect):

    def __init__(self, labels, features):
        SimAspect.__init__(self, labels)
        self._features = features

    @memoized
    def feature_aspect_similarity(self, word, aspect, method='path'):
        sim = lambda x: self._wns.word_similarity(word, x, method)
        return max(map(sim, self._features[aspect]) + [0.0])



class WeightedSimAspect(SimAspect):
    '''
    Simple aspect category classifier based on WordNet and semantic similarity.
    '''

    def __init__(self, labels, weights):
        SimAspect.__init__(self, labels)
        self._weights = weights

    @classmethod
    def train(cls, labeled_featuresets, feature_num=5):
        '''
        Compute the weight for each feature token in each category
        The weight is computed as token_count / total_feature_count
        '''
        labels = labeled_featuresets.keys()
        weights = {}
        for c in labeled_featuresets:
            weight = []
            commons = labeled_featuresets[c].most_common(feature_num)
            print c, commons
            total_count = float(sum([count for w, count in commons]))
            for w, count in commons:
                weight.append((w, count / total_count))
            weights[c] = weight
        return cls(labels, weights)

    @memoized
    def feature_aspect_similarity(self, word, aspect, method='path'):
        '''
        Input word is compared to each feature word using semantic similarity. The whole similarity
        score is computed as weighted sum.
        '''
        sim = lambda x: self._wns.word_similarity(word, x, method)
        features, weights = zip(*self._weights[aspect])
        scores = map(sim, features)
        return np.dot(np.array(scores), np.array(weights).transpose())


from sematch.semantic.classification import SimpleClassification, SemanticClassification

ABSA15Restu_Train =  FileIO.filename('eval/aspect/ABSA-15_Restaurants_Train_Final.xml')
ABSA15Restu_Test =  FileIO.filename('eval/aspect/ABSA15_Restaurants_Test.xml')
ABSA16Restu_Train =  FileIO.filename('eval/aspect/ABSA16_Restaurants_Train_SB1_v2.xml')
ABSA16Restu_Test =  FileIO.filename('eval/aspect/ABSA16_Restaurants_Test_Gold.xml')

def extract_pairs(dataset):
    pairs = []
    with open(dataset, 'r') as f:
        corpus = f.read()
        opinions = bs(corpus).findAll('opinion')
        for op in opinions:
            if not op['target'] == 'NULL':
                t = op['target']
                #c = op['category'].split('#')[0]
                c = op['category']
                pairs.append((t, c))
    return pairs

absa16_train = extract_pairs(ABSA16Restu_Train)
absa16_test = extract_pairs(ABSA16Restu_Test)
absa15_train = extract_pairs(ABSA15Restu_Train)
absa15_test = extract_pairs(ABSA15Restu_Test)

X_train, y_train = zip(*absa16_train)
X_test, y_test = zip(*absa16_test)

# bow_model = SimpleSVM.train(X_train, y_train)
# bow_model.evaluate(X_test, y_test)
#
# tfidf_model = SimpleSVM.train(X_train, y_train, model='tfidf')
# tfidf_model.evaluate(X_test, y_test)

# onehot_model = SemanticSVM.train(X_train, y_train)
# onehot_model.evaluate(X_test, y_test)
#
# wordnet_model = SemanticSVM.train(X_train, y_train, feature='wordnet')
# wordnet_model.evaluate(X_test, y_test)

# word2vec_model = SemanticSVM.train(X_train, y_train, feature='word2vec')
# word2vec_model.evaluate(X_test, y_test)


word2vec_model = SemanticClassification.train(X_train, y_train, feature='wordnet', wn_method='lch')
word2vec_model.evaluate(X_test, y_test)


