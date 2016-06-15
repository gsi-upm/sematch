from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
#import spacy

StopWords = stopwords.words('english')

FunctionWords = ['about', 'across', 'against', 'along', 'around', 'at',
                 'behind', 'beside', 'besides', 'by', 'despite', 'down',
                 'during', 'for', 'from', 'in', 'inside', 'into', 'near', 'of',
                 'off', 'on', 'onto', 'over', 'through', 'to', 'toward',
                 'with', 'within', 'without', 'anything', 'everything',
                 'anyone', 'everyone', 'ones', 'such', 'it', 'itself',
                 'something', 'nothing', 'someone', 'the', 'some', 'this',
                 'that', 'every', 'all', 'both', 'one', 'first', 'other',
                 'next', 'many', 'much', 'more', 'most', 'several', 'no', 'a',
                 'an', 'any', 'each', 'no', 'half', 'twice', 'two', 'second',
                 'another', 'last', 'few', 'little', 'less', 'least', 'own',
                 'and', 'but', 'after', 'when', 'as', 'because', 'if', 'what',
                 'where', 'which', 'how', 'than', 'or', 'so', 'before', 'since',
                 'while', 'although', 'though', 'who', 'whose', 'can', 'may',
                 'will', 'shall', 'could', 'be', 'do', 'have', 'might', 'would',
                 'should', 'must', 'here', 'there', 'now', 'then', 'always',
                 'never', 'sometimes', 'usually', 'often', 'therefore',
                 'however', 'besides', 'moreover', 'though', 'otherwise',
                 'else', 'instead', 'anyway', 'incidentally', 'meanwhile']
#r'(?u)\b\w\w+\b'
reg_tokenizer = RegexpTokenizer(r'[a-z]+')
#reg_tokenizer = RegexpTokenizer(r'\w+')

lemma = WordNetLemmatizer()
porter = PorterStemmer()

def reg_tokenize(text):
    return reg_tokenizer.tokenize(text)

def remove_stopwords(tokens):
    return [w for w in tokens if w.lower() not in StopWords]

def clean_context(text):
    tokens = reg_tokenize(text)
    tokens = remove_stopwords(tokens)
    return ' '.join(tokens)

def is_noun(tag):
    return tag.lower() in ['nn','nns','nn$','nn-tl','nn+bez','nn+hvz','nns$', 'np', \
                           'np$', 'np+bez', 'nps', 'nps$', 'nr', 'np-tl', 'nrs', 'nr$']

def word_tokenize(text):
    tokens = reg_tokenize(text.lower())
    tokens = [w for w in tokens if w not in StopWords]
    tokens = [w for w in tokens if w not in FunctionWords]
    return tokens

def lemmatization(tokens):
    tokens = [lemma.lemmatize(w) for w in tokens]
    #tokens = [porter.stem(w) for w in tokens]
    return tokens

# class SpacyNLP:
#
#     #http://textminingonline.com/tag/noun-phrase-extraction
#
#     def __init__(self):
#         self.nlp = spacy.load('en')
#
#     def tokenize(self, text):
#         doc = self.nlp(text)
#         for np in doc.noun_chunks:
#             print np
#         for ent in doc.ents:
#             print ent

