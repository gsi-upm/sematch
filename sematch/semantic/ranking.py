from collections import Counter
from itertools import combinations
import networkx as nx

class GraphRank:

    def __init__(self):
        pass


    # ambiguous_synsets = self.word2synset(ambiguous_word)
    # if not ambiguous_synsets:
    #     return None
    # if len(ambiguous_synsets) == 1:
    #     return ambiguous_synsets[0]
    # context_words = list(set(context_words))
    # context_synsets = []
    # for word in context_words:
    #     if word != ambiguous_word:
    #         context = wn.synsets(word, pos=wn.NOUN)
    #         if context:
    #             for con in context:
    #                 context_synsets.append(con)
    # context_synsets = list(set(context_synsets))
    # all_synsets = [x for x in ambiguous_synsets]
    # for x in context_synsets:
    #     if x not in ambiguous_synsets:
    #         all_synsets.append(x)
    # synset_id_dic = {all_synsets[i]: i for i in range(len(all_synsets))}
    # graph = nx.Graph()
    # for pair in combinations(all_synsets, 2):
    #     x, y = pair
    #     sim_score = self.similarity(x, y, method)
    #     if sim_score > 0:
    #         graph.add_edge(synset_id_dic[x], synset_id_dic[y], weight=sim_score)
    # ranks = nx.pagerank(graph)
    # result = {x: ranks[synset_id_dic[x]] for x in ambiguous_synsets if synset_id_dic[x] in ranks}
    # return Counter(result).most_common(1)[0][0]