from gensim.models.doc2vec import Doc2Vec
from numpy import array
from gensim import matutils
from sematch.utility import FileIO

CATEGORY2VEC = 'db/categories/cat2vec'

class DocModel:

    def __init__(self, model_file):
        self.model = Doc2Vec.load(FileIO.filename(model_file))

    #Check if category is contained in model
    def check_doc(self, doc):
        if self.model.docvecs.__contains__(doc):
            return True
        else:
            return False

    #return most similar categories
    def similar_doc(self, doc):
        return self.model.docvecs.most_similar(doc)

    #compare category similarity
    def doc_similarity(self, doc1, doc2):
        return self.model.docvecs.similarity(doc1, doc2)

    #compare categories similarity
    def doc_set_similarity(self, docs1, docs2):
        return self.model.docvecs.n_similarity(docs1, docs2)

    #return vector of a category
    def doc_vectorize(self, doc):
        v_doc = matutils.unitvec(self.model.docvecs[doc])
        return v_doc

    #return mean viector of a set of category
    def doc_set_vectorize(self, docs):
        v_docs = [self.model.docvecs[doc] for doc in docs]
        v_docs = matutils.unitvec(array(v_docs).mean(axis=0))
        return v_docs

cat = DocModel(CATEGORY2VEC)
print cat.similar_doc('http://dbpedia.org/resource/Category:NeXT')
print cat.doc_similarity('http://dbpedia.org/resource/Category:X_servers',
                         'http://dbpedia.org/resource/Category:Integrated_development_environments')
print cat.doc_vectorize('http://dbpedia.org/resource/Category:NeXT')
print cat.doc_set_vectorize(['http://dbpedia.org/resource/Category:NeXT','http://dbpedia.org/resource/Category:X_servers'])

