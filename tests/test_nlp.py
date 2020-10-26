

def test_extraction():
    from sematch.nlp import Extraction
    from sematch.semantic.sparql import EntityFeatures
    upm = EntityFeatures().features('http://dbpedia.org/resource/Technical_University_of_Madrid')
    extract = Extraction()
    assert extract.extract_nouns(upm['abstract']) is not None
    assert extract.extract_verbs(upm['abstract']) is not None
    assert extract.extract_chunks_doc(upm['abstract']) is not None
    cats = extract.category_features(upm['category'])
    assert extract.category2words(cats) is not None



def test_rake():
    from sematch.nlp import RAKE
    from sematch.semantic.sparql import EntityFeatures
    upm = EntityFeatures().features('http://dbpedia.org/resource/Technical_University_of_Madrid')
    rake = RAKE()
    assert rake.extract(upm['abstract']) is not None


def test_TFIDF():
    corpus = ['This is the first document.','This is the second second document.','And the third one.','Is this the first document?',]
    from sematch.nlp import TFIDF
    tfidf = TFIDF(corpus)
    assert tfidf.idf('document') is not None
    assert tfidf.tfidf('I need a document and second') is not None


def test_Spacy():
    from sematch.nlp import SpaCyNLP
    sy = SpaCyNLP()
    print(sy.pos_tag(u'This is the second second document.'))

def test_feature_extractor():
    from sematch.nlp import FeatureExtractor
    from sematch.nlp import EntityFeature
    from sematch.nlp import SpaCyNLP
    from sematch.utility import FileIO
    import itertools
    sy = SpaCyNLP()
    w_extractor = FeatureExtractor(sy.pos_tag)
    features = EntityFeature.load(feature_dict_file='models/query_features.json')
    query = FileIO.read_json_file('dataset/ned/query_ned_cleaned.txt')
    candidates = list(itertools.chain.from_iterable(map(lambda x: x['candidate'], query)))
    set_candidates = list(set(candidates))
    for can in set_candidates[:10]:
        print(w_extractor.entity_word_features([can], features))


def test_entity_feature():
    from sematch.utility import FileIO
    from sematch.nlp import EntityFeature
    query = FileIO.read_json_file('dataset/ned/query_ned_cleaned.txt')
    question = FileIO.read_json_file('dataset/ned/question_ned_cleaned.txt')
    tweet = FileIO.read_json_file('dataset/ned/tweet_ned_cleaned.txt')
    import itertools
    candidates = list(itertools.chain.from_iterable(map(lambda x:x['candidate'], question)))
    set_candidates = list(set(candidates))
    print(len(set_candidates))
    EntityFeature.candidate_features(set_candidates, export_file='models/question_features.json')


if __name__ == '__main__':
    test_feature_extractor()
