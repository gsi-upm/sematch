
class Memoize:

    def __init__(self, fn, n=0):
        self.fn = fn
        self.memo = {}
        self.n = n

    def __call__(self, *args):
        if not self.memo.has_key(args[self.n]):
            self.memo[args[self.n]] = self.fn(*args)
        return self.memo[args[self.n]]

    def key_value(self, key):
        if not self.memo.has_key(key):
            raise Exception("Can not find the key!")
        else:
            return self.memo[key]


def fib(n):
    if n < 2: return 1
    return fib(n-1) + fib(n-2)

fib = Memoize(fib)
print fib(10)
print fib.memo
print fib.key_value(5)

