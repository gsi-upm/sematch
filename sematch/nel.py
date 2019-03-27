
from collections import Counter
from sematch.nlp import word_tokenize
import math


class EntityDisambiguation:

    def __init__(self, extractor):
        self._extractor = extractor

    def inverse_entity_frequency(self, candidate_features):
        entity_len = len(candidate_features.keys())
        ief_dict = {}
        for candidate, features in candidate_features.iteritems():
            for word in features:
                if word in ief_dict:
                    ief_dict[word] = ief_dict[word] + 1.0
                else:
                    ief_dict[word] = 1.0
        for word in ief_dict:
            count = ief_dict[word]
            score = math.log(entity_len / (1 + count))
            ief_dict[word] = score + 1.0
        return ief_dict

    def text_disambiguate(self, context, candidates, similarity):
        '''
        Compute context and candidate similarity using text relatedness
        :param context:
        :param candidates:
        :param similarity: TFIDF or LSA
        :return:
        '''
        result = {}
        context_words = ' '.join(self._extractor.context_features(context))
        candidate_features = self._extractor.entity_descriptions(candidates)
        for candidate, feature in candidate_features.iteritems():
            result[candidate] = similarity(context_words, feature)
        return Counter(result).most_common(1)[0][0]

    def category_disambiguate(self, context, candidates, similarity):
        '''
        Compute context and candidate similarity using words-categories similarity
        :param context:
        :param candidates:
        :param similarity: sim([words], [cats])
        :return:
        '''
        result = {}
        context_words = self._extractor.context_features(context)
        candidate_features = self._extractor.entity_categories(candidates)
        for candidate, feature in candidate_features.iteritems():
            result[candidate] = similarity(context_words, feature)
        return Counter(result).most_common(1)[0][0]

    def category_disambiguate_max(self, context, candidates, similarity, K=10):
        '''
        Compute context and candidate similarity using maximun word-category similarity
        :param context:
        :param candidates:
        :param similarity: sim(word, cat)
        :param K:
        :return:
        '''
        result = {}
        context_words = self._extractor.context_features(context)
        candidate_features = self._extractor.entity_categories(candidates)
        for candidate, features in candidate_features.iteritems():
            score = {}
            for x in context_words:
                for y in features:
                    score[(x, y)] = similarity(x, y)
            topk = Counter(score).most_common(K)
            if topk:
                word, scores = zip(*topk)
                result[candidate] = sum(scores)
            else:
                result[candidate] = -1.0
        return Counter(result).most_common(1)[0][0]

    def word_disambiguate(self, context, candidates, similarity, K=10):
        result = {}
        context_words = self._extractor.context_features(context)
        candidate_features = self._extractor.entity_word_features(candidates)
        ief_dict = self.inverse_entity_frequency(candidate_features)
        for candidate, features in candidate_features.iteritems():
            score = {}
            for x in context_words:
                for y in features:
                    score[(x, y)] = similarity(x, y) * ief_dict[y]
            topk = Counter(score).most_common(K)
            if topk:
                word, scores = zip(*topk)
                result[candidate] = sum(scores)
            else:
                result[candidate] = -1.0
        if not result:
            return candidates[0]
        return Counter(result).most_common(1)[0][0]

    # def disambiguate_backup(self, context, candidates, similarity, K=5, Weighted=True):
    #     result = {}
    #     context_words = self._feature_extraction.description_features(context.lower())
    #     if not context_words:
    #         context_words = word_tokenize(context)
    #     candidate_features = {}
    #     for candidate in candidates:
    #         entity_features = self._feature.description(candidate)
    #         candidate_words = self._feature_extraction.description_features(entity_features)
    #         if candidate_words:
    #             candidate_features[candidate] = candidate_words
    #     if Weighted:
    #         ief_dict = self.inverse_entity_frequency(candidate_features)
    #     for candidate, features in candidate_features.iteritems():
    #         score = {}
    #         for x in context_words:
    #             for y in features:
    #                 if Weighted:
    #                     score[(x, y)] = similarity(x, y) * ief_dict[y]
    #                 else:
    #                     score[(x, y)] = similarity(x, y)
    #         topk = Counter(score).most_common(K)
    #         if topk:
    #             word, scores = zip(*topk)
    #             result[candidate] = sum(scores)
    #         else:
    #             result[candidate] = -1.0
    #     return Counter(result).most_common(1)[0][0]

