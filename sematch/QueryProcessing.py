import nltk

class Query:

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
