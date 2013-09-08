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
        Context().reset_chain().stepin(self)
        self.reporter.before(self)
        return self
    begin = enter = __enter__

    def __exit__(self, etype=None, evalue=None, trace=None):
        self.reporter.after(self)
        self.children = []
        Context().reset_chain()
        return not etype
    done = leave = __exit__

    def __str__(self):
        return self.message

# ========
# Describe
# ========

class Describe(object):
    '''
    Test suite class.
    alias: Description
    '''

    def __init__(self, message):
        self.message = message
        self.local = {}
        self.hooks = {}
        self.parent = Context().current
        self.children = []
        self.skip = False

    def __enter__(self):
        Context().stepin(self)
        World().before_describe(self)
        return self

    def __exit__(self, etype=None, evalue=None, trace=None):
        if etype is ExitContextSignal:
            self.skip = True
        World().after_describe(self)
        self.parent.children.append(self)
        Context().stepout()
        return not etype or etype is ExitContextSignal

    def __str__(self):
        return self.message

    def call(self, callback):
        if callback not in ["before", "after"]:
            return
        this = self
        hook = None
        while True:
            hook = this.hooks.get(callback)
            if this.parent == World() or hook:
                break
            else:
                this = this.parent
        if hook:
            hook()

    def before(self, fn):
        self.hooks["before"] = fn
        return self

    def after(self, fn):
        self.hooks["after"] = fn
        return self

    def get(self, key):
        if key in self.local:
            return self.local[key]
        elif self.parent != World():
            return self.parent.get(key)
        return None

    def set(self, key, value=None):
        self.local[key] = value

# ==
# It
# ==

class It(object):
    ''' Test case class '''

    def __init__(self, message, obj=None):
        self.message = message
        self.obj = obj
        self.parent = Context().current
        self.exception = None
        self.skip = False

    def __enter__(self):
        Context().stepin(self)
        self.parent.call("before")
        World().before_it(self)
        return self.obj

    def __exit__(self, etype=None, evalue=None, trace=None):
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

    def set(self, key, value=None):
        self.parent.set(key, value)

    def get(self, var):
        return self.parent.get(var)
