

## Introduction

The name of Sematch is composed based on Spanish "se" and English "match". It is also the abbreviation of semantic matching.

Sematch is a semantic entity search framework aiming to provide a framework combining the natural language processing techniques and linked of data techniques. Sematch is especially used for retrieving a list of entities from knowledge base using natural language queries. In the current prototype of sumach, you can try the following examples in your project. The results of executing each natural language query are a list of entities. The current prototype is using DBpedia SPARQL endpoint. The Sematch framework is designed to fit in different knowledge graph and different endpoints. We are still implementing more features of Sematch.

```
	from sematch import QueryEngine
	
	engine = Engine()
	print engine.query('university Spain')
	print engine.query('lakes China')
	print engine.query('airports in France')
	print engine.query('mountains Italy')
	print engine.query('lakes United States')
```

We have provided a RESTful web server based on python Flask. By running 
```
	python SematchServer.py 
```
you can have a running web-based interface.

This project is still under development.

The project is mainly maintained by Ganggao Zhu.

You can contact me via gzhu@dit.upm.es

## License

```
Copyright 2015 UPM-GSI: Group of Intelligent Systems - Universidad Politécnica de Madrid (UPM)

Licensed under the Apache License, Version 2.0 (the "License"); 
You may not use this file except in compliance with the License. 
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by 
applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific 
language governing permissions and limitations under the License.
```
![GSI Logo](http://gsi.dit.upm.es/templates/jgsi/images/logo.png)