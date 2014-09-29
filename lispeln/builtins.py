from lispeln.constants import Float, Integer


def plus(*args):
    for arg in args:
        if type(arg) not in [Float, Integer]:
            raise Exception("Invalid argument type: %s - Expected: Float or Integer" % str(type(arg)))
    s = sum(arg.value for arg in args)
    if type(s) == float:
        return Float(s)
    if type(s) == int:
        return Integer(s)
    raise Exception("Invalid result type: %s" % str(type(s)))