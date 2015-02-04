from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from collections import deque
import argparse
import json

def read_json_file(name):
    data = []
    with open(name,'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def save_json_file(name, data):
    with open(name, 'w') as f:
        for d in data:
            json.dump(d, f)
            f.write("\n")

def append_json_file(name, data):
    with open(name, 'a') as f:
        for d in data:
            json.dump(d, f)
            f.write("\n")

def save_list_file(name, data):
    with open(name,'w') as f:
        for d in data:
            f.write(d)
            f.write('\n')

def read_list_file(name):
    with open(name,'r') as f:
        data = [line.strip() for line in f]
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

    def synset_expand(self, queue, synset):
        for h in synset.hyponyms():
            queue.append(h)
        for h in synset.hypernyms():
            queue.append(h)

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
            if self.sem_hub.get(key):
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
        """
        self.tpl_2 = """
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
        """
        self.tpl_3 = """
            SELECT DISTINCT ?relation ?subject WHERE {
            {
                <%s> ?relation ?subject.
            }
            UNION
            {
                ?subject ?relation <%s>.
            }
            } GROUP BY ?subject
        """
        self.tpl_5 = """
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


if __name__ == "__main__":
    wordnet = WordNetLD()
    autoQuery = AutoQuery()
    parser = argparse.ArgumentParser(description="Retrieving entities of given entity type based on another entity\
     which has some relation with the required entities")
    parser.add_argument("feature", help="entity type")
    parser.add_argument("entity", help="some entity such as country author")
    args = parser.parse_args()
    types = wordnet.type_links(args.feature, 1, 0.5)
    retrieved = autoQuery.query(types, args.entity)
    save_list_file("resource.dat", retrieved)
