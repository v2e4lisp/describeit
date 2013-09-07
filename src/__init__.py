from core import *
import reporter

World().set_reporter(reporter.Default())
describe = Description = Describe
it = It


# def skip():
#     raise ExitContextSignal("get out of the context")

# def this():
#     return Context().current
