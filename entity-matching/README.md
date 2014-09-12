![GSI Logo](http://gsi.dit.upm.es/templates/jgsi/images/logo.png)
[Sematch](http://gsi.dit.upm.es)
==================================

Introduction
---------------------

Sematch is a simple restful semantic matching server used for matching structured data, including
database records, rdf intances. The queries and the data are all structured according to the configuration.
The matching process is not just the key word matching. We have implemented a semantic similarity package
for calculating the similarity between the query and data semantically.

We implemented three modules, including semantic service, semantic similarity and semantic search. The matching
result would vary according to user's preference by changing the configurations of the system. The matching 
framework is very easy to configure and extend. 

## Construct the similarity configuration

We use spring dependency injection to construct the similarity configuration. You can either use the
implemented similarity modules or implement your own similarity module, and then use simple xml
configuration file to configure the similarity.

The implemented semantic similarity algorithms include ontolgoy based conceptual similarity such as
Rada, Wu&Palm, L&C, CGM, Li, meaningful level similarity, numerical similarity, string
similarity and set similarity. Those ontolgy or taxonomy based semantic similarity algorithms are used 
to calculate the similarities between concepts in the same hierarchical taxonomy built with Simple Knowledge 
Organization System(SKOS). 

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
