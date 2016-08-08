# coding=utf-8
from sematch.utility import FileIO
from sematch.knowledge.sparql import BaseSPARQL
from sematch.semantic.relatedness import EntityRelatedness

data_file = 'eval/entity-relatedness/KORE_entity_relatedness/rankedrelatedentities.txt'
relatedness = EntityRelatedness()

def load_dataset():
    with open(FileIO.filename(data_file), 'r') as f:
        data = [line.strip() for line in f]
    entities = {}
    N = len(data)
    for i in range(0, N, 21):
        d = data[i:i+21]
        entities[d[0]] = d[1:]
    return entities

data = load_dataset()
sparql = BaseSPARQL()

def literal2uri(terms):
    res_str = terms.decode('utf-8')
    uri_str = 'http://dbpedia.org/resource/%s'
    link = uri_str % '_'.join(res_str.split())
    try:
        redirect = sparql.check_redirect(link)
    except:
        print link
        return None
    if redirect:
        return redirect[0]
    else:
        return link

retrieved = FileIO.read_json_file('eval/entity-relatedness/KORE_entity_relatedness/rank-entity.json')
# key_exist = [x['query'].keys()[0] for x in retrieved]
# for key in data:
#     if key not in key_exist:
#         doc = {}
#         doc['query'] = {key:literal2uri(key)}
#         entities = [{e:literal2uri(e)} for e in data[key]]
#         doc['entities'] = entities
#         print doc
#         FileIO.append_json_file('eval/entity-relatedness/KORE_entity_relatedness/rank-entity.json', [doc])

# json_data = []
# for x in retrieved:
#     doc = {}
#     key = x['query'].keys()[0]
#     value = x['query'][key]
#     doc['query'] = {'words':key, 'link':value}
#     e_list = []
#     for i in range(len(x['entities'])):
#         item = x['entities'][i]
#         key = item.keys()[0]
#         value = item[key]
#         e_list.append({'words':key, 'link':value, 'rank':i+1})
#     doc['entities'] = e_list
#     json_data.append(doc)
#
# FileIO.save_json_file('eval/entity-relatedness/KORE_entity_relatedness/rank-entity2.json', json_data)

for x in retrieved:
    pass

    #print relatedness.uri2synsets(link)