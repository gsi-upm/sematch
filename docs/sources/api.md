 
#Similarity API

Some common interfaces for semantic information are provided so that novel similarity metrics are easy to implement with Sematch. The main semantic resources include:

- **Depth** is the path length between a root and a specific concept in taxonomy.
- **Shortest Path Length** is the shortest path length between two concepts in taxonomy.
- **Least Common Subsumer** is the common parent of two concepts which has maximun depth.
- **Corpus-based IC** is the information content computed from sense-annotated corpora such as SemCor or Brown Corpus
- **Graph-based IC** is the information content computed from Knowledge graph

To design a new semantic similarity metric in WordNet, you can take the implementation of WPath method as example.

```Python
def wpath(self, c1, c2, k=0.8):
    lcs = self.least_common_subsumer(c1,c2)
    path = c1.shortest_path_distance(c2)
    weight = k ** self.synset_ic(lcs)
    return 1.0 / (1 + path*weight)
```

To design a new semantic similarity metric for YAGO concepts, you can not only use corpus based IC **synset_ic**, buth also use **concept_ic** which computes graph-based IC.

```Python
def wpath_graph(self, c1, c2, k=0.9):
    lcs = self.least_common_subsumer(c1, c2)
    path = c1.shortest_path_distance(c2)
    yago_lcs = self.synset2yago(lcs)
    weight = k ** self._graph_ic.concept_ic(yago_lcs)
    return 1.0 / (1 + path*weight)
```

To add new semantic similarity metric in common Taxonomy class, you use the similar interface as previous two examples.

```
def wpath(self, c1, c2, k=0.8):
    lcs = self.least_common_subsumer(c1, c2)
    path = self.shortest_path_length(c1, c2) - 1
    weight = k ** self.concept_ic(lcs)
    return 1.0 / (1 + path * weight)
```
The common Taxonomy and ConceptSimilarity class are designed for ontology classes of KGs, thus it only contains graph-based IC. The corpus-based IC computation requires concept-annotated corpus so we only provide YAGO concept with such support since YAGO concepts are built based on WordNet and corresponding synsets have existing sense-annotated corpora. In concequence, to compute YAGO concept similarity, user can use both kind of IC resources.


#Taxonomy API

Within the **Taxonomy** class, **ConceptSimilarity** class and **GraphIC** class, user can parse any concept taxonomies where 
concepts are represented hiearchically such as Wikipedia categories, [Open Diretory Project](https://www.dmoz.org/), [Medical Subject Headings](https://www.nlm.nih.gov/mesh/), [ACM Term ClassificationIn](https://www.acm.org/publications/class-2012) and many others. For those ontology classes with the support of Knowledge Graph, **GraphIC** can be used to compute graph-based information content. Otherwise, user needs to implement similar class of **GraphIC** based on specific data management system or just use those metrics only dependent on path length, depth, least common subsumer, such as path, wup, li, and wpath (set k parameter as 1).  We provide an example of using these general classes for computing semantic similarity.

You need to first implement **DataTransform** class to convert concept taxonomy data into nodes, labels, and edges. Nodes is a set of concept links. Labels is corresponding labels of nodes. Edges is list of (super-concept, sub-concept) tuples. Note that in edges those node are represented by their list index. 


```python
from sematch.semantic.ontology import DBpedia

class DBpediaDataTransform(DataTransform):

    def __init__(self):
        self._ontology = DBpedia()

    def transform(self):
        nodes =  map(lambda x:x.toPython(), self._ontology.classes)
        node_id = {n:i for i,n in enumerate(nodes)}
        labels = [self._ontology.token(value) for i,value in enumerate(self._ontology.classes)]
        edges = []
        for i, node in enumerate(nodes):
            children = self._ontology.subClass(node)
            children = [child for child in children if child in nodes]
            children_ids = map(lambda x:node_id[x], children)
            for child_id in children_ids:
                edges.append((i, child_id))
        return nodes, labels, edges

```



