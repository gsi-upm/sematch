import rdflib

class Ontology:

    def __init__(self, src):
        self.graph = rdflib.Graph()
        self.onto = self.graph.parse(src)
        self.classes = [self.graph.subjects(rdflib.RDF.type, rdflib.OWL.Class)]
        self.properties = [self.graph.subjects(rdflib.RDF.type, rdflib.OWL.ObjectProperty)]

    def children(self, c):
        return [son for son in self.graph.subjects(rdflib.RDFS.subClassof, c)]

    def range(self, c):
        return [r for r in self.graph.subjects(rdflib.RDFS.range, c)]

    def domain(self, c):
        return [r for r in self.graph.subjects(rdflib.RDFS.domain, c)]

