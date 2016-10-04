![Logo](https://dl.dropboxusercontent.com/u/74428083/sematch/logo.png)

## Introduction




## Examples

### Word Similarity

### Text Similarity

### Query Expansion

The first demo system overview is shown as below.
![overview](https://dl.dropboxusercontent.com/u/74428083/sematch/overview.png)

This is the corresponding online [demo](http://demos.gsi.dit.upm.es/sematch/).
In the current prototype of sematch, you can try the following examples in your project to retrieve a list of entities using combination of keywords e.g. a entity type and a related entity.

```
	from sematch.QueryEngine import Engine
	
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

You can contact me via gzhu [at] dit.upm.es

##Publications

Ganggao Zhu and Carlos A. Iglesias [Computing Semantic Similarity of Concepts in Knowledge Graphs](http://ieeexplore.ieee.org/document/7572993/), TKDE, 2016.

Ganggao Zhu and Carlos A. Iglesias [Sematch: Semantic Entity Search from Knowledge Graph](http://km.aifb.kit.edu/ws/sumpre2015/paper4.pdf)
In SumPre 2015 ESWC

##About Sematch

The name of Sematch is composed based on Spanish "se" and English "match". The logo of Sematch is based on
Chinese [Yin and Yang](http://en.wikipedia.org/wiki/Yin_and_yang) which is written
in [I Ching](http://en.wikipedia.org/wiki/I_Ching). Somehow, it correlates to 0 and 1 in computer science.
It is also the abbreviation of semantic matching because semantic similarity helps to match concepts, words,
entities semantically, instead of exact matching. Sematch aims to provide a framework to develop and evaluate
semantic similarity measures and their application for both textual corpus and structural knowledge graphs.

## License

```
Copyright 2016 UPM-GSI: Group of Intelligent Systems - Universidad Politécnica de Madrid (UPM)

Licensed under the Apache License, Version 2.0 (the "License"); 
You may not use this file except in compliance with the License. 
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by 
applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific 
language governing permissions and limitations under the License.
```
![GSI Logo](http://vps161.cesvima.upm.es/images/stories/logos/gsi.png)
