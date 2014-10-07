from lispeln.scheme.assignment import Define, Set
from lispeln.scheme.constants import Nil, Boolean, Integer, Float, String
from lispeln.scheme.derived import Pair, Let, Begin, Car, Cdr
from lispeln.scheme.expressions import Quote
from lispeln.scheme.logic import And, Or, If
from lispeln.scheme.procedure import Call, Lambda
from lispeln.scheme.symbol import Symbol

__author__ = 'schreon'

def quote_nil(_):
    return "()"

def quote_boolean(b):
    if b.value == True:
        return "#t"
    else:
        return "#f"

def quote_value(o):
    return "%s" % o.value

def quote_string(s):
    return '"%s"' % s.value

def quote_call(c):
    s = "(%s" % quote_expression(c.operator)
    for op in c.operands:
        s += " " + quote_expression(op)
    s += ")"
    return s

def quote_quote(q):
    return "'%s" % quote_expression(q.expression)

def quote_let(l):
    # TODO
    pass

def quote_define():
    pass

def quote_set():
    pass

def quote_pair():
    pass

def quote_begin():
    pass

def quote_car():
    pass

def quote_cdr():
    pass

def quote_if():
    pass

def quote_and():
    pass

def quote_or():
    pass

def quote_lambda():
    pass

quote_map = {
    # assignment
    Define: quote_define,
    Set: quote_set,

    # derived
    Pair: quote_pair,
    Let: quote_let,
    Begin: quote_begin,
    Car: quote_car,
    Cdr: quote_cdr,

    # constants
    Nil: quote_nil,
    Integer: quote_value,
    Float: quote_value,
    String: quote_string,
    Boolean: quote_boolean,

    # expression
    Quote: quote_quote,

    # logic
    If: quote_if,
    And: quote_and,
    Or: quote_or,

    # procedure
    Call: quote_call,
    Lambda: quote_lambda,

    # symbol
    Symbol: quote_value,
}

def quote_expression(expression):
    quote_func = quote_map.get(expression.__class__, None)
    if quote_func is None:
        raise Exception("No quote function defined for %s" % str(expression.__class__))
    else:
        return quote_func(expression)
