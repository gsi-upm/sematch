from flask import Flask, jsonify, json, request, render_template as template
from QueryEngine import Engine
import os

DEBUG = True
SECRET_KEY = 'Secret_development_key'

app = Flask(__name__)
app.config.from_object(__name__)

engine = Engine()

@app.route('/api/queries')
def queries():
    query = request.args.get('query')
    return json.dumps(engine.type_entity_query_construction(query))

@app.route('/api/types')
def types():
    query = request.args.get('query')
    return json.dumps(engine.types(query))

@app.route('/api/entities')
def entities():
    query = request.args.get('query')
    return json.dumps(engine.entities(query))

@app.route('/api/search')
def search():
    query = request.args.get('query')
    results = engine.search(query)
    relation_dict = {}
    for res in results:
        if res['relation'] in relation_dict:
            relation_dict[res['relation']].append(res)
        else:
            relation_dict[res['relation']] =[]
            relation_dict[res['relation']].append(res)
    return json.dumps([{'relation':key, 'entities':relation_dict[key]} for key in relation_dict.keys()])

@app.route('/')
def home():
    return template('demo.html')

def runserver():
    port = int(os.environ.get('PORT', 5005))
    app.run(host='demos.gsi.dit.upm.es', port=port)

if __name__ == '__main__':
    runserver()