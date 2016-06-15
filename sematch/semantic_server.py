from flask import Flask, json, request
import gensim
import os

DEBUG = False
SECRET_KEY = 'Secret_development_key'
app = Flask(__name__)

word2vec = gensim.models.Word2Vec.load('')

@app.route('/api/sim/word2vec')
def word_similarity():
    query = request.args.get('query').split()
    w1 = query[0]
    w2 = query[1]
    return json.dumps(word2vec.similarity(w1,w2))

def runserver():
    port = int(os.environ.get('PORT', 5005))
    app.run(host='localhost', port=port)

if __name__ == '__main__':
    runserver()
