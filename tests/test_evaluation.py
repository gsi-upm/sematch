
def test_wordsim_evaluation():
    from sematch.evaluation import WordSimEvaluation
    from sematch.semantic.similarity import WordNetSimilarity
    wordsim_eval = WordSimEvaluation()
    wns = WordNetSimilarity()
    #define similarity metrics
    lin = lambda x, y: wns.word_similarity(x, y, 'lin')
    wpath = lambda x, y: wns.word_similarity_wpath(x, y, 0.8)
    #evaluate similarity metrics
    assert wordsim_eval.evaluate_multiple_metrics({'lin':lin, 'wpath':wpath}, 'noun_simlex') is not None
    #performa Steiger's Z significance Test
    assert wordsim_eval.statistical_test('wpath', 'lin', 'noun_simlex') is not None