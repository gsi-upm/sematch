![GSI Logo](http://gsi.dit.upm.es/templates/jgsi/images/logo.png)
[Semantic Matching](http://gsi.dit.upm.es)
==================================

Introduction
---------------------
Semantic matching provide a possible way to match the data that user really want
even thought there are no common phrases between user query and the data. 
We implemented three modules, including semantic service, semantic similarity and 
semantic search. The matching result would vary according to user's preference by
changing the configurations of the system. The matching framework is very easy to
configure and extend. 

## Semantic Similarity

In semantic similarity, we implement a extensible framework for calculating the 
semantic similarities between data. The data are represented as plain Strings so that
the users can easily implemente their own functions for calculating semantic similarity
between different types of data. We have implemented several semantic similarity algorithms
such as ontolgoy based concept similarity, level similarity, numerical similarity, and String
similarity. We implement several state of the art of structure based algorithms for 
ontology based methods and we propose a new one too. Those ontolgy or taxonomy based
semantic similarity algorithms are used to calculate the similarities between concepts
in the same hierarchical taxonomy built with Simple Knowledge Organization System(SKOS). 
The algorithms that have been implemented include Rada, Wu&Palm, L&C, CGM, Li. 

Users are free to extend the semantic similarity algorithms by extending two classes,
SimilarityMeasure and SimCompute.

## Semantic Service
In semantic service, we implement the configurable restful service for semantic 
matching. Including a restful server and ajax client. 


## Semantic Search
In semantic search, we use lucene to index the data. Different with the lucene's
default matching and scoring funcionality, we implement our scoring functionality
by calling the semantic similarity algorithms. Therefore, the data are retrieval and
ranked according to their semantic similarity socres.

About this repository
------------------------------
This is the root github repository of the Semantic Matching project.
For more information, contact us through: http://gsi.dit.upm.es
