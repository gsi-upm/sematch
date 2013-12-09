import bottle
from bson.json_util import dumps
from simrec import Recommender
from bottle import TEMPLATE_PATH, route, jinja2_template as template
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.geo
cities = db.es_cities

TEMPLATE_PATH.append("./templates")

#data_set = cities.find({},{'name':1,'geo':1,'area':1,'population':1})
#data_set = [city for city in data_set]
#rec = Recommender(data_set)

@route('/city/<id:int>')
def get_city(id):
    city = cities.find_one({"id":id})
    return template('item.html',item=city)

#return json city by id
@route('/json/city/id/<id:int>', method='GET')
def get_json_city_by_id(id):
    return dumps(cities.find_one({"id":id}))

#return json city by name
@route('/json/city/name/<name>', method='GET')
def get_json_city_by_name(name):
    return dumps(cities.find_one({"name":name}))

#return all cities json data
@route('/json/cities', method='GET')
def get_cities():
    return dumps([city for city in cities.find()])

bottle.run(host='localhost',port=8080)



