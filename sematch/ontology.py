from rdflib import RDF, RDFS, OWL
from sematch.utility import FileIO
import rdflib

class DBpedia:

    def __init__(self, src='models/dbpedia_2015-04.owl'):
        self.graph = rdflib.Graph()
        self.graph.parse(FileIO.filename(src))
        self.root = 'http://www.w3.org/2002/07/owl#Thing'
        self.classes = [s for s in self.graph.subjects(RDF.type, OWL.Class)]
        self.o_properties = [s for s in self.graph.subjects(RDF.type, OWL.ObjectProperty)]
        self.d_properties = [s for s in self.graph.subjects(RDF.type, OWL.DatatypeProperty)]
        self.uri2class = {c.toPython():c for c in self.classes}
        self.uri2class[self.root] = rdflib.URIRef(self.root)
        self.class_labels = [self.token(c) for c in self.classes]

    def superClass(self, x):
        return [o.toPython() for s, v, o in self.graph.triples((self.uri2class[x], RDFS.subClassOf, None))]

    def subClass(self, x):
        return [s.toPython() for s, v, o in self.graph.triples((None, RDFS.subClassOf, self.uri2class[x]))]

    def allSubClass(self, x, subList = []):
        for sub in self.subClass(x):
            subList.append(sub)
            self.allSubClass(sub, subList)
        return subList

    def allSuperClass(self, x, superList = []):
        for super in self.superClass():
            superList.append(super)
            self.allSuperClass(super, superList)
        return superList

    def siblingsClass(self, x):
        siblings = []
        for parent in self.superClass(x):
            for child in self.subClass(parent):
                if child != x:
                    siblings.append(child)
        return siblings

    def token(self, x):
        t = [o for o in self.graph.objects(x, RDFS.label) if o.language=='en']
        if t == []:
            return None
        return t[0].toPython()

    def lexicon(self, tag, lst):
        return [(self.token(x), x.n3(), tag) for x in lst if self.token(x)]

    def range(self, p):
        return [o for o in self.graph.objects(p, RDFS.range)]

    def domain(self, p):
        return [o for o in self.graph.objects(p, RDFS.domain)]



# class Matcher:
#
#     def __init__(self):
#         self.sim = Similarity()
#         self.string_sim_th = 0.9
#         self.ngram = 5
#
#     def token_filter(self, tokens):
#         tags = self.token_pos_split(tokens,1)
#         if len(tokens) == 1:
#             if tags[0] not in ['NN','NNS','NNP','NNPS','VB','VBD','VBG','VBN','VBP','VBZ']:
#                 return False
#         for t in tags:
#             if t in ['WRB','WDT', 'WP', 'WP$','CD']:
#                 return False
#         return True
#
#     #i=0, tokens; i=1 pos
#     def token_pos_split(self, tokens, i=0):
#         return [token[i] for token in tokens]
#
#     def lexicons(self, query):
#         tokens_lst = self.segmentation(query)
#         tokens_lst = filter(self.token_filter, tokens_lst)
#         matchers = [self.instance_matching, self.class_matching, self.property_matching]
#         return reduce(lambda x,y:x+y, [self.matching(tokens_lst, m) for m in matchers])
#
#     def matching(self, tokens_lst, matcher):
#         split = self.token_pos_split
#         matches = [matcher(split(tokens)) for tokens in tokens_lst if matcher(split(tokens))]
#         if matches:
#             matches = reduce(lambda x,y:x+y, matches)
#         return matches
#
#     def sim_string(self, tokens, lex):
#         x = ''.join(tokens).lower().decode('utf-8')
#         y = lex[0].replace(' ','').lower()
#         return self.sim.string(x,y) > self.string_sim_th
#
#     def lex_form(self, tokens, lex):
#         return (' '.join(tokens), lex[1], lex[2])
#
#     def token_matching(self, tokens, lex, sim, lexicon):
#         return [lex(tokens, l) for l in lexicon if sim(tokens, l)]
#
#     def class_matching(self, tokens):
#         classes = self.ontology.T_Lexicon()
#         return self.token_matching(tokens, self.lex_form, self.sim_string, classes)
#
#     def property_matching(self, tokens):
#         properties = self.ontology.P_Lexicon()
#         return self.token_matching(tokens, self.lex_form, self.sim_string, properties)
