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

