import re
from context import Context
from world import World

class Describe(object):
    def __init__(self, message):
        self.message = message
        self.local = {}
        self.skip = False

    def __enter__(self):
        if self.skip:
            return None
        Context().stepin(self)
        return self

    def __exit__(self, etype=None, evalue=None, trace=None):
        if self.skip:
            return True
        Context().stepout()
        return False if etype and etype is not ExitContextSignal else True

    def __str__(self):
        return self.message

    @staticmethod
    def skip(*args, **kwargs):
        desc = Description(*args, **kwargs)
        desc.skip = True
        return desc

    def get(self, key, value=None):
        return self.local.get(key, value)

    def set(self, key, value=None):
        self.local[key] = value
Description = Describe

class It(object):

    @staticmethod
    def skip(*args, **kwargs):
        it = It(*args, **kwargs)
        it.skip = True
        return it

    def __init__(self, message, obj=None):
        self.message = message
        self.obj = obj
        self.skip = False

    def __enter__(self):
        if self.skip:
            return None
        Context().stepin(self)
        return self.obj

    def __exit__(self, etype=None, evalue=None, trace=None):
        if self.skip:
            return True
        World().append(self, (etype, evalue, trace))
        Context().stepout()
        return True

    def __str__(self):
        return self.message
