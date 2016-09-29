
class EntityIndex:

    def __init__(self, solr_uri='http://localhost:8983/solr/%s'):
        from pysolr import Solr
        self._names = Solr(solr_uri % 'names')
        self._types = Solr(solr_uri % 'types')
        self._redirects = Solr(solr_uri % 'redirects')
        self._entities = Solr(solr_uri % 'entities')
        self._categories = Solr(solr_uri % 'categories')

    def redirect(self, dbr):
        query = 'dbr:"%s"'
        data = self._redirects.search(query % dbr)
        data = [d['redirect'][0] for d in data]
        if data:
            return data[0]
        return None

    def entity_category(self, dbr):
        query = 'dbr:"%s"'
        data = self._categories.search(query % dbr, **{'rows':500})
        data = [d['category'][0] for d in data]
        if data:
            return data
        return None

    def entity_type(self, dbr):
        query = 'dbr:"%s"'
        data = self._types.search(query % dbr)
        data = [d['type'][0] for d in data]
        if data:
            return data[0]
        return None

    def has_entity(self, dbr):
        query = 'dbr:"%s"'
        data = self._entities.search(query % dbr)
        data = [d['dbr'][0] for d in data]
        if data:
            return True
        return False

    def redirect_filter(self, link):
        red = self.redirect(link)
        return red if red else link

    def disambiguation_page_filter(self, link):
        return True if link.__contains__('(disambiguation)') else False

    def entity_candidates(self, text):
        query = 'name:"%s"'
        data = self._names.search(query % text, **{'rows':500})
        data = [d['dbr'][0] for d in data]
        data = map(self.redirect_filter, data)
        data = list(set(data))
        data = [d for d in data if not self.disambiguation_page_filter(d)]
        return data


#################OFFLINE PROCESS###############################

from sematch.utility import FileIO
from pymongo import MongoClient
from pysolr import Solr
import re
import json

LABELS = 'db/names/labels_en.nt'
CORPUS = 'db/names/labels.json'
REDIRECTS = 'db/redirect/redirects_en.nt'
TYPES = 'db/types/instance_types_lhd_dbo_en.nt'
CATEGORIES = 'db/categories/article-categories_en.nt'

#this is for redirect links and type links
def process_triple_links(source, relation, solr_uri, skip_head=False):
    solr = Solr(solr_uri)
    with open(FileIO.filename(source),'r') as f:
        if skip_head:
            f.next()
        i = 1
        upload = []
        for line in f:
            data = line.split()
            link_1 = data[0].lstrip('<')
            link_1 = link_1.rstrip('>')
            link_2 = data[2].lstrip('<')
            link_2 = link_2.rstrip('>')
            d = {}
            d['dbr'] = link_1
            d[relation] = link_2
            d['id'] = i
            upload.append(d)
            if i % 100000 == 0:
                print i
                solr.add(upload, commit=True)
                upload = []
            i = i + 1
        if upload:
            print i
            solr.add(upload, commit=True)

def clean_names(source, corpus):
    i = 1
    with open(FileIO.filename(source),'r') as f:
        f.next()
        for line in f:
            data = line.split()
            link = data[0].lstrip('<')
            link = link.rstrip('>')
            name = ' '.join(data[2:-1]).lstrip('"')
            name = name[:-4]
            #remove those (disambiguations) and such
            name = re.sub(r'\([^)]*\)', '', name)
            name = name.strip().lower()
            data = {}
            data['dbr'] = link
            data['label'] = name
            with open(FileIO.filename(corpus), 'a') as f_j:
                json.dump(data, f_j)
                f_j.write("\n")
            i = i + 1
            print i

def indexing_names(corpus):
    #client = MongoClient()
    #db = client.lod
    #dbpedia = db.names
    solr = Solr('http://localhost:8983/solr/names')
    with open(FileIO.filename(corpus), 'r') as f:
        id_n = 0
        upload = []
        for line in f:
            data = json.loads(line)
            d = {}
            d['dbr'] = data['dbr']
            d['name'] = data['label']
            upload.append(d)
            if id_n % 10000 == 0:
                print id_n
                solr.add(upload, commit=True)
                upload = []
            id_n = id_n + 1
        if upload:
            print id_n
            solr.add(upload, commit=True)

def indexing_dbr_from_mongo():
    solr = Solr('http://localhost:8983/solr/entities')
    client = MongoClient()
    db = client.lod
    dbpedia = db.dbpedia
    lines = dbpedia.find().sort('_id')
    int_id = 1
    upload = []
    for line in lines:
        d = {}
        d['id'] = line['_id']
        d['dbr'] = line['dbr']
        d['comment'] = line['abstract']
        d['abstract'] = line['long-abstract']
        upload.append(d)
        if int_id % 10000 == 0:
            print int_id
            solr.add(upload, commit=True)
            upload = []
        int_id = int_id + 1
    if upload:
        print int_id
        solr.add(upload, commit=True)


#process_triple_links(CATEGORIES,'category','http://localhost:8983/solr/categories',skip_head=True)
