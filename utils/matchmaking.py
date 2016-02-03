from numpy import linalg as LA
from nltk.corpus import wordnet_ic
from scipy.stats import spearmanr
from scipy.stats import pearsonr
from scipy.stats import kendalltau
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import RDF, RDFS, OWL
import networkx as nx
import numpy as np
import random
import math
import csv

#concepts for testing
concepts = ['Java','Scala','C','C++','Objective-C','JavaScript','Python','Nodejs','Spring','Django','IOS','Android']

#manual alignment of concepts in DBpedia Knowledge Graph
dbpedia = {'Java':'http://dbpedia.org/resource/Java_(programming_language)',
           'Scala':'http://dbpedia.org/resource/Scala_(programming_language)',
           'C':'http://dbpedia.org/resource/C_(programming_language)',
           'C++':'http://dbpedia.org/resource/C++',
           'Objective-C':'http://dbpedia.org/resource/Objective-C',
           'JavaScript':'http://dbpedia.org/resource/JavaScript',
           'Python':'http://dbpedia.org/resource/Python_(programming_language)',
           'Nodejs':'http://dbpedia.org/resource/Node.js',
           'Spring':'http://dbpedia.org/resource/Spring_Framework',
           'Django':'http://dbpedia.org/resource/Django_(web_framework)',
           'IOS':'http://dbpedia.org/resource/IOS',
           'Android':'http://dbpedia.org/resource/Android_(operating_system)'}

#concepts are constructed in graph, a simple implementation of skos.
#narrower is similar to sub_class, and broader is similar to sub_class_of
G_taxonomy = nx.DiGraph()
G_taxonomy.add_nodes_from(['Dev', 'Programming', 'Framework', 'Java-Family', 'C-Family', 'Web', 'Mobile'])
G_taxonomy.add_nodes_from(concepts)
G_taxonomy.add_edges_from([('Dev','Programming'),('Dev','Framework')], t='narrower')
G_taxonomy.add_edges_from([('Programming','Dev'),('Framework','Dev')], t='broader')
G_taxonomy.add_edges_from([('Programming','Java-Family'),('Programming','C-Family')], t='narrower')
G_taxonomy.add_edges_from([('Programming','JavaScript'),('Programming','Python')], t='narrower')
G_taxonomy.add_edges_from([('Java-Family','Programming'),('C-Family','Programming')], t='broader')
G_taxonomy.add_edges_from([('JavaScript','Programming'),('Python','Programming')], t='broader')
G_taxonomy.add_edges_from([('Framework','Web'),('Framework','Mobile')], t='narrower')
G_taxonomy.add_edges_from([('Web','Framework'),('Mobile','Framework')], t='broader')
G_taxonomy.add_edges_from([('Java-Family','Java'),('Java-Family','Scala')], t='narrower')
G_taxonomy.add_edges_from([('Java','Java-Family'),('Scala','Java-Family')], t='broader')
G_taxonomy.add_edges_from([('C-Family','C'),('C-Family','C++'),('C-Family','Objective-C')], t='narrower')
G_taxonomy.add_edges_from([('C','C-Family'),('C++','C-Family'),('Objective-C','C-Family')], t='broader')
G_taxonomy.add_edges_from([('Web','Nodejs'),('Web','Spring'),('Web','Django')], t='narrower')
G_taxonomy.add_edges_from([('Nodejs','Web'),('Spring','Web'),('Django','Web')], t='broader')
G_taxonomy.add_edges_from([('Mobile','IOS'),('Mobile','Android')], t='narrower')
G_taxonomy.add_edges_from([('IOS','Mobile'),('Android','Mobile')], t='broader')

G_skos = nx.DiGraph(G_taxonomy)
G_skos.add_edges_from([('Java-Family','Spring'),('Spring','Java-Family')], t='related')
G_skos.add_edges_from([('Java','Android'),('Android','Java')], t='related')
G_skos.add_edges_from([('JavaScript','Nodejs'),('Nodejs','JavaScript')], t='related')
G_skos.add_edges_from([('Python','Django'),('Django','Python')], t='related')
G_skos.add_edges_from([('Objective-C','IOS'),('IOS','Objective-C')], t='related')

class SPARQL:

    def __init__(self, url="http://dbpedia.org/sparql"):
        self.url = url
        self.sparql = SPARQLWrapper(url)
        self.sparql.setReturnFormat(JSON)
        self.tpl = """SELECT DISTINCT %s WHERE {\n\t%s\n}"""

    def execution(self,query):
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        return results["results"]["bindings"]

    def triple(self, subject, predicate, object):
        return """ \n\t%s %s %s .""" % (subject, predicate, object)

    def union(self, triples):
        triples = map(lambda x: """{ %s }""" % x, triples)
        return "\n UNION ".join(triples)

    def uri(self, x):
        return '<%s>' % x

    def resources(self, x):
        t = self.triple('?s', self.uri(RDF.type), self.uri(OWL.Thing))
        t1 = self.triple('?s', '?p', self.uri(x))
        t2 = self.triple(self.uri(x),'?p','?s')
        t += self.union([t1,t2])
        return [r["s"]["value"] for r in self.execution(self.tpl % ('?s', t))]

#semantic matching including semantic similarity for categorical data and numerical data
class Matching:

    def __init__(self, G):
        self.G = G
        self.root = 'Dev'
        self.max_length = 6.0
        self.weights = {'narrower':0.6, 'broader':0.8, 'related':0.7}
        #manual alignment of concepts in DBpedia Knowledge Graph
        self.dbpedia = {'Java':'http://dbpedia.org/resource/Java_(programming_language)',
           'Scala':'http://dbpedia.org/resource/Scala_(programming_language)',
           'C':'http://dbpedia.org/resource/C_(programming_language)',
           'C++':'http://dbpedia.org/resource/C++',
           'Objective-C':'http://dbpedia.org/resource/Objective-C',
           'JavaScript':'http://dbpedia.org/resource/JavaScript',
           'Python':'http://dbpedia.org/resource/Python_(programming_language)',
           'Nodejs':'http://dbpedia.org/resource/Node.js',
           'Spring':'http://dbpedia.org/resource/Spring_Framework',
           'Django':'http://dbpedia.org/resource/Django_(web_framework)',
           'IOS':'http://dbpedia.org/resource/IOS',
           'Android':'http://dbpedia.org/resource/Android_(operating_system)'}
        self.sparql = SPARQL()

    def similarity(self, name):
        def function(x, y):
            return getattr(self, name)(x,y)
        return function

    def jaccard(self, a, b):
        r1 = self.dbpedia[a]
        r2 = self.dbpedia[b]
        A = self.sparql.resources(r1)
        B = self.sparql.resources(r2)
        AB = [r for r in A if r in B]
        return len(AB) * 10.0 / (len(A)+len(B)-len(AB))

    def rada(self, a, b):
        d = len(nx.shortest_path(self.G, a, b)) - 1
        return 1 - d/(self.max_length * 2)

    def wup(self, a, b):
        p1 = nx.shortest_path(self.G, a, self.root)
        p2 = nx.shortest_path(self.G, b, self.root)
        n = len(p1)
        m = len(p2)
        i = 1
        lcs = 'Dev'
        while i <= n and i <= m:
            if p1[-i] == p2[-i]:
                lcs = p1[-i]
            i = i + 1
        dc = len(nx.shortest_path(self.G, lcs, self.root))
        dc = dc * 2.0
        da = len(nx.shortest_path(self.G, a, lcs))
        db = len(nx.shortest_path(self.G, b, lcs))
        return dc / (da + db + dc)

    def graph(self, a, b):
        sim = 1.0
        d = nx.shortest_path(self.G, a, b)
        for i in range(len(d) - 1):
            l = self.G[d[i]][d[i+1]]['t']
            sim = sim * self.weights[l]
        sim = math.log(1 + sim, 2)
        return sim

    def graph_2(self, a, b):
        d = nx.shortest_path(self.G, a, b)
        d_path = len(d) - 1
        w = 0
        for i in range(len(d) - 1):
            l = self.G[d[i]][d[i+1]]['t']
            w += self.weights[l]
        sim = 1.0 + w
        sim = sim / (1.0 + d_path)
        return math.log(1 + sim, 2)


    def numerical(self, x, y, semantic, alpha=0.25, beta=0.1):
        if semantic == 'exact':
            if x == y:
                return 1
            else:
                return 0
        if semantic == 'broad':
            if x < y:
                return 1
            else:
                v = x - y
                v = alpha * v
                return 1 - v
        if semantic == 'narrow':
            if x > y:
                return 1
            else:
                v = x - y
                v = alpha * v
                return 1 - v
        if semantic == 'close':
            v = x - y
            v = abs(v)
            v = alpha * v
            return 1 - v
        if semantic == 'related':
            v = x - y
            v = beta * v
            return 0.5 - v


#simple matchmaking system
class Matchmaking:

    def __init__(self, G):
        self.M = Matching(G)
        self.weights = {'Skill':0.8,'Experience':0.2}

    def matchmaking(self, query, profiles):
        results = []
        for p in profiles:
            match = {}
            match['Skill'] = self.M.graph(query['Skill'],p['Skill'])
            match['Experience'] = self.M.numerical(query['Experience'],p['Experience'],'narrow')
            results.append(self.givenWeight(match))
        return results

    def givenWeight(self, match):
        sim = 0
        for key in self.weights.keys():
            sim = sim + match[key]*self.weights[key]
            print sim
        return sim

    def ahpWeight(matrix):
        eigenvalues, eigenvector = LA.eig(matrix)
        maxindex=np.argmax(eigenvalues)
        weight=eigenvector[:, maxindex]
        weight.tolist()
        weight=[ w/sum(weight) for w in weight ]
        #print eigenvalues
        #print eigenvector
        return weight

class Evaluation:

    def __init__(self, concepts, G):
        self.data = None
        self.headers = None
        self.concepts = concepts
        self.G = G
        self.matchmaking = Matchmaking(self.G)
        self.samples = [{'Skill':c,'Experience':e} for c in self.concepts for e in [1,3,5,7]]
        self.load_data('matchmaking-data.csv')
        self.pairs_taxonomy = [(p.split()[0],p.split()[2]) for p in self.headers[1:11]]
        self.pairs_graph = [(p.split()[0],p.split()[2]) for p in self.headers[11:]]
        self.pairs_all = [(p.split()[0],p.split()[2]) for p in self.headers[1:]]

    def correlation(self, name):
        def function(x, y):
            return getattr(self, name)(x,y)
        return function

    def pearson(self, x, y):
        return pearsonr(x,y)

    def spearman(self, x, y):
        return spearmanr(x,y)

    def kendall(self, x, y):
        return kendalltau(x, y)

    def evaluate(self, cor, method):
        human_1_taxonomy = self.normalise(self.data[0][1:11])
        human_2_taxonomy = self.normalise(self.data[1][1:11])
        human_3_taxonomy = self.normalise(self.data[2][1:11])

        print 'human_1', method, cor, self.eval_semantic_similarity(cor, method, self.pairs_taxonomy, human_1_taxonomy)
        #print 'human_2', method, cor, self.eval_semantic_similarity(cor, method, self.pairs_taxonomy, human_2_taxonomy)
        print 'human_3', method, cor, self.eval_semantic_similarity(cor, method, self.pairs_taxonomy, human_3_taxonomy)

    def eval_semantic_similarity(self, cor, method, pairs, human):
        sim_lst = self.semantic_similarity(method, pairs)
        return self.correlation(cor)(sim_lst, human)[0]

    def normalise(self, lst):
        lst = map(float, lst)
        return map(lambda x:x/5.0, lst)

    def semantic_similarity(self, method, pairs):
        return [self.matchmaking.M.similarity(method)(x,y) for x,y in pairs]

    def random_sample(self, n):
        return random.sample(self.samples, n)

    def load_data(self, name):
        if not self.data:
            f = open(name, 'r')
            try:
                reader = csv.reader(f)
                tmp = [row for row in reader]
                self.headers = tmp[0]
                self.data = tmp[1:]
            finally:
                f.close()
        return self.headers, self.data

eval = Evaluation(concepts, G_skos)
eval.evaluate('pearson', 'graph_2')
eval.evaluate('pearson', 'graph')
eval.evaluate('pearson', 'rada')
eval.evaluate('pearson', 'wup')
#eval.evaluate('pearson', 'wup')
#eval.evaluate('pearson','rada')