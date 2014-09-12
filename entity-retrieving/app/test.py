from indexer import Index
from searcher import Searcher

index = Index()
searcher = Searcher()

#es = id_code_map['2510769']
#madrid = id_code_map['3117732']
#es_list = sub_taxonomy(es, code_all)
#madrid_list = sub_taxonomy(madrid, es_list, depth=1)

sub_places = index.sub_areas('2510769', index.admin1)
print sub_places
#sub_keys = list(sub_places)
#print sub_places[sub_keys[1]]
#sub_places2 = index.sub_areas(sub_keys[1], index.admin2)
#print sub_places2

config = []
config.append({'sim':'string','weight':1.0, 'field':'name'})
query = {'config':config, 'name':'madrid'}
results = searcher.search(query, index.dataset[:100],'gid')
print results





