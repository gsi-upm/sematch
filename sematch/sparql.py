from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, RDFS, OWL
import requests

class BaseSPARQL:

    def __init__(self, url="http://dbpedia.org/sparql"):
        self._url = url
        self._sparql = SPARQLWrapper(url)
        self._sparql.setReturnFormat(JSON)
        self._tpl = """SELECT DISTINCT %s WHERE {\n\t%s\n}"""
        self._count_tpl = """SELECT %s WHERE {\n\t%s\n}"""


    def request_execution(self, query):
        params={
                "default-graph": "http://dbpedia.org",
                "query": query,
                "debug": "on",
                "format": "application/json",
                "timeout": 30000,
            }
        result = requests.get(self._url, params=params)
        return result.text

    def execution(self, query):
        #print query
        self._sparql.setQuery(query)
        results = self._sparql.query().convert()
        #print results
        return results["results"]["bindings"]

    #SELECT DISTINCT ?x WHERE is query line containing variables
    #{?s ?p ?o . ?s2 ?p2 ?o } is triples line of query

    def execution_template(self, variable, query, triples, template):
        """retrieve query results from sparql end point"""
        return [r[variable]["value"] for r in self.execution(template % (query, triples))]

    def create_query(self, variable, triples):
        """create a sparql query in string based on template, variable and triples"""
        return self._tpl % (self.q_mark(variable), triples)

    def resource_query(self, variable, triples):
        """execute query to return resources"""
        return self.execution_template(variable, self.q_mark(variable), triples, self._tpl)

    def count_query(self, variable, triples):
        """execute query to return counts """
        query = 'count(%s) as %s' % (self.q_mark(variable), self.q_mark(variable))
        return self.execution_template(variable, query, triples, self._count_tpl)[0]

    def literal(self, label, lang='en'):
        return '"%s"@%s' % (label, lang)

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

    def composeXY(self, f, g):
        return lambda x, y: f(y, g(x))

    def uri(self, x):
        return '<%s>' % x

    def new_triple(self, v, triple):
        def function(triple_type, x, y):
            v2, triple2 = triple_type(x, y, v)
            return v2, triple + triple2
        return function

    def v_triple(self, s, p, o):
        """unknown s, p, o"""
        return self.triple(self.q_mark(s), self.q_mark(p), self.q_mark(o))

    def s_triple(self, s, p, o):
        """known s, unknown p, o"""
        return self.triple(self.uri(s), self.q_mark(p), self.q_mark(o))

    def p_triple(self, s, p, o):
        """known p, unknown s, o"""
        return self.triple(self.q_mark(s), self.uri(p), self.q_mark(o))

    def o_triple(self, s, p, o):
        """known o, unknown s, p"""
        return self.triple(self.q_mark(s), self.q_mark(p), self.uri(o))

    def sp_triple(self, s, p, v):
        """given known subject and predicate, object is a variable"""
        return v, self.triple(self.uri(s), self.uri(p), self.q_mark(v))

    def po_triple(self, p, o, v):
        """given known predicate and object, subject is a variable"""
        return v, self.triple(self.q_mark(v), self.uri(p), self.uri(o))

    def so_triple(self, s, o, v):
        """given known subject and object, predicate is a variable"""
        return v, self.triple(self.uri(s), self.q_mark(v), self.uri(o))

    def label(self, s, lang='en'):
        """query the lable of a resource"""
        return self.resource_query(*self.new_triple('o',
               self.lang_filter('o', lang))(self.sp_triple, s, RDFS.label))

    def thing(self, s):
        return self.po_triple(RDF.type, OWL.Thing, s)

    def type_of_thing(self, concept, v):
        """given the type such as movie, return a list of movien entities"""
        return self.new_triple(*self.thing(v))(self.po_triple, RDF.type, concept)

    def domain(self, property):
        return self.resource_query(*self.sp_triple(property, RDFS.domain, 'o'))

    def range(self, property):
        return self.resource_query(*self.sp_triple(property, RDFS.range, 'o'))

    def subclass(self, concept):
        return self.resource_query(*self.po_triple(RDFS.subClassOf, concept, 's'))


class EntityFeatures(BaseSPARQL):

    def __init__(self):
        BaseSPARQL.__init__(self)

    def type(self, entity):
        return self.resource_query(*self.sp_triple(entity, RDF.type, 'o'))

    def category(self, entity):
        return self.resource_query(*self.sp_triple(entity,
                                'http://purl.org/dc/terms/subject', 'o'))

    def abstract(self, entity, lang='en'):
        return self.resource_query(*self.new_triple('o',
            self.lang_filter('o', lang))(self.sp_triple, entity,
                'http://dbpedia.org/ontology/abstract'))

    def features(self, entity):
        return {
            'type':self.type(entity),
            'category':self.category(entity),
            'abstract':self.abstract(entity)[0]
        }

class StatSPARQL(BaseSPARQL):

    def __init__(self):
        BaseSPARQL.__init__(self)

    def entity_N(self, cal=False, default=4298433):
        """select count(?s) where ?s is thing"""
        if cal:
            return int(self.count_query(*self.thing('s')))
        return default

    def concept_freq(self, concept):
        """select count(?s) where ?s is concept. ?s is thing"""
        return self.count_query(*self.type_of_thing(concept, 's'))

    # select count(?p) where ?s1 is c1 . ?s2 is c2 . ?s1 ?p ?s2 or ?s2 ?p ?s1
    # the types of two subjects are known
    def concept_coocurence(self, c1, c2):
        s1, t1 = self.type_of_thing(c1, 's1')
        s2, t2 = self.type_of_thing(c2, 's2')
        t3 = self.v_triple(s1, 'p', s2)
        t4 = self.v_triple(s2, 'p', s1)
        count_1 = self.count_query('p', t1 + t2 + t3)
        count_2 = self.count_query('p', t1 + t2 + t4)
        return int(count_1) + int(count_2)

    # select count(?p) where ?s is concept ?s ?p ?o or ?o ?p ?s
    def concept_relation(self, concept):
        s1, t1 = self.type_of_thing(concept, 's1')
        s2, t2 = self.thing('s2')
        t3 = self.v_triple(s1, 'p', s2)
        t4 = self.v_triple(s2, 'p', s1)
        count_1 = self.count_query('p', t1 + t2 + t3)
        count_2 = self.count_query('p', t1 + t2 + t4)
        return int(count_1) + int(count_2)

    # select count(?p) where s ?p ?o or ?o ?p s
    # subject is known
    def entity_relation(self, entity):
        s1, t1 = self.thing('s1')
        t2 = self.s_triple(entity, 'p', s1)
        t3 = self.o_triple(s1, 'p', entity)
        count_1 = self.count_query('p', t1 + t2)
        count_2 = self.count_query('p', t1 + t3)
        return int(count_1) + int(count_2)


class NameSPARQL(BaseSPARQL):

    """query resource through names"""

    def __init__(self):
        BaseSPARQL.__init__(self)
        self.name = 'http://dbpedia.org/property/name'
        self.commonName = 'http://dbpedia.org/property/commonName'
        self.longName = 'http://dbpedia.org/ontology/longName'
        self.demonym = 'http://dbpedia.org/ontology/demonym'
        self.acronym = 'http://dbpedia.org/property/acronym'
        self.redirect_pages = 'http://dbpedia.org/ontology/wikiPageRedirects'
        self.disambiguation_pages = 'http://dbpedia.org/ontology/wikiPageDisambiguates'

    def wiki2dbpedia(self, wiki_uri):
        if wiki_uri.__contains__('https://en.wikipedia.org/wiki/'):
            wiki_uri = wiki_uri.replace('https:', 'http:')
            q = self.triple('?s', self.uri('http://xmlns.com/foaf/0.1/isPrimaryTopicOf'), self.uri(wiki_uri))
            return self.resource_query('s', q)
        return []

    def redirect(self, name):
        t = self.triple('?x', self.uri(RDFS.label), self.literal(name))
        return t + self.triple('?x', self.uri(self.redirect_pages), '?s')

    def check_redirect(self, dbr):
        return self.resource_query(*self.sp_triple(dbr, self.redirect_pages, 's'))

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

    def name2entities(self, name):
        s, t0 = self.thing('s')
        t1 = self.triple('?s', self.uri(RDFS.label), self.literal(name))
        t2 = self.triple('?s', self.uri(RDFS.label), self.literal(name.title()))
        t3 = self.redirect(name)
        t4 = self.triple('?s', self.uri(self.demonym), self.literal(name))
        t5 = self.triple('?s', self.uri(self.acronym), self.literal(name))
        t = self.union([t1, t2, t3, t4, t5])
        return self.resource_filter(self.resource_query(s, t + t0))

    def name2entities_expand(self, name):
        s, t0 = self.thing('s')
        t1 = self.triple('?s', self.uri(self.name), self.literal(name))
        t2 = self.triple('?s', self.uri(self.commonName), self.literal(name))
        t3 = self.triple('?s', self.uri(self.longName), self.literal(name))
        t = self.union([t1, t2, t3])
        return self.resource_filter(self.resource_query(s, t+t0))


class QueryGraph(BaseSPARQL):

    def __init__(self):
        BaseSPARQL.__init__(self)

    def type_entity_query(self, concepts, entity):
        """
        Construct type entity queries.
        Some more possible patterns.
        ?x ?p1 ?y. ?y ?p2 <%s>.
        ?x ?p1 ?y. <%s> ?p2 ?y.
        ?y ?p1 ?x. ?y ?p2 <%s>
        ?y ?p1 ?x. <%s> ?p2 ?y.
        :param concepts:
        :param entity:
        :return:
        """
        triples = map(lambda x: self.po_triple(RDF.type, x, 's'), concepts)
        t1 = [t for v, t in triples]
        t1 = self.union(t1)
        t2 = self.s_triple(entity, 'p', 's')
        t3 = self.o_triple('s', 'p', entity)
        res1 = self.resource_query('s', t1 + t2)
        res2 = self.resource_query('s', t1 + t3)
        return res1 + res2
