from flask import Flask, jsonify, json, request, render_template as template
from pymongo import MongoClient
from sparql import AutoQuery
from wordnet_ld import WordNetLD

client = MongoClient('localhost', 27017)
db = client.geoname_database
country_collection = db.countries
wordnet_collection = db.wordnet_ld
autoQuery = AutoQuery()
wordnet = WordNetLD()

DEBUG = True
SECRET_KEY = 'Secret_development_key'

app = Flask(__name__)
app.config.from_object(__name__)

def search_types(feature, simType, threshold):
    synsets = wordnet.search_synsets(feature, simType)
    #filter by similarity threshold
    synsets = [synset for synset in synsets if synset['sim'] >= float(threshold)]
    synsets_map = {}
    for synset in synsets:
        synsets_map[synset['offset']] = synset
    for key, value in synsets_map.iteritems():
        value['link'] = []
        for feature in wordnet_collection.find({'offset':key}, {'_id':0}):
            if feature.get('dbpedia'):
                value['link'].append(feature['dbpedia'])
            if feature.get('yago_dbpedia'):
                value['link'].append(feature['yago_dbpedia'])
    synsets = [value for key, value in synsets_map.iteritems() if value['link']]
    return synsets

@app.route('/sematch/api/types')
def get_types():
    feature = request.args.get('feature')
    country = request.args.get('country')
    sim = request.args.get('sim')
    threshold = request.args.get('threshold')
    return json.dumps(search_types(feature, sim, threshold))

@app.route('/sematch/api/match')
def match():
    feature = request.args.get('feature')
    country = request.args.get('country')
    sim = request.args.get('sim')
    threshold = request.args.get('threshold')
    synsets = search_types(feature, sim, threshold)
    types = []
    for synset in synsets:
        types += synset['link']
    results = autoQuery.auto_query(types, country)
    return json.dumps(results)

@app.route('/')
def home():
    country_list = []
    countries = country_collection.find()
    for c in countries:
        country = {}
        country['name'] = c['name']
        country['link'] = c['dbpedia_link']
        country_list.append(country)
    return template('sematch.html', countries=country_list)








