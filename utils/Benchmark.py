from utility import FileIO
from Expansion import SynsetExpansion
from QueryEngine import Engine

class Experiment:

    def __init__(self):
        self.dataset = FileIO.read_json_file("sematch/benchmark-data/data.txt")
        self.results = FileIO.read_list_file("sematch/benchmark-data/result.txt")
        self.queries = [(d['query'],d['entity']) for d in self.dataset]
        self.relevants = [d['result'] for d in self.dataset]
        self.synsetExpansion = SynsetExpansion()
        self.engine = Engine()
        self.sims = ['wup', 'lch', 'res','jcn', 'lin']
        self.thresholds = [0.9,1]
        self.gpcs = ['gpc1', 'gpc2', 'gpc3', 'gpc4', 'gpc5', 'gpc6']

    @staticmethod
    def measure(relevant, retrieved):
        a = len(relevant)
        b = len(retrieved)
        ab = 0
        for re in retrieved:
            if re in relevant:
                ab += 1
        recall = float(ab) / float(a)
        if b == 0:
            precision = 0
        else:
            precision = float(ab) / float(b)
        if precision + recall == 0:
            f = 0
        else:
            f = 2 * (precision * recall) / (precision + recall)
        return recall, precision , f

    def query_info(self, id):
        tQ, eURI = self.queries[id]
        relevant_data = self.relevants[id]
        print id, '\tquery: ', ' '.join(self.dataset[id]['terms'])
        print tQ, eURI
        print 'N(relevant)=', len(relevant_data)

    def print_query(self, id, gpc, sim, th):
        tQ, eURI = self.queries[id]
        tURIs = self.typeExpansion.expandType(tQ, sim, th)
        print "Number(types)=", len(tURIs)
        query = self.engine.query(gpc, tURIs, eURI)
        #result = self.engine.sparql.execute(query)
        result = self.engine.sparql.request_execution(query)
        print result

    def experiment(self, id, gpcs, sim, th):
        tQ, eURI = self.queries[id]
        relevant_data = self.relevants[id]
        tURIs = self.typeExpansion.expandType(tQ, sim, th)
        result = self.engine.run(gpcs,tURIs, eURI)
        #print sim, th, gpcs
        #print "N(type uris)=",len(tURIs)
        #print 'N(returned)=', len(result)
        #print 'recall is %f, precison is %f, f measure is %f' % Experiment.measure(relevant_data,result)
        print Experiment.measure(relevant_data,result)

    def analysis(self):
        data = self.results
        data = [d.lstrip('(') for d in data]
        data = [d.rstrip(')') for d in data]
        data = [d.split(',') for d in data]
        data = [map(float, d) for d in data]
        data = [data[i:i+20] for i in range(0,len(data),20)]
        sum_data = data[0]
        for d in data[1:]:
            for i in range(20):
                sum_data[i][0] += d[i][0]
                sum_data[i][1] += d[i][1]
                sum_data[i][2] += d[i][2]

        for i in range(20):
            print i+1, '***************'
            print sum_data[i][0] / 22.0
            print sum_data[i][1] / 22.0
            print '***************'

