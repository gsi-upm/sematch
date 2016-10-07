

def test_sim_graph():
    from sematch.semantic.graph import SimGraph
    from sematch.semantic.similarity import WordNetSimilarity
    from sematch.nlp import Extraction, lemmatization
    from sematch.sparql import EntityFeatures
    from collections import Counter
    madrid = EntityFeatures().features('http://dbpedia.org/resource/Tom_Cruise')
    words = Extraction().extract_words_sent(madrid['abstract'])
    words = list(set(lemmatization(words)))
    wns = WordNetSimilarity()
    word_graph = SimGraph(words, wns.word_similarity)
    word_scores = word_graph.page_rank()
    words, scores =zip(*Counter(word_scores).most_common(10))
    assert words is not None