import json
import ConfigParser
import os

class Configuration:

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('settings.cfg')

    def getConfig(self,section,variable):
        return self.config.get(section,variable)


class FileIO:

    @staticmethod
    def path():
        return os.path.dirname(__file__)

    @staticmethod
    def filename(name):
        if FileIO.path() not in name:
            name = os.path.join(FileIO.path(), name)
        return name

    @staticmethod
    def read_json_file(name):
        data = []
        with open(FileIO.filename(name),'r') as f:
            for line in f:
                data.append(json.loads(line))
        return data

    @staticmethod
    def save_json_file(name, data):
        with open(FileIO.filename(name), 'w') as f:
            for d in data:
                json.dump(d, f)
                f.write("\n")

    @staticmethod
    def append_json_file(name, data):
        with open(FileIO.filename(name), 'a') as f:
            for d in data:
                json.dump(d, f)
                f.write("\n")

    @staticmethod
    def append_list_file(name, data):
        with open(FileIO.filename(name), 'a') as f:
            for d in data:
                f.write(d)
                f.write('\n')

    @staticmethod
    def save_list_file(name, data):
        with open(FileIO.filename(name),'w') as f:
            for d in data:
                f.write(d)
                f.write('\n')

    @staticmethod
    def read_list_file(name):
        with open(FileIO.filename(name),'r') as f:
            data = [line.strip() for line in f]
        return data


def trace(f):
    def g(x):
        print f.__name__, x
        value = f(x)
        print 'return', repr(value)
        return value
    return g


# config = Configuration()
# print type(config.getConfig('expansion','sim'))
# print type(config.getConfig('expansion', 'th'))
# print config.getConfig('expansion','gpcs')


import Levenshtein
import math


#String similarity

def string_similarity(X, Y):
    return Levenshtein.ratio(X, Y)

#convert the distance to similarity

def fraction(x):
    return 1 / (1 + x)

#difference of two list

def difference(X, Y):
    return [X[i] - Y[i] for i in range(len(X))]

def square(self, x):
    return x**2

#The length of X and Y should be identical

def minkowski(X, Y, r):
    distance = difference(X,Y)
    distance = map(abs, distance)
    distance = map(lambda x:pow(x,r), distance)
    distance = sum(distance)
    distance = pow(distance, 1/r)
    return fraction(distance)

#manhattan similarity is when r in minkowski equals 1

def manhattan(X, Y):
    return minkowski(X,Y,1)

#euclidean similarity is when r in minkowski equals 2

def euclidean(X, Y):
    return minkowski(X,Y,2)
