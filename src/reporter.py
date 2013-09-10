from termcolor import cprint, colored
from sys import stdout
from traceback import format_exception
import core

def its(obj):
    if isinstance(obj, core.It):
        return [obj]
    return reduce(lambda acc, child: acc + its(child), obj.children, [])

def chains(obj):
    def t(obj, parent):
        chain = parent + [obj]
        if isinstance(obj, core.It):
            return [chain]
        return reduce(lambda acc, c: acc + t(c, chain), obj.children, [])
    return map(lambda x: Chain(x), t(obj, []))

def active_chains(obj):
    cs = obj if isinstance(obj, list) else chains(obj)
    return filter(lambda x: not x.skip, cs)

def inactive_chains(obj):
    cs = obj if isinstance(obj, list) else chains(obj)
    return filter(lambda x: x.skip, cs)

def to_chain(obj):
    if isinstance(obj, list):
        return Chain(obj)
    ret = [obj]
    while True:
        obj = hasattr(obj, 'parent') and getattr(obj, 'parent')
        if not obj:
            break
        ret = [parent] + ret
    return Chain(ret)

class Chain(object):
    def __init__(self, chain):
        self.chain = chain
        self.it = chain[-1]
        self.exception = self.it.exception
        self.ex = format_exception(*self.exception) if self.exception else None
        self.description = " ".join(map(lambda x: str(x), self.chain))
        self.skip = self.inactive = self.it.skip
        self.active = not self.skip

class ReporterBase(object):
    '''
    Reporter API.
    Reporter class should implement some of the following methods
    '''
    def before(self, world):
        ''' called when the whole test begin but after entering the world'''
        pass

    def after(self, world):
        ''' called when the whole test is done but before exiting the world'''
        pass

    def before_it(self, it):
        ''' called when before current testcase begin '''
        pass

    def after_it(self, it):
        ''' called when current testcase is done '''
        pass

    def before_describe(self, describe):
        ''' called when current testsuite begin '''
        pass

    def after_describe(self, describe):
        ''' called when current testsuite is done '''
        pass

class Default(ReporterBase):
    PASS = colored(' -', 'green');
    FAIL= colored(' *', 'red');

    def before(self, world):
        print("\n" * 2)
        stdout.write(" " * 10)
        stdout.flush()

    def after(self, world):
        cs = active_chains(world)
        self.__summary(cs)
        index = 0
        for chain in cs:
            if chain.exception:
                index += 1

                # description
                cprint("  {}). {}".format(index, chain.description), "red")

                # "Traceback (most recent call last):"
                cprint("    " + chain.ex[0], "grey", end='')

                # this is the very first file that raise the exception.
                cprint(" => " + chain.ex[1], "cyan", end='')

                # other traceback file info
                cprint("    ".join([''] + chain.ex[2:-2]), "grey", end='')

                # assertion error message
                print ("    " + chain.ex[-1])

    def after_it(self, it):
        if it.skip:
            return
        if it.exception:
            stdout.write(Default.FAIL)
            stdout.flush()
        else:
            stdout.write(Default.PASS)
            stdout.flush()

    def __summary(self, cs):
        ''' summary of the whole testsuite'''
        total = len(cs)
        failed = len(filter(lambda x: x.exception, cs))
        passed = total - failed
        print("\n")
        print("    Passed: {}/{}.  Failed: {}/{}".format(passed, total, failed, total))
        print("\n" * 2)
