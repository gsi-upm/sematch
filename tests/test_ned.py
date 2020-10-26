

def test_name_dict():
    from sematch.nlp import NameDict
    name = NameDict.load()
    print(name.match('apple'))

def test_embedding():
    from gensim.models.doc2vec import Doc2Vec
    from gensim.models import Word2Vec

def test_candidate_feature():
    pass


def test_evaluation():
    from sematch.utility import FileIO
    query = FileIO.read_json_file('dataset/ned/query_ned_cleaned.txt')
    question = FileIO.read_json_file('dataset/ned/question_ned_cleaned.txt')
    tweet = FileIO.read_json_file('dataset/ned/tweet_ned_cleaned.txt')
    print(len(query))
    print(len(question))
    print(len(tweet))


def test_query_ned():
    from sematch.nlp import FeatureExtractor
    from sematch.nlp import EntityFeature
    from sematch.nlp import SpaCyNLP
    from sematch.utility import FileIO
    from sematch.semantic.relatedness import TextRelatedness
    from sematch.nel import EntityDisambiguation
    import itertools
    sy = SpaCyNLP()
    features = EntityFeature.load(feature_dict_file='models/query_features.json')
    extractor = FeatureExtractor(features, sy.pos_tag)
    ned = EntityDisambiguation(extractor)
    rel = TextRelatedness()
    from sematch.semantic.similarity import WordNetSimilarity
    wns = WordNetSimilarity()
    #print(wns.word_similarity('cooling', 'air_conditioner', 'li'))
    #similarity = lambda x,y : rel.text_similarity(x,y, model='lsa')

    query = FileIO.read_json_file('dataset/ned/query_ned_cleaned.txt')
    query = [q for q in query if extractor.context_features(q['query'])]
    print(len(query))
    import warnings
    warnings.filterwarnings("ignore")
    metrics = ['path', 'wup', 'res', 'lin', 'jcn', 'wpath']
    for m in metrics:
        print(m)
        similarity = lambda x, y: wns.word_similarity(x, y, m)
        for k in range(1, 21):
            gold = []
            predict = []
            for q in query:
                gold.append(q['gold'])
                #e = ned.text_disambiguate(q['query'], q['candidate'], similarity)
                e = ned.word_disambiguate(q['query'], q['candidate'], similarity, K=k)
                predict.append(e)
            from sklearn.metrics import precision_recall_fscore_support
            #from sklearn.metrics import classification_report
            #print classification_report(gold, predict)
            print(precision_recall_fscore_support(gold, predict, average='weighted')[2])

if __name__ == '__main__':
    test_query_ned()
