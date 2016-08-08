from BeautifulSoup import BeautifulSOAP as bs
from sematch.semantic.wsd import WSD
from sematch.utility import FileIO
import xml.etree.ElementTree as ET
import re

from sematch.nlp import most_common_vocab
from nltk import ConfusionMatrix
from nltk.corpus import wordnet as wn
from nltk.corpus import senseval, semcor
from collections import Counter
import numpy as np
import pandas as pd
import random


#This mapping is copied from stackoverflow
#http://stackoverflow.com/questions/16381218/how-do-i-get-the-definition-for-a-sense-in-nltks-senseval-module
# A map of SENSEVAL senses to WordNet 3.0 senses.
# SENSEVAL-2 uses WordNet 1.7, which is no longer installable on most modern
# machines and is not the version that the NLTK comes with.
# As a consequence, we have to manually map the following
# senses to their equivalent(s).
SV_SENSE_MAP = {
    "HARD1": ["difficult.a.01"],    # not easy, requiring great physical or mental
    "HARD2": ["hard.a.02",          # dispassionate
              "difficult.a.01"],
    "HARD3": ["hard.a.03"],         # resisting weight or pressure
    "interest_1": ["interest.n.01"], # readiness to give attention
    "interest_2": ["interest.n.03"], # quality of causing attention to be given to
    "interest_3": ["pastime.n.01"],  # activity, etc. that one gives attention to
    "interest_4": ["sake.n.01"],     # advantage, advancement or favor
    "interest_5": ["interest.n.05"], # a share in a company or business
    "interest_6": ["interest.n.04"], # money paid for the use of money
    "cord": ["line.n.18"],          # something (as a cord or rope) that is long and thin and flexible
    "formation": ["line.n.01","line.n.03"], # a formation of people or things one beside another
    "text": ["line.n.05"],                 # text consisting of a row of words written across a page or computer screen
    "phone": ["telephone_line.n.02"],   # a telephone connection
    "product": ["line.n.22"],       # a particular kind of product or merchandise
    "division": ["line.n.29"],      # a conceptual separation or distinction
    "SERVE12": ["serve.v.02"],       # do duty or hold offices; serve in a specific function
    "SERVE10": ["serve.v.06"], # provide (usually but not necessarily food)
    "SERVE2": ["serve.v.01"],       # serve a purpose, role, or function
    "SERVE6": ["service.v.01"]      # be used by; as of a utility
}



class SensevalTest:

    def __init__(self):
        self._interest = {"interest_1": "interest.n.01", # readiness to give attention
                    "interest_2": "interest.n.03", # quality of causing attention to be given to
                    "interest_3": "pastime.n.01",  # activity, etc. that one gives attention to
                    "interest_4": "sake.n.01",     # advantage, advancement or favor
                    "interest_5": "interest.n.05", # a share in a company or business
                    "interest_6": "interest.n.04", # money paid for the use of money
                    }
        self._line = {
            "cord": ["line.n.18"],  # something (as a cord or rope) that is long and thin and flexible
            "formation": ["line.n.01", "line.n.03"],  # a formation of people or things one beside another
            "text": ["line.n.05"],  # text consisting of a row of words written across a page or computer screen
            "phone": ["telephone_line.n.02"],  # a telephone connection
            "product": ["line.n.22"],  # a particular kind of product or merchandise
            "division": ["line.n.29"],  # a conceptual separation or distinction
        }
        self._interest_ss = map(wn.synset, [self._interest[key] for key in self._interest])
        self._offset2interest = {wn.synset(self._interest[key]).offset(): key for key in self._interest}

    def interest_dataset_info(self):
        print 'Interest Dataset'
        dataset = senseval.instances('interest.pos')
        pairs = [(i.context, i.senses[0]) for i in dataset]
        gold = [y for x, y in pairs]
        print 'Dataset size: ', len(gold)
        senses = Counter(gold)
        print 'Class Distribution'
        for ss in senses:
            print ss, ' ', senses[ss]
        stats = {}
        for x, y in pairs:
            stats.setdefault(y, []).append(' '.join([word for word, tag in x]))
        print 'Examples'
        for ss in senses:
            print ss
            print stats[ss][0]
            print stats[ss][1]

    def load_dataset(self, name):
        dataset = senseval.instances(name)
        pairs = [(i.context, i.senses[0]) for i in dataset]
        dataset_pairs = []
        for x, y in pairs:
            features = self.context2feature(x)
            if features:
                dataset_pairs.append((features, y))
        return dataset_pairs

    def context2feature(self, context):
        context_words = []
        for p in context:
            try:
                word, tag = p
            except:
                continue
            if tag.startswith('NN'):
                context_words.append(word)
        return ' '.join(context_words)

    def evaluate_interest(self, dataset, method):
        wsd = WSD(name=method)
        test = []
        gold = []
        for t, g in dataset:
            ss = wsd.max_senses(t, self._interest_ss)
            test.append(self._offset2interest[ss.offset()])
            gold.append(g)
        cm = ConfusionMatrix(gold, test)
        #print(cm.pretty_format(sort_by_count=True, show_percents=True, truncate=9))
        print cm
        return gold, test, self._interest.keys()

senseval_test = SensevalTest()
pairs = senseval_test.load_dataset('line.pos')
cat_report = most_common_vocab(pairs)
for c in cat_report:
    print c, cat_report[c].most_common(20)


class SemCorTest:

    def __init__(self, k=1):
        self._num = k

    def load_dataset(self):
        dataset = self.random_dataset(1)
        for sentece in dataset[0][:10]:
            self.sentence_feature(sentece)

    def random_dataset(self, k):
        names = random.sample(semcor.fileids(), k)
        datasets = [semcor.tagged_sents(n, tag='both') for n in names]
        return datasets

    def sentence_feature(self, sent):
        for s in sent:
            print s

# test_semcor = SemCorTest()
# test_semcor.load_dataset()

# wsd = WSD()
#
# class Dataset:
#
#     def __init__(self):
#         self.dataset = FileIO.filename('eval/wsd/eng-coarse-all-words.xml')
#         self.goldstandard = FileIO.filename('eval/wsd/dataset21.test.key')
#         self.senseval = FileIO.filename('eval/wsd/corpora/english-lex-sample/train/eng-lex-sample.training.xml')
#         self.senseval_trial = FileIO.filename('eval/wsd/corpora/english-lex-sample/trial/lexical-sample-english-xml')
#
#     def load_goldstandard(self):
#         data_lst = []
#         with open(self.goldstandard, 'r') as f:
#             for line in f:
#                 line, sep, lemma = line.strip().rpartition(' !! ')
#                 lemma, pos = lemma[6:].split('#')
#                 text_id, sep, line = line.partition(' ')
#                 instance_id, sep, line = line.partition(' ')
#                 sensekey = line.split()
#                 if pos == 'n':
#                     if len(wsd.word2synset(lemma)) > 1:
#                         data = {}
#                         data['word'] = lemma
#                         data['id'] = instance_id
#                         data['gold'] = map(wsd.semcor2synset, sensekey)
#                         data_lst.append(data)
#         return data_lst
#
#     def remove_tags(self, text):
#         tags = {i: " " for i in re.findall("(<[^>\n]*>)", text.strip())}
#         no_tag_text = reduce(lambda x, kv: x.replace(*kv), tags.iteritems(), text)
#         return " ".join(no_tag_text.split())
#
#
#     def load_dataset(self):
#         test = {}
#         with open(self.dataset, 'r') as f:
#             corpus = f.read()
#             for text in bs(corpus).findAll('text'):
#                 for sent in text.findAll('sentence'):
#                     context_sent = " ".join([self.remove_tags(i) for i in
#                                              str(sent).split('\n') if self.remove_tags(i)])
#                     context_sent = wsd.context2words(context_sent)
#                     context = []
#                     for ins in sent.findAll('instance'):
#                         if ins['pos'] == 'n':
#                             context.append(ins['lemma'].lower())
#                     for ins in sent.findAll('instance'):
#                         if ins['pos'] == 'n':
#                             obj_dic = {}
#                             obj_dic['lemma'] = ins['lemma']
#                             obj_dic['context'] = context
#                             test[ins['id']] = obj_dic
#         return test
#
#     def load_senseval_sample(self):
#         with open(self.senseval_trial,'r') as f:
#             corpus = f.read()
#             corpus = bs(corpus).findAll('corpus')
#             lex = corpus[0].findAll('lexelt')
#             sum_count = 0
#             for l in lex:
#                 print l['item']
#                 ins = l.findAll('instance')
#                 print len(ins)
#                 sum_count += len(ins)
#             print sum_count
#
#     def xml_parse(self):
#         tree = ET.parse(self.senseval)
#         root = tree.getroot()
#         print root.tag
#
#     def load_senseval(self):
#         with open(self.senseval,'r') as f:
#             p = re.compile('<head>\w+<\/head>')
#             corpus = f.read()
#             corpus = bs(corpus).findAll('corpus')
#             lex = corpus[0].findAll('lexelt')
#             dataset = []
#             for l in lex:
#                 word,pos = l['item'].split('.')
#                 if pos == 'n':
#                     ins = l.findAll('instance')
#                     for sent in ins:
#                         answers = []
#                         for s in str(sent).split('\n'):
#                             if s.startswith('<answer'):
#                                 sense = bs(s).find('answer')['senseid']
#                                 try:
#                                     if sense.__contains__('%'):
#                                         answers.append(wsd.semcor2synset(sense))
#                                 except:
#                                     pass
#                             if re.findall("(<head>)", s):
#                                 context = p.sub('', s)
#                         if answers:
#                             context = wsd.context2words(context)
#                             dataset.append((word, answers, context))
#             return dataset
#
#
# data = Dataset()
#
# def evaluate_baseline():
#     gold = data.load_goldstandard()
#     N = len(gold)
#     baseline_random = [wsd.disambiguate_baseline_random(x['word']) for x in gold]
#     baseline_first = [wsd.disambiguate_baseline_first(x['word']) for x in gold]
#     baseline_random_result = [baseline_random[i] in gold[i]['gold'] for i in range(N)]
#     baseline_first_result = [baseline_first[i] in gold[i]['gold'] for i in range(N)]
#     #
#     accuracy_random = len([x for x in baseline_random_result if x is True])*1.0 / N
#     accuracy_first = len([x for x in baseline_first_result if x is True])*1.0 / N
#     #
#     print 'random accuraccy ', accuracy_random
#     print 'first accuraccy ', accuracy_first
#
# def evaluate_semeval2007(wsd_method, sim_method):
#     gold = data.load_goldstandard()
#     gold_dict = {d['id']: d['gold'] for d in gold}
#     #print len(gold_dict)
#     test = data.load_dataset()
#     #print len(test)
#     result = []
#     i = 1
#     for key in gold_dict:
#         context = test[key]['context']
#         word = test[key]['lemma']
#         if wsd_method == 'pagerank':
#             syn = wsd.disambiguate_pagerank(context, word, sim_method)
#         if wsd_method == 'maxsim':
#             syn = wsd.disambiguate_max_similarity(context, word, sim_method)
#         if syn in gold_dict[key]:
#             #print i, True
#             result.append(True)
#         else:
#             #print i, False
#             result.append(False)
#         i += 1
#     accuracy = len([x for x in result if x is True]) * 1.0 / len(gold_dict)
#     return accuracy
#
#
# def evaluate_senseval2(wsd_method, sim_method):
#     test = data.load_senseval()
#     #print len(test)
#     result = []
#     i = 1
#     for t in test:
#         word, answers, context = t
#         if wsd_method == 'pagerank':
#             syn = wsd.disambiguate_pagerank(context, word, sim_method)
#         if wsd_method == 'maxsim':
#             syn = wsd.disambiguate_max_similarity(context, word, sim_method)
#         if syn in answers:
#             #print i, True
#             result.append(True)
#         else:
#             #print i, False
#             result.append(False)
#         i += 1
#     accuracy = len([x for x in result if x is True]) * 1.0 / len(test)
#     return accuracy
#data.load_senseval_sample()

#for m in ['wpath']:
#    print 'pagerank', m, evaluate_semeval2007('pagerank', m)
#    print 'maxsim', m, evaluate_semeval2007('maxsim', m)

# for m in wsd.sim_methods:
#     print 'maxsim', m, evaluate_senseval2('maxsim', m)
#     print 'pagerank',m,evaluate_senseval2('pagerank', m)



