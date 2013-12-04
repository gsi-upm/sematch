#from sklearn.metrics import pairwise 
from operator import itemgetter
import Levenshtein
import math

class Similarity:
    """
    This class is used for calculating similarities.
    """
   # def __init__(self):

    #String similarity
    
    def string(self, X, Y):
        return Levenshtein.ratio(X, Y)

    #convert the distance to similarity

    def d_to_s(self, x):
        return 1 / (1 + x)

    #sigmoid function

    def sigmoid(self, x):
        if x > 500:
            return 0
        return self.d_to_s(math.exp(x))

    #difference of two list

    def difference(self, X, Y):
        return [X[i] - Y[i] for i in range(len(X))]

    def square(self, x):
        return x**2

    #The length of X and Y should be identical

    def minkowski(self, X, Y, r):
        distance = self.difference(X,Y)
        distance = map(abs, distance)
        distance = map(lambda x:pow(x,r), distance)
        distance = sum(distance)
        distance = pow(distance, 1/r)
        return self.d_to_s(distance)

    #manhattan similarity is when r in minkowski equals 1

    def manhattan(self, X, Y):
        return self.minkowski(X,Y,1)

    #euclidean similarity is when r in minkowski equals 2

    def euclidean(self, X, Y):
        return self.minkowski(X,Y,2)

    #Numerical similarity

    def numeric(self, X, Y, scale=1000000):
        X = float(X)
        Y = float(Y)
        diff = X - Y 
        diff = diff/scale
        sim = self.sigmoid(abs(diff))
        return sim*2

    #cosine similarity

    #def cosine(self, X, Y):
    #    return pairwise.cosine_similarity(X,Y)


    #get the least common ancestor

    def common_depth(self, X, Y, shorter):
        c_depth = 0
        for i in range(shorter):
            j = 3 * i
            k = j + 3
            if X[j:k] == Y[j:k]:
                c_depth += 1
            else:
                break
        return c_depth

    #Taxonomical similarity

    def taxonomy(self, X, Y, up=0.7, down=0.8):
        depth_x = len(X) / 3
        depth_y = len(Y) / 3
        sim = 1
        if depth_x > depth_y:
            depth_common = self.common_depth(X, Y, depth_y)
        else:
            depth_common = self.common_depth(X, Y, depth_x)
        path_up = depth_x - depth_common
        path_down = depth_y - depth_common
        if path_up == 0 and path_down == 0:
            sim = 1
        elif path_up == 0:
            sim = math.pow(down, path_down)
        elif path_down == 0:
            sim = math.pow(up, path_up)
        else:
            sim = math.pow(down, path_down) * math.pow(up, path_up)
        return math.log(sim+1,2)

    
class Recommender:
    """
    Simple similarity-based recommendation system
    """
    def __init__(self, data_set):
        self.data_set = data_set
        self.sim = Similarity()
        self.sim_map = {}
        self.sim_map['numeric'] = self.sim.numeric
        self.sim_map['string'] = self.sim.string
        self.sim_map['taxonomy'] = self.sim.taxonomy
    
    def create_tasks(self, query, resource):
        tasks = []
        for conf in query['config']:
            s = self.sim_map[conf['sim']]
            w = conf['weight']
            q = query[conf['field']]
            r = resource[conf['field']]
            tasks.append((s, w, (q, r))) 
        return tasks

    def task_unit(self, task):
        func, weight, args = task
        return weight*func(*args)

    def compute(self, query, resource):
        tasks = self.create_tasks(query, resource)
        return map(self.task_unit, tasks)

    def recommend(self, query, top_n=10):
        results = []
        for data in self.data_set:
            results.append((data['key'], sum(self.compute(query, data))))
        results = sorted(results, key=itemgetter(1), reverse=True)
        return results[:top_n]
    
