

def test_extraction():
    from sematch.nlp import Extraction
    from sematch.sparql import EntityFeatures
    entity_f = EntityFeatures()
    yin_and_yang = entity_f.features('http://dbpedia.org/resource/Yin_and_yang')
    assert yin_and_yang is not None
    extract = Extraction()
    assert 'Chinese' in extract.extract_chunks_doc(yin_and_yang['abstract'])
    assert 'philosophy' in extract.extract_words_doc(yin_and_yang['abstract'])
