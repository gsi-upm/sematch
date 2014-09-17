from flask import Flask, jsonify, json, request, render_template as template
from pymongo import MongoClient
import sematch

client = MongoClient('localhost', 27017)
db = client.geoname_database
country_collection = db.countries
autoQuery = sematch.AutoQuery()
wordnet = sematch.WordNetLD()

DEBUG = True
SECRET_KEY = 'Secret_development_key'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/sematch/api/types')
def get_types():
    feature = request.args.get('feature')
    country = request.args.get('country')
    sim = request.args.get('sim')
    threshold = request.args.get('threshold')
    return json.dumps(wordnet.search_types(feature, sim, threshold))

@app.route('/sematch/api/match')
def match():
    feature = request.args.get('feature')
    country = request.args.get('country')
    sim = request.args.get('sim')
    threshold = request.args.get('threshold')
    synsets = wordnet.search_types(feature, sim, threshold)
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








