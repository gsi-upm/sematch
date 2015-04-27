from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
from QueryProcessing import Query
from Expansion import SynsetExpansion
from Utility import FileIO
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
        self.query_processor = Query()
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
            q = self.query % e
            self.sparql.setQuery(q)
            results = self.sparql.query().convert()
            e_links += [result["uri"]["value"] for result in results["results"]["bindings"]]
        return e_links


class SynsetLinker(Linker):

    def __init__(self):
        self.links = FileIO.read_json_file("db/type-linkings.txt")
        self.links = {data['offset']:data for data in self.links}
        self.query_processor = Query()
        self.expander = SynsetExpansion(0.95, 'wup')

    def offset(self, synset):
        return str(synset.offset() + 100000000)

    def link_append(self, typeLinks, lst):
        if typeLinks.get('dbpedia'):
            lst.append(typeLinks['dbpedia'])

        if typeLinks.get('yago_dbpedia'):
            lst.append(typeLinks['yago_dbpedia'])

    def linking(self, query):
        tokens = self.query_processor.tokenization(query)
        pos = self.query_processor.pos(tokens)
        types = [x for (x,y) in pos if y == 'NN' or y == 'NNS']
        links = []
        for t in types:
            synsets = self.expander.synsets(t)
            for s in synsets:
                if self.links.get(self.offset(s)):
                    self.link_append(self.links.get(self.offset(s)), links)
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
