from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, RDFS, OWL
import requests

class BaseSPARQL:

    def __init__(self, url="http://dbpedia.org/sparql"):
        self.url = url
        self.sparql = SPARQLWrapper(url)
        self.sparql.setReturnFormat(JSON)
        self.tpl = """SELECT DISTINCT %s WHERE {\n\t%s\n}"""
        self.count_tpl = """SELECT %s WHERE {\n\t%s\n}"""

    def request_execution(self, query):
        params={
                "default-graph": "http://dbpedia.org",
                "query": query,
                "debug": "on",
                "format": "application/json",
                "timeout": 30000,
            }
        result = requests.get(self.url, params=params)
        return result.text

    def execution(self, query):
        #print query
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        #print results
        return results["results"]["bindings"]

    def result(self, x, y, q, tpl):
        #self.request_execution(self.tpl % (y, q))
        return [r[x]["value"] for r in self.execution(tpl % (y, q))]

    def execution_query(self, query):
        x, q = query
        return self.tpl % (self.q_mark(x), q)

    def execution_result(self, query):
        x, q = query
        return self.result(x, self.q_mark(x), q, self.tpl)

    def counter(self, query):
        x, q = query
        y = 'count(%s) as %s' % (self.q_mark(x), self.q_mark(x))
        return self.result(x, y, q, self.count_tpl)[0]

    def literal(self, label, lang='en'):
        return '"%s"@%s' % (label, lang)

    def new_triple(self, s, p, o, q):
        return self.triple(self.q_mark(s), self.q_mark(p), self.q_mark(o)) + q

    def new_subject(self, query):
        p,o,q,v = query
        s = self.variable('s',v)
        return s, self.new_triple(s,p,o,q), v

    def new_predicate(self, query):
        s,o,q,v = query
        p = self.variable('p',v)
        return p, self.new_triple(s,p,o,q), v

    def new_object(self, query):
        s,p,q,v = query
        o = self.variable('o',v)
        return o, self.new_triple(s,p,o,q), v

    def new_subject_predicate(self, query):
        o,q,v = query
        s = self.variable('s',v)
        p = self.variable('p',v)
        return s,p,self.new_triple(s,p,o,q), v

    def new_predicate_object(self, query):
        s,q,v = query
        p = self.variable('p',v)
        o = self.variable('o',v)
        return p,o,self.new_triple(s,p,o,q), v

    def new_subject_object(self,query):
        p,q,v = query
        s = self.variable('s',v)
        o = self.variable('o',v)
        return s,o, self.new_triple(s,p,o,q), v

    def subject(self, s, query=''):
        if query:
            p,o,q,v = query
        else:
            v = {}
            p = self.variable('p',v)
            o = self.variable('o',v)
            q = ''
        return p, o, self.triple(self.uri(s), self.q_mark(p), self.q_mark(o)) + q, v

    def predicate(self, p, query=''):
        if query:
            s,o,q,v = query
        else:
            v = {}
            s = self.variable('s',v)
            o = self.variable('o',v)
            q = ''
        return s, o, self.triple(self.q_mark(s), self.uri(p), self.q_mark(o)) + q, v

    def object(self, o, query=''):
        if query:
            s,p,q,v = query
        else:
            v = {}
            s = self.variable('s',v)
            p = self.variable('p',v)
            q = ''
        return s,p, self.triple(self.q_mark(s), self.q_mark(p), self.uri(o)) + q, v

    def subject_predicate(self, s, p, query=''):
        if query:
            o,q,v = query
        else:
            v = {}
            o = self.variable('o',v)
            q = ''
        return o, self.triple(self.uri(s), self.uri(p), self.q_mark(o)) + q, v

    def predicate_object(self, p, o, query=''):
        if query:
            s,q,v = query
        else:
            v = {}
            s = self.variable('s',v)
            q = ''
        return s, self.triple(self.q_mark(s), self.uri(p), self.uri(o)) + q, v

    def subject_object(self, s, o, query=''):
        if query:
            p,q,v = query
        else:
            v = {}
            p = self.variable('p',v)
            q = ''
        return p, self.triple(self.uri(s), self.q_mark(p), self.uri(o)) + q, v

    def label(self, query=''):
        if query:
            s,q,v = query
        else:
            v = {}
            s = self.variable('s',v)
            q = ''
        o = self.variable('o',v)
        return s, o, self.triple(self.q_mark(s), self.uri(RDFS.label), self.q_mark(o)) + q, v

    def type(self, type, query=''):
        if query:
            s,q,v = query
        else:
            v = {}
            s = self.variable('s', v)
            q = ''
        return s, self.triple(self.q_mark(s), self.uri(RDF.type), self.uri(type)) + q, v

    def thing(self, query=''):
        if query:
            s,q,v = query
        else:
            v = {}
            s = self.variable('s',v)
            q = ''
        return s, self.triple(self.q_mark(s), self.uri(RDF.type), self.uri(OWL.Thing)) + q, v

    def domain(self, property):
        o,q,v = self.subject_predicate(property, RDFS.domain)
        query = o,q
        return self.execution_result(query)

    def range(self, property):
        o,q,v = self.subject_predicate(property, RDFS.range)
        query = o,q
        return self.execution_result(query)

    def subclass(self, c):
        s,q,v = self.predicate_object(RDFS.subClassOf, c)
        query = s,q
        return self.execution_result(query)

    def variable(self, x, v):
        l = v.setdefault(x,[])
        n = len(l)
        y = x + str(n)
        l.append(y)
        return y

    def triple(self, subject, predicate, object):
        return """ \n\t%s %s %s .""" % (subject, predicate, object)

    def union(self, triples):
        triples = map(lambda x: """{ %s }""" % x, triples)
        return "\n UNION ".join(triples)

    def lang_filter(self, variable, lang):
        return """ \n\tFILTER( lang(%s) = "%s") .""" % (self.q_mark(variable), lang)

    def regex_filter(self, variable, expression):
        return """\n\tFILTER regex(%s, "%s") .""" % (variable, expression)

    def lcase_filter(self, variable, expression):
        return """\n\tFILTER(lcase(str(%s)) = '%s') .""" % (variable, expression)

    def q_mark(self, x):
        return '?%s' % x

    def composeX(self, f, g):
        return lambda x: f(g(x))

    def composeXY(self,f, g):
        return lambda x,y:f(y,g(x))

    def uri(self, x):
        return '<%s>' % x


class EntityFeatures(BaseSPARQL):

    def __init__(self):
        BaseSPARQL.__init__(self)

    def entity_type(self, entity):
        query = 'type', self.triple(self.uri(entity), self.uri(RDF.type), self.q_mark('type'))
        return self.execution_result(query)

    def entity_category(self, entity):
        query = 'cat', self.triple(self.uri(entity), self.uri('http://purl.org/dc/terms/subject'), self.q_mark('cat'))
        return self.execution_result(query)

    def entity_abstract(self, entity):
        query = self.triple(self.uri(entity), self.uri('http://dbpedia.org/ontology/abstract'), self.q_mark('abstract'))
        query = 'abstract', query + self.lang_filter('abstract', 'en')
        return self.execution_result(query)[0]


    def entity_features(self, entity):
        return {
            'type':self.entity_type(entity),
            'category':self.entity_category(entity),
            'abstract':self.entity_abstract(entity)
        }


class NameSPARQL(BaseSPARQL):

    def __init__(self):
        BaseSPARQL.__init__(self)
        self.name = 'http://dbpedia.org/property/name'
        self.commonName = 'http://dbpedia.org/property/commonName'
        self.longName = 'http://dbpedia.org/ontology/longName'
        self.demonym = 'http://dbpedia.org/ontology/demonym'
        self.acronym = 'http://dbpedia.org/property/acronym'
        self.redirect_pages = 'http://dbpedia.org/ontology/wikiPageRedirects'
        self.disambiguation_pages = 'http://dbpedia.org/ontology/wikiPageDisambiguates'

    # def literal_mapping_property(self, segment, property):
    #     t0 = self.triple('?s', self.uri(RDF.type), self.uri(property))
    #     t1 = t0 + self.literal_mapping_label(segment)
    #     t2 = t0 + self.literal_mapping_title(segment)
    #     q = self.union([t1, t2])
    #     query = 's', q
    #     return self.execution_result(query)
    #
    # def literal_mapping_general_property(self, segment):
    #     return self.literal_mapping_property(segment, RDF.Property)
    #
    # def literal_mapping_datatype_property(self, segment):
    #     return self.literal_mapping_property(segment, OWL.DatatypeProperty)

    # def literal_mapping_object_property(self, segment):
    #     return self.literal_mapping_property(segment, OWL.ObjectProperty)

    def literal_mapping_class(self, segment):
        t0 = self.triple('?s', self.uri(RDF.type), self.uri(OWL.Class))
        t1 = t0 + self.literal_mapping_label(segment)
        t2 = t0 + self.literal_mapping_title(segment)
        q = self.union([t1, t2])
        query = 's', q
        return self.execution_result(query)

    def literal_mapping_lower(self, segment):
        t = self.triple('?s', self.uri(RDFS.label), '?q')
        return t + self.lcase_filter('?q', segment.lower())

    def wiki2dbpedia(self, wiki_uri):
        if wiki_uri.__contains__('https://en.wikipedia.org/wiki/'):
            wiki_uri = wiki_uri.replace('https:', 'http:')
            q = self.triple('?s', self.uri('http://xmlns.com/foaf/0.1/isPrimaryTopicOf'), self.uri(wiki_uri))
            query = 's', q
            return self.execution_result(query)
        return []

    def redirect_mapping(self, segment):
        t = self.triple('?x', self.uri(RDFS.label), self.literal(segment))
        return t + self.triple('?x', self.uri(self.redirect_pages), '?s')

    def check_redirect(self, dbr):
        q = self.triple(self.uri(dbr), self.uri(self.redirect_pages), '?s')
        query = 's', q
        return self.execution_result(query)

    # check dbpedia resource, no redirect page,
    def resource_filter(self, data):
        result = [d for d in data if d.__contains__('http://dbpedia.org/resource/')]
        # remove categories
        result = [d for d in result if not d.__contains__('http://dbpedia.org/resource/Category')]
        new_result = []
        for res in result:
            redirect = self.check_redirect(res)
            if redirect:
                new_result.append(redirect[0])
            else:
                new_result.append(res)
        return list(set(new_result))

    def entity_mapping(self, segment):
        # t0 = self.triple('?s', self.uri(RDF.type), self.uri(OWL.Thing))
        t1 = self.triple('?s', self.uri(RDFS.label), self.literal(segment))
        t2 = self.triple('?s', self.uri(RDFS.label), self.literal(segment.title()))
        t3 = self.redirect_mapping(segment)
        t4 = self.triple('?s', self.uri(self.name), self.literal(segment))
        t5 = self.triple('?s', self.uri(self.commonName), self.literal(segment))
        t6 = self.triple('?s', self.uri(self.longName), self.literal(segment))
        t7 = self.triple('?s', self.uri(self.demonym), self.literal(segment))
        t8 = self.triple('?s', self.uri(self.acronym), self.literal(segment))
        q = self.union([t1, t2, t3, t4, t5, t6, t7, t8])
        query = 's', q
        return self.resource_filter(self.execution_result(query))