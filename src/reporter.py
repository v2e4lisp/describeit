# -*- coding: utf-8 -*-
from termcolor import cprint, colored
from sys import stdout
from traceback import *

class Default:
    OK = colored(' ¶', 'green');
    FAIL= colored(' ¶', 'red');

    def before(self, world):
        print("\n" * 2)
        stdout.write(" " * 10)
        stdout.flush()

    def after(self, errors):
        self.__summary(errors)
        index = 0
        for err in errors:
            if err[-1]:
                index += 1
                ex = format_exception(*err[1])
                de = " ".join(map(lambda x: str(x), err[0]))
                cprint("  {}). {}".format(index, de), "red")
                cprint("    " + ex[0], "grey", end='')
                cprint(" => " + ex[1], "cyan", end='')
                cprint("    ".join(['']+ex[2:]), "grey")

    def ok(self, the):
        stdout.write(Default.OK)
        stdout.flush()

    def fail(self, tarce, the):
        stdout.write(Default.FAIL)
        stdout.flush()

    def __summary(self, errors):
        print("\n")
        total = len(errors)
        passed = len(filter(lambda x: not x[-1], errors))
        failed = total - passed
        print("    Passed: {}/{}.  Failed: {}/{}".format(passed, total, failed, total))
        print("\n" * 2)
