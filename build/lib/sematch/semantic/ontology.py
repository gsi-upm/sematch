#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2017 Ganggao Zhu- Grupo de Sistemas Inteligentes
# gzhu[at]dit.upm.es
# DIT, UPM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from rdflib import RDF, RDFS, OWL
from sematch.utility import FileIO
import rdflib

class DBpedia:

    """This class implement a wrapper for dbpedia ontology"""

    def __init__(self, src='models/dbpedia_2015-04.owl'):
        self.graph = rdflib.Graph()
        self.graph.parse(FileIO.filename(src))
        self.root = 'http://www.w3.org/2002/07/owl#Thing'
        self.classes = [s for s in self.graph.subjects(RDF.type, OWL.Class)]
        self.o_properties = [s for s in self.graph.subjects(RDF.type, OWL.ObjectProperty)]
        self.d_properties = [s for s in self.graph.subjects(RDF.type, OWL.DatatypeProperty)]
        self.uri2class = {c.toPython():c for c in self.classes}
        self.uri2class[self.root] = rdflib.URIRef(self.root)
        self.class_labels = [self.token(c) for c in self.classes]

    def superClass(self, x):
        return [o.toPython() for s, v, o in self.graph.triples((self.uri2class[x], RDFS.subClassOf, None))]

    def subClass(self, x):
        return [s.toPython() for s, v, o in self.graph.triples((None, RDFS.subClassOf, self.uri2class[x]))]

    def allSubClass(self, x, subList = []):
        for sub in self.subClass(x):
            subList.append(sub)
            self.allSubClass(sub, subList)
        return subList

    def allSuperClass(self, x, superList = []):
        for super in self.superClass():
            superList.append(super)
            self.allSuperClass(super, superList)
        return superList

    def siblingsClass(self, x):
        siblings = []
        for parent in self.superClass(x):
            for child in self.subClass(parent):
                if child != x:
                    siblings.append(child)
        return siblings

    def token(self, x):
        t = [o for o in self.graph.objects(x, RDFS.label) if o.language=='en']
        if t == []:
            return None
        return t[0].toPython()

    def lexicon(self, tag, lst):
        return [(self.token(x), x.n3(), tag) for x in lst if self.token(x)]

    def range(self, p):
        return [o for o in self.graph.objects(p, RDFS.range)]

    def domain(self, p):
        return [o for o in self.graph.objects(p, RDFS.domain)]
