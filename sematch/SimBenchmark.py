from nltk.corpus import wordnet as wn
from Similarity import SemanticSimilarity
from Utility import FileIO
from scipy.stats import spearmanr
from scipy.stats import pearsonr
from scipy.stats import kendalltau

class Evaluation():

    def __init__(self):
        self.datasets = ['combined.csv','EN-MC-30.txt','EN-RG-65.txt',\
                         'MEN_dataset_lemma_form_full', 'Mtruk.csv','rw.txt',\
                         'SimLex-999.txt','wordsim_relatedness_goldstandard.txt',\
                         'wordsim_similarity_goldstandard.txt']
        self.semsim = SemanticSimilarity()

    def process_dataset(self,name):
        data = FileIO.read_list_file(name)
        new_data = []
        for d in data:
            d_list = d.split('\t')
            new_data.append('\t'.join([d_list[0], d_list[1], d_list[2]]))
        FileIO.save_list_file('eval-datasets/lexical/7.txt', new_data)

    def load_dataset(self, dataset_id):
        data = FileIO.read_list_file('eval-datasets/lexical/%s.txt' % dataset_id)
        word_pairs = map(lambda x: (x.split()[0], x.split()[1]), data)
        human = [d.split()[2] for d in data]
        return word_pairs,human

    def correlation(self, name):
        def function(x, y):
            return getattr(self, name)(x,y)
        return function

    def spearman(self,x,y):
        return spearmanr(x,y)

    def pearson(self,x,y):
        return pearsonr(x,y)

    def kendal(self,x,y):
        return kendalltau(x,y)

    def sim_measure(self, word_pairs, method):
        scores = [method(x,y) for x,y in word_pairs]
        return scores

    def wordnet(self, name):
        def function(x,y):
            sim = self.semsim.sim(name)
            print x,y
            synsets1 = wn.synsets(x)
            synsets2 = wn.synsets(y)
            scores = [ sim(syn1, syn2) for syn1 in synsets1 for syn2 in synsets2]
            print max(scores)
            return max(scores)
        return function

    def compare_correlation(self, cor_method, scores, human):
        cor = self.correlation(cor_method)(scores,human)
        return cor[0]


# eval = Evaluation()
# sim = eval.wordnet('wup')
# words, human = eval.load_dataset(2)
# scores = eval.sim_measure(words, sim)
# print "correlation ", eval.compare_correlation('spearman', scores, human)

# eval.process_dataset('eval-datasets/lexical/'+eval.datasets[5])
