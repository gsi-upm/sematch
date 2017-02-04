# Natural Language Processing

The nlp.py module provides several simple natural language processing functions, including tokenization, stopwords filtering, lemmatization, part of speech tagging (POS) using NLTK. This module is mainly used for processing textual data in WordNet and DBpedia, such as WordNet synset glosses and DBpedia abstracts and categories. Apart from NLTK, we implement a rule-based word and chunk extraction module Extraction and a keyword extraction algrithm RAKE, in order to extract words, chunks, and keywords features from WordNet and DBpedia.

## Keywords Extraction

With entity abstracts, you can use RAKE algorithm to extract keywords from abstract.

```python
from sematch.nlp import RAKE
from sematch.semantic.sparql import EntityFeatures
upm = EntityFeatures().features('http://dbpedia.org/resource/Technical_University_of_Madrid')
rake = RAKE()
print rake.extract(upm['abstract'])
(u'madrid (spanish: universidad polit\xe9cnica de madrid, upm)', u'spanish university, located', 
u'madrid.', u'architecture, originating mainly', u'spain,', u'el mundo,', u'time network,', 
u'fields,', u'fifty engineering schools throughout europe.',
 u'top technical university', u'technical university')
```

## Words and Entity Extraction

Apart from keywords, you can use Extraction class to extract nouns and proper nouns from entity abstract.
```python
from sematch.nlp import Extraction
from sematch.semantic.sparql import EntityFeatures
upm = EntityFeatures().features('http://dbpedia.org/resource/Technical_University_of_Madrid')
extract = Extraction()
print extract.extract_nouns(upm['abstract'])
[u'technical', u'university', u'madrid', u'polytechnic', u'university',
 u'madrid', u'spanish', u'universidad', u'polit\xe9cnica', u'madrid', 
 u'upm', u'university', u'madrid', u'result', u'technical', u'school',
  u'engineer', u'architecture', u'century', u'student', u'class', u'year',
   u'university', u'el', u'mundo', u'technical', u'university', u'madrid', 
   u'rank', u'university', u'spain', u'majority', u'engineer', u'school', 
   u'institution', u'spain', u'field', u'europe', u'upm', u'part', u'time', 
   u'network', u'group', u'engineer', u'school', u'europe']

print extract.extract_verbs(upm['abstract'])
[u'call', u'locate', u'found', u'merge', u'originate', u'attend', u'accord', 
u'rank', u'conduct', u'rank', u'lead', u'fifty']

print extract.extract_chunks_doc(upm['abstract'])
[u'Technical University', u'Madrid', u'Polytechnic University', 
u'Madrid', u'Universidad Polit\xe9cnica', u'Madrid', u'University', 
u'Madrid', u'Technical Schools', u'Engineering', u'Architecture', u'El Mundo',
 u'Technical University', u'Madrid', u'Spain', u'Engineering Schools', 
 u'Spain', u'Europe', u'UPM', u'TIME', u'Europe']

cats = extract.category_features(upm['category'])
print extract.category2words(cats)
[u'technical', u'madrid', u'university', u'public', u'forestry', 
u'college', u'establishment', u'institution', u'spain']
```

## Words Rank

In order to rank words in entity abstract according to their topical cohenrence, you can use sematch to implement a graph-based ranking algorithm using word similarity graph. First, extract nouns in entity abstract and compute their pairwise similarity using WordNetSimilarity. Then nouns and similarity scores are parsed into SimGraph to rank words based on PageRank algorithms. In the end, top-N words are aquired using PageRank socre based on word's topical centrallity. 

```
from sematch.semantic.graph import SimGraph
from sematch.semantic.similarity import WordNetSimilarity
from sematch.nlp import Extraction, word_process
from sematch.semantic.sparql import EntityFeatures
from collections import Counter
tom = EntityFeatures().features('http://dbpedia.org/resource/Tom_Cruise')
words = Extraction().extract_nouns(tom['abstract'])
words = word_process(words)
wns = WordNetSimilarity()
word_graph = SimGraph(words, wns.word_similarity)
word_scores = word_graph.page_rank()
words, scores =zip(*Counter(word_scores).most_common(10))
print words
(u'picture', u'action', u'number', u'film', u'post', u'sport', 
u'program', u'men', u'performance', u'motion')
```