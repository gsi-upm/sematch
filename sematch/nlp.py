from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer, SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import RegexpParser
from collections import Counter
import string

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

SpecialWords = ['.', ',', '?', '"', '``', "''", "'", '--', '-', ':', ';', '(',
             ')', '$', '000', '1', '2', '10,' 'I', 'i', 'a',]

punctuations = string.punctuation

noun_pos = ['nn','nns','nn$','nn-tl','nn+bez','nn+hvz','nns$', 'np', \
                           'np$', 'np+bez', 'nps', 'nps$', 'nr', 'np-tl', 'nrs', 'nr$']

#r'(?u)\b\w\w+\b'
#r'[a-z]+'
#r'\w+'
#r'''(?x)
#([A-Z]\.)+        # abbreviations, e.g. U.S.A.
#| \w+(-\w+)*        # words with optional internal hyphens
#| \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
#| \w+[\x90-\xff]  # these are escaped emojis
#| [][.,;"'?():-_`]  # these are separate tokens
#'''

tokenization_pattern = r'\w+'
noun_chunk_pattern = r"T: {<(JJ|NN|NNS|NNP|NNPS)>+<(NN|NNS|NNP|NNPS|CD)>|<(NN|NNS|NNP|NNPS)>}"

reg_tokenizer = RegexpTokenizer(tokenization_pattern)
chunk_parser = RegexpParser(noun_chunk_pattern)

lemma = WordNetLemmatizer()
porter = PorterStemmer()
lancaster = LancasterStemmer()


def reg_tokenize(text):
    return reg_tokenizer.tokenize(text)

def remove_stopwords(tokens):
    return [w for w in tokens if w.lower() not in StopWords]

def clean_context(text):
    tokens = reg_tokenize(text)
    tokens = remove_stopwords(tokens)
    return ' '.join(tokens)

def is_noun(tag):
    return tag.lower() in noun_pos

def word_tokenize(text):
    tokens = reg_tokenize(text.lower())
    tokens = [w for w in tokens if w not in StopWords]
    tokens = [w for w in tokens if w not in FunctionWords]
    return tokens

def lemmatization(tokens):
    tokens = [lemma.lemmatize(w) for w in tokens]
    #tokens = [porter.stem(w) for w in tokens]
    return tokens

def feature_words_of_category(corpus):
    '''
    sentence and category pairs
    '''
    cat_word = {}
    for words, cat in corpus:
        cat_word.setdefault(cat, []).extend(lemmatization(word_tokenize(words)))
    return {cat:Counter(cat_word[cat]) for cat in cat_word}

def noun_phrases(tags):
    phrases = []
    for subtree in chunk_parser.parse(tags).subtrees():
        if subtree.label() == 'T':
            labels = subtree.leaves()
            labels = [x for x, y in labels]
            phrases.append(' '.join(labels))
    return phrases

