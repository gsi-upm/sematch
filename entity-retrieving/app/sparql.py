from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON

class AutoQuery:
    """Automatically construct the SPARQL queries"""

    def __init__(self, url="http://dbpedia.org/sparql"):
        self.sparql = SPARQLWrapper(url)
        self.sparql.setReturnFormat(JSON)
        self.type = """{?subject rdf:type <%s>}"""
        self.tpl_1 = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    SELECT DISTINCT ?subject ?relation WHERE {
    %s.
    ?subject ?relation <%s>.
    } GROUP BY ?subject
    """
        self.tpl_2 = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    SELECT DISTINCT ?subject ?relation WHERE {
    %s.
    ?subject ?relation1 ?someObject.
    ?someObject ?relation2 <%s>.
    } GROUP BY ?subject
    """
        
    def execute_query(self, query, sim, type):
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        resources = []
        for result in results["results"]["bindings"]:
            res = {}
            res['link'] = result["subject"]["value"].replace(\
                "http://dbpedia.org/resource/","http://en.wikipedia.org/wiki/")
            res['name'] = result["label"]["value"]
            res['abstract'] = result["abstract"]["value"]
            res['sim'] = sim
            res['type'] = type
            resources.append(res)
        return resources


    def auto_query(self, types, country):
        type_query = ""
        for i in range(len(types)-1):
            s = self.type % types[i]
            s += " UNION "
            type_query += s
        s = self.type % types[len(types)-1]
        type_query += s
        query = self.tpl_1 % (type_query, country)
        print query
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        response = {}
        for result in results["results"]["bindings"]:
            relation = result["relation"]["value"]
            group = response.setdefault(relation, [])
            group.append(result["subject"]["value"])
        response_json = []
        for key, value in response.iteritems():
            obj = {}
            obj['relation'] = key
            obj['resources'] = value
            response_json.append(obj)
        return response_json
