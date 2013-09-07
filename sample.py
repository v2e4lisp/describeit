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

def p(x):
    x.set("user", "wenjun.yan")

def z(x):
    print x.get("user")

World().begin()

with describe("Test fibonacci function with some random args "):
    with it("should return the right answer", The(fib)) as x:
        x.when.apply(1).should.Return(1)
        x.when.apply(3).should.Return(2)
        assert True
        # it.when.apply(1,2,3, a=1, b=2).should.Return(22222222)
        # it.when.apply(1).should.Return(321)
        # it.when.apply(1).should.Return(121)

with describe("default assert statment") as x:
    x.before(p).after(z)
    with it.skip("should work"):
        assert True, 'action!'

    with describe("How about true?"):
        with it("should fail"):
            assert False
        with describe("Yes, I assert true"):
            with it("it should be True"):
                assert True, 'action....'

World().done()
