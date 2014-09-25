import sematch

wordnet = sematch.WordNetLD()
autoQuery = sematch.AutoQuery()
dataset = sematch.read_json_file("test.txt")

for data in dataset:
    query = data['query']
    entity = data['entity']
    result = data['result']
    types = wordnet.type_links(query[0], 1, 0.5)
    retrieved = autoQuery.query(types, entity)
    a = len(result)
    b = len(retrieved)
    a_b = 0
    for re in retrieved:
        if re in result:
            a_b += 1
    recall = float(a_b) / float(a)
    precision = float(a_b) / float(b)
    print recall, precision
