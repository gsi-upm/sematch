import json
import csv

#read json file
def read_json_file(name):
    data = []
    with open(name,'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

#save json file
def save_json_file(name,data):
    with open(name, 'w') as f:
        for d in data:
            json.dump(d, f)
            f.write("\n")

#save dict to file
def save_dict_file(name, data):
    with open(name,'w') as f:
        for key, value in data.iteritems():
            f.write(key)
            f.write("\t")
            f.write(value)
            f.write("\n")

#read file to dict
def read_dict_file(name):
    with open(name,'r') as f:
        data = {}
        for line in f:
            line = line.strip()
            key, value = line.split()
            data[key] = value
    return data

#save list to file
def save_list_file(name, data):
    with open(name,'w') as f:
        for d in data:
            f.write(d)
            f.write('\n')

#read small size file, load into meomery at onece.
def read_list_file(name):
    with open(name,'r') as f:
        data = [line.strip() for line in f]
    return data


def class_filter():
    filter_class = ["A","P"] #A means country, state, region, and P means city village....
    index = read_list_file("geo_data/es_geo_index_feature_map.txt") 
    index = [line.split()[0] for line in index if line.split()[1] in filter_class]
    index.sort()
    save_list_file("geo_data/es_city_index_all.txt", index)
    
#check the rdf dump consistency, scrape from the geonmae.org with latest updates.
def consistency_check(index_list, children_map, child_parent_map):
    queue = deque(["6255148"])
    keys = list(children_map)
    traversed = []
    while queue:
        item = queue.popleft()
        traversed.append(item)
        if item in keys:
            children = children_map[item]
            for child in children:
                queue.append(child)
    print "Traversed item number is %d" % len(traversed)
    not_traversed = [key for key in keys if key not in traversed]
    wrong = [n for n in not_traversed if n not in index_list]
    miss_items = []
    for w in wrong:
        miss_items += children_map[w]
    # rdf = scraping_geo_rdf(miss_items)
    # save_list_file("geo_data/miss_item_list.txt",rdf)
    miss_child_parent = {m:child_parent_map[m] for m in miss_items}
    save_dict_file("geo_data/miss_child_parent.txt", miss_child_parent)
    build_child_parent_map("geo_data/miss_item_list.txt", "geo_data/miss_child_parent_new.txt")
    

