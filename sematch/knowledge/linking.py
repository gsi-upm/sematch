from sematch.nlp import WebQuestion,TwitterText, SearchQuery, clean_context
from sematch.semantic.analysis import EntityCommentModel
from sematch.semantic.analysis import EntityAbstractModel
from sematch.semantic.analysis import TypeModel
from sematch.semantic.analysis import CatModel
from sematch.utility import string_similarity
from sematch.knowledge.index import entity_candidates
from collections import Counter

class Combiner:

    def sim_normalization(self, simList):
        pass

    def sim2rank(self, simList):
        pass

    def comb_sum(self, simList):
        pass

    def comb_anz(self, simList):
        pass

    def comb_mnz(self, simList):
        pass

    def borda(self, rankList):
        pass

    def condorcet(self, rankList):
        pass

    def reciprocal(self, rankList):
        pass


class Matching:

    def __init__(self, tokens):
        self.tokens = tokens
        self.N = len(self.tokens)
        self.segments = [(j,j+i) for i in range(1, self.N + 1) for j in range(self.N - i + 1)]
        self.segment2entity = {}

    def entities(self):
        for s in self.segments:
            sf = self.surface_form(s).lower()
            entities = entity_candidates(sf)
            if entities:
                self.add(s, entities)
        span = self.maximun_span()
        result = {}
        for seg in self.segment2entity:
            x,y = seg
            if y - x == span:
                entities = self.segment2entity[seg]
                sf = self.surface_form(seg)
                for entity in entities:
                    result[entity] = self.uri_similarity(sf,entity)
        return result

    def uri_similarity(self, text, entity):
        fragment = entity[28:]
        #fragment = re.sub(r'\([^)]*\)', '', fragment)
        x = str(text).lower()
        y = str(fragment).lower()
        return string_similarity(x,y)

    def surface_form(self, segment):
        begin, end = segment
        return ' '.join(self.tokens[begin:end])

    #add the mapped entities into lexicon
    def add(self, segment, entities):
        map(lambda x:self.add_entry(segment, x), entities)

    def add_entry(self, segment, entity):
        self.segment2entity.setdefault(segment, []).append(entity)

    def maximun_span(self):
        max_span = 1
        for seg in self.segment2entity:
            x,y = seg
            span = y - x
            if span > max_span:
                max_span = span
        return max_span


class EntityLinking:

    def __init__(self):
        #latent semantic models and tfidf model using distributional semantics of words
        self.comment = EntityCommentModel()
        self.abstract = EntityAbstractModel()
        #embedding models for category and types
        self.type = TypeModel()
        self.category = CatModel()

    def spoting(self, text):
        #blob = WebQuestion(text)
        blob = SearchQuery(text)
        phrases = blob.phrases
        #print blob.tags
        #print phrases
        result = {}
        for p in phrases:
            match = Matching(p.split())
            entities = match.entities()
            if entities:
                result[p] = entities
        return result

    def weighting(self, score_dict, w):
        return Counter({key:w*value for key, value in score_dict.items()})

    def comment_tfidf_similarity(self, context, candidates):
        comment_tfidf = self.comment.text_entities_similarity(context, candidates.keys(), model='tfidf')
        return Counter(comment_tfidf)

    def abstract_tfidf_similarity(self, context, candidates, w=1):
        abstract_tfidf = self.abstract.text_entities_similarity(context, candidates.keys(), model='tfidf')
        return self.weighting(abstract_tfidf,w)

    def comment_lsi_similarity(self,context, candidates):
        lsi = self.comment.text_entities_similarity(context, candidates.keys(), model='lsi')
        return Counter(lsi)

    def abstract_lsi_similarity(self, context, candidates, w=1):
        lsi = self.abstract.text_entities_similarity(context, candidates.keys(), model='lsi')
        return self.weighting(lsi,w)

    def type_similarity(self, context, candidates, w=1):
        type_score = self.type.context_entities(context, candidates.keys())
        return self.weighting(type_score,w)

    def category_similarity(self, context, candidates, w=4):
        cat_score = self.category.context_entities(context, candidates.keys())
        return self.weighting(cat_score, w)

    def disambiguation(self, text, candidates):
        context = clean_context(text)
        results = {}
        for key in candidates:
            if len(candidates[key]) == 1:
                results[key] = candidates[key].keys()[0]
                continue
            entities = Counter(candidates[key])
            #scorer = self.weighting(entities, 3)#best given 3
            #scorer = self.comment_tfidf_similarity(context, entities)
            #scorer = self.comment_lsi_similarity(context, entities)
            #scorer = self.abstract_tfidf_similarity(context, entities)
            #scorer = self.abstract_lsi_similarity(context, entities)
            #scorer = self.category_similarity(context, entities)
            scorer = self.type_similarity(context, entities)
            link, score = scorer.most_common(1)[0]
            results[key] = link
        return results

    def annotate(self, text):
        spots = self.spoting(text)
        return self.disambiguation(text, spots)

