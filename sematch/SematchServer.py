from flask import Flask, jsonify, json, request, render_template as template
from QueryEngine import Engine
import os


DEBUG = True
SECRET_KEY = 'Secret_development_key'

app = Flask(__name__)
app.config.from_object(__name__)

engine = Engine()

@app.route('/sematch/api/queries')
def queries():
    query = request.args.get('query')
    return json.dumps(engine.sparql_construction(query))

@app.route('/sematch/api/types')
def types():
    query = request.args.get('query')
    return json.dumps(engine.types(query))

@app.route('/sematch/api/entities')
def entities():
    query = request.args.get('query')
    return json.dumps(engine.entities(query))

@app.route('/sematch/api/search')
def search():
    query = request.args.get('query')
    return json.dumps(engine.query(query))

@app.route('/')
def home():
    return template('demo.html')

def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port)

if __name__ == '__main__':
    runserver()