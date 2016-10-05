
from sematch.sparql import NameSPARQL
import requests


class DBpediaSpotlight:
    """simple wrapper implementation of dbpedia spotlight web service using local server"""


    def __init__(self):
        self.uri = 'http://localhost:8888/rest/'
        self.dbr = 'http://dbpedia.org/resource/'
        self.confidence = 0.5
        self.support = 20

    def create_obj(self, x):
        obj = {}
        obj['uri'] = self.dbr + x['@uri']
        obj['label'] = x['@label']
        obj['score'] = x['@finalScore']
        obj['context'] = x['@contextualScore']
        obj['support'] = x['@support']
        return obj

    def take_resource(self, data):
        resource_list = []
        if type(data['resource']) is list:
            for x in data['resource']:
                resource_list.append(self.create_obj(x))
        elif type(data['resource']) is dict:
            x = data['resource']
            resource_list.append(self.create_obj(x))
        return resource_list

    def mentions(self, res):
        data = {}
        data['mention'] = res['@name']
        data['offset'] = res['@offset']
        data['mappings'] = self.take_resource(res)
        return data

    def service(self, url, text):
        headers = {'Accept': 'application/json'}
        params={
                "text": text,
                "confidence": self.confidence,
                "support": self.support,
            }
        return requests.get(url,params=params,headers=headers)


    #use dbpedia spotlight to generate candidate dbpedia resources
    def candidates(self, text):
        url = self.uri+'candidates'
        result = self.service(url, text).json()
        results = []
        if result['annotation'].get('surfaceForm'):
            result = result['annotation']['surfaceForm']
            if type(result) is list:
                for res in result:
                    results.append(self.mentions(res))
            elif type(result) is dict:
                results.append(self.mentions(result))
        return results

    #use dbpedia spotlight to annotate text
    def annotate(self, text):
        url = self.uri + 'annotate'
        result = self.service(url, text).json()
        results = {}
        if result.get('Resources'):
            for res in  result['Resources']:
                results[res['@surfaceForm']] = res['@URI']
        return results

class TAGME:
    # a python wrapper of tagme web api
    # http://tagme.di.unipi.it/


    def __init__(self, key):
        self.uri = 'http://tagme.di.unipi.it/tag'
        self.dbr = 'http://dbpedia.org/resource/'
        self.rho = 0.1
        self.key = key

    def service(self, url, text):
        headers = {'Accept': 'application/json'}
        params={
                "text": text,
                "lang": 'en',
                "key": self.key
            }
        return requests.get(url,params=params,headers=headers)

    #use dbpedia spotlight to annotate text
    def annotate(self, text):
        result = {}
        data = self.service(self.uri, text).json()
        if data.get('annotations'):
            for d in data['annotations']:
                if float(d['rho']) > self.rho:
                    result[d['spot']] = self.dbr + '_'.join(d['title'].split())
        return result

import urllib2
import urllib
import json
import gzip

from StringIO import StringIO


class BabelNet:

    def __init__(self, key, langs='EN'):
        self.service_disambiguate = 'https://babelfy.io/v1/disambiguate'
        self.service_synsetIds = 'https://babelnet.io/v2/getSynsetIds'
        self.service_synset = 'https://babelnet.io/v2/getSynset'
        self.api_key = key
        self.langs = langs

    def service(self, url, params):
        params['key'] = self.api_key
        params['langs'] = self.langs
        url = url + '?' + urllib.urlencode(params)
        request = urllib2.Request(url)
        request.add_header('Accept-encoding', 'gzip')
        response = urllib2.urlopen(request)
        data = []
        if response.info().get('Content-Encoding') == 'gzip':
	        buf = StringIO( response.read())
	        f = gzip.GzipFile(fileobj=buf)
	        data = json.loads(f.read())
        return data

    def synset_id(self, word):
        params= {
                'word': word,
                'pos':'NOUN',
            }
        data = self.service(self.service_synsetIds,params)
        return data

    def synset(self, id):
        params = {
            'id':id,
            'filterLangs':'EN'
        }
        data = self.service(self.service_synset, params)
        return data

    def wn_synsets(self, word):
        data = self.synset_id(word)
        data = [self.synset(d['id']) for d in data]
        data = [self.wn_offset(d) for d in data]
        return [d for d in data if d is not None]

    def wn_offset(self, synset):
        if synset.get('wnOffsets'):
            return synset['wnOffsets']
        return None

    def disambiguate(self, text):
        params={
                'text': text,
            }
        data = self.service(self.service_disambiguate, params)
        print data
        # retrieving data
        for result in data:# retrieving token fragment
            tokenFragment = result.get('tokenFragment')
            tfStart = tokenFragment.get('start')
            tfEnd = tokenFragment.get('end')
            print str(tfStart) + "\t" + str(tfEnd)

            # retrieving char fragment
            charFragment = result.get('charFragment')
            cfStart = charFragment.get('start')
            cfEnd = charFragment.get('end')
            print str(cfStart) + "\t" + str(cfEnd)

            # retrieving BabelSynset ID
            synsetId = result.get('babelSynsetID')
            print synsetId

    def annotate(self, text):
        params={
                'text': text,
                'annType':'NAMED_ENTITIES'
            }
        data = self.service(self.service_disambiguate, params)
        result = []
        for d in data:
            if d.get('DBpediaURL'):
                result.append(d['DBpediaURL'])
        return list(set(result))


#
# class Matching:
#
#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.N = len(self.tokens)
#         self.segments = [(j,j+i) for i in range(1, self.N + 1) for j in range(self.N - i + 1)]
#         self.segment2entity = {}
#
#     def entities(self):
#         for s in self.segments:
#             sf = self.surface_form(s).lower()
#             entities = entity_candidates(sf)
#             if entities:
#                 self.add(s, entities)
#         span = self.maximun_span()
#         result = {}
#         for seg in self.segment2entity:
#             x,y = seg
#             if y - x == span:
#                 entities = self.segment2entity[seg]
#                 sf = self.surface_form(seg)
#                 for entity in entities:
#                     result[entity] = self.uri_similarity(sf,entity)
#         return result
#
#     def uri_similarity(self, text, entity):
#         fragment = entity[28:]
#         #fragment = re.sub(r'\([^)]*\)', '', fragment)
#         x = str(text).lower()
#         y = str(fragment).lower()
#         return string_similarity(x,y)
#
#     def surface_form(self, segment):
#         begin, end = segment
#         return ' '.join(self.tokens[begin:end])
#
#     #add the mapped entities into lexicon
#     def add(self, segment, entities):
#         map(lambda x:self.add_entry(segment, x), entities)
#
#     def add_entry(self, segment, entity):
#         self.segment2entity.setdefault(segment, []).append(entity)
#
#     def maximun_span(self):
#         max_span = 1
#         for seg in self.segment2entity:
#             x,y = seg
#             span = y - x
#             if span > max_span:
#                 max_span = span
#         return max_span


