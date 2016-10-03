from sematch.utility import FileIO
from sematch.parsing.segmentation import QuerySegmentation
from sematch.knowledge.sparql import BaseSPARQL
from collections import defaultdict
import re


from sematch.nlp import tokenization
from sematch.nlp import StopWords
from sematch.knowledge.graph import KnowledgeGraph


class EnumerateSegment:

    def sequence(self, n):
        count = 2 ** n
        transformer = lambda x:bin(x)[2:].zfill(n)
        return map(transformer, range(count))

    def segment(self, tokens):
        n = len(tokens) - 1
        sequences = self.sequence(n)
        segmentations = []
        for s in sequences:
            segmentation = []
            begin = 0
            for i in range(n):
                end = i + 1
                if s[i] == '1':
                    segmentation.append(' '.join(tokens[begin:end]))
                    begin = end
            segmentation.append(' '.join(tokens[begin:end+1]))
            segmentations.append(segmentation)
        return segmentations

class ViterbiSegment:

    def segment(self, text, P):
        """Find the best segmentation of the string of characters, given the
        UnigramTextModel P."""
        # best[i] = best probability for text[0:i]
        # words[i] = best word ending at position i
        n = len(text)
        words = [''] + list(text)
        best = [1.0] + [0.0] * n
        ## Fill in the vectors best, words via dynamic programming
        for i in range(n+1):
            for j in range(0, i):
                w = text[j:i]
                if P[w] * best[i - len(w)] >= best[i]:
                    best[i] = P[w] * best[i - len(w)]
                    words[i] = w
        ## Now recover the sequence of best words
        sequence = []; i = len(words)-1
        while i > 0:
            sequence[0:0] = [words[i]]
            i = i - len(words[i])
        ## Return sequence of best words and overall probability
        return sequence, best[-1]

class RecursiveSegment:

    def binarySplit(self, words):
        return [(words[:i+1], words[i+1:]) for i in range(len(words))]

    def segment(self, words):
        if not words: return []
        return [[first] + self.segment(rest) for (first, rest) in self.binarySplit(words)]


     #def viterbi_segmentation(self, text):
    #  lexicon = self.matching(text)
       #  self.disambiguate(text, lexicon)
       #  n = lexicon.N
       #  segments = [(0,0)] + [(0,0)] * n
       #  best = [1.0] + [0.0] * n
       #  for i in range(n+1):
       #      for j in range(0, i):
       #          s = (j,i)
       #          w = self.scoring(s, lexicon)
       #          if w + best[j] >= best[i]:
       #              best[i] = w + best[j]
       #              segments[i] = s
       #  sequence = []
       #  i = n
       #  while i > 0:
       #      sequence[0:0] = [segments[i]]
       #      x,y = segments[i]
       #      l = y-x
       #      i = i - l
       #  #sequence = map(lambda x:' '.join(x), sequence)
       # #sequence = [seq for seq in sequence if seq in lexicon.get_segments()]
       #  entities = [lexicon.entity(seq) for seq in sequence if lexicon.has_segment(seq)]
       #  sequence = [lexicon.surface_form(seq) for seq in sequence if lexicon.has_segment(seq)]
       #  return {sequence[i]:entities[i] for i in range(len(entities))}
        # for seq in sequence:
        #     print seq, lexicon.candidate(seq)
        # return best[-1]
     #   pass

class QuerySegmentation:

# who/whom --> PERSON
# when --> TIME/DATE
# where/what place --> LOCATION
# what time (of day) --> TIME
# what day (of the week) --> DAY
# what/which month --> MONTH
# what age/how old --> AGE
# what brand --> PRODUCT
# what --> NAME
# how far/tall/high --> LENGTH
# how large/hig/small --> AREA
# how heavy --> WEIGHT
# how rich --> MONEY
# how often --> FREQUENCY
# how many --> NUMBER
# how long --> LENGTH/DURATION
# why/for what --> REASON

    def __init__(self):
        self.graph = KnowledgeGraph()
        self.window_size = 3
        self.special_segments = ['give me all', 'give me', 'which', 'who', 'what', 'when']

    def remove_segments(self, query):
        x = query.lower()
        for seg in self.special_segments:
            index = x.find(seg)
            if index >= 0:
                pre = x[0:index]
                post = x[index+len(seg):]
                x = pre + post
        return x

    def token_filter(self, token, keys):
        for k in keys:
            if token in k.split():
                return True
        return False

    def weighting(self, L):
        for key in L.keys():
            n = len(key.split())
            L[key]['weight'] = n**n

    def lexicon(self, tokens, segments):
        L = {}
        for s in segments:
            if s.lower() not in StopWords:
                resources = self.graph.segment_resources(s)
                if resources:
                    L[s] = {}
                    L[s]['resources'] = resources
        self.weighting(L)
        tokens = filter(lambda x:self.token_filter(x, L.keys()), tokens)
        return tokens, L

    def fragment(self, query):
        """Given a natural language query, this function tokenize the query,
        check the Knowledge Graph for valid segments, store the segments and their uris
        into a dictionary. Count each segment and its frequency in Knowledge Graph"""
        query = self.remove_segments(query)
        tokens = tokenization(query)
        n = len(tokens)
        segments = [' '.join(tokens[j:j+i]) for i in range(1, self.window_size + 1) for j in range(n - i + 1)]
        tokens, L = self.lexicon(tokens, segments)
        return tokens, L

    def viterbi_segmentation(self, query):
        """Find the best segmentation of the query based on viterbi algorithm using maximun span"""
        tokens, lexicon = self.fragment(query)
        n = len(tokens)
        segments = [' '] + tokens
        best = [1.0] + [0.0] * n
        for i in range(n+1):
            for j in range(0, i):
                s = tokens[j:i]
                k = ' '.join(s)
                if lexicon.get(k):
                    w = lexicon[k]['weight']
                    if w + best[i - len(s)] >= best[i]:
                        best[i] = w + best[i - len(s)]
                        segments[i] = s
        sequence = []
        i = len(segments)-1
        while i > 0:
            sequence[0:0] = [segments[i]]
            i = i - len(segments[i])
        sequence = map(lambda x:' '.join(x), sequence)
        return sequence, lexicon, best[-1]

    def segmentation(self, query):
        sequence, lexicon, score = self.viterbi_segmentation(query)
        resources = {}
        for seq in sequence:
            resources[seq] = lexicon[seq]['resources']
        return sequence, resources


def test():
    queries = ["who produce film starring Natalie Portman",
            "give me all video game publish by mean hamster software",
            "give me all soccer club in Spain",
            "river which Brooklyn Bridge crosses",
            "The Green Mile Tom Hanks",
            "Nobel Prize China",
            'vietnam travel national park',
            'vietnam travel airports',
            'Indian food',
            'Neil Gaiman novels',
            'films shot in Venice',
            'Works by Charles Rennie Mackintosh',
            'List of countries in World War Two',
            'Paul Auster novels',
            'State capitals of the United States of America',
            'Novels that won the Booker Prize',
            'countries which have won the FIFA world cup',
            'EU countries',
            'Films directed by Akira Kurosawa',
            'Airports in Germany',
            'Universities in Catalunya',
            'Give me all professional skateboarders from Sweden',
            'Give me all cars that are produced in Germany',
            'Give me all movies directed by Francis Ford Coppola',
            'Give me all companies in Munich',
            'Give me a list of all lakes in Denmark',
            'Give me all Argentine films',
            'Give me a list of all American inventions',
            'Give me the capitals of all countries in Africa',
            'Give me all presidents of the United States',
            'Give me all actors starring in Batman Begins',
            'Which actors were born in Germany?',
            'Give me all films produced by Hal Roach',
            'Give me all books written by Danielle Steel',
            'Give me all movies with Tom Cruise']

    s = QuerySegmentation()
    for i in range(len(test)):
        print i, test[i], '\n'
        seq,resources = s.segmentation(test[i])
        print seq, '\n'
        for key in resources.keys():
            print key, '\n'
            print resources[key], '\n\n'

#test()

s = QuerySegmentation()
print s.segmentation('iphone 6s')

#T:type
#E:entity
#OP:ObjectProperty
#DP:DataProperty
#Q:questions
# TAGS = ['T','E','OP','DP','Q']

class Grammar:

    def __init__(self):
        self.production = '(\w+)\s*->\s*(\w+(\s+\w+)*)$'
        self.grammar = FileIO.read_list_file('db/grammar')
        self.none_terminal_rules = self.parse_rules()
        self.start = 'Q'

    def parse_rules(self):
        r = {}
        PRODUCTION = re.compile(self.production)
        for line in self.grammar:
            match = PRODUCTION.match(line)
            lhs, rhs = match.group(1), match.group(2)
            a,b = rhs.split()
            c1 = ' '.join([a,b])
            c2 = ' '.join([b,a])
            r.setdefault(c1, []).append(lhs)
            r.setdefault(c2, []).append(lhs)
        return r

    def terminal_rules(self, L):
        productions = {}
        for lexicon in L.keys():
            for tag in L[lexicon].keys():
                productions.setdefault(lexicon, []).append(tag)
        return productions

class Node:

    def __init__(self, symbol, left, right, terminal):
        self.symbol = symbol
        self.left = left
        self.right = right
        self.terminal = terminal

class QNode:

    def __init__(self, urls, query):
        self.urls = urls
        self.query = query

class QueryConstruction(BaseSPARQL):

    def __init__(self, rules):
        BaseSPARQL.__init__(self)

    def build(self, tokens, root, ):
        pass

    def construct(self, root, lexica):
        rule = ' '.join([root.symbol, root.left.symbol, root.right.symbol])
        if rule in ['Q T E','Q E T']:
            if root.left.symbol == 'T':
                a = root.left
                b = root.right
            else:
                a = root.right
                b = root.left

            t = lexica[a.terminal]['T'][0]
            s,q,v = self.type(t)
            query = s,q,v
            p,o,q,v = self.new_predicate_object(query)
            query = o,q,v
            self.generate(query, b, lexica)

    def generate(self, query, node, lexica):
        if node.terminal:
            pass

class SemanticParser:

    def __init__(self):
        self.grammar = Grammar()
        self.lex_parser = QuerySegmentation()
        self.rules = self.grammar.none_terminal_rules
        self.query = QueryConstruction()

    def parse(self, query):
        segments, lexica = self.lex_parser.segmentation(query)
        nodes = self.CKY(segments, lexica)
        for n in nodes:
            self.query.construct(n, lexica)

    #Cocke-Kasami-Younger (CKY) bottom up parsing algorithm
    def CKY(self, tokens, lexica):
        terminals = self.grammar.terminal_rules(lexica)
        N = len(tokens) + 1
        chart = defaultdict(list)
        for i in range(1, N):
            for symbol in terminals[tokens[i-1]]:
                chart[(i-1,i)].append(Node(symbol,None,None,tokens[i-1]))
        for i in range(2, N):
            for j in range(i-1,-1,-1):
                for k in range(j+1,i):
                    for x in chart[(j,k)]:
                        for y in chart[(k,i)]:
                            c = ' '.join([x.symbol,y.symbol])
                            if c in self.rules:
                                for symbol in self.rules[c]:
                                    chart[(j,i)].append(Node(symbol, x, y, None))
        return [node for node in chart[(0, N - 1)] if node.symbol == self.grammar.start]

    def print_parse_tree(self, root, level):
        if root.terminal:
            print level*'*', root.symbol, root.terminal
        else:
            print level*'*', root.symbol
            self.print_parse_tree(root.left, 8+level)
            self.print_parse_tree(root.right, 8+level)

test = ["river which Brooklyn Bridge crosses",
        'mayors city United States',
        'airports in China',
        'In which country does the Ganges start?',
        'When is the movie Worst Case Scenario going to be in cinemas in the Netherlands',
        'Who is the mayor of Berlin?',
        'How many student does the Free University in Amsterdam have',
        'Give me all professional skateboarders from Sweden.',
        'When was Alberta admitted as province?']


parser = SemanticParser()
parser.parse(test[8])