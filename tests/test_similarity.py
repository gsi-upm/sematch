# -*- coding: utf-8 -*-

def test_word_similarity():
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


def test_yago_concept_similarity():
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

def test_dbpedia_concept_similarity():
    from sematch.semantic.graph import DBpediaDataTransform, Taxonomy
    from sematch.semantic.similarity import ConceptSimilarity
    concept_sim = ConceptSimilarity(Taxonomy(DBpediaDataTransform()), 'models/dbpedia_type_ic.txt')
    c1 = concept_sim.name2concept('species')
    c2 = concept_sim.name2concept('organ')
    print c1, c2
    print concept_sim.hyponyms('http://dbpedia.org/ontology/Instrument')
    print concept_sim.hypernyms('http://dbpedia.org/ontology/Instrument')
    print concept_sim.similarity('http://dbpedia.org/ontology/Guitar', 'http://dbpedia.org/ontology/Organ')
    print concept_sim.similarity('http://dbpedia.org/ontology/Guitar', 'http://dbpedia.org/ontology/Organ', 'path')
    print concept_sim.similarity('http://dbpedia.org/ontology/Guitar', 'http://dbpedia.org/ontology/Organ', 'wup')

def test_synset_expand():
    from sematch.semantic.similarity import WordNetSimilarity
    wns = WordNetSimilarity()
    cat = wns.word2synset('cat')[0]
    assert wns.synset_expand(cat) is not None

def test_entity_similarity():
    from sematch.semantic.similarity import EntitySimilarity
    entity_sim = EntitySimilarity()
    assert entity_sim.similarity('http://dbpedia.org/resource/Madrid',
                                 'http://dbpedia.org/resource/Barcelona') is not None
    assert entity_sim.relatedness('http://dbpedia.org/resource/Madrid', 'http://dbpedia.org/resource/Barcelona') is not None

# from sematch.semantic.similarity import EntitySimilarity
# entity_sim = EntitySimilarity()
# print entity_sim.similarity('http://dbpedia.org/resource/Madrid',
#                             'http://dbpedia.org/resource/Barcelona')
# print entity_sim.similarity('http://dbpedia.org/resource/Apple_Inc.',
#                             'http://dbpedia.org/resource/Steve_Jobs')
#
# print entity_sim.relatedness('http://dbpedia.org/resource/Madrid',
#                              'http://dbpedia.org/resource/Barcelona')
# print entity_sim.relatedness('http://dbpedia.org/resource/Apple_Inc.',
#                              'http://dbpedia.org/resource/Steve_Jobs')

# from sematch.semantic.similarity import YagoTypeSimilarity
# yagosim = YagoTypeSimilarity()
# print yagosim.yago_similarity('http://dbpedia.org/class/yago/Dancer109989502',
#                         'http://dbpedia.org/class/yago/Actor109765278', 'wpath')
# print yagosim.yago_similarity('http://dbpedia.org/class/yago/Dancer109989502',
#                         'http://dbpedia.org/class/yago/Singer110599806', 'wpath')
# print yagosim.yago_similarity('http://dbpedia.org/class/yago/Dancer109989502',
#                         'http://dbpedia.org/class/yago/Actor109765278', 'wpath_graph')
# print yagosim.yago_similarity('http://dbpedia.org/class/yago/Dancer109989502',
#                         'http://dbpedia.org/class/yago/Singer110599806', 'wpath_graph')

# from sematch.semantic.graph import DBpediaDataTransform, Taxonomy
# from sematch.semantic.similarity import ConceptSimilarity
# concept_sim = ConceptSimilarity(Taxonomy(DBpediaDataTransform()), 'models/dbpedia_type_ic.txt')
# c1 = concept_sim.name2concept('actor')
# c2 = concept_sim.name2concept('film')
# print c1, c2
# print concept_sim.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'path')
# print concept_sim.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'wup')
# print concept_sim.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'li')
# print concept_sim.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'res')
# print concept_sim.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'lin')
# print concept_sim.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'jcn')
# print concept_sim.similarity('http://dbpedia.org/ontology/Actor', 'http://dbpedia.org/ontology/Film', 'wpath')
#




