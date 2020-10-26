

def test_embedding():
    from gensim.models import KeyedVectors
    from sematch.utility import FileIO
    from sematch.semantic.relatedness import WordRelatedness
    model_wiki = KeyedVectors.load_word2vec_format(FileIO.filename('models/w2v-model-enwiki_w2vformat'), binary=True)
    model_news = KeyedVectors.load_word2vec_format(FileIO.filename('models/googlenews.bin'), binary=True)
    rel = WordRelatedness(model_news)
    print(rel.word_similarity('happy','sad'))

def test_category():
    from gensim.models.doc2vec import Doc2Vec
    from sematch.utility import FileIO
    from sematch.semantic.relatedness import ConceptRelatedness
    model_category = Doc2Vec.load(FileIO.filename('models/category/cat2vec'))
    cat2vec_rel = ConceptRelatedness(model_category)
    print(cat2vec_rel.word_similarity('happy','sad'))

def test_text():
    from sematch.semantic.relatedness import TextRelatedness
    text = TextRelatedness()
    print(text.text_similarity('scientist actor','actor', 'tfidf'))
    print(text.text_similarity('scientist', 'researcher', 'lsi'))



if __name__ == '__main__':
    test_embedding()
