import json

#read json file
def read_json_file(name):
    data = []
    with open(name,'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

#save json file
def save_json_file(name, data):
    with open(name, 'w') as f:
        for d in data:
            json.dump(d, f)
            f.write("\n")

#read small size file, load into meomery at onece.
def read_list_file(name):
    with open(name,'r') as f:
        data = [line.strip() for line in f]
    return data

#read file to dict
def read_dict_file(name):
    with open(name,'r') as f:
        data = {}
        for line in f:
            line = line.strip()
            key, value = line.split()
            data[key] = value
    return data

def query_process():
    query = read_list_file('queries.txt')
    dataset = []
    for q in query:
        item = {}
        q_s = q.split()
        item['qid'] = q_s[0]
        item['terms'] = q_s[1:]
        dataset.append(item)
    return dataset

def result_process():
    result = read_list_file('qrels.txt')
    dataset = {}
    for r in result:
        r_s = r.split()
        r_list = dataset.setdefault(r_s[0], [])
        r_list.append(r_s[2])
    return dataset

def combine_data():
    query = query_process()
    result = result_process()
    for q in query:
        q['result'] = result[q['qid']]
    save_json_file('dataset.txt',query)

combine_data()