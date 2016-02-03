from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
from nlp import QueryProcessor
from Expansion import SynsetExpansion
from utility import FileIO
import abc
import spotlight


class Linker(object):

    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def linking(self, data):
        """link text to LOD"""

class DBpediaSpotlight(Linker):

    def __init__(self):
        self.uri = 'http://spotlight.dbpedia.org/rest/annotate'
        self.confidence = 0.2
        self.support = 20

    def linking(self, query):
        annotations = spotlight.annotate(self.uri,query,confidence=self.confidence, support=self.support)
        annotations = [a['URI'] for a in annotations]
        return annotations

class SPARQLEntityLinker(Linker):

    def __init__(self, url="http://dbpedia.org/sparql"):
        self.url = url
        self.sparql = SPARQLWrapper(url)
        self.sparql.setReturnFormat(JSON)
        self.query_processor = QueryProcessor()
        self.query = '''select distinct ?uri where {
                    ?uri rdfs:label "%s"@en .
                    {?uri rdf:type <http://dbpedia.org/ontology/Place>} UNION
                    {?uri rdf:type <http://dbpedia.org/ontology/Person>} UNION
                    {?uri rdf:type <http://dbpedia.org/ontology/Agent>}
                    }'''
        self.category = {
            "GPE":"http://dbpedia.org/ontology/Country",
            "PERSON":"http://dbpedia.org/ontology/Person",
                         }

    def linking(self, query):
        tokens = self.query_processor.tokenization(query)
        entities = []
        for i in range(len(tokens)):
            entities.append(tokens[i])
        for i in range(len(tokens)-1):
            entities.append(' '.join([tokens[i], tokens[i+1]]))
        e_links = []
        for e in entities:
            q = self.query % e.title()
            self.sparql.setQuery(q)
            results = self.sparql.query().convert()
            e_links += [result["uri"]["value"] for result in results["results"]["bindings"]]
        return e_links


class SynsetLinker(Linker):

    def __init__(self):
        self.links = FileIO.read_json_file("db/type-linkings.txt")
        self.links = {data['offset']:data for data in self.links}
        self.query_processor = QueryProcessor()
        self.expander = SynsetExpansion(0.95, 'wup')

    def offset(self, synset):
        return str(synset.offset() + 100000000)


    def link_append(self, synset, lst):
        if self.links.get(self.offset(synset)):
            typeLinks = self.links.get(self.offset(synset))
            if typeLinks.get('dbpedia'):
                lst.append(typeLinks['dbpedia'])

            if typeLinks.get('yago_dbpedia'):
                lst.append(typeLinks['yago_dbpedia'])
            return True
        else:
            return False

    def searching(self, query, sim, th):
        self.expander.sim = sim
        self.expander.th = th
        synsets_lst, synsets_tuple = self.expander.synsets_exapnsion(query)
        results = []
        for synset, score in synsets_tuple:
            syn_obj = {}
            syn_obj['synset'] = synset.__str__()
            syn_obj['lemmas'] = ' '.join(synset._lemma_names)
            syn_obj['definition'] = synset._definition
            syn_obj['sim'] = score
            link_lst = []
            self.link_append(synset,link_lst)
            syn_obj['LOD'] = link_lst
            results.append(syn_obj)
        return results

    def linking(self, query):
        tokens = self.query_processor.tokenization(query)
        pos = self.query_processor.pos(tokens)
        types = [x for (x,y) in pos if y == 'NN' or y == 'NNS']
        links = []
        for t in types:
            synsets_lst, synsets_score_tuple = self.expander.synsets_exapnsion(t)
            for s in synsets_lst:
                self.link_append(s,links)
        return links

class LinkerFactory(Linker):

    @abc.abstractmethod
    def linking(self, data):
        """link text to LOD"""

    def __init__(self, name):
        self.linker = self.getLinker(name)()

    def getLinker(self, name):
        def create():
            return getattr(self, name)()
        return create


class EntityLinkers(LinkerFactory):

    def __init__(self, name):
        LinkerFactory.__init__(self,name)

    def spotlight(self):
        return DBpediaSpotlight()

    def sparqllinker(self):
        return SPARQLEntityLinker()

    def linking(self, data):
        return self.linker.linking(data)

class TypeLinkers(LinkerFactory):

    def __init__(self, name):
        LinkerFactory.__init__(self,name)

    def synsetLinker(self):
        return SynsetLinker()

    def linking(self, data):
        return self.linker.linking(data)

