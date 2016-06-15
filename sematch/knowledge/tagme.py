
#a python wrapper of tagme web api
#http://tagme.di.unipi.it/

import requests


class TAGME:

    def __init__(self):
        self.uri = 'http://tagme.di.unipi.it/tag'
        self.dbr = 'http://dbpedia.org/resource/'
        self.rho = 0.1

    def service(self, url, text):
        headers = {'Accept': 'application/json'}
        params={
                "text": text,
                "lang": 'en',
                "key": 'abc2016ZtQlV78F4'
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

