from collections import deque
import utils
import gc

#taxonomy coder
#001 stand for global, root node
#001001 stand for a continent 
#001001001 should stand for a country 
#
#every thousand represents a level. start with 1 until 999
#    Earth   geonameID=6295630
#    AF : Africa         geonameId=6255146
#    AS : Asia           geonameId=6255147
#    EU : Europe         geonameId=6255148
#    NA : North America      geonameId=6255149
#    OC : Oceania            geonameId=6255151
#    SA : South America      geonameId=6255150
#    AN : Antarctica         geonameId=6255152

def taxonomy_coder():
    #each parent will contain a list of children.
    #need to count the maximum children length in order to 
    #decide how many digits for a level.
    parent_child_list = utils.read_list_file(\
            'data-sematch/hierarchy.txt')
    parent_children_map= {}
    for pairs in parent_child_list:
        pairs = pairs.split('\t')
        parent, child = (pairs[0],pairs[1])
        if child != '0':
            parent_children_map.setdefault(\
                    parent,[]).append(child)
    keys = list(parent_children_map)
    children_lengths = map(lambda x:len(\
            parent_children_map[x]), keys)
    print "numbers of the parent is %d" % len(keys)
    print "max children length is %d" % max(children_lengths)
    print "min children length is %d" % min(children_lengths)

    #breadth first tree traverse based coder.
    format = "%0*d"
    id_code_map = {}
    queue = deque(["6295630"]) #Earth
    id_code_map["6295630"] = "001"
    while queue:
        item = queue.popleft()
        if item in keys :
            count = 1
            code_parent = id_code_map[item]
            children = parent_children_map[item]
            for child in children:
                queue.append(child)
                code = format % (3, count)
                code = code_parent + code
                id_code_map[child] = code
                count += 1
    utils.save_dict_file("geo_taxonomy.txt", id_code_map)

#load the geo name dataset
def load_geoname_data(file_path):
    name_list = utils.read_list_file(file_path)
    geo_names = []
    for gname in name_list:
        name = gname.split('\t')
        name_dict = {}
        name_dict['gid'] = name[0] #geonameID
        name_dict['name'] = name[1] #place name
        name_dict['asici'] = name[2] #asici version name
        #feature class and feature code
        name_dict['feature'] = '.'.join((name[6],name[7]))
        #country code and admin code
        #geoname only provide 2 levels, would be better for all
        #need to check if the data is null
        if name[10]:
            name_dict['admin1'] = '.'.join((name[8], name[10]))
        else:
            name_dict['admin1'] = 'null'
        if name[11]:
            name_dict['admin2'] = '.'.join((name_dict['admin1'], name[11]))
        else:
            name_dict['admin2'] = 'null'
        geo_names.append(name_dict)
    #manual garbage collection because those data segments are big
    del name_list[:]
    gc.collect()
    return geo_names


#spain 2510769
#china 1814991
#madrid 3117732
#zhejiang 1784764
#default depth return all the sub taxonomy
#depth 1 means 1 sublevel, depth 2 means until 2 sublevel.
#return a sub taxonomy given the context
def sub_taxonomy(pattern, code_list, depth=0):
    if depth == 0:
        return [code for code in code_list if code.startswith(pattern)]
    else:
        len_pattern = len(pattern)
        len_sub = 3*depth
        len_all = len_pattern + len_sub
        return [code for code in code_list if code.startswith(pattern)\
                and len_pattern< len(code) <= len_all]

#if __name__ == '__main__':
    #taxonomy_coder()

#read the taxonomy from file which contain geonanmeID and code map.
id_code_map = utils.read_dict_file("geo_taxonomy.txt")
#build the code and geonameID map, search a geoname by code
code_id_map = { id_code_map[key]:key for key in id_code_map }
#all the code list used for deriving hierarchical sub taxonomy.
code_all = list(code_id_map)
es = id_code_map['2510769']
madrid = id_code_map['3117732']
es_list = sub_taxonomy(es, code_all)
madrid_list = sub_taxonomy(madrid, es_list, depth=1)
dataset = load_geoname_data("data-sematch/ES.txt")

