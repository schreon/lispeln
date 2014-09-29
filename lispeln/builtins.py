from lispeln.constants import Float, Integer, Boolean
from lispeln.expressions import Procedure


def _plus(*args):
    for arg in args:
        if type(arg) not in [Float, Integer]:
            raise Exception("Invalid argument type: %s - Expected: Float or Integer" % str(type(arg)))
    s = sum(arg.value for arg in args)
    if type(s) == float:
        return Float(s)
    if type(s) == int:
        return Integer(s)
    raise Exception("Invalid result type: %s" % str(type(s)))

def _minus(*args):
    for arg in args:
        if type(arg) not in [Float, Integer]:
            raise Exception("Invalid argument type: %s - Expected: Float or Integer" % str(type(arg)))
    if len(args) == 1:
        s = -args[0].value
    else:
        s = args[0].value - sum(arg.value for arg in args[1:])
    if type(s) == float:
        return Float(s)
    if type(s) == int:
        return Integer(s)
    raise Exception("Invalid result type: %s" % str(type(s)))

def _equals(arg1, arg2):
    if arg1 == arg2:
        return Boolean(True)
    else:
        return Boolean(False)

def _less_than(arg1, arg2):
    if arg1 < arg2:
        return Boolean(True)
    else:
        return Boolean(False)

def _less_equal(arg1, arg2):
    if arg1 <= arg2:
        return Boolean(True)
    else:
        return Boolean(False)

def _greater_than(arg1, arg2):
    if arg1 > arg2:
        return Boolean(True)
    else:
        return Boolean(False)

def _greater_equal(arg1, arg2):
    if arg1 >= arg2:
        return Boolean(True)
    else:
        return Boolean(False)

def _and(*args):
    res = Boolean(True)
    for arg in args:
        if arg == Boolean(False):
            return Boolean(False)
        else:
            res = arg
    return res

def define_builtins(env):
    env['+'] = Procedure(_plus)
    env['-'] = Procedure(_minus)
    env['eq?'] = Procedure(_equals, num_args=2)
    env['<'] = Procedure(_less_than, num_args=2)
    env['<='] = Procedure(_less_equal, num_args=2)
    env['>'] = Procedure(_greater_than, num_args=2)
    env['>='] = Procedure(_greater_equal, num_args=2)
    env['and'] = Procedure(_and)