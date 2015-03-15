from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
import requests

class QueryExecution:

    """Automatically construct the SPARQL queries"""

    def __init__(self, url="http://dbpedia.org/sparql"):
        self.sparql = SPARQLWrapper(url)
        self.sparql.setReturnFormat(JSON)

    def execute(self, query):
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        return [result["x"]["value"] for result in results["results"]["bindings"]]

    def request_execution(self, query):
        params={
                "default-graph": "http://dbpedia.org",
                "query": query,
                "debug": "on",
                "format": "application/json",
                "timeout": 30000,
            }
        result = requests.get('http://dbpedia.org/sparql',params=params)
        print result.url
        return result.text

class GPS:

    def __init__(self):
        self.sparql_tpl = """SELECT DISTINCT ?x WHERE {\n\t%s\n}\nGROUP BY ?x"""
        self.str_rdftype = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'

    def gen_rdftype(self, t):
        return """?x %s <%s>""" % (self.str_rdftype, t)

    def rdftype(self,t):
        if type(t) is list:
            return self.type_union(t)
        else:
            return self.gen_rdftype(t)

    def query(self, name, t, e):
        return self.sparql_tpl % self.gpc(name)(t,e)

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
        self.split_n = 20
        self.gps = GPS()

    @staticmethod
    def chunks(l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

    @staticmethod
    def remove_duplicates(lst):
        return list(set(lst))

    def query(self, gpc, t, e):
        return self.gps.query(gpc,t,e)

    def run_gpc(self, gpc, types, e):
        results = []
        for t in Engine.chunks(types, self.split_n):
            results += self.sparql.execute(self.query(gpc,t,e))
        return Engine.remove_duplicates(results)

    def run(self, gpcs, types, e):
        results = []
        for gpc in gpcs:
            results += self.run_gpc(gpc, types, e)
        return Engine.remove_duplicates(results)


