from termcolor import cprint, colored
from sys import stdout
from traceback import *
import core

def its(obj):
    if isinstance(obj, core.It):
        return [obj]
    return reduce(lambda acc, child: acc + its(child), obj.children, [])

def chains(obj):
    def t(obj, parent):
        chain = parent + [obj]
        if isinstance(obj, core.It):
            return [parent + [obj]]
        return reduce(lambda acc, c: acc + t(c, chain), obj.children, [])
    return t(obj, [])

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
    OK = colored(' -', 'green');
    FAIL= colored(' *', 'red');

    def before(self, world):
        print("\n" * 2)
        stdout.write(" " * 10)
        stdout.flush()

    def after(self, world):
        cs = chains(world)
        self.__summary(map(lambda x: x[-1], cs))
        index = 0
        for chain in cs:
            # the last one is a testcase (It object)
            it = chain.pop()
            if it.exception:
                index += 1
                # get the exception infomation
                ex = format_exception(*it.exception)
                # the description for this testcase
                de = " ".join(map(lambda x: str(x), chain))

                cprint("  {}). {}".format(index, de), "red")
                cprint("    " + ex[0], "grey", end='')
                # this is the very first file that raise the exception.
                cprint(" => " + ex[1], "cyan", end='')
                cprint("    ".join(['']+ex[2:]), "grey")

    def before_it(self, it):
        pass

    def after_it(self, it):
        if it.exception:
            stdout.write(Default.OK)
            stdout.flush()
        else:
            stdout.write(Default.FAIL)
            stdout.flush()

    def before_describe(self, describe):
        pass

    def after_describe(self, describe):
        pass

    def __summary(self, its):
        ''' summary of the whole testsuite'''
        total = len(its)
        passed = len(filter(lambda x: x.exception, its))
        failed = total - passed
        print("\n")
        print("    Passed: {}/{}.  Failed: {}/{}".format(passed, total, failed, total))
        print("\n" * 2)
