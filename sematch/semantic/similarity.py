from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content
from gensim.models import Word2Vec
from sematch.nlp import word_tokenize, lemma, porter, lemmatization
from sematch.knowledge import graph
from sematch.semantic.score import Score
from sematch.utility import FileIO,memoized
import math


def graph_ic_reader(filename):
    data = FileIO.read_list_file(filename)
    ic_dic = {}
    for d in data:
        item = d.split()
        offset = int(item[0])
        count = int(item[1])
        ic_dic[offset] = count
    return ic_dic

def graph_ic_writer(filename, items):
    data = []
    for key in items.keys():
        data.append(' '.join([str(key),str(items[key])]))
    FileIO.append_list_file(filename, data)

class GraphSimilarity(Score):

    def __init__(self):
        self.ic_graph = graph_ic_reader('db/graph-ic.txt')
        self.graph = graph.KnowledgeGraph()
        self.entity_N = self.graph.entity_N()

    def pmi(self, c1, c2):
        freq_1 = self.graph.synset_entity_count(c1)
        freq_2 = self.graph.synset_entity_count(c2)
        freq_common = self.graph.synset_coocurrence(c1,c2)
        p_1 = 1.0 * freq_1 / self.entity_N
        p_2 = 1.0 * freq_2 / self.entity_N
        p_12 = 1.0 * freq_common / self.entity_N
        if p_1 == 0 or p_2 == 0:
            return 0
        prob = p_12/(p_1*p_2)
        if prob < 0.0001:
            return 0
        return math.log(prob)

    def concept_graph_freq(self, c):
        key = c.offset()
        if key in self.ic_graph:
            return self.ic_graph[key]
        count = self.graph.synset_entity_count(c)
        graph_ic_writer('db/graph-ic.txt',{key:count})
        self.ic_graph[key] = count
        return count

    def entity_ic(self, c):
        freq = self.concept_graph_freq(c)
        if freq == 0:
            return 0
        prob = 1.0 * freq / self.entity_N
        return -math.log(prob)

    def res_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        return self.entity_ic(lcs)

    def lin_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        lcs_ic = self.entity_ic(lcs)
        c1_ic = self.entity_ic(c1)
        c2_ic = self.entity_ic(c2)
        combine = c1_ic + c2_ic
        if c1_ic == 0 or c2_ic == 0:
            return 0
        return 2.0 * lcs_ic / combine

    def jcn_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        lcs_ic = self.entity_ic(lcs)
        c1_ic = self.entity_ic(c1)
        c2_ic = self.entity_ic(c2)
        lcs_ic = 2.0 * lcs_ic
        if c1_ic == 0 or c2_ic == 0:
            return 0
        return 1.0/1+(c1_ic + c2_ic - lcs_ic)

    def wpath_graph(self, c1,c2, k=0.8):
        lcs = self.least_common_subsumer(c1,c2)
        path = c1.shortest_path_distance(c2)
        weight = k ** self.entity_ic(lcs)
        return 1.0 / (1 + path*weight)



class WordNetSimilarity(Score):

    # wns = WordNetSimilarity()
    # print wns.word_similarity('rooster', 'voyage', 'res')
    # print wns.word_similarity('rooster', 'voyage', 'li')
    # print wns.word_similarity('rooster', 'voyage', 'jcn')

    # beef = wn.synset('beef.n.02')
    # lamb = wn.synset('lamb.n.05')
    # octopus = wn.synset('octopus.n.01')
    # shellfish = wn.synset('shellfish.n.01')
    # meat = wn.synset('meat.n.01')
    # seafood = wn.synset('seafood.n.01')
    # food = wn.synset('food.n.02')
    # service = wn.synset('service.n.02')
    # atmosphere = wn.synset('atmosphere.n.01')
    # coffee = wn.synset('coffee.n.01')

    # print beef, lamb, octopus, shellfish, meat, seafood, food

    # wns = WordNetSimilarity()
    # wns.similarity_all_methods(beef, octopus)
    # wns.similarity_all_methods(beef, lamb)
    # wns.similarity_all_methods(food, coffee)

    def __init__(self):
        self.ic_corpus = wordnet_ic.ic('ic-brown.dat')
        self.semcor_ic = wordnet_ic.ic('ic-semcor.dat')
        self.wn_max_depth = 19

    #return all the noun synsets in wordnet
    def get_all_synsets(self):
        return wn.all_synsets('n')

    def get_all_lemma_names(self):
        return wn.all_lemma_names('n')

    def offset2synset(self, offset):
        '''
        offset2synset('06268567-n')
        Synset('live.v.02')
        '''
        return wn._synset_from_pos_and_offset(str(offset[-1:]), int(offset[:8]))

    def synset2offset(self, ss):
        return '%08d-%s' % (ss.offset(), ss.pos())

    #semcor live%2:43:06::
    def semcor2synset(self, sense):
        return wn.lemma_from_key(sense).synset()

    def semcor2offset(self, sense):
        '''
        semcor2synset('editorial%1:10:00::')
        06268567-n
        '''
        return self.synset2offset(self.semcor2synset(sense))

    def word2synset(self, word):
        w = lemma.lemmatize(word)
        syns = wn.synsets(w, pos=wn.NOUN)
        if not syns:
            syns = wn.synsets(porter.stem(w), pos=wn.NOUN)
        return syns

    @memoized
    def similarity(self, c1, c2, name='path'):
        return self.method(name)(c1, c2)

    @memoized
    def word_similarity(self, w1, w2, name='path'):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        scores = [self.similarity(c1, c2, name) for c1 in s1 for c2 in s2] + [0]
        return max(scores)

    def similarity_all_methods(self, c1, c2):
        print 'path', self.similarity(c1, c2, name='path')
        print 'lch', self.similarity(c1, c2, name='lch')
        print 'wup', self.similarity(c1, c2, name='wup')
        print 'li', self.similarity(c1, c2, name='li')
        print 'res', self.similarity(c1, c2, name='res')
        print 'lin', self.similarity(c1, c2, name='lin')
        print 'jcn', self.similarity(c1, c2, name='jcn')
        print 'wpath', self.similarity(c1, c2, name='wpath')

    def word_similarity_wpath(self, w1, w2, m, k):
        s1 = wn.synsets(w1, pos=wn.NOUN)
        s2 = wn.synsets(w2, pos=wn.NOUN)
        scores = [self.k_method(m)(c1, c2, k) for c1 in s1 for c2 in s2]
        return max(scores)

    def least_common_subsumer(self, c1, c2):
        return c1.lowest_common_hypernyms(c2)[0]

    def synset_ic(self, c):
        return information_content(c, self.ic_corpus)

    def dpath(self, c1, c2, alpha=1.0, beta=1.0):
        lcs = self.least_common_subsumer(c1, c2)
        path = c1.shortest_path_distance(c2)
        path = 1.0 / (1 + path)
        path = path**alpha
        depth = lcs.max_depth() + 1
        depth = depth*1.0/(1 + self.wn_max_depth)
        depth = depth**beta
        return math.log(1+path*depth,2)

    def wpath(self, c1, c2, k=0.9):
        lcs = self.least_common_subsumer(c1,c2)
        path = c1.shortest_path_distance(c2)
        weight = k ** self.synset_ic(lcs)
        return 1.0 / (1 + path*weight)

    def li(self, c1, c2, alpha=0.2,beta=0.6):
        path = c1.shortest_path_distance(c2)
        lcs = self.least_common_subsumer(c1, c2)
        depth = lcs.max_depth()
        #print path, lcs, depth
        x = math.exp(-alpha*path)
        y = math.exp(beta*depth)
        #print y
        z = math.exp(-beta*depth)
        a = y - z
        b = y + z
        return x * (a/b)

    def path(self, c1, c2):
        return c1.path_similarity(c2)

    def wup(self, c1, c2):
        return c1.wup_similarity(c2)

    def lch(self, c1, c2):
        return c1.lch_similarity(c2)

    def res(self, c1, c2):
        return c1.res_similarity(c2, self.ic_corpus)

    def jcn(self, c1, c2):
        lcs = self.least_common_subsumer(c1, c2)
        c1_ic = self.synset_ic(c1)
        c2_ic = self.synset_ic(c2)
        lcs_ic = self.synset_ic(lcs)
        #print lcs, lcs_ic, c1_ic, c2_ic
        diff = c1_ic + c2_ic - 2*lcs_ic
        return 1.0/(1 + diff)

    def lin(self, c1, c2):
        return c1.lin_similarity(c2, self.ic_corpus)

    def gloss_overlap(self, c1, c2):
        gloss1 = lemmatization(word_tokenize(c1.definition()))
        gloss2 = lemmatization(word_tokenize(c2.definition()))
        gloss1 = set(map(porter.stem, gloss1))
        gloss2 = set(map(porter.stem, gloss2))
        return len(gloss1.intersection(gloss2))

    def elesk(self, c1, c2):
        '''
            extended lesk algorithm, measuring word overlaps in definitions.
            similarity(A,B) = overlap(gloss(A), gloss(B))
          + overlap(gloss(hypo(A)), gloss(B))
          + overlap(gloss(hypo(A)), gloss(hypo(B)))
          + overlap(gloss(A), gloss(hypo(B)))
        '''
        hypo1 = c1.hyponyms()
        hypo2 = c2.hyponyms()
        sim = self.gloss_overlap(c1, c2)
        for h1 in hypo1:
            sim += self.gloss_overlap(h1, c2)
            for h2 in hypo2:
                sim += self.gloss_overlap(h1, h2)
        for h2 in hypo2:
            sim += self.gloss_overlap(c1, h2)
        return sim


class Word2VecSimilarity:

    def __init__(self, trained_file=None,
                 google_news='db/GoogleNews-vectors-negative300.bin'):
        if trained_file:
            self._model = Word2Vec.load(FileIO.filename(trained_file))
        else:
            self._model = Word2Vec.load_word2vec_format(FileIO.filename(google_news), binary=True)

    def similar_word(self, word):
        return self._model.most_similar(word)

    @memoized
    def word_similarity(self, w1, w2):
        try:
            sim = self._model.similarity(w1, w2)
        except:
            return 0.0
        return sim

class GloveSimilarity:

    def __init__(self):
        pass


class TextSimilarity:

    def __init__(self):
        self.sim = WordNetSimilarity()

    def extract_words(self, text):
        return lemmatization(word_tokenize(text))

    def sum_words_similarity(self, words1, words2, method='path'):
        return sum([max([self.sim.word_similarity(w1, w2, method) for w2 in words2]) for w1 in words1])

    def text_similarity(self, t1, t2, method='path'):
        words1 = self.extract_words(t1)
        words2 = self.extract_words(t2)
        N1 = len(words1)
        N2 = len(words2)
        sum_1 = self.sum_words_similarity(words1, words2, method) / N1
        sum_2 = self.sum_words_similarity(words2, words1, method) / N2
        return (sum_1 + sum_2) / 2.0
