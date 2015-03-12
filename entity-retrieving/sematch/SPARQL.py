from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON

templates = {
    1:"""
            SELECT DISTINCT ?subject ?relation WHERE {
            {
                %s.
                ?subject ?relation <%s>.
            }
            UNION
            {
                %s.
                <%s> ?relation ?subject.
            }
            } GROUP BY ?subject
        """,
    2:"""
            SELECT DISTINCT ?subject ?relation WHERE {
            {
                %s.
                ?subject ?relation ?someObject.
                ?someObject ?relation2 <%s>.
            }
            UNION
            {
                %s.
                <%s> ?relation ?someObject.
                ?someObject ?relation2 ?subject.
            }
            } GROUP BY ?subject
        """,
    3:"""
            SELECT DISTINCT ?relation ?subject WHERE {
            {
                <%s> ?relation ?subject.
            }
            UNION
            {
                ?subject ?relation <%s>.
            }
            } GROUP BY ?subject
        """,
    4:"""
            SELECT DISTINCT ?subject ?relation WHERE {
            {
                %s.
                ?subject ?relation ?someObject.
                ?someObject ?relation2 <%s>.
            }
            UNION
            {
                %s.
                ?subject ?relation ?someObject.
                <%s> ?relation2 ?someObject.
            }
            UNION
            {
                %s.
                <%s> ?relation ?someObject.
                ?someObject ?relation2 ?subject.
            }
            UNION
            {
                %s.
                <%s> ?relation ?someObject.
                ?subject ?relation2 ?someObject.
            }
            } GROUP BY ?subject
        """
}

class AutoQuery:

    """Automatically construct the SPARQL queries"""

    def __init__(self, url="http://dbpedia.org/sparql"):
        self.sparql = SPARQLWrapper(url)
        self.sparql.setReturnFormat(JSON)
        self.type = """{?subject rdf:type <%s>}"""

    def chunks(self, l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i+n]

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


    def retrieve_entity_obj(self, resource):
        query = self.tpl_3 % (resource, resource)
        print query
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        entity = {}
        entity['resource'] = resource
        entity['data'] = []
        for result in results["results"]["bindings"]:
            entity['data'].append((result['relation']['value'], \
                result['subject']['value']))
        return entity

    def auto_types(self, types):
        if len(types) == 1:
            return """?subject rdf:type <%s>""" % types[0]
        else:
            type_query = ""
            for i in range(len(types)-1):
                s = self.type % types[i]
                s += " UNION "
                type_query += s
            s = self.type % types[len(types)-1]
            type_query += s
            return type_query

    def auto_query(self, query):
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

    def resources(self, results):
        resources = []
        for res in results:
            resources += res['resources']
        return list(set(resources))

    def query(self, types, entity, level):
        results = []
        if level == 1:
            for types_splited in self.chunks(types, 10):
                type_query = self.auto_types(types_splited)
                query = self.tpl_1 % (type_query, entity, type_query, entity)
                results += self.auto_query(query)
        elif level == 2:
            for types_splited in self.chunks(types, 10):
                type_query = self.auto_types(types_splited)
                query = self.tpl_2 % (type_query, entity, type_query, entity)
                results += self.auto_query(query)
        return self.resources(results)