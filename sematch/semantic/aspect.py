from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer, PorterStemmer
from collections import Counter
import json

class Aspect:

    def __init__(self):
        self.aspects = ['food','drinks','service','ambience','location']
        self.lemma = WordNetLemmatizer()
        self.porter = PorterStemmer()
        self.aspect_features = self.load_feature()

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

    def word_similarity(self, w1, w2):
        s1 = self.word2synsets(w1)
        s2 = self.word2synsets(w2)
        scores = [c1.path_similarity(c2) for c1 in s1 for c2 in s2] + [0]
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

    def target2aspect(self, targets):
        context = targets.lower().split()
        score = {}
        for aspect in self.aspects:
            score[aspect] = sum([self.word_aspect_similarity(w, aspect) for w in context])
        return Counter(score).most_common(1)[0][0]

a = Aspect()
print 'Feature: Taiwanese food => FOOD'
print a.target2aspect('Taiwanese food')
print 'Feature: bagels => FOOD'
print a.target2aspect('bagels')
print 'Feature: blond wood decor => AMBIENCE'
print a.target2aspect('blond wood decor')
print 'Feature: live jazz band => AMBIENCE'
print a.target2aspect('live jazz band')
print 'Feature: staff => SERVICE'
print a.target2aspect('staff')
print 'Feature: Winnie => SERVICE'
print a.target2aspect('winnie')
print 'Feature: view => LOCATION'
print a.target2aspect('view')
print 'Feature: place => LOCATION'
print a.target2aspect('place')
print 'Feature: strawberry daiquiries => DRINKS'
print a.target2aspect('strawberry daiquiries')
print 'Feature: Wine list => DRINKS'
print a.target2aspect('Wine list')













