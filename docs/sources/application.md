## Semantic Search

Sematch offers semantic search in terms of searching entities (e.g. `http://dbpedia.org/resource/Tom Cruise`)  and concepts (e.g.`http://dbpedia.org/ontology/Actor`), which are implemented in **Matcher** class.

##### Search LOD concept links

Users may need to search LOD concept links through natural language words. Sematch offers this search with Multilingual support.  An input word will be mapped to WordNet synsets, and then the mapped synsets having LOD links are retrieved. We provide 68423 synset-yago mappings by processing YAGO data. Note that we only consider common nouns. You can use different languages such as English words, car, university, singer; Spanish words, coche, universidad, cantante; Chinese words, 汽车, 大学, 歌手, to search for links. 

```python
from sematch.application import Matcher
matcher = Matcher()
#use English word to search LOD ontology class links 
print matcher.type_links('actor')
#use Spanish word to search LOD ontology class links 
print matcher.type_links('coche', lang='spa')
#use Chinese word to search LOD ontology class links 
print matcher.type_links('猫', lang='cmn')
```
Sematch supports Taxonomy based concept expansion. Users need to enable the expansion with the following code example.

```Python
from sematch.application import Matcher
matcher = Matcher(expansion=True)
print matcher.type_links('singer')
```

 With concept expansion, Sematch will perform depth-based tree search in WordNet taxonomy to find all the sub-concepts. For example,  singer's sub-concept baritone will be returned as well given query singer. Note that the results may be different with different languages because the lemma to synset mapping are different for different languages.

##### Search entities using concepts

Having LOD concept links, you can search entities belonging to a specific type from DBpedia using SPARQL queries through rdf:type.  We use SPARQL templates to construct such queries automatically and exectue the SPARQL queries in [DBpedia Sparql Endpoint](http://dbpedia.org/sparql) remotely. With the following code examples, entities belonging to scientist type will be retrieved, including their name, abstracts, and DBpedia links. With different language queries, Sematch will return entity's textual label and abstract in corresponding language. Sematch first use concept search to find concept links, and then those concept links are used to construct SPARQL queries. An example of automatically generated SPARQL query is shown.

```python
matcher.match_type('scientist')
matcher.match_type('científico', 'spa')
matcher.match_type('科学家', 'cmn')
```
```
SELECT DISTINCT ?s, ?label, ?abstract WHERE {
    {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/NuclearPhysicist110364643> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Econometrician110043491> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Sociologist110620758> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Archeologist109804806> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Neurolinguist110354053> . } 
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Thing> . 
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER( lang(?label) = "en") . 
    ?s <http://dbpedia.org/ontology/abstract> ?abstract . 
    FILTER( lang(?abstract) = "en") .
} LIMIT 5000
```

Since DBpedia endpoint has query size limitation, Sematch will decompose bigger queries into smaller ones and extecute them separately. Then results are combined when all the SPARQL queries are exectuted. Thus, the query execution may be slow if a query can be mapped to multiple concepts or query expansion is enabled. 

##### Search entities using concepts and entity restriction

It is common that users may only want to search for a smaller group of entities having a specific type and some restrctions such as location, person, event to name a few. For example,  searching for someone's song or movie (e.g `movies of Tom Cruise`.) or searching for `scientists in Spain`. Such queries are composed by a concept and an entity, representing information needs of entities having type of the concept and having some relations with the entity(e.g, `movies` that have some relation with entity `Tom Cruise`).  Usually, concepts correspond to meaningful common nouns, while entities correspond to specific proper nouns (e.g. university is common noun and Madrid is proper noun, query university of Madrid refers to all the universities located in Madrid). Sematch uses template to formulate SPARQL queries for such query patterns. The common nouns and proper nouns in the query are linked to concept and entity respectively. Then concept and entity links are used to construct the SPARQL query. Finally, the execution results give you a list of entities having type (rdf:type) of common noun, which have some semantic relation with proper noun. In addition, if query expansion is enabled, concepts will be expanded based on WordNet taxonomy in order to match more related entities. You can check out the technical details in the following publication.   


- Ganggao Zhu, and Carlos Angel Iglesias. "Sematch: Semantic Entity Search from Knowledge Graph." SumPre-HSWI@ ESWC. 2015.

The common noun to YAGO concept mapping is based on *type_link* function as shown above, while the proper noun to DBpedia instance mapping is currently based on exact string matching using SPARQL queries. So it is required to make sure that the spell and string of the instance names are correct.

```python
from sematch.sparql import NameSPARQL
#a simple linker to match proper noun through labels and names.
name_linker = NameSPARQL()
name_linker.name2entities('China')#'http://dbpedia.org/resource/China'
name_linker.name2entities('Spain')#'http://dbpedia.org/resource/Spain'
name_linker.name2entities('Tom Cruise')#'http://dbpedia.org/resource/Tom_Cruise'
```
For example, to map `Tom Cruise` to proper instance, the following SPARQL query is executed. 

```
SELECT DISTINCT ?s WHERE {
    {  
    ?s <http://www.w3.org/2000/01/rdf-schema#label> "Tom Cruise"@en . }
 UNION {  
    ?s <http://www.w3.org/2000/01/rdf-schema#label> "Tom Cruise"@en . }
 UNION {  
    ?x <http://www.w3.org/2000/01/rdf-schema#label> "Tom Cruise"@en . 
    ?x <http://dbpedia.org/ontology/wikiPageRedirects> ?s . }
 UNION {  
    ?s <http://dbpedia.org/ontology/demonym> "Tom Cruise"@en . }
 UNION {  
    ?s <http://dbpedia.org/property/acronym> "Tom Cruise"@en . } 
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Thing> .
} LIMIT 5000
SELECT DISTINCT ?s WHERE {
     
    <http://dbpedia.org/resource/Tom_Cruise> <http://dbpedia.org/ontology/wikiPageRedirects> ?s .
} LIMIT 5000
```

 The following examples are illustrated to search entities with concept and restriction. We do not provide mutilingual version of this function because of the query processing problem. User can implement the multilingual version with proper segmentation and proper noun or entity extraction. Currently, we use rule based noun extraction and named phrase extraction for English text.                                      

```python
print matcher.match_entity_type('university in Madrid')
print matcher.match_entity_type('movies with Tom Cruise')
```

For example, to match `movies with Tom Cruise`, the SPARQL query is shown. 

```
SELECT DISTINCT ?s, ?label, ?abstract WHERE {
    {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Movie106613686> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Film> . } 
    <http://dbpedia.org/resource/Tom_Cruise> ?p ?s . 
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER( lang(?label) = "en") . 
    ?s <http://dbpedia.org/ontology/abstract> ?abstract . 
    FILTER( lang(?abstract) = "en") .
} LIMIT 5000
```


## Similarity-Based Classification

We have implemented two similarity based classification model (unsupervised **SimClassifier** and supvervised **SimSVMClassifier**) in order to evaluate similarity metrics and provide similarity based text classification. 

The idea of similarity based classification is to extract most N frequent words associated with a class label so that those words are used as features to represet the label. Then, with given target words, by comparing the semantic similarity between target words and feature words, the correct label can be determined. The unsupervised **SimClassifier** chooses the corect label with the highest similarity score. The supervised **SimSVMClassifier** employs a Support Vector Machine (SVM) with a linear kernel and the trained SVM classifier is used to predict the correct label. Within similarity-based classification, the effectiveness of different knowledge-based semantic similarity metrics can be evaluated in applications apart from word similarities.

```python
from sematch.evaluation import AspectEvaluation
from sematch.application import SimClassifier, SimSVMClassifier
from sematch.semantic.similarity import WordNetSimilarity
evaluation = AspectEvaluation()
X, y = evaluation.load_dataset()
wns = WordNetSimilarity()
sim_metric = wns.word_similarity
simclassifier = SimClassifier.train(zip(X,y), sim_metric)
evaluation.evaluate(X,y, simclassifier)
simSVMclassifier = SimSVMClassifier.train(X, y, sim_metric)
evaluation.evaluate(X, y, simSVMclassifier)
```

We use the sentence-level Aspect-based Sentiment Analysis for illustration. In this task, aspect target words are associated to a list of aspect categories. We use the restaurant domain, which contains category classes of SERVICE, FOOD, DRINKS, AMBIENCE, etc. The aspect category classification task consists in assigning aspect category to opinion target words. This task challenges semantic relatedness methods, especially for corpus-based methods. For instance, in restaurant review corpora, those target words such as fish and wine would appear in same surrounding contexts (e.g., “the fish is delicious and the wine is great”). Since corpus-based methods are based on calculating co-occurrences of terms in a corpus, they can hardly discriminate terms from different categories that are frequently collocated (e.g., fish and wine). In such scenario, knowledge-based methods are useful to include the structural knowledge from domain taxonomy. Semantic similarity methods can be used to measure the taxonomical similarity between target words and aspect category in order to classify the target words into correct aspect category. We processed the dataset and got 4406 tuples containing target words and their categories. For example, ("wine list", "DRINKS") and ("spicy tuna roll", "FOOD"). For more details, reader can check the following articles.



- Ganggao Zhu, and Carlos A. Iglesias. ["Computing Semantic Similarity of Concepts in Knowledge Graphs."](http://ieeexplore.ieee.org/document/7572993/) IEEE Transactions on Knowledge and Data Engineering 29.1 (2017): 72-85.

- Oscar Araque, Ganggao Zhu, Manuel Garcia-Amado and Carlos A. Iglesias [Mining the Opinionated Web: Classification and Detection of Aspect Contexts for Aspect Based Sentiment Analysis](http://sentic.net/sentire2016araque.pdf),  ICDM sentire, 2016.









