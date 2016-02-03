import nltk
from nltk.tokenize import RegexpTokenizer
from pygoogle import pygoogle

StopWords = nltk.corpus.stopwords.words('english')

def tokenization(query):
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(query)

def remove_stopwords(tokens):
    return [w for w in tokens if w.lower() not in StopWords]

def pos(tokens):
    return nltk.pos_tag(tokens)

def google_search_for_wiki(query):
    wiki = ' site:wikipedia.org'
    query = query + wiki
    g = pygoogle(query)
    g.pages = 5
    #g.rsz = 10
    return g.get_urls()

class QueryProcessor:

    def __init__(self):
        self.stopwords = nltk.corpus.stopwords.words('english')

    def is_noun(self,tag):
        return tag.lower() in ['nn','nns','nn$','nn-tl','nn+bez',\
    'nn+hvz', 'nns$','np','np$','np+bez','nps',\
    'nps$','nr','np-tl','nrs','nr$']

    def tokenization(self, query):
        return nltk.word_tokenize(query)

    def stopword_remove(self, tokens):
        return [w for w in tokens if w.lower() not in self.stopwords]

    def pos(self, tokens):
        return nltk.pos_tag(tokens)

    def ner(self, tokens):
        tagged = self.pos(tokens)
        return nltk.chunk.ne_chunk(tagged)

    def wsd(self, tokens, word):
        return nltk.wsd.lesk(tokens, word,'n')

    def processing(self, query):
        tokens = self.tokenization(query)
        tokens = self.stopword_remove(tokens)
