#from sematch.nlp import WebQuestion,TwitterText, SearchQuery, clean_context
# from sematch.semantic.analysis import EntityCommentModel
# from sematch.semantic.analysis import EntityAbstractModel
# from sematch.semantic.analysis import TypeModel
# from sematch.semantic.analysis import CatModel
# from sematch.utility import string_similarity
#from sematch.index import entity_candidates
from collections import Counter


class EntityIndex:

    def __init__(self, solr_uri='http://localhost:8983/solr/%s'):
        from pysolr import Solr
        self._names = Solr(solr_uri % 'names')
        self._types = Solr(solr_uri % 'types')
        self._redirects = Solr(solr_uri % 'redirects')
        self._entities = Solr(solr_uri % 'entities')
        self._categories = Solr(solr_uri % 'categories')

    def redirect(self, dbr):
        query = 'dbr:"%s"'
        data = self._redirects.search(query % dbr)
        data = [d['redirect'][0] for d in data]
        if data:
            return data[0]
        return None

    def entity_category(self, dbr):
        query = 'dbr:"%s"'
        data = self._categories.search(query % dbr, **{'rows':500})
        data = [d['category'][0] for d in data]
        if data:
            return data
        return None

    def entity_type(self, dbr):
        query = 'dbr:"%s"'
        data = self._types.search(query % dbr)
        data = [d['type'][0] for d in data]
        if data:
            return data[0]
        return None

    def has_entity(self, dbr):
        query = 'dbr:"%s"'
        data = self._entities.search(query % dbr)
        data = [d['dbr'][0] for d in data]
        if data:
            return True
        return False

    def redirect_filter(self, link):
        red = self.redirect(link)
        return red if red else link

    def disambiguation_page_filter(self, link):
        return True if link.__contains__('(disambiguation)') else False

    def entity_candidates(self, text):
        query = 'name:"%s"'
        data = self._names.search(query % text, **{'rows':500})
        data = [d['dbr'][0] for d in data]
        data = map(self.redirect_filter, data)
        data = list(set(data))
        data = [d for d in data if not self.disambiguation_page_filter(d)]
        return data

def extract_entity_feature_local():
    pass

def extract_entity_feature_online(entity):
    from sematch.sparql import EntityFeatures
    return EntityFeatures().entity_features(entity)

class WordFeature:

    def __init__(self, good_tags=set(['NN','NNS'])):
        import nltk
        self._tokenize = nltk.tokenize.RegexpTokenizer(r'\w+').tokenize
        self._pos_tag = nltk.pos_tag
        self._lemmatize = nltk.stem.WordNetLemmatizer().lemmatize
        self._stop_words = set(nltk.corpus.stopwords.words('english'))
        self._good_tags = good_tags

    def category_words(self, categories):
        def extract_words(cat_uri):
            words = cat_uri.replace('http://dbpedia.org/resource/Category:', '').split('_')
            words = self._tokenize(' '.join(words))
            tagged_words = self._pos_tag(words)
            return [word.lower() for word, tag in tagged_words
                      if tag in self._good_tags and word.lower() not in self._stop_words]
        import itertools
        candidates = itertools.chain.from_iterable(extract_words(c) for c in categories)
        candidates = map(self._lemmatize, set(candidates))
        return list(set(candidates))

    def type_words(self, types):
        pass


wf = WordFeature()

feature = extract_entity_feature_online('http://dbpedia.org/resource/NeXT')
cats = feature['category']
print wf.category_words(cats)

def extract_context_feature():
    pass

class WordSimEntityRank:

    def __init__(self, sim="wordnet"):
        from sematch.semantic.similarity import WordNetSimilarity
        from sematch.semantic.similarity import Word2VecSimilarity
        self.wordsim = WordNetSimilarity() if sim == "wordnet" else Word2VecSimilarity()

    def rank_entities(self, context, E):

        def compare(x, y):
            if x < y:
                return True
            else:
                return False

        for i in range(len(E) - 1, 0, -1):
            for j in range(i):
                if compare(E[j], E[j + 1]):
                    temp = E[j]
                    E[j] = E[j + 1]
                    E[j + 1] = temp



    def feature_similarity(self):
        pass



class IREntityRank:

    def __init__(self):
        pass

class EnbeddingRank:

    def __init__(self):
        pass



#
# class Matching:
#
#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.N = len(self.tokens)
#         self.segments = [(j,j+i) for i in range(1, self.N + 1) for j in range(self.N - i + 1)]
#         self.segment2entity = {}
#
#     def entities(self):
#         for s in self.segments:
#             sf = self.surface_form(s).lower()
#             entities = entity_candidates(sf)
#             if entities:
#                 self.add(s, entities)
#         span = self.maximun_span()
#         result = {}
#         for seg in self.segment2entity:
#             x,y = seg
#             if y - x == span:
#                 entities = self.segment2entity[seg]
#                 sf = self.surface_form(seg)
#                 for entity in entities:
#                     result[entity] = self.uri_similarity(sf,entity)
#         return result
#
#     def uri_similarity(self, text, entity):
#         fragment = entity[28:]
#         #fragment = re.sub(r'\([^)]*\)', '', fragment)
#         x = str(text).lower()
#         y = str(fragment).lower()
#         return string_similarity(x,y)
#
#     def surface_form(self, segment):
#         begin, end = segment
#         return ' '.join(self.tokens[begin:end])
#
#     #add the mapped entities into lexicon
#     def add(self, segment, entities):
#         map(lambda x:self.add_entry(segment, x), entities)
#
#     def add_entry(self, segment, entity):
#         self.segment2entity.setdefault(segment, []).append(entity)
#
#     def maximun_span(self):
#         max_span = 1
#         for seg in self.segment2entity:
#             x,y = seg
#             span = y - x
#             if span > max_span:
#                 max_span = span
#         return max_span


# class EntityLinking:
#
#     def __init__(self):
#         #latent semantic models and tfidf model using distributional semantics of words
#         self.comment = EntityCommentModel()
#         self.abstract = EntityAbstractModel()
#         #embedding models for category and types
#         self.type = TypeModel()
#         self.category = CatModel()
#
#     def spoting(self, text):
#         #blob = WebQuestion(text)
#         blob = SearchQuery(text)
#         phrases = blob.phrases
#         #print blob.tags
#         #print phrases
#         result = {}
#         for p in phrases:
#             match = Matching(p.split())
#             entities = match.entities()
#             if entities:
#                 result[p] = entities
#         return result
#
#     def weighting(self, score_dict, w):
#         return Counter({key:w*value for key, value in score_dict.items()})
#
#     def comment_tfidf_similarity(self, context, candidates):
#         comment_tfidf = self.comment.text_entities_similarity(context, candidates.keys(), model='tfidf')
#         return Counter(comment_tfidf)
#
#     def abstract_tfidf_similarity(self, context, candidates, w=1):
#         abstract_tfidf = self.abstract.text_entities_similarity(context, candidates.keys(), model='tfidf')
#         return self.weighting(abstract_tfidf,w)
#
#     def comment_lsi_similarity(self,context, candidates):
#         lsi = self.comment.text_entities_similarity(context, candidates.keys(), model='lsi')
#         return Counter(lsi)
#
#     def abstract_lsi_similarity(self, context, candidates, w=1):
#         lsi = self.abstract.text_entities_similarity(context, candidates.keys(), model='lsi')
#         return self.weighting(lsi,w)
#
#     def type_similarity(self, context, candidates, w=1):
#         type_score = self.type.context_entities(context, candidates.keys())
#         return self.weighting(type_score,w)
#
#     def category_similarity(self, context, candidates, w=4):
#         cat_score = self.category.context_entities(context, candidates.keys())
#         return self.weighting(cat_score, w)
#
#     def disambiguation(self, text, candidates):
#         context = clean_context(text)
#         results = {}
#         for key in candidates:
#             if len(candidates[key]) == 1:
#                 results[key] = candidates[key].keys()[0]
#                 continue
#             entities = Counter(candidates[key])
#             #scorer = self.weighting(entities, 3)#best given 3
#             #scorer = self.comment_tfidf_similarity(context, entities)
#             #scorer = self.comment_lsi_similarity(context, entities)
#             #scorer = self.abstract_tfidf_similarity(context, entities)
#             #scorer = self.abstract_lsi_similarity(context, entities)
#             #scorer = self.category_similarity(context, entities)
#             scorer = self.type_similarity(context, entities)
#             link, score = scorer.most_common(1)[0]
#             results[key] = link
#         return results
#
#     def annotate(self, text):
#         spots = self.spoting(text)
#         return self.disambiguation(text, spots)
#
