from lispeln.scheme.constants import Float, Integer, Boolean
from lispeln.scheme.derived import Pair
from lispeln.scheme.procedure import Procedure


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

def _mul(*args):
    for arg in args:
        if type(arg) not in [Float, Integer]:
            raise Exception("Invalid argument type: %s - Expected: Float or Integer" % str(type(arg)))
    s = args[0].value
    for arg in args[1:]:
        s *= arg.value
    if type(s) == float:
        return Float(s)
    if type(s) == int:
        return Integer(s)
    raise Exception("Invalid result type: %s" % str(type(s)))

def _div(*args):
    for arg in args:
        if type(arg) not in [Float, Integer]:
            raise Exception("Invalid argument type: %s - Expected: Float or Integer" % str(type(arg)))
    s = args[0].value
    q = 1
    for arg in args[1:]:
        q *= arg.value
    s /= q
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

def _cons(arg1, arg2):
    return Pair(arg1, arg2)

def _car(pair):
    return pair.first

def _cdr(pair):
    return pair.rest

def define_builtins(env):
    env['+'] = Procedure(_plus, name='+')
    env['-'] = Procedure(_minus, name='-')
    env['*'] = Procedure(_mul, name='*')
    env['/'] = Procedure(_div, name='/')
    env['eq?'] = Procedure(_equals, num_args=2, name='eq?')
    env['='] = Procedure(_equals, num_args=2, name='=')
    env['<'] = Procedure(_less_than, num_args=2, name='<')
    env['<='] = Procedure(_less_equal, num_args=2, name='<=')
    env['>'] = Procedure(_greater_than, num_args=2, name='>')
    env['>='] = Procedure(_greater_equal, num_args=2, name='>=')
    env['cons'] = Procedure(_cons, num_args=2, name='cons')
    env['car'] = Procedure(_car, num_args=1, name='car')
    env['cdr'] = Procedure(_cdr, num_args=1, name='cdr')