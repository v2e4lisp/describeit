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
    Set before callback function for its direct children. NOT recursively.

    alias: setup

    arguments:
    fn -- function()

    return: None
    '''
    this().before(fn)
setup = before

# after function
def after(fn):
    '''
    Set after callback function for its direct children. NOT recursively.

    alias: teardown

    arguments:
    fn -- function()

    return: None
    '''
    this().after(fn)
teardown = after

# this function
def this(key=None, value=None):
    '''
    1. when key, and value are None,
    return the current testcase(aka `It`) or testsuite(aka `describe`)

    2. when key is set and value is None,
    return the local variable's value.
    It's a shortcut for `this().get(key)`

    3. when key and value are set,
    set the local variable key = value.
    It's a shortcut for `this().set(key, value)`

    arguments:
    key -- local var name
    value -- local var value

    return:
    1. current `It` or `describe`
    2. current variable
    3. None
    '''
    if key is None:
        t = core.Context().current
        if not t == core.World():
            return t
    elif value is None:
        return this().get(key)
    else:
        this().set(key, value)

# skip function
def skip():
    '''
    Skip a testcase or testsuite

    arguments: None

    return: None
    '''
    raise core.ExitContextSignal("get out of the context")
