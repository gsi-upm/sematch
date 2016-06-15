from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from itertools import groupby
from nltk.chunk import RegexpParser
from sematch.utility import FileIO
from sematch.nlp import StopWords


STANFORD_TAGGER = FileIO.filename('lib/stanford/stanford-postagger.jar')
STANFORD_MODEL = FileIO.filename('lib/stanford/models/')
STANFORD_NER = FileIO.filename('lib/stanford-ner/stanford-ner.jar')
STANFORD_NER_MODEL = FileIO.filename('lib/stanford-ner/classifiers/')

stanford_tagger_lower = StanfordPOSTagger(STANFORD_MODEL+'english-caseless-left3words-distsim.tagger',STANFORD_TAGGER)
stanford_tagger = StanfordPOSTagger(STANFORD_MODEL+'english-left3words-distsim.tagger',STANFORD_TAGGER)
stanford_ner = StanfordNERTagger(STANFORD_NER_MODEL+'english.conll.4class.distsim.crf.ser.gz',STANFORD_NER)
#stanford_ner = StanfordNERTagger(STANFORD_NER_MODEL+'english.conll.4class.caseless.distsim.crf.ser.gz',STANFORD_NER)

stanford_tokenizer = StanfordTokenizer(STANFORD_TAGGER)

def stanford_tokenize(text):
    return stanford_tokenizer.tokenize(text)

chunk_grammar = """CHUNK: {<NNP><IN><DT><NNS>}
                                 {<NNP><NNP><NNP><NNP>}
                                 {<NNP|NNPS><NNP|NNPS><NNP|NNPS>}
                                 {<NNP|NNPS><NNP|NNPS>}
                                 {<NN|NNS><NNP|NNPS>}
                                 {<NNP|NNPS><NN|NNS>}
                                 {<NNP|NNPS>+}
                                 {<NN|NNS><NN|NNS>+}"""


chunk_parser = RegexpParser(chunk_grammar)


def phrase_chunk(text):
    # print self.tags
    phrases = []
    tokens = stanford_tokenize(text)
    tags = stanford_tagger_lower.tag(tokens)
    for subtree in chunk_parser.parse(tags).subtrees():
        if subtree.label() == 'CHUNK':
            labels = subtree.leaves()
            labels = [x for x, y in labels]
            phrases.append(' '.join(labels))
    return phrases


def entity_recognition(text):
    entities = []
    tokens = stanford_tokenize(text)
    tags = stanford_ner.tag(tokens)
    print tags
    for tag, chunk in groupby(tags, lambda x: x[1]):
        if tag != "O":
            entities.append((" ".join(w for w, t in chunk), tag))
    return entities


class Text:

    def __init__(self, tokenize=stanford_tokenize, tagger=stanford_tagger,):
        self.tokenize = tokenize
        self.pos = tagger

    def extract_entity_by_chunking(self,text):
        return phrase_chunk(text)

    def extract_entity_by_ner(self, text):
        return entity_recognition(text)

    #common nouns
    def common_nouns(self, text):
        tags = self.tagger.tag(self.tokenize(text))
        return [x for x,y in self.tags if y in ['NN', 'NNS']]

class WebQuestion(Text):

    def __init__(self, text):
        Text.__init__(self,text, tokenize=stanford_tokenize, tagger=stanford_tagger_lower)

