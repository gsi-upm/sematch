

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
