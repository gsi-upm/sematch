from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic

class WordNetLD:

    def __init__(self):
        self.synsets_list = list(wn.all_synsets())
        self.synset_to_id = { s:s.offset for s in self.synsets_list }
        self.brown_ic = wordnet_ic.ic('ic-brown.dat')
        #self.id_to_synset = { s.offset:s for s in self.synsets_list}

    # def get_mappings(self, offsets):
    #     results = []
    #     for i in offsets:
    #         if link_map_index.get(i):
    #             print link_map_index[i]
    #             results.append(link_map_index[i])
    #     return results

    def add_obj(self, slist, synset, sim):
        obj = {}
        obj['simbol'] = str(synset)
        obj['definition'] = synset.definition
        obj['offset'] = str(self.synset_to_id[synset]+100000000)
        obj['sim'] = sim
        slist.append(obj)

    def similarity(self, syn1, syn2, simType):
        if simType == '1':
            return syn1.wup_similarity(syn2)
        if simType == '2':
            return syn1.path_similarity(syn2)
        if simType == '3':
            return syn1.lch_similarity(syn2)
        if simType == '4':
            return syn1.res_similarity(syn2, self.brown_ic)
        if simType == '5':
            return syn1.jcn_similarity(syn2, self.brown_ic)
        if simType == '6':
            return syn1.lin_similarity(syn2, self.brown_ic)

    #use wn built in search to get synsets using lemma search,
    #and expand the synsets with its children and parent and siblings.
    def search_synsets(self, query, simType):
        synsets = wn.synsets(query, pos=wn.NOUN)
        synsets_list = []
        for s in synsets:
            self.add_obj(synsets_list, s, 1.0)
            for h in s.hyponyms():
                sim = self.similarity(s, h, simType)
                self.add_obj(synsets_list, h, sim)
            for h in s.hypernyms():
                sim = self.similarity(s, h, simType)
                self.add_obj(synsets_list, h, sim)
                for son in h.hyponyms():
                    sim = self.similarity(s, son, simType)
                    self.add_obj(synsets_list, son, sim)
        return synsets_list

