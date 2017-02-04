
## Word Similarity

The key module of Sematch is measuring semantic similarity based on taxonomies. The word similarity is computed based on WordNet taxonomy with various semantic similarity metrics. Sematch extends the NLTK version of WordNet and similarities with lemmatization, multilingual support [Open Multilingual WordNet](http://compling.hss.ntu.edu.sg/omw/) and more semantic similarity metrics into a single class **WordNetSimilarity**. NLTK provides path, lch, wup, res, lin, and jcn, while jcn metric has divide zero problem. In Sematch, we provide uniformed metric interfaces and include two more metrics li and wpath. Those metric names and their corresponding publications are listed as below.

- **path**
Rada, Roy, et al. "Development and application of a metric on semantic nets." IEEE transactions on systems, man, and cybernetics 19.1 (1989): 17-30.
- **lch**
Leacock, Claudia, and Martin Chodorow. "Combining local context and WordNet similarity for word sense identification." WordNet: An electronic lexical database 49.2 (1998): 265-283.
- **wup**
Wu, Zhibiao, and Martha Palmer. "Verbs semantics and lexical selection." Proceedings of the 32nd annual meeting on Association for Computational Linguistics. Association for Computational Linguistics, 1994.
- **li**
Li, Yuhua, Zuhair A. Bandar, and David McLean. "An approach for measuring semantic similarity between words using multiple information sources." IEEE Transactions on knowledge and data engineering 15.4 (2003): 871-882.
- **res**
Resnik, Philip. "Using information content to evaluate semantic similarity in a taxonomy." arXiv preprint cmp-lg/9511007 (1995).
- **lin**
Lin, Dekang. "An information-theoretic definition of similarity." ICML. Vol. 98. No. 1998. 1998.
- **jcn**
Jiang, Jay J., and David W. Conrath. "Semantic similarity based on corpus statistics and lexical taxonomy." arXiv preprint cmp-lg/9709008 (1997).
- **wpath**
Zhu, Ganggao, and Carlos A. Iglesias. "Computing Semantic Similarity of Concepts in Knowledge Graphs." IEEE Transactions on Knowledge and Data Engineering 29.1 (2017): 72-85.

You can compute multilingual word similarity with various semantic similarity metrics using WordNet. Some examples are shown as below.

```python
from sematch.semantic.similarity import WordNetSimilarity
wns = WordNetSimilarity()
# Computing English word similarity using Li method
print wns.word_similarity('dog', 'cat', 'li') # 0.449327301063

# Computing Spanish word similarity using Lin method
print wns.monol_word_similarity('perro', 'gato', 'spa', 'lin') #0.876800984373

# Computing Chinese word similarity using  Wu & Palmer method
print wns.monol_word_similarity('狗', '猫', 'cmn', 'wup') # 0.857142857143

# Computing Spanish and English word similarity using Resnik method
print wns.crossl_word_similarity('perro', 'cat', 'spa', 'eng', 'res') #7.91166650904

# Computing Spanish and Chinese word similarity using Jiang & Conrad method
print wns.crossl_word_similarity('perro', '猫', 'spa', 'cmn', 'jcn') #0.31023804699

# Computing Chinese and English word similarity using WPath method
print wns.crossl_word_similarity('狗', 'cat', 'cmn', 'eng', 'wpath')#0.593666388463

```


## YAGO Concept Similarity


Apart from word similarity, **YagoTypeSimilarity** extends the **WordNetSimilarity** to compute semantic similarity between YAGO concepts (e.g. `http://dbpedia.org/class/yago/Actor109765278`). In order to achieve this, Sematch created WordNet synset and YAGO concept mappings based on the [YAGO dataset](http://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/yago/downloads/). Using the synset version in WordNet for YAGO concepts has three main advantages. First, it is convenient and fast to explore taxonomy structure and derive structural information (depth, path length, least common subsumer) using existing WordNet taxonomy in NLTK. Note that YAGO concepts are originally created based on WordNet synsets. Second, existing information contents computed from SemCor or Brown Corpus can be directly used to compute YAGO concept similarity with metrics such as res, lin, jcn and wpath. Finally, words can be mapped to YAGO concepts easily which is useful for semantic matching applications. 

 Apart from the existing metrics, in **YagoTypeSimilarity**, we also implemented those metrics res, lin, jcn and wpath with graph-based information content that is computed from YAGO concept's frequency in DBpedia by executing SPARQL queries to DBpedia endpoint. In summary, **YagoTypeSimilarity** maps YAGO concepts to WordNet synsets and computes their semantic similarity using WordNet taxonomy and either corpus-based or graph-based information content. We give some examples for illustration.

```python
from sematch.semantic.similarity import YagoTypeSimilarity
yago_sim = YagoTypeSimilarity()

#Mapping a word to yago links in DBpedia
dancer = yago_sim.word2yago('dancer')# e.g. 'http://dbpedia.org/class/yago/Dancer109989502'
actor = yago_sim.word2yago('actor') # e.g. 'http://dbpedia.org/class/yago/Actor109765278'
singer = yago_sim.word2yago('singer')# e.g. 'http://dbpedia.org/class/yago/Singer110599806'

#Mapping a yago link to WordNet synset
print yago_sim.yago2synset('http://dbpedia.org/class/yago/Actor109765278') 
Synset('actor.n.01')

#Measuring YAGO concept similarity through WordNet taxonomy and corpus based information content
yago_sim.yago_similarity('http://dbpedia.org/class/yago/Dancer109989502', 
                        'http://dbpedia.org/class/yago/Actor109765278', 'wpath')
0.642

yago_sim.yago_similarity('http://dbpedia.org/class/yago/Dancer109989502',
                        'http://dbpedia.org/class/yago/Singer110599806', 'wpath')
0.544

#Measuring YAGO concept similarity based on graph-based IC 
yago_sim.yago_similarity('http://dbpedia.org/class/yago/Dancer109989502', 
                        'http://dbpedia.org/class/yago/Actor109765278', 'wpath_graph')
0.423

yago_sim.yago_similarity('http://dbpedia.org/class/yago/Dancer109989502',
                        'http://dbpedia.org/class/yago/Singer110599806', 'wpath_graph')
0.328
```

## DBpedia Concept Similarity

Since YAGO concepts have corresponding mappings to WordNet synsets, we can reuse exsiting codes for computing semantic similarity of YAGO concepts. However, DBpedia concepts (ontology classes) in DBpedia ontology does not have such mappings, so we created **Taxonomy** class to parse such kind of concept taxonomy and implemented **ConceptSimilarity** class with all the semantic similarity metrics used in WordNet taxonomy. Since concept taxonomies such as DBpedia concept taxonomy does not have concept-annotated corpus like SemCor for WordNet, those semantic similarity metrics based on information contents can not be used. In order to solve this problem, we implemented graph-based information content (**GraphIC** class) relies on concept distribution in Knowledge Graph like DBpedia. For more technical details, user should refer the following article.

- Zhu, Ganggao, and Carlos A. Iglesias. "Computing Semantic Similarity of Concepts in Knowledge Graphs." IEEE Transactions on Knowledge and Data Engineering 29.1 (2017): 72-85.


Then you can parse DBpedia concept data to **Taxonomy** and **ConceptSimilarity** for computing semantic similarity between DBpedia concepts.

```python
from sematch.semantic.graph import DBpediaDataTransform, Taxonomy
from sematch.semantic.similarity import ConceptSimilarity
concept = ConceptSimilarity(Taxonomy(DBpediaDataTransform()), 'models/dbpedia_type_ic.txt')
print concept.name2concept('actor')
print concept.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'path')
print concept.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'wup')
print concept.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'li')
print concept.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'res')
print concept.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'lin')
print concept.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'jcn')
print concept.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'wpath')
```


## DBpedia Entity Similarity


We provide two methods to measure entity similarity. One is **entity relatedness** which is based on DBpedia link association which mainly measures entity link overlap between entities. You can check the detail of the method in the following article

- **entity relatedness** Milne, David, and Ian H. Witten. "Learning to link with wikipedia." Proceedings of the 17th ACM conference on Information and knowledge management. ACM, 2008.
                                                    
Another one is **entity similarity** measure which is based on YAGO concept similarity. First YAGO concepts of entity is extracted from DBpedia using **EntityFeatures** class. Then, top 5 concets with highest graph-based information contents are selected and composed as concept list. Finally, we compute semantic similarity of two entities by calculating semantic similarity of two concept lists, which is similar to compute text similarity based two word lists. You can check the function details in the following publication.

- **entity similarity** Mihalcea, Rada, Courtney Corley, and Carlo Strapparava. "Corpus-based and knowledge-based measures of text semantic similarity." AAAI. Vol. 6. 2006.

```python
from sematch.semantic.similarity import EntitySimilarity
entity_sim = EntitySimilarity()
print entity_sim.similarity('http://dbpedia.org/resource/Madrid',
                            'http://dbpedia.org/resource/Barcelona')
0.409923677282

print entity_sim.similarity('http://dbpedia.org/resource/Apple_Inc.',
                            'http://dbpedia.org/resource/Steve_Jobs')
0.0904545454545

print entity_sim.relatedness('http://dbpedia.org/resource/Madrid', 
                             'http://dbpedia.org/resource/Barcelona')
0.457984139871

print entity_sim.relatedness('http://dbpedia.org/resource/Apple_Inc.',
                             'http://dbpedia.org/resource/Steve_Jobs')
0.465991132787
```

You can see from the example that the **entity similarity** gives very low similarity score to entity *http://dbpedia.org/resource/Apple_Inc.* and entity *http://dbpedia.org/resource/Steve_Jobs* because semantic similarity measures entity's taxonomical similarity. Apple_Inc is a company and Steve_Jobs is a person. Although they are clearly related, they are not similar type.



