
from __future__ import division

from scipy.stats import spearmanr
from scipy.stats import pearsonr

from sematch.semantic.similarity import YagoTypeSimilarity
from sematch.utility import FileIO

import numpy as np
from scipy.stats import t, norm
from math import atanh, pow
from numpy import tanh


class SteigerTest:

    """
    Functions for calculating the statistical significant differences between two dependent or independent correlation
    coefficients.The Fisher and Steiger method is adopted from the R package http://personality-project.org/r/html/paired.r.html
    and is described in detail in the book 'Statistical Methods for Psychology'
    The Zou method is adopted from http://seriousstats.wordpress.com/2012/02/05/comparing-correlations/
    Credit goes to the authors of above mentioned packages!
    Author: Philipp Singer (www.philippsinger.info)

    This is the class based on the original implementation from Philipp.

    """
    def __init__(self, confidence=None):
        self._confidence = confidence if confidence else 0.95

    def rz_ci(self, r, n):
        zr_se = pow(1/(n - 3), .5)
        moe = norm.ppf(1 - (1 - self._confidence)/float(2)) * zr_se
        zu = atanh(r) + moe
        zl = atanh(r) - moe
        return tanh((zl, zu))

    def rho_rxy_rxz(self, rxy, rxz, ryz):
        num = (ryz-1/2.*rxy*rxz)*(1-pow(rxy,2)-pow(rxz,2)-pow(ryz,2))+pow(ryz,3)
        den = (1 - pow(rxy,2)) * (1 - pow(rxz,2))
        return num/float(den)

    def dependent_corr(self, xy, xz, yz, n, twotailed=False, method='steiger'):
        """
        Calculates the statistic significance between two dependent correlation coefficients
        @param xy: correlation coefficient between x and y
        @param xz: correlation coefficient between x and z
        @param yz: correlation coefficient between y and z
        @param n: number of elements in x, y and z
        @param twotailed: whether to calculate a one or two tailed test, only works for 'steiger' method
        @param conf_level: confidence level, only works for 'zou' method
        @param method: defines the method uses, 'steiger' or 'zou'
        @return: t and p-val
        """
        if method == 'steiger':
            d = xy - xz
            determin = 1 - xy * xy - xz * xz - yz * yz + 2 * xy * xz * yz
            av = (xy + xz)/2
            cube = (1 - yz) * (1 - yz) * (1 - yz)

            t2 = d * np.sqrt((n - 1) * (1 + yz)/(((2 * (n - 1)/(n - 3)) * determin + av * av * cube)))
            p = 1 - t.cdf(abs(t2), n - 3)

            if twotailed:
                p *= 2

            return t2, p
        elif method == 'zou':
            L1 = self.rz_ci(xy, n)[0]
            U1 = self.rz_ci(xy, n)[1]
            L2 = self.rz_ci(xz, n)[0]
            U2 = self.rz_ci(xz, n)[1]
            rho_r12_r13 = self.rho_rxy_rxz(xy, xz, yz)
            lower = xy - xz - pow((pow((xy - L1), 2) + pow((U2 - xz), 2) - 2 * rho_r12_r13 * (xy - L1) * (U2 - xz)), 0.5)
            upper = xy - xz + pow((pow((U1 - xy), 2) + pow((xz - L2), 2) - 2 * rho_r12_r13 * (U1 - xy) * (xz - L2)), 0.5)
            return lower, upper
        else:
            raise Exception('Wrong method!')

    def independent_corr(self, xy, ab, n, n2 = None, twotailed=True, method='fisher'):
        """
        Calculates the statistic significance between two independent correlation coefficients
        @param xy: correlation coefficient between x and y
        @param xz: correlation coefficient between a and b
        @param n: number of elements in xy
        @param n2: number of elements in ab (if distinct from n)
        @param twotailed: whether to calculate a one or two tailed test, only works for 'fisher' method
        @param conf_level: confidence level, only works for 'zou' method
        @param method: defines the method uses, 'fisher' or 'zou'
        @return: z and p-val
        """

        if method == 'fisher':
            xy_z = 0.5 * np.log((1 + xy)/(1 - xy))
            ab_z = 0.5 * np.log((1 + ab)/(1 - ab))
            if n2 is None:
                n2 = n

            se_diff_r = np.sqrt(1/(n - 3) + 1/(n2 - 3))
            diff = xy_z - ab_z
            z = abs(diff / se_diff_r)
            p = (1 - norm.cdf(z))
            if twotailed:
                p *= 2

            return z, p
        elif method == 'zou':
            L1 = self.rz_ci(xy, n)[0]
            U1 = self.rz_ci(xy, n)[1]
            L2 = self.rz_ci(ab, n2)[0]
            U2 = self.rz_ci(ab, n2)[1]
            lower = xy - ab - pow((pow((xy - L1), 2) + pow((U2 - ab), 2)), 0.5)
            upper = xy - ab + pow((pow((U1 - xy), 2) + pow((ab - L2), 2)), 0.5)
            return lower, upper
        else:
            raise Exception('Wrong method!')



class WordSimDataset:
    """
    This class is used to prepare and separate word similarity datasets.

    """

    def __init__(self):
        self._yago = YagoTypeSimilarity()

    def load_dataset(self, name):
        data = FileIO.read_list_file('eval/lexical/%s' % name)
        print "dataset ", name, " ", len(data), " word pairs"
        word_pairs = map(lambda x: (x.split()[0], x.split()[1]), data)
        human = map(float, map(lambda x: x.split()[2], data))
        return word_pairs, human

    def load_result(self, name):
        data = FileIO.read_list_file('eval/results/%s' % name)
        methods = data[0].split()[2:]
        scores = {m: [] for m in methods}
        for r in data[1:]:
            items = r.split()[2:]
            for i in range(len(items)):
                scores[methods[i]].append(float(items[i]))
        return scores

    #check if lcs word is used as type in DBpedia
    def check_word_graph(self, w1, w2):
        s1, s2 = self._yago.best_synset_pair(w1, w2)
        lcs = self._yago.least_common_subsumer(s1, s2)
        yago_concept = self._yago.synset2yago(lcs)
        graph_ic = self._yago._graph_ic.concept_ic(yago_concept)
        return True if graph_ic else False


    #check if both words are used as type in DBpedia
    def check_word_type(self, w1, w2):
        s1, s2 = self._yago.best_synset_pair(w1, w2)
        yago_concept_1 = self._yago.synset2yago(s1)
        yago_concept_2 = self._yago.synset2yago(s2)
        graph_ic_1 = self._yago._graph_ic.concept_ic(yago_concept_1)
        graph_ic_2 = self._yago._graph_ic.concept_ic(yago_concept_2)
        return True if graph_ic_1 and graph_ic_2 else False

    #check if both words are in WordNet Noun Taxonomy
    def check_word_noun(self, w1, w2):
        s1 = self._yago.word2synset(w1)
        s2 = self._yago.word2synset(w2)
        return True if s1 and s2 else False

    def separate_dataset(self, in_file, out_file, check_function):
        out_data = []
        word_pairs, human = self.load_dataset(in_file)
        for i, pairs in enumerate(word_pairs):
            w1, w2 = pairs
            h = human[i]
            if check_function(w1, w2):
                out_data.append(' '.join([w1, w2, str(h)]))
        FileIO.save_list_file('eval/lexical/%s' % out_file, out_data)

class WordSimEvaluation:

    def __init__(self, metric='Spearman'):
        self._dataset = WordSimDataset()
        self._steiger_test = SteigerTest()
        self._correlation = lambda x, y: spearmanr(x, y) if metric == 'Spearman' else lambda x, y: pearsonr(x, y)

    def evaluate_wpath_k(self, dataset, save_results=False):
        word_pairs, human = self._dataset.load_dataset(dataset)
        for k in range(1, 11):
            sims = [self._dataset._yago.word_similarity_wpath(w1, w2, k/10.0) for w1, w2 in word_pairs]
            sims = map(lambda x:round(x, 3), sims)
            cor = self._correlation(sims, human)[0]
            cor = "%.3f" % round(cor, 3)
            print k, ' ', cor

    def evaluate_sim_metric(self, sim_func, dataset, save_results=False):
        sim = [self.sim.word_similarity(w1,w2,m) for w1,w2 in dataset.pairs()]
        sim = map(lambda x:round(x,3), sim)
        cor = self.correlation(cor_measure)(sim, dataset.human())[0]
        cor = "%.3f" % round(cor,3)
        print m, ' ', cor

    def statistical_test(self):
        pass

    def sim_eval_file(self, methods, dataset):
        result = []
        result.append(' '.join(['word1','word2']+methods))
        for w1,w2 in dataset.pairs():
            scores = [self.sim.word_similarity(w1,w2,m) for m in methods]
            scores = map(lambda x:"%.3f" % round(x,3), scores)
            result.append(' '.join([w1,w2]+scores))
        FileIO.save_list_file('eval/results/%s'% dataset.name, result)

    def sim_eval_analysis_file(self, cor_measure, filename):
        print filename
        dataset = Dataset(filename)
        result = Result(filename)
        ratings = result.ratings()
        for key in ratings:
            cor = self.correlation(cor_measure)(ratings[key], dataset.human())[0]
            cor = "%.3f" % round(cor,3)
            print key, ' ', cor


# data = FileIO.read_list_file('eval/lexical/SimLex-999.txt')
# data = data[1:]
# data_p = []
# for d in data:
#     l = d.split()
#     if l[2] == 'N':
#         data_p.append(' '.join([l[0],l[1],l[3]]))
# FileIO.save_list_file('eval/lexical/simlex_n.txt',data_p)

#   word similarity of noun
#   noun_rg.txt
#   noun_mc.txt
#   noun_ws353.txt
#   noun_ws353-sim.txt
#   noun_simlex.txt

#   the lcs is in knowledge graph
#   graph_rg.txt
#   graph_mc.txt
#   graph_ws353.txt
#   graph_ws353-sim.txt
#   graph_simlex.txt

#   both words are in knowledge graph
#   type_rg.txt
#   type_mc.txt
#   type_ws353.txt
#   type_ws353-sim.txt
#   type_simlex.txt

# eval = Evaluation()
# sim_methods_noun = ['path','lch','wup','li','res','lin','jcn','wpath']
# sim_methods_graph = ['path','lch','wup','li','res','res_graph','lin','jcn','wpath','wpath_graph']
# sim_methods_type = ['path','lch','wup','li','res','res_graph','lin','lin_graph','jcn','jcn_graph','wpath','wpath_graph']
word_noun = ['noun_rg.txt','noun_mc.txt','noun_ws353.txt','noun_ws353-sim.txt','noun_simlex.txt']
# word_graph = ['graph_rg.txt','graph_mc.txt','graph_ws353.txt','graph_ws353-sim.txt','graph_simlex.txt']
# word_type = ['type_rg.txt','type_mc.txt','type_ws353.txt','type_ws353-sim.txt','type_simlex.txt']
# datasets = [Dataset(f) for f in word_type]
# for d in datasets:
#     eval.sim_eval_file(sim_methods_type, d)
# for f in word_type:
#     eval.sim_eval_analysis_file('spearman', f)
#datasets = ['noun_rg.txt']
#datasets = [Dataset(d) for d in datasets]
#for d in datasets:
#    eval.sim_eval_file(sim_methods,d)
#for d in datasets:
#    check_words = eval.check_word_graph
    #check_words = eval.check_word_type
    #check_words = eval.check_word_noun
#    eval.create_sub_dataset(d, check_words, 'graph_simlex.txt')
#eval.sim_eval_analysis_file('spearman','noun_rg.txt')
# for d in datasets:
#     eval.sim_eval_wpath_k('spearman', 'wpath_graph', d)

path = [0.781, 0.724, 0.314, 0.618, 0.584]
lch = [0.781, 0.724, 0.314, 0.618, 0.584]
wup = [0.755, 0.729, 0.348, 0.633, 0.542]
li = [0.787, 0.719, 0.337, 0.636, 0.586]
res = [0.776, 0.733, 0.347, 0.637, 0.535]
lin = [0.784, 0.752, 0.310, 0.609, 0.582]
jcn = [0.775, 0.820, 0.292, 0.592, 0.579]
wpath = [0.795, 0.740, 0.349, 0.652, 0.603]

method_human = {'path':path, 'lch':lch, 'wup':wup, 'li':li, 'res':res, 'lin':lin, 'jcn':jcn, 'wpath':wpath}

def steiger_test(dataset, method, index):
    ratings = Result(dataset).ratings()
    N = len(ratings[method])
    rate_x = ratings[method]
    for y in ratings.keys():
        if not method == y:
            rate_y = ratings[y]
            print method, y
            cor = spearmanr(rate_x, rate_y)[0]
            xy = round(cor, 3) # correlation x method with y method
            xz = method_human[method][index] #correlation x method with human
            yz = method_human[y][index] #correlation y method with human
            print 'xz, yz, xy, N :', xz, yz, xy, N
            tmp = dependent_corr(xz, yz, xy, N, method='steiger')[1]
            if tmp < 0.05:
                print 'Significant: ', tmp
            else:
                print 'Not Significant: ', tmp

steiger_test('noun_simlex.txt', 'wpath', 4)


