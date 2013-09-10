from the import The
from src import *
import time

def iraise(x):
    raise Exception(x)

def fib(x):
    memo = {}
    def _fib():
        if x in (0, 1): return 1
        if x not in memo: memo[x] = fib(x-2) + fib(x-1)
        return memo[x]
    return _fib()

def p():
    this("user", "wenjun.yan")

def z():
    print this("user")

core.World().begin()

with describe("Test fibonacci function with some random args "):
    with it("should return the right answer", The(fib)) as x:
        x.when.apply(1).should.Return(1)
        x.when.apply(3).should.Return(2)
        skip()
        assert True
        # it.when.apply(1,2,3, a=1, b=2).should.Return(22222222)
        # it.when.apply(1).should.Return(321)
        # it.when.apply(1).should.Return(121)

with describe("default assert statment"):
    before(p)
    # after(z)
    with it("should work"):
        assert False , "I'm False"

    with describe("assert false"):
        with it("should fail"):
            The(this).apply("user").should.Return("wenjun.yan")

        with describe("Yes, I assert true"):
            with it("it should be True"):
                assert True, 'action....'

core.World().done()
