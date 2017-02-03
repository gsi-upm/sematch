
def test_wordsim_evaluation():
    from sematch.evaluation import WordSimEvaluation
    from sematch.semantic.similarity import WordNetSimilarity
    evaluation = WordSimEvaluation()
    print evaluation.dataset_names()
    wns = WordNetSimilarity()
    # define similarity metrics
    wpath = lambda x, y: wns.word_similarity_wpath(x, y, 0.8)
    # evaluate similarity metrics
    print evaluation.evaluate_metric('wpath', wpath, 'noun_simlex')
    # performa Steiger's Z significance Test
    print evaluation.statistical_test('wpath', 'path', 'noun_simlex')
    wpath_es = lambda x, y: wns.monol_word_similarity(x, y, 'spa', 'path')
    wpath_en_es = lambda x, y: wns.crossl_word_similarity(x, y, 'eng', 'spa', 'wpath')
    print evaluation.evaluate_metric('wpath_es', wpath_es, 'rg65_spanish')
    print evaluation.evaluate_metric('wpath_en_es', wpath_en_es, 'rg65_EN-ES')



def test_classification_evaluation():
    from sematch.evaluation import AspectEvaluation
    from sematch.application import SimClassifier, SimSVMClassifier
    from sematch.semantic.similarity import WordNetSimilarity
    evaluation = AspectEvaluation()
    X, y = evaluation.load_dataset()
    wns = WordNetSimilarity()
    word_sim = lambda x, y: wns.word_similarity(x, y)
    simclassifier = SimClassifier.train(zip(X,y), word_sim)
    evaluation.evaluate(X,y, simclassifier)
    simSVMclassifier = SimSVMClassifier.train(X, y, word_sim)
    evaluation.evaluate(X, y, simSVMclassifier)