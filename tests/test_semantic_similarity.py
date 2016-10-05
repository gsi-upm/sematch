# -*- coding: utf-8 -*-



def test_wordnet_similarity():
    from sematch.semantic.similarity import WordNetSimilarity
    wns = WordNetSimilarity()
    assert wns.word_similarity('dog', 'cat') == 0.2
    assert wns.monol_word_similarity('perro', 'gato') == 0.25
    assert wns.crossl_word_similarity('perro', 'cat') == 0.2


def test_yagotype_similarity():
    from sematch.semantic.similarity import YagoTypeSimilarity
    yagosim = YagoTypeSimilarity()
    print yagosim.word2yago('university')

test_yagotype_similarity()