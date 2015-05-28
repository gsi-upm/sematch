from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
from QueryProcessing import Query
from LODLinkers import EntityLinkers
from LODLinkers import SynsetLinker
from Utility import Configuration
import requests
import rdflib

class QueryExecution:

    def __init__(self, url="http://dbpedia.org/sparql"):
        self.url = url
        self.sparql = SPARQLWrapper(url)
        self.sparql.setReturnFormat(JSON)

    def execute(self, name, query):
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        return self.qgp(name)(results)

    def teq(self, results):
        """type entity query"""
        query_results = []
        for result in results["results"]["bindings"]:
            obj = {}
            obj['uri'] = result["x"]["value"]
            obj['relation'] = result["rel"]["value"]
            obj['label'] = result["l"]["value"]
            obj['comments'] = result["c"]["value"]
            query_results.append(obj)
        return {obj['uri']:obj for obj in query_results}

    def qgp(self, name):
        def function(results):
            return getattr(self, name)(results)
        return function

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

class QueryGraphPattern:

    def gen_rdftype(self, t):
        return """?x <%s> <%s>""" % (rdflib.RDF.type, t)

    def rdftype(self,t):
        if type(t) is list:
            return self.type_union(t)
        else:
            return self.gen_rdftype(t)

    def lang_filter(self, variable, lang):
        return """ \n\tFILTER( lang(%s) = "%s") .""" % (variable, lang)

    def type_entity_query(self, name, t, e):
        tpl = """SELECT DISTINCT ?x ?rel ?l ?c WHERE {\n\t%s\n}\nGROUP BY ?x"""
        q = self.gpc(name)(t,e)
        q += """ \n\t?x <%s> ?l .""" % rdflib.RDFS.label
        q += """ \n\t?x <%s> ?c .""" % rdflib.RDFS.comment
        q += """ \n\t?p <%s> ?rel .""" % rdflib.RDFS.label
        q += """ \n\tFILTER( lang(?rel) = "en" and lang(?l) = "en" and lang(?c) = "en" ) ."""
        return tpl % q

    def entity_query(self, e):
        pass

    def entity_literal_query(self, e, p):
        tpl = """SELECT DISTINCT ?o WHERE {\n\t%s\n}"""
        q = self.gpc0(e,p)
        q += self.lang_filter('?o','en')
        return tpl % q

    def entity_entity_query(self, e1, e2):
        pass

    def gpc0(self, e, p):
        return """\n\t<%s> <%s> ?o .""" % (e, p)

    def gpc1(self, t, e):
        return self.rdftype(t) + """ .\n\t?x ?p <%s> .""" % e

    def gpc2(self, t, e):
        return self.rdftype(t) + """ .\n\t<%s> ?p ?x.""" % e

    def gpc3(self, t, e):
        return self.rdftype(t) + """ .\n\t?x ?p1 ?y.\n\t?y ?p2 <%s>.""" %e

    def gpc4(self, t, e):
        return self.rdftype(t) + """ .\n\t?x ?p1 ?y.\n\t<%s> ?p2 ?y.""" %e

    def gpc5(self, t, e):
        return self.rdftype(t) + """ .\n\t?y ?p1 ?x.\n\t?y ?p2 <%s>.""" %e

    def gpc6(self, t, e):
        return self.rdftype(t) + """ .\n\t?y ?p1 ?x.\n\t<%s> ?p2 ?y.""" %e

    def gpc(self, name):
        def function(t, e):
            return getattr(self, name)(t,e)
        return function

    def type_union(self, types):

        if len(types) == 1:
            return self.gen_rdftype(types[0])
        else:
            rdftypes = map(self.gen_rdftype, types)
            rdftypes = map(lambda x: """{ %s }""" % x, rdftypes)
            return "\n UNION ".join(rdftypes)

class Engine:

    def __init__(self):
        self.sparql = QueryExecution()
        self.entityLinker = EntityLinkers('sparqllinker')
        self.typeLinker = SynsetLinker()
        self.query_processor = Query()
        self.config = Configuration()
        self.gpcs = ['gpc1','gpc2']
        self.split_n = 5
        self.qgp = QueryGraphPattern()

    @staticmethod
    def chunks(l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    @staticmethod
    def remove_list_duplicates(lst):
        return list(set(lst))

    def type_entity_query_construction(self, query):
        type_links = self.types(query)
        entity_links = self.entities(query)
        queries = []
        for e in entity_links:
            for gpc in self.gpcs:
                for t in Engine.chunks(type_links, self.split_n):
                    queries.append(self.qgp.type_entity_query(gpc,t,e))
        return queries

    def entity_literal_query_construction(self, e, p):
        pass

    def search_types(self, query, sim, th):
        return self.typeLinker.searching(query, sim, th)

    def sparql_execution(self, name, queries):
        results_dic = {}
        for q in queries:
            results = self.sparql.execute(name, q)
            for key in results.keys():
                if key not in results_dic:
                    results_dic[key] = results[key]
        return [results_dic[key] for key in results_dic.keys()]

    def types(self, query):
        return self.typeLinker.linking(query)

    def entities(self, query):
        return self.entityLinker.linking(query)

    def search(self, query):
        queries = self.type_entity_query_construction(query)
        return self.sparql_execution('teq', queries)

