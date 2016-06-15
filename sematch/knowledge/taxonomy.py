from sematch.knowledge.dbpedia import Ontology
import networkx as nx


#TODO use networkx to index type taxonomy

#https://networkx.github.io/documentation/latest/reference/classes.html
#http://arxiv.org/pdf/1204.0245v1.pdf
#https://github.com/prpole/roget-tools
#http://dlacombejr.github.io/programming/2015/09/28/visualizing-cifar-10-categories-with-wordnet-and-networkx.html

#wikipedia category taxonomy http://purl.org/dc/terms/subject
#<http://dbpedia.org/resource/Albedo> <http://purl.org/dc/terms/subject> <http://dbpedia.org/resource/Category:Climatology> .

class DBpediaTypeTaxonomy:

    def __init__(self):
        self.ontology = Ontology()
        self.graph = nx.Graph()
        self.classes = self.ontology.uri2class.keys()
        self.class2id = {self.classes[i]:i for i in range(len(self.classes))}
        self.id2class = {i:self.classes[i] for i in range(len(self.classes))}
        self.root = self.class2id[self.ontology.root]
        self.build_taxonomy()

    def build_taxonomy(self):
        map(self.graph.add_node, self.id2class.keys())
        for node in self.graph.nodes():
            subs = self.ontology.subClass(self.id2class[node])
            subs = [sub for sub in subs if sub in self.classes]
            map(lambda x:self.graph.add_edge(node,self.class2id[x]), subs)

    def page_rank(self):
        return nx.pagerank(self.graph)

    def hits(self):
        return nx.hits(self.graph)

#
# tax = DBpediaTypeTaxonomy()
# pr = tax.page_rank()
#
# print pr

# child = tax.graph[tax.root]
# for res in map(lambda x:tax.id2class[x], child.keys()):
#     print res