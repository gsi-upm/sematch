from collections import deque
from SPARQLWrapper import SPARQLWrapper, JSON
from simrec import Recommender
import urllib2
import json
import re
import csv
import multiprocessing
import re
import gc

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

class Worker(multiprocessing.Process):

    def __init__(self, task_queue, result_queue, index):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.index = index

    def test(self):
        rdf = []
        for item in iter(self.task_queue.get, 'STOP'):
            if item in self.index:
                rdf.append(item)
        self.result_queue.put(rdf)

    def run(self):
        proc_name = self.name
        print "Starting %s .." % proc_name
        pattern = re.compile(".org/(\d+)/")
        result = {}
        ids = []
        rdf = []
        for items in iter(self.task_queue.get, 'STOP'):
            for item in items:
                start = item.find("<gn:Feature")
                end = item.find("<rdfs")
                number = re.search(pattern,item[start:end]).group(1)
                if number in self.index:
                    ids.append(number)
                    rdf.append(item.strip())
            del items[:]
            gc.collect()
        result["index"] = ids
        result["data"] = rdf
        self.result_queue.put(result)
        print "Ending %s ..." % proc_name

    def run_scan_whole_geo_file(self):
        proc_name = self.name
        print "Starting %s .." % proc_name
        pattern = re.compile(".org/(\d+)/")
        rdf = []
        for items in iter(self.task_queue.get, 'STOP'):
            aNull = False
            i = iter(items)
            while not aNull:
                try:
                    item = i.next()
                    number = re.search(pattern,item).group(1)
                    if number in self.index:
                        item = i.next()
                        rdf.append(item.strip())
                    else:
                        i.next()
                except StopIteration:
                    aNull = True
            del items[:]
            gc.collect()
        self.result_queue.put(rdf)
        print "Ending %s ..." % proc_name

def load_file_lines(name, number, info, queue, start=1, end=0):
    """
    given a file name, read every number lines and put into queue, and produce line information
    every info lines. only extract the lines between start and end if given the start and end.
    """
    with open(name,'r') as f:
        count = 1
        line = f.readline()
        data = []
        while line:
            if end == 0:
                if count > start:
                    data.append(line)
                    if count % number == 0:
                        queue.put(data)
                        data = []
            else:
                if count >= start and count <= end:
                    data.append(line)
                    if count % number == 0:
                        queue.put(data)
                        data = []
            line = f.readline()
            count += 1
            if count % info == 0:
                print count
        if data:
            queue.put(data)

def boss():
    NUMBER_OF_PROCESSES = 2
    results = multiprocessing.Queue(5)
    tasks = multiprocessing.Queue(NUMBER_OF_PROCESSES)
    #index = read_file('geo_index_es.txt')
    index = read_file('city_index_es.txt')
    # used to test index
    # index = range(10000)[::100]
    # index = map(str,index)
    #initial annd start the workers.
    workers = [ Worker(tasks,results,index) for i in range(NUMBER_OF_PROCESSES) ]
    for w in workers:
        w.daemon = True
        w.start()
    # for i in range(10000):
    #   tasks.put(i)
    #read a specific number of lines from the file into memory and put into the queue.
    #do the whole file scan 
    #load_file_lines("all-geonames-rdf.txt", 300000, 1000000, tasks)
    load_file_lines("es_rdf.txt", 10000, 10000, tasks)
    #Notify the child process to stop.
    for w in workers:
        tasks.put("STOP")
    #collecting the computing results and wait the child processes finish.
    #the calling order matters. The join() should be called after collecting 
    #the result by calling result queue with get(), otherwise, the child process
    #will block.
    # rdf = []
    # for w in workers:
    #   rdf += results.get()
    # for w in workers:
    #   w.join()
    #save result and exit
    #save_file('es_rdf.txt',rdf)
    rdf = []
    ids = []
    for w in workers:
        result = results.get()
        ids += result["index"]
        rdf += result["data"]
    for w in workers:
        w.join()
    ids.sort()
    save_file('city_extracted_rdf_index.txt',ids)
    save_file('city_extracted_rdf.txt',rdf)

    print "Finished..."
    print "num active children:", multiprocessing.active_children()

#build the index of the city entity from the geo entitys.
def filter_city():
    filter_class = ["A","P"] #A means country, state, region, and P means city village....
    index = read_list_file("geo_data/es_geo_index_feature_map.txt") 
    index = [line.split()[0] for line in index if line.split()[1] in filter_class]
    index.sort()
    save_list_file("geo_data/es_city_index_all.txt", index)
    
#scraping the missing city entity from the geoname.org
def scraping_missing_city():
    city_all = read_list_file("geo_data/es_city_index_all.txt")
    city_ex = read_list_file("geo_data/city_ex_index.txt")
    lost = [line for line in all_index if line not in ex_index]
    print "start scraping.."
    print "Need to extract %s city entities from geoname.org" % len(lost)
    rdf = scraping_geo_rdf(lost)
    save_list_file("geo_data/ex_web_rdf.txt",rdf)

def scraping_geo_rdf(scraping_list):
    path = "http://www.geonames.org/%s/about.rdf"
    count = 1
    rdf = []
    for geo_id in scraping_list:
        url = path % geo_id
        about_rdf = urllib2.urlopen(url).read()
        print count, '\t', url
        count += 1
        begin = about_rdf.find("<gn:Feature")
        end = about_rdf.find("<foaf:Document")
        about_rdf = about_rdf[begin:end]
        about_rdf = about_rdf.replace("\n","")
        if not about_rdf:
            break
        rdf.append(about_rdf)
    return rdf

def scraping_dbpedia(scraping_map):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    dbpedia = []
    count = 1
    for key in scraping_map:
        #city = "http://dbpedia.org/resource/La_Matilla"
        city = scraping_map[key]
        sparql.setQuery("""
            SELECT *
    WHERE {<"""+city+"""> <http://dbpedia.org/ontology/abstract> ?abstract .
FILTER(lang(?abstract) = "en").
optional{<"""+city+"""> <http://dbpedia.org/ontology/PopulatedPlace/areaTotal> ?area} .
optional{<"""+city+"""> <http://dbpedia.org/ontology/populationTotal> ?population} .}
""")
        results = sparql.query().convert()
        if results["results"]["bindings"]:
            print count
            count += 1
            result = results["results"]["bindings"][0]
            entity = {}
            entity['key'] = key
            entity['uri'] = city
            entity['abstract'] = result["abstract"]["value"]
            if result.get('area'):
                entity['area'] = result["area"]["value"]
            if result.get('population'):
                entity['population'] = result["population"]["value"]
                dbpedia.append(entity)
    return dbpedia


#remove the unnecesaary info in the rdf entity.             
def clean_rdf():
    data = read_list_file("geo_data/city_extracted_rdf.txt")
    newData = []
    for d in data:
        begin = d.find("<gn:Feature")
        end = d.find("</rdf:")
        newData.append(d[begin:end])
    save_list_file("geo_data/city_ex_rdf_clean.txt",newData)

def dbpedia_links(index):
    links_dbpedia = read_list_file("geo_data/geonames_links.nt")
    if not index:
        index = read_list_file("geo_data/city_index_all.txt")
    pattern = re.compile(".org/(\d+)/")
    geo_db_map = {}
    for line in links_dbpedia:
        line = line.rstrip(".\n")
        dbpedia, p, geoname = line.split()
        geo_id = re.search(pattern, geoname)
        if geo_id:
            geo_id = geo_id.group(1)
            if geo_id in index:
                dbpedia = dbpedia.lstrip("<")
                dbpedia = dbpedia.rstrip(">")
                geo_db_map[geo_id] = dbpedia
    save_dict_file("geo_data/dbpedia_link_map.txt",geo_db_map)
    print "total number of dbpeida links is %d" % len(geo_db_map)
    return geo_db_map

#build the index of the entities.
def indexing_rdf(inName, outName):
    rdf_list = read_list_file(inName)
    pattern = re.compile(".org/(\d+)/")
    index_list = []
    for rdf in rdf_list:
        start = rdf.find("<gn:Feature")
        end = rdf.find("<rdfs")
        g_id = re.search(pattern, rdf[start:end]).group(1)
        index_list.append(g_id)
    save_list_file(outName, index_list)

def build_child_parent_map(inName, outName):
    rdf_list = read_list_file(inName)
    pattern = re.compile(".org/(\d+)/")
    child_parent_map = {}
    for rdf in rdf_list:
        id_s = rdf.find("<gn:Feature")
        id_e = rdf.find("<rdfs")
        rdf_id = re.search(pattern, rdf[id_s:id_e]).group(1)
        p_s = rdf.find("<gn:parentFeature")
        p_e = rdf.find("<gn:parentCountry")
        p_id = re.search(pattern, rdf[p_s:p_e]).group(1)
        child_parent_map[rdf_id] = p_id
    save_dict_file(outName, child_parent_map)

#build the index of rdf. child_parent_map id parent: id. id_entity_map id:entity
def get_id_rdf_map(fileName):
    rdf_list = read_list_file(fileName)
    pattern = re.compile(".org/(\d+)/")
    id_rdf_map = {}
    for rdf in rdf_list:
        id_s = rdf.find("<gn:Feature")
        id_e = rdf.find("<rdfs")
        rdf_id = re.search(pattern, rdf[id_s:id_e]).group(1)
        id_rdf_map[rdf_id] = rdf
    return id_rdf_map

#build the parent children map. geoname:[children]
def build_reverse_index(child_parent_map):
    children_map = {}
    for key, value in child_parent_map.iteritems():
        if children_map.get(value):
            children_map.get(value).append(key)
        else:
            children = []
            children.append(key)
            children_map[value] = children
    keys = list(children_map)
    children_lengths = map(lambda x:len(children_map[x]), keys)
    print "total number of items are %d" % sum(children_lengths)
    print "max length is %d" % max(children_lengths)
    print "min length is %d" % min(children_lengths)
    return children_map

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
    

def patch_child_parent_map():
    child_parent_map = read_dict_file("geo_data/child_parent_map.txt")
    correct = read_dict_file("geo_data/miss_child_parent_new.txt")
    print "total number of child parent map is %d" % len(child_parent_map)
    print "total number of correct is %d" % len(correct)
    erros = ["6324921","6325087","6325210","6325249"]
    for e in erros:
        del child_parent_map[e]
        del correct[e]
    print "total number of child parent map is %d after removing errors" % len(child_parent_map)
    print "total number of correct is %d after removing errors" % len(correct)
    for key in correct:
        child_parent_map[key] = correct[key]
    save_dict_file("geo_data/child_parent_map.txt", child_parent_map)

#identifier coding in resource url
#001001001 stands for a branch. every thousand represents a level.
#001001002 stands for the brothers of the first entity.
#001001 stands for the parent entity.
def build_identifier_map(children_map):
    format = "%0*d"
    id_code_map = {}
    keys = list(children_map)
    queue = deque(["6255148"]) #Europe
    id_code_map["6255148"] = "001"
    traversed = []
    while queue:
        item = queue.popleft()
        traversed.append(item)
        if item in keys:
            count = 1
            code_parent = id_code_map[item]
            children = children_map[item]
            for child in children:
                queue.append(child)
                code = format % (3, count)
                code = code_parent + code
                id_code_map[child] = code
                count += 1
    print "Traversed item number is %d" % len(traversed)
    print "Identifers length is %d" % len(id_code_map)
    save_dict_file("geo_data/id_code_map.txt", id_code_map)

#To generate the skos taxonomy
def build_taxonomy():
    id_rdf_map= get_id_rdf_map("geo_data/city_ex_rdf.txt")
    # indexing_rdf("geo_data/city_ex_rdf", "geo_data/city_ex_index.txt")
    index_list = read_list_file("geo_data/city_ex_index.txt")
    erros = ["6324921","6325087","6325210","6325249"]
    for e in erros:
        index_list.remove(e)
    print "total number of cities is %d" % len(index_list)
    # build_child_parent_map("geo_data/city_ex_rdf.txt", "geo_data/child_parent_map.txt")
    child_parent_map = read_dict_file("geo_data/child_parent_map.txt")
    children_map = build_reverse_index(child_parent_map)
    print "total number of children_map is %d" % len(children_map)
    # consistency_check(index_list, children_map, child_parent_map)
    # patch_child_parent_map()
    # build_identifier_map(children_map)
    id_code_map = read_dict_file("geo_data/id_code_map.txt")
    print "total number of identifers %d" % len(id_code_map)
    #dbpedia_map = dbpedia_links(index)
    dbpedia_map = read_dict_file("geo_data/dbpedia_link_map.txt")
    print "total number of dbpeida links is %d" % len(dbpedia_map)
    dbpedia_data_map = scraping_dbpedia(dbpedia_map)

    queue = deque(["2510769"])
    keys = list(children_map)
    taxonomy = {}
    rdf_pre =  '<rdf:Description rdf:about="http://www.gsi.dit.upm.es/geo/#%s">'
    rdf_post = '</rdf:Description>'
    same_as = '<owl:sameAs rdf:resource="http://sws.geonames.org/%s/"/>'
    broader = '<skos:broader rdf:resource="http://www.gsi.dit.upm.es/geo/#%s"/>'
    narrower = '<skos:narrower rdf:resource="http://www.gsi.dit.upm.es/geo/#%s"/>'
    related = '<skos:related rdf:resource="%s"/>'
    area = '<dbpedia-owl:PopulatedPlace/areaTotal>%s</dbpedia-owl:PopulatedPlace/areaTotal>'
    population = '<dbpedia-owl:populationTotal>%s</dbpedia-owl:populationTotal>'
    abstract = '<dbpedia-owl:abstract>%s</dbpedia-owl:abstract>'
    while queue:
        item = queue.popleft()
        geo_rdf = id_rdf_map[item]
        name_start = geo_rdf.find("<gn:name>")
        name_end = geo_rdf.find("</gn:name>") + 10
        geo_name = geo_rdf[name_start:name_end]
        lat_s = geo_rdf.find("<wgs84_pos:lat")
        lat_e = geo_rdf.find("</wgs84_pos:lat") + 16
        geo_lat = geo_rdf[lat_s:lat_e]
        lon_s = geo_rdf.find("<wgs84_pos:long")
        lon_e = geo_rdf.find("</wgs84_pos:long") + 17
        geo_lon = geo_rdf[lon_s:lon_e]
        new_rdf = taxonomy.get(item)
        if not new_rdf:
            new_rdf = ""
            taxonomy[item] = new_rdf
        new_rdf = geo_lon + new_rdf
        new_rdf = geo_lat + new_rdf
        if item in dbpedia_map:
            new_rdf = related % dbpedia_map[item] + new_rdf
            db_data = dbpedia_data_map[item]
            new_rdf = abstract % db_data['abstract'].encode('utf-8') + new_rdf
            if db_data.get('area'):
                new_rdf = area % db_data['area'].encode('utf-8') + new_rdf
            if db_data.get('population'):
                new_rdf = population % db_data['population'].encode('utf-8') + new_rdf
        new_rdf = same_as % item + new_rdf
        new_rdf = geo_name + new_rdf
        print new_rdf
        if item in keys:
            code_parent = id_code_map[item]
            children = children_map[item]
            for child in children:
                queue.append(child)
                code_child = id_code_map[child]
                child_rdf = broader % code_parent
                taxonomy[child] = child_rdf
                new_rdf = new_rdf + narrower % code_child
        new_rdf = rdf_pre % id_code_map[item] + new_rdf
        new_rdf = new_rdf + rdf_post
        print new_rdf
        taxonomy[item] = new_rdf
    save_dict_file("geo_data/es_city_skos_taxonomy.txt",taxonomy)


if __name__ == '__main__':
    #boss()
    #build_taxonomy()
    dbpedia_map = read_dict_file("../geo_data/dbpedia_link_map.txt")
    keys = list(dbpedia_map)
    #json_data = scraping_dbpedia(dbpedia_map)
    #save_json_file("geo_data/dbpedia_data.txt",json_data)
    json_data = read_json_file("../geo_data/dbpedia_data.txt")
    print "total number of scrapped entity is %d" % len(json_data)
    c_pop = 0
    c_area = 0
    c_abstract = 0
    miss_abstract = []
    for data in json_data:
        if data.get('population'):
            c_pop += 1
        if data.get('area'):
            c_area += 1
        if data.get('abstract'):
            c_abstract += 1
        if not data.get('abstract'):
            miss_abstract.append(data)
    print "total number of population is %d" % c_pop
    print "total number of area is %d" % c_area
    print "total number of abstract is %d" % c_abstract
    #print miss_abstract
    # scrapped = [data['key'] for data in json_data]
    # missed = [key for key in keys if key not in scrapped]
    # print "total number of missed entities are %d" % len(missed)
    # missed_map = {key:dbpedia_map[key] for key in missed}
    #save_dict_file("geo_data/missed_dbpedia_data.txt", missed_map)
    #dbpedia_links([])
    data_set = [data for data in json_data if data.get('population') and data.get('area') and data.get('abstract')]
    print "total number of entity in data set is %d" % len(data_set)
    skos_f = open("../geo_data/es_city_skos_taxonomy.txt")
    skos_data = {}
    for line in skos_f:
        key,value = line.split('\t')
        skos_data[key] = value
    skos_f.close()
    pattern = re.compile("geo/#(\d+)")
    for data in data_set:
        key = data['key']
        skos = skos_data[key]
        g_s = skos.find("<rdf:Description")
        g_e = skos.find("<gn:name")
        geograph = re.search(pattern, skos[g_s:g_e]).group(1)
        n_s = g_e + 9
        n_e = skos.find("</gn:name")
        name = skos[n_s:n_e]
        lat_s = skos.find("<wgs84_pos:lat") + 15
        lat_e = skos.find("</wgs84_pos:lat")
        lat = skos[lat_s:lat_e]
        lon_s = skos.find("<wgs84_pos:long") + 16
        lon_e = skos.find("</wgs84_pos:long")
        lon = skos[lon_s:lon_e]
        data['geo'] = geograph
        data['name'] = name
        data['lat'] = lat
        data['lon'] = lon
    config = []
    #config.append({'sim':'string','weight':0.05, 'field':'name'})
    #config.append({'sim':'numeric','weight':0.15, 'field':'area'})
    config.append({'sim':'numeric','weight':1, 'field':'population'})
    #config.append({'sim':'taxonomy','weight':1, 'field':'geo'})
    data_dict = {data['key']:data for data in data_set}
    rec = Recommender(data_set, config)
    print rec.recommend(data_dict['3117735'])
    

        







