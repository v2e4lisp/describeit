from context import Context, ExitContextSignal
from copy import copy
from reporter import Default

class World(object):
    instance = None

    def __new__(cls, error=None, reporter = Default):
        if not cls.instance:
            i = cls.instance = super(World, cls).__new__(cls)
            i.message = error or "[Describe]"
            i.reporter = reporter()
            i.errors = []
        if error:
            i.add(error)
        return cls.instance

    def __enter__(self):
        Context().reset_chain().stepin(self)
        self.reporter.before(self)
        return self
    begin = enter = __enter__

    def __exit__(self, etype=None, evalue=None, trace=None):
        self.reporter.after(self.errors)
        self.errors = []
        Context().reset_chain()
        return False if etype and etype is not ContextException else True
    done = leave = __exit__

    def __str__(self):
        return self.message

    def add(self, it, ex):
        etype = ex[0]
        chain = copy(Context().chain)

        if etype and etype is not ExitContextSignal:
            self.reporter.fail(it, ex)
            self.errors.append([chain, ex])
        else:
            self.reporter.ok(it)
            self.errors.append([chain, None])
    append = add
