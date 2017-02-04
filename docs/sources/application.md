## Semantic Matching

Sematch offers **Matcher** class for matching entities (e.g. `http://dbpedia.org/resource/Tom Cruise`) and entity types (e.g.`http://dbpedia.org/ontology/Actor`). The type matching first maps Multilingual word forms to WordNet synsets and performs synset expansion using depth-based tree search to find all the sub-concepts of the synset in WordNet taxonomy. Then, the mapped synsets having LOD links are retrieved. We provide 68423 synset-yago mappings by processing YAGO data. Note that we only consider common nouns. You can use English words, car, university, singer; Spanish words, coche, universidad, cantante; Chinese words, 汽车, 大学, 歌手, to search for type links. The results may be different with different languages because the lemma to synset mapping are different for different languages.

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
Having LOD ontology classes, you can match entities from DBpedia using SPARQL queries. As a word can be mapped to many LOD ontology classes including sub-concepts, we split the SPARQL queries and exectue them separately in order to match full list of entities related to a specific type word. We use SPARQL templates to construct such queries automatically and exectue the SPARQL queries in [DBpedia Sparql Endpoint](http://dbpedia.org/sparql).

```python
matcher.match_type('scientist')
matcher.match_type('científico', 'spa')
matcher.match_type('科学家', 'cmn')
```
With the above code, we have 56730 scientist entities including their name, abstracts, and DBpedia links. Within different language setting, the function will return entity's textual label and abstract in corresponding language. Those multilingual word forms are mapped to WordNet synsets and corresponding YAGO concepts. Then YAGO concepts are used to construct the SPARQL queries. An example of automatically generated SPARQL query is shown.

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

In addition to match entities with specific types, you can add entities to restrict the results, such as `movies of Tom Cruise`. This stands for give me `movies` that have some relation with entity `Tom Cruise`. Like the words can be mapped to WordNet concepts, this kind of muti-word expressions can be mapped to real world entities representing their meanings. Usually, such expressions are composed by a meaningful common noun and a specific proper noun, which we can call as type entity pattern. For example, university (common noun) and Madrid (proper noun) refer to all the universities located in Madrid. Such expressions have been used as categorical labels such as Wikipedia categories, while we use type entity pattern to formulate SPARQL queries in order to expand and match entities. The **Matcher** maps common nouns and proper nouns in the query to YAGO concepts and entity instances respectively. Then *type entity* SPARQL query template is used to construct the query based on type link and entity link. Finally, the execution results give you a list of entities having type (rdf:type) of common noun, which have some semantic relation with proper noun. Moreover, semantic expansion is performed with common noun based on WordNet taxonomy in order to match more related entities. You can check out the technical details in the following publication.   


- Zhu, Ganggao, and Carlos Angel Iglesias. "Sematch: Semantic Entity Search from Knowledge Graph." SumPre-HSWI@ ESWC. 2015.

The common noun to YAGO concept mapping is based on *type_link* function as shown above, while the proper noun to DBpedia instance mapping is based on exact string matching using SPARQL queries. So it is required to make sure that the spell and string of the instance names are correct.

```python
from sematch.sparql import NameSPARQL
#a simple linker to match proper noun through labels and names.
name_linker = NameSPARQL()
name_linker.name2entities('China')#'http://dbpedia.org/resource/China'
name_linker.name2entities('Spain')#'http://dbpedia.org/resource/Spain'
name_linker.name2entities('Tom Cruise')#'http://dbpedia.org/resource/Spain'

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

Use the following example to match entities. We do not provide mutilingual version of type entity pattern matching because of the query processing. User can implement the multilingual version with proper segmentation and proper noun or entity extraction. Currently, we use rule based noun extraction and named phrase extraction for English text.                                      

```python
print matcher.match_entity_type('university in Madrid')
print matcher.match_entity_type('movies with Tom Cruise')
```

For example, to match `movies with Tom Cruise`, some of the SPARQL queries are shown. We retrieve all the entities and merge them based on their DBpedia resource links.

```
SELECT DISTINCT ?s, ?label, ?abstract WHERE {
    {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Newsreel106616703> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Shoot-'em-up106616216> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/SkinFlick106617413> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Movie106613686> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Cartoon106616464> . } 
    <http://dbpedia.org/resource/Tom_Cruise> ?p ?s . 
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER( lang(?label) = "en") . 
    ?s <http://dbpedia.org/ontology/abstract> ?abstract . 
    FILTER( lang(?abstract) = "en") .
} LIMIT 5000

SELECT DISTINCT ?s, ?label, ?abstract WHERE {
    {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/FilmNoir106617165> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/CollageFilm106615818> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/RoughCut106617644> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/TalkingPicture106618822> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Musical107019172> . } 
    <http://dbpedia.org/resource/Tom_Cruise> ?p ?s . 
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER( lang(?label) = "en") . 
    ?s <http://dbpedia.org/ontology/abstract> ?abstract . 
    FILTER( lang(?abstract) = "en") .
} LIMIT 5000


SELECT DISTINCT ?s, ?label, ?abstract WHERE {
    {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Feature106615026> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/SilentMovie106617752> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/FinalCut106615216> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/SpaghettiWestern106618653> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Musical> . } 
    <http://dbpedia.org/resource/Tom_Cruise> ?p ?s . 
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER( lang(?label) = "en") . 
    ?s <http://dbpedia.org/ontology/abstract> ?abstract . 
    FILTER( lang(?abstract) = "en") .
} LIMIT 5000


SELECT DISTINCT ?s, ?label, ?abstract WHERE {
    {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/HomeMovie106615458> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Film> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/ShortSubject106616314> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/HorseOpera106616035> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/CinemaVerite106617011> . } 
    <http://dbpedia.org/resource/Tom_Cruise> ?p ?s . 
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER( lang(?label) = "en") . 
    ?s <http://dbpedia.org/ontology/abstract> ?abstract . 
    FILTER( lang(?abstract) = "en") .
} LIMIT 5000


SELECT DISTINCT ?s, ?label, ?abstract WHERE {
    {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Telefilm106614628> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Documentary106616806> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Peepshow106617527> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/SlowMotion106617866> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Three-D106618937> . } 
    <http://dbpedia.org/resource/Tom_Cruise> ?p ?s . 
    ?s <http://www.w3.org/2000/01/rdf-schema#label> ?label . 
    FILTER( lang(?label) = "en") . 
    ?s <http://dbpedia.org/ontology/abstract> ?abstract . 
    FILTER( lang(?abstract) = "en") .
} LIMIT 5000

```
You can see from above SPARQL example, we are able to match more entities by performing concept expansion. You can disable the expansion with the following example.

```Python
from sematch.application import Matcher
matcher = Matcher(expansion=False)
matcher.match_entity_type('movies with Tom Cruise')
```

The SPARQL queries will be limited to movies. Note that two query patterns are needed in order to match all the relations.

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

SELECT DISTINCT ?s, ?label, ?abstract WHERE {
    {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/class/yago/Movie106613686> . }
 UNION {  
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Film> . } 
    ?s ?p <http://dbpedia.org/resource/Tom_Cruise> . 
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



- Zhu, Ganggao, and Carlos A. Iglesias. ["Computing Semantic Similarity of Concepts in Knowledge Graphs."](http://ieeexplore.ieee.org/document/7572993/) IEEE Transactions on Knowledge and Data Engineering 29.1 (2017): 72-85.

- Oscar Araque, Ganggao Zhu, Manuel Garcia-Amado and Carlos A. Iglesias [Mining the Opinionated Web: Classification and Detection of Aspect Contexts for Aspect Based Sentiment Analysis](http://sentic.net/sentire2016araque.pdf),  ICDM sentire, 2016.









