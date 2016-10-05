from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import information_content

from gensim.models import Word2Vec

from sematch.nlp import word_tokenize, lemma, porter, lemmatization
from sematch.utility import FileIO, memoized
from sematch.sparql import StatSPARQL

from collections import Counter
import math

class GraphIC:

    """
    This class is used to compute graph-based IC in knowledge graph, which is
    basically the proportion of instances tagged with a specific concept
    """

    def __init__(self, ic_file):
        self._ic_file = ic_file
        self._graph_ic = self.graph_ic_reader(ic_file)
        self._graph_stats = StatSPARQL()
        self._N = self._graph_stats.entity_N()

    def concept_ic(self, concept):
        """
        Compute the ic value of a concept using sparql query
        :param concept: a id of concept, here is the uri of concept
        :return: the ic value of the concept
        """
        if concept in self._graph_ic:
            return self._graph_ic[concept]
        else:
            freq = int(self._graph_stats.concept_freq(concept))
            if freq == 0:
                ic = 0.0
            else:
                prob = 1.0 * freq / self._N
                ic = -math.log(prob)
            self.graph_ic_writer(self._ic_file, [{'concept':concept, 'ic':str(ic)}])
            self._graph_ic[concept] = ic
            return ic

    def graph_ic_reader(self, filename):
        """
        Load the saved IC values
        :param filename: the file containing IC values of concepts
        :return: a dictionary concept:IC
        """
        data = FileIO.read_json_file(filename)
        return {d['concept']:float(d['ic']) for d in data}

    def graph_ic_writer(self, filename, data):
        """
        Save the ic values for a concept for faster access.
        :param filename:
        :param data:
        :return:
        """
        FileIO.append_json_file(filename, data)

class ConceptSimilarity:
    """
    This class is used to compute taxonomical semantic similarity scores between
    concepts that are located in a concept taxonomy. A taxonomy object needs to be passed into
    this class in order to find the structural information of concepts such as depth, path length,
    and so on. The graph-based IC is needed for semantic similarity measures wpath, res, lin, jcn.
    """
    def __init__(self, taxonomy, ic_file):
        self._taxonomy = taxonomy
        self._graph_ic = GraphIC(ic_file)

    def name2concept(self, name):
        """
        This function maps a string name to a node in taxonomy based on node's labels
        :param name: string name of a concept
        :return: the node id if contains the named node otherwise None.
        """
        return self._taxonomy._label2id[name] if self._taxonomy._label2id.get(name) else None

    def concept_ic(self, concept):
        """
        Get the graph-based IC of a concept. the ic of virtual root is 0
        :param concept: the node id of concept
        :return: the ic value of concept
        """
        if concept == self._taxonomy._root:
            return 0.0
        else:
            return self._graph_ic.concept_ic(self._taxonomy._nodes[concept])

    def path(self, c1, c2):
        """
        Rada's shortest path based similarity metric
        :param c1:
        :param c2:
        :return: similarity score in [0,1]
        """
        return 1.0/ self._taxonomy.shortest_path_length(c1, c2)

    def wup(self, c1, c2):
        """
        Wu and Palm's similarity metric
        :param c1:
        :param c2:
        :return:
        """
        lcs = self._taxonomy.least_common_subsumer(c1, c2)
        depth_c1 = self._taxonomy.depth(c1)
        depth_c2 = self._taxonomy.depth(c2)
        depth_lcs = self._taxonomy.depth(lcs)
        return 2.0*depth_lcs / (depth_c1 + depth_c2)

    def li(self, c1, c2, alpha=0.2, beta=0.6):
        path = self._taxonomy.shortest_path_length(c1, c2) - 1
        lcs = self._taxonomy.least_common_subsumer(c1, c2)
        depth = self._taxonomy.depth(lcs)
        # print path, lcs, depth
        x = math.exp(-alpha * path)
        y = math.exp(beta * depth)
        # print y
        z = math.exp(-beta * depth)
        a = y - z
        b = y + z
        return x * (a / b)

    def res(self, c1, c2):
        lcs = self._taxonomy.least_common_subsumer(c1, c2)
        return self.concept_ic(lcs)

    def lin(self, c1, c2):
        lcs = self._taxonomy.least_common_subsumer(c1, c2)
        lcs_ic = self.concept_ic(lcs)
        c1_ic = self.concept_ic(c1)
        c2_ic = self.concept_ic(c2)
        combine = c1_ic + c2_ic
        if c1_ic == 0.0 or c2_ic == 0.0:
            return 0.0
        return 2.0 * lcs_ic / combine

    def jcn(self, c1, c2):
        lcs = self._taxonomy.least_common_subsumer(c1, c2)
        lcs_ic = self.concept_ic(lcs)
        c1_ic = self.concept_ic(c1)
        c2_ic = self.concept_ic(c2)
        lcs_ic = 2.0 * lcs_ic
        if c1_ic == 0.0 or c2_ic == 0.0:
            return 0.0
        return 1.0 / 1 + (c1_ic + c2_ic - lcs_ic)

    def wpath(self, c1, c2, k=0.8):
        lcs = self._taxonomy.least_common_subsumer(c1, c2)
        path = self._taxonomy.shortest_path_length(c1, c2) - 1
        weight = k ** self.concept_ic(lcs)
        return 1.0 / (1 + path * weight)



class WordNetSimilarity:

    # wns = WordNetSimilarity()
    # print wns.word_similarity('rooster', 'voyage', 'res')
    # print wns.word_similarity('rooster', 'voyage', 'li')
    # print wns.word_similarity('rooster', 'voyage', 'jcn')

    # print beef, lamb, octopus, shellfish, meat, seafood, food

    # wns = WordNetSimilarity()
    # wns.similarity_all_methods(beef, octopus)
    # wns.similarity_all_methods(beef, lamb)
    # wns.similarity_all_methods(food, coffee)

    def __init__(self, ic_corpus='brown'):
        self._ic_corpus = wordnet_ic.ic('ic-brown.dat') if ic_corpus == 'brown' else wordnet_ic.ic('ic-semcor.dat')
        self._wn_max_depth = 19
        self._default_metrics = ['path','lch','wup','li','res','lin','jcn','wpath']

    def method(self, name):
        def function(syn1, syn2):
            score = getattr(self, name)(syn1, syn2)
            return abs(score)
        return function

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

    def multilingual2synset(self, word, lang='spa'):
        """
        Map words in different language to wordnet synsets
        ['als', 'arb', 'cat', 'cmn', 'dan', 'eng', 'eus', 'fas', 'fin', 'fra', 'fre',
         'glg', 'heb', 'ind', 'ita', 'jpn', 'nno','nob', 'pol', 'por', 'spa', 'tha', 'zsm']
        :param word: a word in different language that has been defined in
        Open Open Multilingual WordNet, using ISO-639 language codes.
        :param lang: the language code defined
        :return: wordnet synsets.
        """
        return wn.synsets(word, lang=lang, pos=wn.NOUN)


    @memoized
    def similarity(self, c1, c2, name='path'):
        """
        Compute semantic similarity between two concepts
        :param c1:
        :param c2:
        :param name:
        :return:
        """
        return self.method(name)(c1, c2)

    def max_synset_similarity(self, syns1, syns2, sim_metric):
        """
        Compute the maximum similarity score between two list of synsets
        :param syns1: synset list
        :param syns2: synset list
        :param sim_metric: similarity function
        :return: maximum semantic similarity score
        """
        return max([sim_metric(c1, c2) for c1 in syns1 for c2 in syns2] + [0])

    @memoized
    def word_similarity(self, w1, w2, name='path'):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        sim_metric = lambda x, y: self.similarity(x, y, name)
        return self.max_synset_similarity(s1, s2, sim_metric)

    @memoized
    def best_synset_pair(self, w1, w2, name='path'):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        sims = Counter({(c1, c2):self.similarity(c1, c2, name) for c1 in s1 for c2 in s2})
        return sims.most_common(1)[0][0]

    def word_similarity_all_metrics(self, w1, w2):
        return {m:self.word_similarity(w1, w2, name=m) for m in self._default_metrics}

    def word_similarity_wpath(self, w1, w2, k):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        sim_metric = lambda x, y: self.wpath(x, y, k)
        return self.max_synset_similarity(s1, s2, sim_metric)

    @memoized
    def monol_word_similarity(self, w1, w2, lang='spa', name='path'):
        """
         Compute mono-lingual word similarity, two words are in same language.
        :param w1: word
        :param w2: word
        :param lang: language code
        :param name: name of similarity metric
        :return: semantic similarity score
        """
        s1 = self.multilingual2synset(w1.decode('utf-8'), lang)
        s2 = self.multilingual2synset(w2.decode('utf-8'), lang)
        sim_metric = lambda x, y: self.similarity(x, y, name)
        return self.max_synset_similarity(s1, s2, sim_metric)

    @memoized
    def crossl_word_similarity(self, w1, w2, lang1='spa', lang2='eng', name='path'):
        """
         Compute cross-lingual word similarity, two words are in different language.
        :param w1: word
        :param w2: word
        :param lang1: language code for word1
        :param lang2: language code for word2
        :param name: name of similarity metric
        :return: semantic similarity score
        """
        s1 = self.multilingual2synset(w1.decode('utf-8'), lang1)
        s2 = self.multilingual2synset(w2.decode('utf-8'), lang2)
        sim_metric = lambda x, y: self.similarity(x, y, name)
        return self.max_synset_similarity(s1, s2, sim_metric)

    def least_common_subsumer(self, c1, c2):
        return c1.lowest_common_hypernyms(c2)[0]

    def synset_ic(self, c):
        return information_content(c, self._ic_corpus)

    def dpath(self, c1, c2, alpha=1.0, beta=1.0):
        lcs = self.least_common_subsumer(c1, c2)
        path = c1.shortest_path_distance(c2)
        path = 1.0 / (1 + path)
        path = path**alpha
        depth = lcs.max_depth() + 1
        depth = depth*1.0/(1 + self._wn_max_depth)
        depth = depth**beta
        return math.log(1+path*depth,2)

    def wpath(self, c1, c2, k=0.8):
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
        return c1.res_similarity(c2, self._ic_corpus)

    def jcn(self, c1, c2):
        lcs = self.least_common_subsumer(c1, c2)
        c1_ic = self.synset_ic(c1)
        c2_ic = self.synset_ic(c2)
        lcs_ic = self.synset_ic(lcs)
        #print lcs, lcs_ic, c1_ic, c2_ic
        diff = c1_ic + c2_ic - 2*lcs_ic
        return 1.0/(1 + diff)

    def lin(self, c1, c2):
        return c1.lin_similarity(c2, self._ic_corpus)

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


class YagoTypeSimilarity(WordNetSimilarity):

    """Extend the WordNet synset to linked data through YAGO mappings"""

    def __init__(self, graph_ic='models/yago_type_ic.txt', mappings="models/type-linkings.txt"):
        WordNetSimilarity.__init__(self)
        self._graph_ic = GraphIC(graph_ic)
        self._mappings = FileIO.read_json_file(mappings)
        self._id2mappings = {data['offset']: data for data in self._mappings}
        self._yago2id = {data['yago_dbpedia']: data['offset'] for data in self._mappings}

    def synset2id(self, synset):
        return str(synset.offset() + 100000000)

    def id2synset(self, offset):
        x = offset[1:]
        return wn._synset_from_pos_and_offset('n', int(x))

    def synset2mapping(self, synset, key):
        mapping_id = self.synset2id(synset)
        if mapping_id in self._id2mappings:
            mapping = self._id2mappings[mapping_id]
            return mapping[key] if key in mapping else None
        else:
            return None

    def synset2yago(self, synset):
        return self.synset2mapping(synset,'yago_dbpedia')

    def synset2dbpedia(self, synset):
        return self.synset2mapping(synset, 'dbpedia')

    def word2dbpedia(self, word):
        return [self.synset2dbpedia(s) for s in self.word2synset(word) if self.synset2dbpedia(s)]

    def word2yago(self, word):
        return [self.synset2yago(s) for s in self.word2synset(word) if self.synset2yago(s)]

    def word_similarity_wpath_graph(self, w1, w2, k):
        s1 = self.word2synset(w1)
        s2 = self.word2synset(w2)
        return max([self.wpath_graph(c1, c2, k) for c1 in s1 for c2 in s2] + [0])

    def res_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        yago = self.synset2yago(lcs)
        return self._graph_ic.concept_ic(yago)

    def lin_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        yago_c1 = self.synset2yago(c1)
        yago_c2 = self.synset2yago(c2)
        yago_lcs = self.synset2yago(lcs)
        lcs_ic = self._graph_ic.concept_ic(yago_lcs)
        c1_ic = self._graph_ic.concept_ic(yago_c1)
        c2_ic = self._graph_ic.concept_ic(yago_c2)
        combine = c1_ic + c2_ic
        if c1_ic == 0.0 or c2_ic == 0.0:
            return 0.0
        return 2.0 * lcs_ic / combine

    def jcn_graph(self, c1, c2):
        lcs = self.least_common_subsumer(c1,c2)
        yago_c1 = self.synset2yago(c1)
        yago_c2 = self.synset2yago(c2)
        yago_lcs = self.synset2yago(lcs)
        lcs_ic = self._graph_ic.concept_ic(yago_lcs)
        c1_ic = self._graph_ic.concept_ic(yago_c1)
        c2_ic = self._graph_ic.concept_ic(yago_c2)
        lcs_ic = 2.0 * lcs_ic
        if c1_ic == 0.0 or c2_ic == 0.0:
            return 0.0
        return 1.0 / 1+(c1_ic + c2_ic - lcs_ic)

    def wpath_graph(self, c1, c2, k=0.9):
        lcs = self.least_common_subsumer(c1, c2)
        path = c1.shortest_path_distance(c2)
        yago_lcs = self.synset2yago(lcs)
        weight = k ** self._graph_ic.concept_ic(yago_lcs)
        return 1.0 / (1 + path*weight)


class WordVecSimilarity:

    def __init__(self, vec_file='models/GoogleNews-vectors-negative300.bin', binary=True):
        """

        :param vec_file: the file storing vectors
        :param binary: if vector are stored in binary. Google news use binary while yelp not
        """
        self._wordvec = Word2Vec.load_word2vec_format(FileIO.filename(vec_file), binary=binary)

    @memoized
    def word_similarity(self, w1, w2):
        try:
            sim = self._wordvec.similarity(w1, w2)
        except:
            return 0.0
        return sim

class TextSimilarity:

    def __init__(self, sim):
        self._sim = sim

    def extract_words(self, text):
        return lemmatization(word_tokenize(text))

    def sum_words_similarity(self, words1, words2, method='path'):
        return sum([max([self._sim.word_similarity(w1, w2, method) for w2 in words2]) for w1 in words1])

    def text_similarity(self, t1, t2, method='path'):
        words1 = self.extract_words(t1)
        words2 = self.extract_words(t2)
        N1 = len(words1)
        N2 = len(words2)
        sum_1 = self.sum_words_similarity(words1, words2, method) / N1
        sum_2 = self.sum_words_similarity(words2, words1, method) / N2
        return (sum_1 + sum_2) / 2.0

