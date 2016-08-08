from sematch.utility import FileIO
from sematch.knowledge.linking import EntityLinking
from sematch.knowledge.dbpedia import Spotlight
from sematch.knowledge.tagme import TAGME
from sematch.knowledge.babelnet import BabelNet
from sematch.knowledge.index import redirect_filter
from sematch.nlp import entity_recognition, phrase_chunk
import json

def metric(retrieved, relevant):
    if len(retrieved) > 0:
        commons = [x for x in relevant if x in retrieved]
        tp = len(commons) * 1.0
        retrieved_count = len(retrieved) * 1.0
        relevant_count = len(relevant) * 1.0
        precision = tp / retrieved_count
        recall = tp / relevant_count
        if precision > 0 or recall > 0:
            f = precision * recall
            f = 2 * f
            f = f / (precision + recall)
            return precision, recall, f
    return 0.0, 0.0, 0.0

def evaluation(retrieved, dataset):
    N = len(dataset)
    p_list = []
    r_list = []
    f_list = []
    for i in range(N):
        text, relevant = dataset[i]
        p,r,f = metric(retrieved[i],relevant)
        p_list.append(p)
        r_list.append(r)
        f_list.append(f)
    sum_p = sum(p_list)
    sum_r = sum(r_list)
    sum_f = sum(f_list)
    average_p = sum_p / N
    average_r = sum_r / N
    average_f = sum_f / N
    return average_p, average_r, average_f

def run_evaluation(linker, dataset):
    i = 1
    retrieved_list = []
    for q,r in dataset:
        result = linker.annotate(q)
        print i, ' ', result
        i = i + 1
        retrieved = []
        for key in result:
            retrieved.append(result[key])
        retrieved = list(set(retrieved))
        retrieved_list.append(retrieved)
    return evaluation(retrieved_list, dataset)

def babelfy_annotation(dataset, filename):
    #has 1000 request limitation
    babel = BabelNet()
    i = 1848
    for q,r in dataset[1848:]:
        result = babel.annotate(q)
        with open(FileIO.filename(filename), 'a') as f:
            json.dump({'link':result}, f)
            f.write("\n")
        print i, result
        i = i + 1

def evaluate_bablefy(dataset, filename):
    retrieved = FileIO.read_json_file(filename)
    retrieved = [d['link'] for d in retrieved]
    return evaluation(retrieved, dataset)


def spotting_dataset(spotfile, dataset):
    linker = EntityLinking()
    for q, r in dataset:
        spots = linker.spoting(q)
        print spots
        with open(FileIO.filename(spotfile), 'a') as f:
            json.dump(spots, f)
            f.write("\n")

def evaluate_spots(spotfile, dataset):
    spots = FileIO.read_json_file(spotfile)
    retrieved_list = []
    for data in spots:
        retrieved = []
        print data
        for key in data:
            retrieved += data[key].keys()
        retrieved = list(set(retrieved))
        retrieved_list.append(retrieved)
    return evaluation(retrieved_list, dataset)


def disambiguation_dataset(spotfile, dataset):
    linker = EntityLinking()
    spots = FileIO.read_json_file(spotfile)
    i = 0
    retrieved_list = []
    for q,r in dataset:
        result = linker.disambiguation(q, spots[i])
        print i, ' ', result
        i = i + 1
        retrieved = []
        for key in result:
            retrieved.append(result[key])
        retrieved = list(set(retrieved))
        retrieved_list.append(retrieved)
    return evaluation(retrieved_list, dataset)

def link_transform(link):
    uri = link.lstrip('<')
    uri = uri.rstrip('>')
    uri = 'http://dbpedia.org/resource/'+ uri[8:]
    return redirect_filter(uri)

def process_webquery_dataset():
    web_query = FileIO.read_list_file('eval/yerd/Y-ERD_spell-corrected.tsv')
    web_query = [data.split('\t') for data in web_query]
    web_query = [data for data in web_query if len(data) > 3]
    query = [data[2] for data in web_query]
    link = [data[4] for data in web_query]
    #linker = EntityLinking()
    dataset = {}
    for i in range(1, len(web_query)):
        dataset.setdefault(query[i], []).append(link_transform(link[i]))
    dataset = {key:value for key, value in dataset.items() if len(value) < 2}
    print len(dataset)
    dataset = [{'query':key, 'link':value} for key,value in dataset.items()]
    FileIO.save_json_file('eval/yerd/webquery.json', dataset)

def dataset_analysis(dataset):
    q_length = [len(t.split()) for t,r in dataset]
    N = len(q_length)
    print N
    print min(q_length)
    print max(q_length)
    print sum(q_length) * 1.0 / N


# Measure the performance in web question data
web_qa = FileIO.read_json_file('eval/qa/new.webquestions.json')
web_qa = [(data['utterance'], [data['dbpedia']]) for data in web_qa]

web_query = FileIO.read_json_file('eval/yerd/webquery.json')
web_query = [(data['query'], data['link']) for data in web_query]

for text, res in web_qa[:10]:
    print text, res
    print entity_recognition(text)
    print phrase_chunk(text)



#tagger = TAGME()
#print run_evaluation(tagger, web_qa)

#babelfy_annotation(web_qa, 'eval/babel_qa.json')

#print evaluate_bablefy(web_qa, 'eval/babel_qa.json')
#print evaluate_bablefy(web_query, 'eval/babel_query.json')

#babel = BabelNet()
#print web_query[10]
#print babel.annotate(web_query[10][0])
#tagger = TAGME()
#print run_evaluation(tagger, web_qa)

#spotting_dataset('eval/query_spots.json', web_query)
#print evaluate_spots('eval/query_spots.json', web_query)
#evaluate DBpedia spotlight
#linker = Spotlight()
#print run_evaluation(linker, web_query)
#print disambiguation_dataset('eval/query_spots.json', web_query)


#linker = Spotlight()
#print run_webQuestions(linker)

# Measure the performance in tweets
# tweet_text = FileIO.read_list_file('eval/tweets/NEEL2016-training.tsv')
# tweet_link = FileIO.read_list_file('eval/tweets/NEEL2016-training_neel.gs')
# tweet_text_dict = {data.split('\t')[0]:data.split('\t')[1] for data in tweet_text}
# tweet_link = [data.split('\t') for data in tweet_link]
# tweet_link = [data for data in tweet_link if data[3].__contains__('http://dbpedia.org/resource/')]
# tweet_data = {}
# for data in tweet_link:
#     if not tweet_data.get(data[0]):
#         tweet_data[data[0]] = []
#         tweet_data[data[0]].append(data[3])
#     else:
#         tweet_data[data[0]].append(data[3])
# tweet = []
# for key in tweet_data:
#     data = {}
#     data['tweet'] = tweet_text_dict[key]
#     data['links'] = tweet_data[key]
#     tweet.append(data)
# FileIO.save_json_file('eval/tweets/eval_data.json',tweet)

# print "***********************Twitter**********************"
#
# tweet = FileIO.read_json_file('eval/tweets/eval_data.json')
# tweet = [(data['tweet'], data['links']) for data in tweet]
# for t in tweet[:20]:
#     text, resource = t
#     print text, resource
#     linker.annotate(text)

#
# queries = ["who produce film starring Natalie Portman",
#             "give me all video game publish by mean hamster software",
#             "give me all soccer club in Spain",
#             "river which Brooklyn Bridge crosses",
#             "The Green Mile Tom Hanks",
#             "Nobel Prize China",
#             'vietnam travel national park',
#             'vietnam travel airports',
#             'Indian food',
#             'Neil Gaiman novels',
#             'films shot in Venice',
#             'Works by Charles Rennie Mackintosh',
#             'List of countries in World War Two',
#             'Paul Auster novels',
#             'State capitals of the United States of America',
#             'Novels that won the Booker Prize',
#             'countries which have won the FIFA world cup',
#             'EU countries',
#             'Films directed by Akira Kurosawa',
#             'Airports in Germany',
#             'Universities in Catalunya',
#             'Give me all professional skateboarders from Sweden',
#             'Give me all cars that are produced in Germany',
#             'Give me all movies directed by Francis Ford Coppola',
#             'Give me all companies in Munich',
#             'Give me a list of all lakes in Denmark',
#             'Give me all Argentine films',
#             'Give me a list of all American inventions',
#             'Give me the capitals of all countries in Africa',
#             'Give me all presidents of the United States',
#             'Give me all actors starring in Batman Begins',
#             'Which actors were born in Germany?',
#             'Give me all films produced by Hal Roach',
#             'Give me all books written by Danielle Steel',
#             'Give me all movies with Tom Cruise',
#             'Who directed One Day in Europe']