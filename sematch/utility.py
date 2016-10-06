import json
import os


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

def square(x):
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


import collections
import functools

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)

