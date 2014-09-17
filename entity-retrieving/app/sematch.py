from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
import json
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic


#read json file
def read_json_file(name):
    data = []
    with open(name,'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

class WordNetLD:

    def __init__(self):
        self.synsets_list = list(wn.all_synsets())
        self.synset_to_id = { s:s.offset for s in self.synsets_list }
        self.brown_ic = wordnet_ic.ic('ic-brown.dat')
        self.sem_hub = read_json_file("semantic-hub.txt")
        self.sem_hub = {data['offset']:data for data in self.sem_hub}

    def add_obj(self, slist, synset, sim):
        obj = {}
        obj['simbol'] = str(synset)
        obj['definition'] = synset.definition
        obj['offset'] = str(self.synset_to_id[synset]+100000000)
        obj['sim'] = sim
        slist.append(obj)

    def similarity(self, syn1, syn2, simType):
        if simType == '1':
            return syn1.wup_similarity(syn2)
        if simType == '2':
            return syn1.path_similarity(syn2)
        if simType == '3':
            return syn1.lch_similarity(syn2)
        if simType == '4':
            return syn1.res_similarity(syn2, self.brown_ic)
        if simType == '5':
            return syn1.jcn_similarity(syn2, self.brown_ic)
        if simType == '6':
            return syn1.lin_similarity(syn2, self.brown_ic)

    #use wn built in search to get synsets using lemma search,
    #and expand the synsets with its children and parent and siblings.
    def search_synsets(self, query, simType):
        synsets = wn.synsets(query, pos=wn.NOUN)
        synsets_list = []
        for s in synsets:
            self.add_obj(synsets_list, s, 1.0)
            for h in s.hyponyms():
                sim = self.similarity(s, h, simType)
                self.add_obj(synsets_list, h, sim)
            for h in s.hypernyms():
                sim = self.similarity(s, h, simType)
                self.add_obj(synsets_list, h, sim)
                for son in h.hyponyms():
                    sim = self.similarity(s, son, simType)
                    self.add_obj(synsets_list, son, sim)
        return synsets_list

    def search_types(self, feature, simType, threshold):
        synsets = self.search_synsets(feature, simType)
        #filter by similarity threshold
        synsets = [synset for synset in synsets if synset['sim'] >= float(threshold)]
        synsets_map = {}
        for synset in synsets:
            synsets_map[synset['offset']] = synset
        for key, value in synsets_map.iteritems():
            value['link'] = []
            feature = self.sem_hub[key]
            if feature.get('dbpedia'):
                value['link'].append(feature['dbpedia'])
            if feature.get('yago_dbpedia'):
                value['link'].append(feature['yago_dbpedia'])
        synsets = [value for key, value in synsets_map.iteritems() if value['link']]
        return synsets

    def type_links(self, feature, simType, threshold):
        types = self.search_types(feature,simType,threshold)
        type_links = []
        for t in types:
            type_links += t['link']
        return type_links



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
    ?subject ?relation ?someObject.
    ?someObject ?relation2 <%s>.
    } GROUP BY ?subject
    """
        self.tpl_3 = """
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
    <%s> ?relation ?subject.
    } GROUP BY ?subject
    """
        self.tpl_4 = """
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
    <%s> ?relation ?someObject.
    ?someObject ?relation2 ?subject.
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


    def auto_query(self, types, entity, tpl):
        type_query = ""
        for i in range(len(types)-1):
            s = self.type % types[i]
            s += " UNION "
            type_query += s
        s = self.type % types[len(types)-1]
        type_query += s
        query = tpl % (type_query, entity)
        #print query
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

    def query(self, types, entity):
        results_1 = self.auto_query(types, entity, self.tpl_1)
        results_2 = self.auto_query(types, entity, self.tpl_2)
        results_3 = self.auto_query(types, entity, self.tpl_3)
        results_4 = self.auto_query(types, entity, self.tpl_4)
        results = [] + results_1
        results += results_2
        results += results_3
        results += results_4
        resources = []
        for res in results:
            resources += res['resources']
        return list(set(resources))

