![logo](img/logo.png)

------------------


## Introduction

Sematch is a semantic similarity analysis library, written in Python 2.7. Semantic similarity is a very useful metric for many applications that require to quantify the semantic similarity between concepts. Sematch focus on knowledge-based semantic similarity using structural knowledge in taxonomy (e.g. depth, path length, least common subsumer), and statistical information contents (corpus-IC and graph-IC). Sematch provides an integrated framework for the development, evaluation and application of semantic similarity with both textual corpus and structural Knowledge Graphs (KGs). 

![logo](img/sematch-motivation.jpg)

Many applications share a common pipeline in using semantic similarity analysis. In textual applications, word similarity is measured based on WordNet with various semantic similarity metrics. Then text similarity (sentence level) is measured by composing word similarities, while document level text could be analysed by identifying important sentences based on text similarity, e.g. TextRank. This process starts from measuring concept similarity (word meanings or senses which are denoted as synsets in WordNet) which captures word level of meaning. This is normally referred as knowledge-based semantic similarity compared to its conterpart corpus-based approaches that are based on word coocurrence (e.g. Pointwise Mutual Information) or distributional semantics (Explict Semantic Analysis, Word2Vec, GLOVE and etc). Concept similarity are normally quantified using various information such as structural knowledge (e.g. path length, depth, least common subsumer) and statistical knowledge ( information content). 

KG based application also have similar pipeline. Entities in KGs are similar to words, while entities are described by concepts  (e.g. dbo:Movie, dbc:English_opera_singers) which are similar to word meanings (senses). Similar to word similarity, entity similarity can be quantified based on concept similarity. Moreover, those concepts in KGs are usually constructed into hierarchical taxonomies, such as DBpedia ontology class, Wikipedia categories, therefore quantifying concept similarity in WordNet or DBpedia relies on similar semantic information (e.g. path length,  depth, least common subsumer, information content) and semantic similarity metrics (e.g. Path, Wu & Palmer,Li,  Resnik, Lin, Jiang & Conrad and WPath). Furthermore, as WordNet concepts have been integrated into many modern KGs such as DBpedia, YAGO and BabelNet, it would be convenient to apply conventional semantic similarity analysis to KGs. Consequently,  Sematch aims to provide a framework to develop and evaluate semantic similarity metrics for concepts, entities, texts and their applications. 



------------------


## Installation





To install Sematch, you need to install its dependencies and download some datasets it requires. In NLTK, you need to download WordNet 3.0 and Open Mutilingual WordNet. We have included experimental datasets and type mappings with YAGO in models folder inside Sematch. However, some datasets such as Aspect Based Sentitiment Analysis you need to download from their original site. 

Currently, you could clone Sematch and setup it in your local.

```shell
git clone http://github.com/gsi-upm/sematch
#after setting up dependencies and downloading datasets, you could test it
cd tests
pytest
```

------------------

## Getting started

- Computing Similarity.

- Search Entities from DBpedia.

- Classify short text into categories.

- Evaluate Metric.

## Software Dependencies

Sematch uses the following dependencies:

- numpy, scipy, scikit-learn are used for scientific computing and machine learning.
- networkx is used for creating taxonomy, similarity graph construction and application.
- nltk is used for natural language processing tasks.
- gensim is used for semantic analysis.
- RDFLib, SPARQLWrapper, requests are used for interacting with Knowledge Graphs.
- Flask is used to implement web services.
- pytest is used for unit testing

You can check out the full requirements.txt for the complete dependent software and corresponding versions.

------------------

## Publications

- Ganggao Zhu and Carlos A. Iglesias [Computing Semantic Similarity of Concepts in Knowledge Graphs](http://ieeexplore.ieee.org/document/7572993/), TKDE, 2016.
- Oscar Araque, Ganggao Zhu, Manuel Garcia-Amado and Carlos A. Iglesias [Mining the Opinionated Web: Classification and Detection of Aspect Contexts for Aspect Based Sentiment Analysis](http://sentic.net/sentire2016araque.pdf),  ICDM sentire, 2016.
- Ganggao Zhu and Carlos A. Iglesias [Sematch: Semantic Entity Search from Knowledge Graph](http://km.aifb.kit.edu/ws/sumpre2015/paper4.pdf)
  ESWC SumPre 2015


------------------

## Support

You can post bug reports and feature requests in [Github issues](https://github.com/gsi-upm/sematch/issues). 
The project is mainly maintained by Ganggao Zhu. You can contact him via gzhu [at] dit.upm.es

------------------

## Why this name, Sematch and Logo?

The name of Sematch is composed based on Spanish "se" and English "match". It is also the abbreviation of semantic matching because semantic similarity metrics help to determine semantic distance of concepts, words, entities, instead of exact matching.

The logo of Sematch is based on Chinese [Yin and Yang](http://en.wikipedia.org/wiki/Yin_and_yang) which is written in [I Ching](http://en.wikipedia.org/wiki/I_Ching). Somehow, it correlates to 0 and 1 in computer science.
