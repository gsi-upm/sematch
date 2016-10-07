
def test_simcat_classifier():
    from sematch.classification import SimCatClassifier
    from sematch.evaluation import ABSAEvaluation
    from sematch.semantic.similarity import WordNetSimilarity
    # defining similarity metric
    wns = WordNetSimilarity()
    sim_metric_jcn = lambda x, y: wns.word_similarity(x, y, 'jcn')
    sim_metric_wpath = lambda x, y: wns.word_similarity_wpath(x, y, 0.9)
    # loadding dataset
    absa_eval = ABSAEvaluation()
    X_train_16, y_train_16 = absa_eval.load_dataset('eval/aspect/ABSA16_Restaurants_Train_SB1_v2.xml')
    X_test_16, y_test_16 = absa_eval.load_dataset('eval/aspect/ABSA16_Restaurants_Train_SB1_v2.xml')
    # train the classifiers
    sim_jcn_classifier = SimCatClassifier.train(zip(X_train_16, y_train_16), sim_metric_jcn)
    sim_wpath_classifier = SimCatClassifier.train(zip(X_train_16, y_train_16), sim_metric_wpath)
    # evaluate the classifiers
    #absa_eval.evaluate(X_test_16, y_test_16, sim_jcn_classifier)
    #absa_eval.evaluate(X_test_16, y_test_16, sim_wpath_classifier)
    assert sim_jcn_classifier is not None
    assert sim_wpath_classifier is not None
