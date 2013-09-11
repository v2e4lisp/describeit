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
        else:
            raise AttributeError('No attribute ' + attr + ' found in Context.')

    def stepin(self, obj):
        self.chain.append(obj)

    def stepout(self):
        self.chain.pop()

    def reset(self):
        self.chain = []
        return self

class ExitContextSignal(Exception): pass

# =====
# Scope
# =====

class Scope(object):
    def __init__(self):
        self.local = {}
        self.parent = Context().current

    def get(self, key):
        if key in self.local:
            return self.local[key]
        elif self.parent != World():
            return self.parent.get(key)
            return None

    def set(self, key, value=None):
        self.local[key] = value

# =====
# world
# =====

class World(object):
    instance = None

    def __new__(cls):
        if not cls.instance:
            i = cls.instance = super(World, cls).__new__(cls)
            i.message = "[Describe]"
            i.reporter = None
            i.children = []
        return cls.instance

    def __getattr__(self, attr):
        if attr in ["before", "after", "before_it",
                    "after_it", "before_describe", "after_describe"]:
            return getattr(self.reporter, attr)
        else:
            raise AttributeError('No attribute ' + attr + ' found in World.')

    def __enter__(self):
        Context().reset().stepin(self)
        self.reporter.before(self)
        return self
    begin = enter = __enter__

    def __exit__(self, etype=None, evalue=None, trace=None):
        self.reporter.after(self)
        self.children = []
        Context().reset()
        return not etype
    done = leave = __exit__

    def __str__(self):
        return self.message

# ========
# Describe
# ========

class Describe(Scope):
    '''
    Test suite class.
    alias: Description
    '''
    HOOKS = {"before_all", "before_each",
             "after_all", "after_each"}

    def __init__(self, message):
        self.message = message
        self.hooks = {}
        self.children = []
        self.skip = False
        super(Describe, self).__init__()

    def __enter__(self):
        Context().stepin(self)
        if not self.parent == World():
            self.parent.call("before_all")
        World().before_describe(self)
        return self

    def __exit__(self, etype=None, evalue=None, trace=None):
        if not self.parent == World():
            self.parent.call("before_after")
        if etype is ExitContextSignal:
            self.skip = True
        World().after_describe(self)
        self.parent.children.append(self)
        Context().stepout()
        return not etype or etype is ExitContextSignal

    def __str__(self):
        return self.message

    def call(self, callback):
        if callback in Describe.HOOKS and self.hooks.get(callback, None):
            self.hooks.get(callback)()

# ==
# It
# ==

class It(Scope):
    ''' Test case class '''

    def __init__(self, message, obj=None):
        self.message = message
        self.obj = obj
        self.exception = None
        self.skip = False
        super(It, self).__init__()

    def __enter__(self):
        Context().stepin(self)
        if not self.parent == World():
            self.parent.call("before_each")
        self.parent.call("before")
        World().before_it(self)
        return self.obj

    def __exit__(self, etype=None, evalue=None, trace=None):
        if not self.parent == World():
            self.parent.call("after_each")
        if etype is ExitContextSignal:
            self.skip = True
        elif etype:
            self.exception = (etype, evalue, trace)
        self.parent.children.append(self)
        World().after_it(self)
        self.parent.call("after")
        Context().stepout()
        return True

    def __str__(self):
        return self.message
