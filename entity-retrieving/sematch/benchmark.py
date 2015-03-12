import sematch

def metrics(retrieved, relevants):
    a = len(relevants)
    b = len(retrieved)
    ab = 0
    for re in retrieved:
        if re in relevants:
            ab += 1
    recall = float(ab) / float(a)
    if b == 0:
        precision = 0
    else:
        precision = float(ab) / float(b)
    return recall, precision

def experiment():
    wordnet = sematch.WordNetLD()
    autoQuery = sematch.AutoQuery()
    dataset = sematch.read_json_file("data.txt")
    sim_thresholds = [0.2, 0.4, 0.6, 0.8, 1.0]
    print sim_thresholds
    sim_types = ['1','2','3','4','5','6']

    for i in range(len(dataset)):
    # for i in range(1,2):
        evaluation = {}
        evaluation['qid'] = i
        evaluation['sim-eval'] = []
        query = dataset[i]['query']
        entity = dataset[i]['entity']
        relevants = dataset[i]['result']
        print query, entity, relevants
        for t in sim_types:
            sim_eval = {}
            sim_eval['simType'] = t
            sim_eval['threshold-eval'] = []
            for th in sim_thresholds:
                th_eval = {}
                th_eval['threshold'] = th
                level_1 = {}
                types = wordnet.type_links(query, t, th)
                retrieved_1 = autoQuery.query(types, entity, 1)
                retrieved_2 = autoQuery.query(types, entity, 2)
                recall, precision = metrics(retrieved_1, relevants)
                level_1['recall'] = recall
                level_1['precision'] = precision
                th_eval['level-1'] = level_1
                level_2 = {}
                recall, precision = metrics(list(set(retrieved_1+retrieved_2)), relevants)
                level_2['recall'] = recall
                level_2['precision'] = precision
                th_eval['level-2'] = level_2
                sim_eval['threshold-eval'].append(th_eval)
            evaluation['sim-eval'].append(sim_eval)
        sematch.append_json_file('eval-results-3.txt', [evaluation])

def analysis(simType, level):
    ignore = [5,7,10,22]
    results = sematch.read_json_file("eval-results-3.txt")
    recall = []
    precision = []
    for i in range(len(results)):
        if i not in ignore:
            evaluation = results[i]['sim-eval']
            for e in evaluation:
                if e['simType'] == simType:
                    thresholds = e['threshold-eval']
                    recall.append([ threshold[level]['recall'] for threshold in thresholds])
                    precision.append([threshold[level]['precision'] for threshold in thresholds])
    avg_recall = []
    avg_precision = []
    for i in range(5):
        x = [rec[i] for rec in recall]
        y = [pre[i] for pre in precision]
        x_len = len(x)
        y_len = len(y)
        avg_recall.append(sum(x)/x_len)
        avg_precision.append(sum(y)/y_len)
    return avg_recall, avg_precision

def results():
    r_1_1,p_1_1 = analysis("1", "level-1")
    r_1_2,p_1_2 = analysis("1", "level-2")
    print r_1_1, p_1_1
    print r_1_2, p_1_2
    r_2_1,p_2_1 = analysis("2", "level-1")
    r_2_2,p_2_2 = analysis("2", "level-2")
    print r_2_1, p_2_1
    print r_2_2, p_2_2
    r_3_1,p_3_1 = analysis("3", "level-1")
    r_3_2,p_3_2 = analysis("3", "level-2")
    print r_3_1, p_3_1
    print r_3_2, p_3_2
    r_4_1,p_4_1 = analysis("4", "level-1")
    r_4_2,p_4_2 = analysis("4", "level-2")
    print r_4_1, p_4_1
    print r_4_2, p_4_2
    r_5_1,p_5_1 = analysis("5", "level-1")
    r_5_2,p_5_2 = analysis("5", "level-2")
    print r_5_1, p_5_1
    print r_5_2, p_5_2
    r_6_1,p_6_1 = analysis("6", "level-1")
    r_6_2,p_6_2 = analysis("6", "level-2")
    print r_6_1, p_6_1
    print r_6_2, p_6_2

#experiment()

#results()

autoQuery = sematch.AutoQuery()
data = autoQuery.retrieve_entity_obj("http://dbpedia.org/resource/Audi_A2")
