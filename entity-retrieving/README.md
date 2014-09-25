##Introduction

DBpedia extracted strucutred information from Wikipedia and make this data as a RDF knowledge base. Nevertherless, quering this structured knowledge base by structured query languages is tedious and error-prone even for skilled users because it requires the end users to be familiar with the complex ontology and SPARQL query language. 

There are many QA systems which are implemented based on DBpedia dataset. We provide a tool to ease users in handling the tasks such as "Give me a list of (some type of data) some relation with (entity)". For example, "give me a list of companies in Spain". In this task, the key filters are company and Spain. Company specify the entity type, and the Spain specify the location. Our tool is able to generate a list of company uris.

##Installation

The system requires several packages including NLTK.

 