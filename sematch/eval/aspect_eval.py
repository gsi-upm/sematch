from BeautifulSoup import BeautifulSOAP as bs
from sematch.nlp import feature_words_of_category
from sematch.eval.utility import generate_report
from sematch.utility import FileIO
#from sematch.eval.plot_tool import generate_plot
from sematch.semantic.aspect import WeightedSimAspect, MaxSimAspect


ABSA15Restu_Train =  FileIO.filename('eval/aspect/ABSA-15_Restaurants_Train_Final.xml')
ABSA15Restu_Test =  FileIO.filename('eval/aspect/ABSA15_Restaurants_Test.xml')
ABSA16Restu_Train =  FileIO.filename('eval/aspect/ABSA16_Restaurants_Train_SB1_v2.xml')
ABSA16Restu_Test =  FileIO.filename('eval/aspect/ABSA16_Restaurants_Test_Gold.xml')

def extract_pairs(dataset):
    pairs = []
    with open(dataset, 'r') as f:
        corpus = f.read()
        opinions = bs(corpus).findAll('opinion')
        for op in opinions:
            if not op['target'] == 'NULL':
                t = op['target']
                #c = op['category'].split('#')[0]
                c = op['category']
                pairs.append((t, c))
    return pairs

def extract_feature_words(data, num):
    feature = {}
    for key in data:
        words, counts = zip(*data[key].most_common(num))
        feature[key] = list(words)
    return feature

class AspectEval:

    def __init__(self):
        self.absa15_train = extract_pairs(ABSA15Restu_Train)
        self.absa15_test = extract_pairs(ABSA15Restu_Test)
        self.absa16_train = extract_pairs(ABSA16Restu_Train)
        self.absa16_test = extract_pairs(ABSA16Restu_Test)
        self.datasets = self.absa15_train + self.absa15_test + self.absa16_train +self.absa16_test
        self.feature_num = 5
        self.featureset = feature_words_of_category(self.datasets)
        self.classifier = WeightedSimAspect.train(self.featureset, self.feature_num)

    def evaluate_sim_method(self, classifier, pairs, method):
        predict = []
        gold = []
        for t, c in pairs:
            gold.append(c)
            p = classifier.classify(t, method)
            predict.append(p)
        return gold, predict, list(set(gold))

    def run_evaluation(self, sim_method='path'):
        # sim_method = ['path','wpath','lch','wup','li','res','lin','jcn']
        print sim_method
        print 4 ** 2 * '----'
        g, p, l = self.evaluate_sim_method(self.classifier, self.datasets, sim_method)
        generate_report(g,p,l)
        #generate_plot(g,p,l, 'Confusion Matrix of '+sim_method)



