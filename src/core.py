import re

# =======
# context
# =======

class Context(object):
    instance = None
    def __new__(cls):
        if not cls.instance:
            i = cls.instance = super(Context, cls).__new__(cls)
            i.chain = []
        return cls.instance

    def __getattr__(self, attr):
        if attr == "current":
            return self.chain[-1]
        elif attr == "parent":
            return self.chain[-2]
        elif attr in ["set", "get", "after_each", "before_each", "only", "skip"]:
            return getattr(self.chain[-1], attr)
        else:
            raise AttributeError('No attribute ' + attr + ' found in Context.')

    def stepin(self, obj):
        self.chain.append(obj)

    def stepout(self):
        self.chain.pop()

    def reset_chain(self):
        self.chain = []
        return self

class ExitContextSignal(Exception): pass

# =====
# world
# =====

class World(object):
    instance = None

    def __new__(cls, error=None):
        if not cls.instance:
            i = cls.instance = super(World, cls).__new__(cls)
            i.message = "[Describe]"
            i.reporter = None
            i.children = []
            i.errors = []
        return cls.instance

    def __getattr__(self, attr):
        if attr in ["before", "after", "before_it",
                    "after_it", "before_describe", "after_describe"]:
            return getattr(self.reporter, attr)
        else:
            raise AttributeError('No attribute ' + attr + ' found in World.')

    def __enter__(self):
        Context().reset_chain().stepin(self)
        self.reporter.before(self)
        return self
    begin = enter = __enter__

    def __exit__(self, etype=None, evalue=None, trace=None):
        self.reporter.after(self)
        self.children = []
        Context().reset_chain()
        return etype and etype is not ExitContextSignal
    done = leave = __exit__

    def __str__(self):
        return self.message

    def set_reporter(self, reporter):
        self.reporter = reporter
        return self

# ========
# Describe
# ========

class Describe(object):
    '''
    Test suite class.
    alias: Description
    '''

    @staticmethod
    def skip(*args, **kwargs):
        ''' Skip the current test suite. '''
        desc = Description(*args, **kwargs)
        desc.skip = True
        return desc

    def __init__(self, message):
        self.message = message
        self.local = {}
        self.parent = Context().current
        self.children = []
        self.skip = False

    def __enter__(self):
        if self.skip:
            return None
        Context().stepin(self)
        World().before_describe(self)
        return self

    def __exit__(self, etype=None, evalue=None, trace=None):
        if self.skip:
            return True
        self.parent.children.append(self)
        World().after_describe(self)
        Context().stepout()
        return etype and etype is not ExitContextSignal

    def __str__(self):
        return self.message

    def get(self, key, value=None):
        return self.local.get(key, value)

    def set(self, key, value=None):
        self.local[key] = value

# ==
# It
# ==

class It(object):
    ''' Test case class '''

    @staticmethod
    def skip(*args, **kwargs):
        ''' Skip the current test case. '''
        it = It(*args, **kwargs)
        it.skip = True
        return it

    def __init__(self, message, obj=None):
        self.message = message
        self.obj = obj
        self.parent = Context().current
        self.exception = None
        self.skip = False

    def __enter__(self):
        if self.skip:
            return None
        Context().stepin(self)
        World().before_it(self)
        return self.obj

    def __exit__(self, etype=None, evalue=None, trace=None):
        if self.skip:
            return True
        if etype:
            self.exception = (etype, evalue, trace)
        self.parent.children.append(self)
        World().after_it(self)
        Context().stepout()
        return True

    def __str__(self):
        return self.message
