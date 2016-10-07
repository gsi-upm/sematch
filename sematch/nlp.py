from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import RegexpParser
import nltk

from sematch.utility import FileIO
from collections import Counter
import itertools
import string
import re

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
                    ')', '$', '000', '1', '2', '10,' 'I', 'i', 'a', ]
NOUNS = ['nn', 'nns', 'nn$', 'nn-tl', 'nn+bez', 'nn+hvz', 'nns$', 'np',
            'np$', 'np+bez', 'nps', 'nps$', 'nr', 'np-tl', 'nrs', 'nr$']

StopWords = set(StopWords)
FunctionWords = set(FunctionWords)

SpecialWords = set(SpecialWords)
NOUNS = set(NOUNS)

lemma = WordNetLemmatizer()
porter = PorterStemmer()
lancaster = LancasterStemmer()


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

reg_tokenizer = RegexpTokenizer(tokenization_pattern)
def reg_tokenize(text):
    return reg_tokenizer.tokenize(text)

def remove_stopwords(tokens):
    return [w for w in tokens if w.lower() not in StopWords]

def clean_context(text):
    tokens = reg_tokenize(text)
    tokens = remove_stopwords(tokens)
    return ' '.join(tokens)

def is_noun(tag):
    return tag.lower() in NOUNS

def word_tokenize(text):
    tokens = reg_tokenize(text.lower())
    tokens = [w for w in tokens if w not in StopWords]
    tokens = [w for w in tokens if w not in FunctionWords]
    return tokens

def sent_tokenize(text):
    return  re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s').split(text)

def lemmatization(tokens):
    tokens = [lemma.lemmatize(w) for w in tokens]
    #tokens = [porter.stem(w) for w in tokens]
    return tokens

def tokenize(text):
    min_length = 3
    words = map(lambda word: word.lower(), word_tokenize(text))
    words = [word for word in words if word not in StopWords]
    tokens = (list(map(lambda token: porter.stem(token), words)))
    p = re.compile('[a-zA-Z]+')
    return list(filter(lambda token: p.match(token) and len(token) >= min_length, tokens))

def tf_idf(docs):
    from sklearn.feature_extraction.text import TfidfVectorizer
    return TfidfVectorizer(tokenizer=tokenize, min_df=3,
                        max_df=0.90, max_features=3000,
                        use_idf=True, sublinear_tf=True,
                        norm='l2').fit(docs)

def feature_values(doc, vectorizer):
    doc_representation = vectorizer.transform([doc])
    features = vectorizer.get_feature_names()
    return [(features[index], doc_representation[0, index])
                 for index in doc_representation.nonzero()[1]]

class RAKE:

    """
    Implementation of RAKE -- Rapid Automatic Keywords Extraction From Individual Documents
    https://github.com/aneesha/RAKE/blob/master/rake.py

    To make a class for rake python implementation for easy incorporation in other modules.
    """

    def __init__(self, stopwords_file, word_tokenize=None, sent_tokenize=None):
        self._stopwords_pattern = self.build_patterns(self.load_stopwords(stopwords_file))
        self._sent_tokenize = sent_tokenize if sent_tokenize else nltk.sent_tokenize
        self._word_tokenize = word_tokenize if word_tokenize else nltk.word_tokenize

    def load_stopwords(self, filename):
        data = FileIO.read_list_file(FileIO.filename(filename))
        data = [d.split() for d in data[1:]] # skip first line, in case more than one word per line
        data = list(itertools.chain.from_iterable(data))
        return data

    def build_patterns(self, stopwords):
        pattern = lambda x: r'\b' + x + r'(?![\w-])'  # added look ahead for hyphen
        stopword_patterns = map(pattern, stopwords)
        return re.compile('|'.join(stopword_patterns), re.IGNORECASE)

    def candidate_phrases(self, text):
        candidates = []
        for s in self._sent_tokenize(text):
            phrases = re.sub(self._stopwords_pattern, '|', s.strip()).split('|')
            for p in phrases:
                p = p.strip().lower()
                candidates.append(p) if p else None
        return candidates

    def ranking_phrases(self, phrases):
        word_frequency = {}
        word_degree = {}
        for p in phrases:
            words = self._word_tokenize(p)
            degree = len(words) - 1
            for w in words:
                word_frequency.setdefault(w, 0)
                word_frequency[w] += 1
                word_degree.setdefault(w, 0)
                word_degree[w] += degree

        for word in word_frequency:
            word_degree[word] += word_frequency[word]

        word_scorer = lambda x: word_degree[x] / 1.0 * word_frequency[x]
        word_score = {word:word_scorer(word) for word in word_frequency}

        phrase_scorer = lambda x: sum([word_score[word] for word in self._word_tokenize(x)])
        phrase_score = {p:phrase_scorer(p) for p in phrases}

        return phrase_score

    def extract(self, text, ratio=3):
        phrases = self.ranking_phrases(self.candidate_phrases(text))
        phrases = Counter(phrases).most_common(len(phrases.keys()) / ratio)
        phrases, _ = zip(*phrases)
        return phrases

chunk_grammar_nounphrase=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'
#chunk_grammar=r'T: {<(JJ|NN|NNS|NNP|NNPS)>+<(NN|NNS|NNP|NNPS|CD)>|<(NN|NNS|NNP|NNPS)>}'
chunk_grammar_phrases = """CHUNK: {<NNP><IN><DT><NNS>}
    {<NNP><NNP><NNP><NNP>}
    {<NNP|NNPS><NNP|NNPS><NNP|NNPS>}
    {<NNP|NNPS><NNP|NNPS>}
    {<NN|NNS><NNP|NNPS>}
    {<NNP|NNPS><NN|NNS>}
    {<NNP|NNPS>+}
    {<NN|NNS><NN|NNS>+}"""
chunk_grammar_propernouns = """CHUNK: {<NNP><NNP><NNP><NNP>}
    {<NNP|NNPS><NNP|NNPS><NNP|NNPS>}
    {<NNP|NNPS><NNP|NNPS>}
    {<NNP|NNPS>+}"""



class Extraction:

    """This class is used to extract nouns, proper nouns, phrases from text"""

    def __init__(self, word_tokenize=None, sent_tokenize=None,
                 pos_tag=None, stop_words=None, punct=None,
                 grammar=chunk_grammar_propernouns):
        self._word_tokenize = word_tokenize if word_tokenize else nltk.word_tokenize
        self._sent_tokenize = sent_tokenize if sent_tokenize else nltk.sent_tokenize
        self._pos_tag = pos_tag if pos_tag else nltk.pos_tag
        self._stop_words = stop_words if stop_words else set(nltk.corpus.stopwords.words('english'))
        self._punct = punct if punct else set(string.punctuation)
        self._chunk_grammar = grammar
        self._chunker = RegexpParser(self._chunk_grammar)

    def extract_chunks_sent(self, sent):
        """
        Extract chunk phrases from a sentence.
        :param sent: a sentence level text.
        :return: chunk phrases
        """
        tags = self._pos_tag(self._word_tokenize(sent))
        chunks = nltk.chunk.tree2conlltags(self._chunker.parse(tags))
        # join constituent chunk words into a single chunked phrase
        return [' '.join(word for word, pos, chunk in group)
                  for key, group in itertools.groupby(chunks, lambda (word, pos, chunk): chunk != 'O') if key]

    def extract_chunks_doc(self, text):
        """
        Extract chunk phrases from a document.
        :param text: a document level text
        :return: chunk phrases
        """
        sents = self._sent_tokenize(text)
        sents = [s for s in sents if s]
        return list(itertools.chain.from_iterable(map(self.extract_chunks_sent, sents)))

    def extract_words_sent(self, sent, good_tags=set(['NN', 'NNS'])):
        """
        Extract desired words from a sentence.
        :param sent: a sentence level text
        :param good_tags: desired word tags
        :return: words with desired word tags
        """
        tagged_words = self._pos_tag(self._word_tokenize(sent))
        words = [word for word, tag in tagged_words
                if tag in good_tags and word.lower() not in self._stop_words
                and not all(char in self._punct for char in word)]
        return list(set(words))

    def extract_words_doc(self, text, good_tags=set(['NN', 'NNS'])):
        """
        Extract desiredwords from document
        :param text: a document level text
        :param good_tags: desired word tags
        :return: words with desired word tags
        """
        sents = self._sent_tokenize(text)
        sents = [s for s in sents if s]
        func_extract = lambda x: self.extract_words_sent(x, good_tags)
        words = list(itertools.chain.from_iterable(map(func_extract, sents)))
        return list(set(words))