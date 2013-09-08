import core
import reporter

# set default reporter
core.World().reporter = reporter.Default()

# ------- API --------
# Describe class
describe = suite = core.Describe

# It class
it = case = core.It

# set reporter function
def set_reporter(cls=reporter.Default()):
    '''
    customize the reporter

    arguments:
    cls -- your reporter class which should be a subclass
           of the `reporter.ReporterBase`
           Can be None which means the default reporter

    return: None
    '''
    if issubclass(cls, reporter.ReporterBase):
        core.World().reporter = cls

# before function
def before(fn):
    '''
    Set before callback function.
    This function will be called when each testcase starts.

    alias: setup

    arguments:
    fn -- function()

    return: None
    '''
    this().before(fn)

# after function
def after(fn):
    '''
    Set after callback function.
    This function will be called when each testcase ends.

    alias: teardown

    arguments:
    fn -- function()

    return: None
    '''
    this().after(fn)

# this function
def this():
    '''
    Return the current current testcase(aka It object) or
    testsuite(aka describe object)

    arguments: None

    return: current `Describe` or `It`
    '''
    t = core.Context().current
    if not t == core.World():
        return t

# skip function
def skip():
    '''
    Skip a testcase or testsuite

    arguments: None

    return: None
    '''
    raise core.ExitContextSignal("get out of the context")
