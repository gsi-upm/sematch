from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer, PorterStemmer
from collections import Counter
import json

class Aspect:

    def __init__(self):
        self.lemma = WordNetLemmatizer()
        self.porter = PorterStemmer()
        self.aspect_features = self.load_feature()
        self.feature_category =self.load_cases()

    def load_cases(self):
        feature_class = {}
        for key in self.aspect_features:
            for word in self.aspect_features[key]:
                feature_class.setdefault(word, []).append(key)
        return feature_class

    def load_feature(self):
        features = {}
        with open('words.json','r') as f:
            data = json.loads(f.read())
            for d in data:
                features[d['class']] = d['list'].keys()
        for key in features:
            words = features[key]
            words = set(map(self.lemma.lemmatize, words))
            words = [w for w in words if self.word2synsets(w)]
            features[key] = words
        features['food'] += ['food']
        features['drinks'] += ['drink','beverage']
        features['service'] += ['service']
        features['ambience'] += ['band','live']
        features['location'] += ['location','position']
        for f in features:
            features[f] = list(set(features[f]))
        return features

    def word2synsets(self, word):
        syns = wn.synsets(word)
        if syns:
            return syns
        else:
            syns = wn.synsets(self.porter.stem(word))
            if syns:
                return syns
            else:
                return []

    def concept_similarity(self, c1, c2):
        score = c1.path_similarity(c2)
        if score:
            return score
        else:
            return 0.0

    def word_similarity(self, w1, w2):
        s1 = self.word2synsets(w1)
        s2 = self.word2synsets(w2)
        scores = [self.concept_similarity(c1,c2) for c1 in s1 for c2 in s2] + [0]
        return max(scores)

    def word_aspect_similarity(self, word, aspect):
        sim = lambda x: self.word_similarity(word, x)
        score = map(sim, self.aspect_features[aspect])
        score = [s for s in score if s > 0.2]
        if score:
            if score.__contains__(1.0):
                return 1.0
            return sum(score) / len(score)
        else:
            return 0.0

    def k_most_similar(self, word, k=5):
        score = {}
        for f in self.feature_category:
            score[f] = self.word_similarity(word, f)
        return Counter(score).most_common(k)

    def knn_classify(self, aspect_terms):
        context = aspect_terms.lower().split()
        context = list(set(map(self.lemma.lemmatize, context)))
        votes = {key:0.0 for key in self.aspect_features}
        for con in context:
            categories = self.k_most_similar(con)
            for cat in categories:
                feature, score = cat
                for v in self.feature_category[feature]:
                    votes[v] += score
        return Counter(votes).most_common(1)[0][0]

    def max_sim_classify(self, targets):
        context = targets.lower().split()
        context = list(set(map(self.lemma.lemmatize, context)))
        score = {}
        for aspect in self.aspect_features:
            score[aspect] = sum([self.word_aspect_similarity(w, aspect) for w in context])
        return Counter(score).most_common(1)[0][0]

a = Aspect()

print 'Feature: Taiwanese food => FOOD'
print a.knn_classify('Taiwanese food')
print 'Feature: bagels => FOOD'
print a.knn_classify('bagels')
print 'Feature: blond wood decor => AMBIENCE'
print a.knn_classify('blond wood decor')
print 'Feature: live jazz band => AMBIENCE'
print a.knn_classify('live jazz band')
print 'Feature: staff => SERVICE'
print a.knn_classify('staff')
print 'Feature: Winnie => SERVICE'
print a.knn_classify('winnie')
print 'Feature: view => LOCATION'
print a.knn_classify('view')
print 'Feature: place => LOCATION'
print a.knn_classify('place')
print 'Feature: strawberry daiquiries => DRINKS'
print a.knn_classify('strawberry daiquiries')
print 'Feature: Wine list => DRINKS'
print a.knn_classify('Wine list')













