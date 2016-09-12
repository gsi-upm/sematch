from rdflib import RDFS
from nltk.corpus import wordnet as wn
from sematch.sparql import BaseSPARQL
from sematch.utility import FileIO


class KnowledgeGraph(BaseSPARQL):

    def __init__(self):
        BaseSPARQL.__init__(self)
        self.synset_links_dic = FileIO.read_json_file("db/type-linkings.txt")
        self.yago_synset_dic = {data['yago_dbpedia']:data['offset'] for data in self.synset_links_dic}
        self.synset_links_dic = {data['offset']:data for data in self.synset_links_dic}

    def synset_link(self, synset):
        link = None
        try:
            link = self.synset_links_dic.get(self.offset(synset)).get('yago_dbpedia')
        except:
            print synset + " can't find any link!"
        finally:
            return link

    def offset(self, synset):
        return str(synset.offset() + 100000000)

    def offset2synset(self, offset):
        x = offset[1:]
        return wn._synset_from_pos_and_offset('n', int(x))

    def word_to_synsets(self, w):
        return wn.synsets(w, pos=wn.NOUN)

    def hyper_concept(self, synset):
        return synset.hypernyms()

    def hypo_concept(self, synset):
        return synset.hyponyms()

    def word_to_yago(self, w):
        yago_links = []
        for s in wn.synsets(w, pos=wn.NOUN):
            link = self.synset_link(s)
            if link:
                yago_links.append(link)
        return yago_links

    def word_to_dbpedia(self, w):
        dbpedia_links = []
        for s in wn.synsets(w, pos=wn.NOUN):
            link = self.synset_links_dic.get(self.offset(s)).get('dbpedia')
            if link:
                dbpedia_links.append(link)
        return dbpedia_links

    def entity_to_entity_N(self, cal=False, default=23628260):
        if cal:
            p,o,q,v = self.new_predicate_object(self.thing())
            query = o,q,v
            s,q,v = self.thing(query)
            query = p,q
            return int(self.counter(query))
        return default

    def synset_entity_count(self, synset):
        return self.entity_count(self.synset_link(synset))

    def entity_count(self, concept):
        s,q,v = self.composeX(self.thing, self.type)(concept)
        query = s,q
        return int(self.counter(query))

    def synset_coocurrence(self, c1, c2):
        return self.entity_type_coocurence(self.synset_link(c1), self.synset_link(c2))

    def entity_type_coocurence(self, c1, c2):
        s,q,v = self.composeXY(self.type, self.composeX(self.thing, self.type))(c1,c2)
        query = s,q
        return int(self.counter(query))

    def entity_N(self, cal=False, default=4298433):
        if cal:
            s,q,v = self.thing()
            query = s,q
            return int(self.counter(query))
        return default

    # select count(?p) where ?s1 is c1 . ?s2 is c2 . ?s1 ?p ?s2 or ?s2 ?p ?s1
    # the types of two subjects are known
    def type_coocurence_count(self, c1, c2):
        p,o,q,v = self.new_predicate_object(self.type(c1))
        query = o,q,v
        o,q,v = self.type(c2, query)
        query = p,q
        count_1 = self.counter(query)
        #print count_1
        s,p,q,v = self.new_subject_predicate(self.type(c1))
        query = s,q,v
        s,q,v = self.type(c2, query)
        query = p,q
        count_2 = self.counter(query)
        #print count_2
        return int(count_1) + int(count_2)


    #select count(?p) where ?s isa concept ?s ?p ?o or ?o ?p ?s
    def type_count(self, concept):
        p,o,q,v = self.composeX(self.new_predicate_object, self.type)(concept)
        query = o,q,v
        o,q,v = self.thing(query)
        query = p,q
        count_1 = self.counter(query)
        #print count_1
        s,p,q,v = self.composeX(self.new_subject_predicate, self.type)(concept)
        query = s,q,v
        s,q,v = self.thing(query)
        query = p,q
        count_2 = self.counter(query)
        #print count_2
        return int(count_1) + int(count_2)

    def type_of_things_labels(self, concept, lang='en'):
        s,o,q,v = self.composeX(self.label, self.composeX(self.thing, self.type))(concept)
        f = self.lang_filter(o, lang)
        query = o, q + f
        return self.execution_result(query)

    def type_of_things_query(self, concept, lang='en'):
        s,q,v = self.composeX(self.thing, self.type)(concept)
        query = s,q
        return self.execution_query(query)

    def type_of_things_resources(self, concept):
        s,q,v = self.composeX(self.thing, self.type)(concept)
        query = s,q
        return self.execution_result(query)

    def subclasses(self, s):
        link = self.link(s)
        if link:
            return self.sparql.subclass_types(link)
        return None

    def entity_type(self, resource):
        o,q,v = self.get_type(resource)
        query = o,q
        return self.execution_result(query)

    def entity_category(self, resource):
        o,q,v = self.get_category(resource)
        query = o, q
        categories = self.execution_result(query)
        cates = [c.replace('http://dbpedia.org/resource/Category:', '') for c in categories]
        cates = [c.lower().split('_') for c in cates]
        return cates

    def entity_classes(self, resource):
        types = self.entity_type(resource)
        type_synsets = []
        for t in types:
            if t in self.yago_synset_dic:
                type_synsets.append(self.yago_synset_dic[t])
            # if t.__contains__('http://dbpedia.org/ontology/'):
            #     print t
        type_synsets = [self.offset2synset(x) for x in type_synsets]
        return type_synsets
        #print types, categories

    # select count(?o) where s ?p ?o
    # subject is known
    def subject_count(self, s):
        p,o,q,v = self.subject(s)
        query = o,q
        return self.counter(query)

    # select count(?s) where ? ?p o
    # object is known
    def object_count(self, o):
        s,p,q,v = self.object(o)
        query = s,q
        return self.counter(query)

    # select count(?s) where ?s p ?o
    # predicate is known
    def predicate_count(self, p):
        s,o,q,v = self.predicate(p)
        query = s,q
        return self.counter(query)

    # select count(?o) where s p ?o
    # subject and predicate are both known
    def subject_predicate_count(self, s, p):
        o,q,v = self.subject_predicate(s,p)
        query = o,q
        return self.counter(query)

    # select count(?s) where ?s p o
    # predicate and object are both known
    def predicate_object_count(self, p, o):
        s,q,v = self.predicate_object(p,o)
        query = s,q
        return self.counter(query)

    # selfct count(?p) where s ?p o
    # subject and object are both known
    def subject_object_count(self, s, o):
        p,q,v = self.subject_object(s,o)
        query = p,q
        return self.counter(query)

    def dbpedia_resource_filter(self, resources):
        return filter(lambda x:str(x).__contains__('dbpedia'), resources)

    def segment_resources(self, segment):
        uri_resources_class = self.class_segment_resources(segment)
        uri_resources_data_property = self.data_property_segment_resources(segment)
        uri_resources_object_property = self.object_property_segment_resources(segment)
        uri_resources_entity = self.entity_segment_resources(segment)
        resources = {}
        if uri_resources_class:
            resources['T'] = uri_resources_class
        if uri_resources_data_property:
            resources['DP'] = uri_resources_data_property
        if uri_resources_object_property:
            resources['OP'] = uri_resources_data_property
        if uri_resources_entity:
            resources['E'] = uri_resources_entity
        return resources

    def entity_segment_resources(self, segment):
        resources = self.literal_mapping_entity(segment)
        resources = self.dbpedia_resource_filter(resources)
        return resources

    def data_property_segment_resources(self, segment):
        resources = self.literal_mapping_datatype_property(segment)
        return resources

    def object_property_segment_resources(self, segment):
        resources = self.literal_mapping_object_property(segment)
        return resources

    def class_segment_resources(self, segment):
        resources = self.literal_mapping_class(segment)
        resources = self.dbpedia_resource_filter(resources)
        yago = self.word_to_yago(segment)
        if yago:
            resources += yago
        return resources

    def domain_range_check(self, property):
        print 'domain', self.domain(property)
        print 'range',self.range(property)

    def associativity(self, e1, e2):
        '''
        measure the link based asscociatity between two entities in KG.
        :param e1:
        :param e2:
        :return:
        '''
        pass

