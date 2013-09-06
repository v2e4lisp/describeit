# -*- coding: utf-8 -*-
from termcolor import cprint, colored
from sys import stdout
from traceback import extract_tb as ext

class Default:
    OK = colored(' ¶', 'green');
    FAIL= colored(' ¶', 'red');

    def before(self, world):
        print("\n" * 2)
        stdout.write(" " * 10)
        stdout.flush()

    def after(self, errors):
        self.__summary(errors)
        errors = filter(lambda x: x[1], errors)
        for e in errors:
            print e[0]
            print ext(e[1][-1])

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
