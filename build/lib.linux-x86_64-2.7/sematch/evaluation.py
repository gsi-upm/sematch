#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2017 Ganggao Zhu- Grupo de Sistemas Inteligentes
# gzhu[at]dit.upm.es
# DIT, UPM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from __future__ import division

from scipy.stats import spearmanr
from scipy.stats import pearsonr

from sematch.semantic.similarity import YagoTypeSimilarity
from sematch.utility import FileIO

import numpy as np
from scipy.stats import t, norm
from math import atanh, pow
from numpy import tanh

from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from nltk import ConfusionMatrix

def generate_report(gold, predict, labels, detailed=True):
    """
    Generate the classification report
    :param gold: the gold label
    :param predict: the predict label
    :param labels: label sets
    :return: none
    """
    if detailed:
        print 'macro averge: ', precision_recall_fscore_support(gold, predict, average='macro')
        print 'micro average: ', precision_recall_fscore_support(gold, predict, average='micro')
        print 'weighted average: ', precision_recall_fscore_support(gold, predict, average='weighted')
    else:
        import warnings
        warnings.filterwarnings("ignore")
    print 'accuracy: ', accuracy_score(gold, predict)
    print classification_report(gold, predict, target_names=labels)
    print ConfusionMatrix(gold, predict)


class SteigerTest:

    """
    This class is used for statistical test for correlations and is based on the original implementation from Philipp.

    Functions for calculating the statistical significant differences between two dependent or independent correlation
    coefficients.The Fisher and Steiger method is adopted from the R package http://personality-project.org/r/html/paired.r.html
    and is described in detail in the book 'Statistical Methods for Psychology'
    The Zou method is adopted from http://seriousstats.wordpress.com/2012/02/05/comparing-correlations/
    Credit goes to the authors of above mentioned packages!
    Author: Philipp Singer (http://www.philippsinger.info/?p=347)
    https://github.com/psinger/CorrelationStats/blob/master/corrstats.py
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

    def independent_corr(self, xy, ab, n, n2 = None, twotailed=False, method='fisher'):
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

    def load_dataset(self, dataset_name):
        """
         This function loads the word similarity dataset

        :param dataset_name: the file name of word similarity dataset
        :return: word pairs and huamn ratings
        """
        data = FileIO.read_list_file('dataset/wordsim/%s.txt' % dataset_name)
        #print "dataset ", dataset_name, " ", len(data), " word pairs"
        word_pairs = map(lambda x: (x.split()[0], x.split()[1]), data)
        human = map(float, map(lambda x: x.split()[2], data))
        return word_pairs, human

    def load_result(self, sim_name, dataset_name):
        """
        This function loads the result of a similarity metric for a specific dataset

        :param sim_name: the name similarity metric
        :param dataset_name: the name of word similarity dataset
        :return: cor relation score and rating scores generated by similarity metric
        """
        data = FileIO.read_list_file('dataset/wordsim/results/%s-%s.txt' % (dataset_name, sim_name))
        data = map(float, data)
        return data[0], data[1:]

    def save_result(self, cor, sim_values, sim_name, dataset_name):
        """
        This function save the result computed by a similarity metric
        :param cor: correlation with human rating
        :param sim_values: similarity scores for word pairs
        :param sim_name: the name of similarity metric
        :param dataset_name: the name of word similarity dataset
        :return:
        """
        data = ["%.3f" % cor]
        data += map(lambda x: "%.3f" % x, sim_values)
        FileIO.save_list_file('dataset/wordsim/results/%s-%s.txt' % (dataset_name, sim_name), data)


    def check_word_graph(self, w1, w2):
        """
         check if lcs word is used as type in DBpedia

        :param w1:
        :param w2:
        :return:
        """
        s1, s2 = self._yago.best_synset_pair(w1, w2)
        lcs = self._yago.least_common_subsumer(s1, s2)
        yago_concept = self._yago.synset2yago(lcs)
        graph_ic = self._yago._graph_ic.concept_ic(yago_concept)
        return True if graph_ic else False


    def check_word_type(self, w1, w2):
        """
        check if both words are used as type in DBpedia
        :param w1:
        :param w2:
        :return:
        """
        s1, s2 = self._yago.best_synset_pair(w1, w2)
        yago_concept_1 = self._yago.synset2yago(s1)
        yago_concept_2 = self._yago.synset2yago(s2)
        graph_ic_1 = self._yago._graph_ic.concept_ic(yago_concept_1)
        graph_ic_2 = self._yago._graph_ic.concept_ic(yago_concept_2)
        return True if graph_ic_1 and graph_ic_2 else False


    def check_word_noun(self, w1, w2):
        """
        check if both words are in WordNet Noun Taxonomy
        :param w1:
        :param w2:
        :return:
        """
        s1 = self._yago.word2synset(w1)
        s2 = self._yago.word2synset(w2)
        return True if s1 and s2 else False

    def separate_dataset(self, in_file, out_file, check_function):
        """
        This function is used to separate the original word similarity dataset.

        word similarity of noun: noun_rg.txt, noun_mc.txt, noun_ws353.txt, noun_ws353-sim.txt, noun_simlex.txt

        the lcs is in knowledge graph: graph_rg.txt, graph_mc.txt, graph_ws353.txt,
        graph_ws353-sim.txt, graph_simlex.txt

        both words are in knowledge graph:  type_rg.txt, type_mc.txt, type_ws353.txt, type_ws353-sim.txt,
        type_simlex.txt

        :param in_file: source dataset file
        :param out_file: target dataset file
        :param check_function: the function of mapping criteria for deciding the word pairs.
        :return:
        """
        out_data = []
        word_pairs, human = self.load_dataset(in_file)
        for i, pairs in enumerate(word_pairs):
            w1, w2 = pairs
            h = human[i]
            if check_function(w1, w2):
                out_data.append(' '.join([w1, w2, str(h)]))
        FileIO.save_list_file('dataset/wordsim/%s.txt' % out_file, out_data)

# data = FileIO.read_list_file('eval/lexical/SimLex-999.txt')
# data = data[1:]
# data_p = []
# for d in data:
#     l = d.split()
#     if l[2] == 'N':
#         data_p.append(' '.join([l[0],l[1],l[3]]))
# FileIO.save_list_file('eval/lexical/noun_simlex.txt',data_p)

class WordSimEvaluation:

    """This class is used for evaluating similarity metrics in word similarity datasets"""

    def __init__(self, metric='Spearman'):
        self._dataset = WordSimDataset()
        self._steiger_test = SteigerTest()
        self._correlation = lambda x, y: spearmanr(x, y) if metric == 'Spearman' else lambda x, y: pearsonr(x, y)

    def dataset_names(self):
        return ['noun_mc', 'noun_rg', 'noun_simlex',
                'noun_ws353', 'noun_ws353-sim', 'rg65_spanish','rg65_EN-ES']

    def evaluate_metric(self, sim_name, sim_func, dataset_name, save_results=False):
        """
        Evaluate a single similarity metric for a dataset

        :param sim_name: the name similarity metric
        :param sim_func: the similarity function
        :param dataset_name: the name of dataset
        :param save_results: True if need to save results
        :return: the correlation of metric with human ratings
        """
        word_pairs, human = self._dataset.load_dataset(dataset_name)
        sim_values = [sim_func(w1, w2) for w1, w2 in word_pairs]
        sim_values = map(lambda x: round(x, 3), sim_values)
        cor = self._correlation(sim_values, human)[0]
        cor = round(cor, 3)
        if save_results:
            self._dataset.save_result(cor, sim_values, sim_name, dataset_name)
        return cor

    def evaluate_multiple_metrics(self, sim_dict, dataset_name):
        """
        Evaluate multiple similarity metrics for a dataset

        :param sim_dict: dictionary of similarity metric name and similarity function
        :param dataset_name: the name of dataset
        :return: a dictionary containing similarity metric name and its correlation with human
        """
        cor_dict = {}
        for sim_name, sim_func in sim_dict.iteritems():
            cor_dict[sim_name] = self.evaluate_metric(sim_name, sim_func, dataset_name, save_results=True)
        return cor_dict

    def evaluate_wpath_k(self, dataset_name, ic='corpus'):
        """
        Evaluate wpath method with different k settings

        :param dataset_name: the name of dataset
        :return: a dictionary containing k settings and its correlation with human
        """
        cor_dic = {}
        for k in range(1, 11):
            if ic == 'corpus':
                sim_func = lambda x, y: self._dataset._yago.word_similarity_wpath(x, y, k/10.0)
            else:
                sim_func = lambda x, y: self._dataset._yago.word_similarity_wpath_graph(x, y, k / 10.0)
            cor_dic[k] = self.evaluate_metric('wpath-'+ str(k), sim_func, dataset_name)
        return cor_dic


    def statistical_test(self, sim_name, compare_name, dataset_name):
        """
        Steiger's Z test on two similarity metrics for a dataset

        :param sim_name: the name of similarity metric
        :param compare_name: the name of comparison similarity metric
        :param dataset_name: the name of dataset
        :return: score of Steiger's Z test and wheter significant or not
        """
        cor_x, scores_x = self._dataset.load_result(sim_name, dataset_name)
        cor_y, scores_y = self._dataset.load_result(compare_name, dataset_name)
        N = len(scores_x)
        cor_z = self._correlation(scores_x, scores_y)[0]
        cor_z = round(cor_z, 3)
        s = self._steiger_test.dependent_corr(cor_x, cor_y , cor_z, N, method='steiger')[1]
        #conf = 1 - self._steiger_test._confidence
        return cor_z, s


class AspectEvaluation:

    """
    This class is used for aspect category classification.
    """
    def __init__(self):
        pass

    def load_dataset(self):
        data = FileIO.read_json_file('dataset/aspect/data.txt')
        X, y = zip(*[(d['text'], d['label']) for d in data])
        return X, y

    def evaluate(self, X, y, classifier, detailed_report=True):
        print "Evaluating..."
        pred = classifier.classify(X)
        generate_report(list(y), list(pred), list(set(y)), detailed_report)


