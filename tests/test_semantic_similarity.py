# -*- coding: utf-8 -*-

def test_wordnet_similarity():
    from sematch.semantic.similarity import WordNetSimilarity
    wns = WordNetSimilarity()
    dog = wns.word2synset('dog')
    cat = wns.word2synset('cat')
    # Measuring semantic similarity between concepts using Path method
    assert wns.similarity(dog[0], cat[0], 'path') is not None # 0.2
    # Computing English word similarity using Li method
    assert wns.word_similarity('dog', 'cat', 'li') is not None# 0.449327301063
    # Computing Spanish word similarity using Lin method
    assert wns.monol_word_similarity('perro', 'gato', 'spa', 'lin') is not None#0.876800984373
    # Computing Chinese word similarity using  Wu & Palmer method
    assert wns.monol_word_similarity('狗', '猫', 'cmn', 'wup') is not None# 0.857142857143
    # Computing Spanish and English word similarity using Resnik method
    assert wns.crossl_word_similarity('perro', 'cat', 'spa', 'eng', 'res') is not None#7.91166650904
    # Computing Spanish and Chinese word similarity using Jiang & Conrad method
    assert wns.crossl_word_similarity('perro', '猫', 'spa', 'cmn', 'jcn') is not None#0.31023804699
    # Computing Chinese and English word similarity using WPath method
    assert wns.crossl_word_similarity('狗', 'cat', 'cmn', 'eng', 'wpath') is not None#0.593666388463


def test_yagotype_similarity():
    from sematch.semantic.similarity import YagoTypeSimilarity
    yagosim = YagoTypeSimilarity()
    dancer = yagosim.word2yago('dancer')
    actor = yagosim.word2yago('actor')
    singer = yagosim.word2yago('singer')
    assert yagosim.yago2synset(actor[0]) is not None
    assert yagosim.yago_similarity(dancer[0], actor[0], 'wpath') is not None
    assert yagosim.yago_similarity(singer[0], actor[0], 'wpath') is not None
    assert yagosim.word2yago('university') is not None
    assert yagosim.yago2synset('http://dbpedia.org/class/yago/EducationalInstitution108276342') is not None
    assert yagosim.yago2synset('http://dbpedia.org/class/yago/Organization108008335') is not None
    assert yagosim.yago2synset('http://dbpedia.org/class/yago/Institution108053576') is not None
    assert yagosim.yago2synset('http://dbpedia.org/class/yago/Organization108008335') is not None
    #using corpus-based IC from brown corpus
    assert yagosim.word_similarity('dancer', 'actor', 'wpath') is not None
    #using graph-based IC from DBpedia
    assert yagosim.word_similarity('dancer', 'actor', 'wpath_graph') is not None

def test_concept_similarity():
    from sematch.semantic.graph import DBpediaDataTransform, Taxonomy
    from sematch.semantic.similarity import ConceptSimilarity
    concept_sim = ConceptSimilarity(Taxonomy(DBpediaDataTransform()), 'models/dbpedia_type_ic.txt')
    c1 = concept_sim.name2concept('species')
    c2 = concept_sim.name2concept('organ')
    uri1 = concept_sim.name2uri('species')
    uri2 = concept_sim.name2uri('organ')
    assert uri1 is not None
    assert uri2 is not None
    assert concept_sim.similarity(c1, c2) is not None
