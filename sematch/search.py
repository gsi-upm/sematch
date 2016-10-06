from sematch.semantic.similarity import YagoTypeSimilarity
from sematch.nlp import Extraction
from sematch.sparql import NameSPARQL, QueryGraph

import itertools

class EntitySearch:

    """This class is used for concept based entity search in DBpedia"""

    def __init__(self):
        self._linker = NameSPARQL()
        self._extracter = Extraction()
        self._yago = YagoTypeSimilarity()
        self._query_graph = QueryGraph()

    def query_process(self, query):
        """
        Process query into concept (common noun) and entity (proper noun). Link them
        to Knowledge Graph uri links respectively.
        :param query: short text query
        :return: tuple of concepts and entities in uris.
        """
        concepts = self._extracter.extract_words_sent(query)
        entities = self._extracter.extract_chunks_sent(query)
        concept_uris = list(itertools.chain.from_iterable(map(self._yago.word2yago, concepts)))
        entity_uris = list(itertools.chain.from_iterable(map(self._linker.name2entities, entities)))
        return list(set(concept_uris)), list(set(entity_uris))

    def search(self, query):
        results = []
        concepts, entities = self.query_process(query)
        for e in entities:
            for i in xrange(0, len(concepts), 5):
                results.extend(self._query_graph.type_entity_query(concepts[i:i + 5], e))
        return list(set(results))


