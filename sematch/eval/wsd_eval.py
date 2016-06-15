from BeautifulSoup import BeautifulSOAP as bs
from sematch.semantic.disambiguation import WSD
from sematch.utility import FileIO
import xml.etree.ElementTree as ET
import re

wsd = WSD()

class Dataset:

    def __init__(self):
        self.dataset = FileIO.filename('eval/wsd/eng-coarse-all-words.xml')
        self.goldstandard = FileIO.filename('eval/wsd/dataset21.test.key')
        self.senseval = FileIO.filename('eval/wsd/corpora/english-lex-sample/train/eng-lex-sample.training.xml')
        self.senseval_trial = FileIO.filename('eval/wsd/corpora/english-lex-sample/trial/lexical-sample-english-xml')

    def load_goldstandard(self):
        data_lst = []
        with open(self.goldstandard, 'r') as f:
            for line in f:
                line, sep, lemma = line.strip().rpartition(' !! ')
                lemma, pos = lemma[6:].split('#')
                text_id, sep, line = line.partition(' ')
                instance_id, sep, line = line.partition(' ')
                sensekey = line.split()
                if pos == 'n':
                    if len(wsd.word2synset(lemma)) > 1:
                        data = {}
                        data['word'] = lemma
                        data['id'] = instance_id
                        data['gold'] = map(wsd.semcor2synset, sensekey)
                        data_lst.append(data)
        return data_lst

    def remove_tags(self, text):
        tags = {i: " " for i in re.findall("(<[^>\n]*>)", text.strip())}
        no_tag_text = reduce(lambda x, kv: x.replace(*kv), tags.iteritems(), text)
        return " ".join(no_tag_text.split())


    def load_dataset(self):
        test = {}
        with open(self.dataset, 'r') as f:
            corpus = f.read()
            for text in bs(corpus).findAll('text'):
                for sent in text.findAll('sentence'):
                    context_sent = " ".join([self.remove_tags(i) for i in
                                             str(sent).split('\n') if self.remove_tags(i)])
                    context_sent = wsd.context2words(context_sent)
                    context = []
                    for ins in sent.findAll('instance'):
                        if ins['pos'] == 'n':
                            context.append(ins['lemma'].lower())
                    for ins in sent.findAll('instance'):
                        if ins['pos'] == 'n':
                            obj_dic = {}
                            obj_dic['lemma'] = ins['lemma']
                            obj_dic['context'] = context
                            test[ins['id']] = obj_dic
        return test

    def load_senseval_sample(self):
        with open(self.senseval_trial,'r') as f:
            corpus = f.read()
            corpus = bs(corpus).findAll('corpus')
            lex = corpus[0].findAll('lexelt')
            sum_count = 0
            for l in lex:
                print l['item']
                ins = l.findAll('instance')
                print len(ins)
                sum_count += len(ins)
            print sum_count

    def xml_parse(self):
        tree = ET.parse(self.senseval)
        root = tree.getroot()
        print root.tag

    def load_senseval(self):
        with open(self.senseval,'r') as f:
            p = re.compile('<head>\w+<\/head>')
            corpus = f.read()
            corpus = bs(corpus).findAll('corpus')
            lex = corpus[0].findAll('lexelt')
            dataset = []
            for l in lex:
                word,pos = l['item'].split('.')
                if pos == 'n':
                    ins = l.findAll('instance')
                    for sent in ins:
                        answers = []
                        for s in str(sent).split('\n'):
                            if s.startswith('<answer'):
                                sense = bs(s).find('answer')['senseid']
                                try:
                                    if sense.__contains__('%'):
                                        answers.append(wsd.semcor2synset(sense))
                                except:
                                    pass
                            if re.findall("(<head>)", s):
                                context = p.sub('', s)
                        if answers:
                            context = wsd.context2words(context)
                            dataset.append((word, answers, context))
            return dataset


data = Dataset()

def evaluate_baseline():
    gold = data.load_goldstandard()
    N = len(gold)
    baseline_random = [wsd.disambiguate_baseline_random(x['word']) for x in gold]
    baseline_first = [wsd.disambiguate_baseline_first(x['word']) for x in gold]
    baseline_random_result = [baseline_random[i] in gold[i]['gold'] for i in range(N)]
    baseline_first_result = [baseline_first[i] in gold[i]['gold'] for i in range(N)]
    #
    accuracy_random = len([x for x in baseline_random_result if x is True])*1.0 / N
    accuracy_first = len([x for x in baseline_first_result if x is True])*1.0 / N
    #
    print 'random accuraccy ', accuracy_random
    print 'first accuraccy ', accuracy_first

def evaluate_semeval2007(wsd_method, sim_method):
    gold = data.load_goldstandard()
    gold_dict = {d['id']: d['gold'] for d in gold}
    #print len(gold_dict)
    test = data.load_dataset()
    #print len(test)
    result = []
    i = 1
    for key in gold_dict:
        context = test[key]['context']
        word = test[key]['lemma']
        if wsd_method == 'pagerank':
            syn = wsd.disambiguate_pagerank(context, word, sim_method)
        if wsd_method == 'maxsim':
            syn = wsd.disambiguate_max_similarity(context, word, sim_method)
        if syn in gold_dict[key]:
            #print i, True
            result.append(True)
        else:
            #print i, False
            result.append(False)
        i += 1
    accuracy = len([x for x in result if x is True]) * 1.0 / len(gold_dict)
    return accuracy


def evaluate_senseval2(wsd_method, sim_method):
    test = data.load_senseval()
    #print len(test)
    result = []
    i = 1
    for t in test:
        word, answers, context = t
        if wsd_method == 'pagerank':
            syn = wsd.disambiguate_pagerank(context, word, sim_method)
        if wsd_method == 'maxsim':
            syn = wsd.disambiguate_max_similarity(context, word, sim_method)
        if syn in answers:
            #print i, True
            result.append(True)
        else:
            #print i, False
            result.append(False)
        i += 1
    accuracy = len([x for x in result if x is True]) * 1.0 / len(test)
    return accuracy
#data.load_senseval_sample()

#for m in ['wpath']:
#    print 'pagerank', m, evaluate_semeval2007('pagerank', m)
#    print 'maxsim', m, evaluate_semeval2007('maxsim', m)

for m in wsd.sim_methods:
    print 'maxsim', m, evaluate_senseval2('maxsim', m)
    print 'pagerank',m,evaluate_senseval2('pagerank', m)