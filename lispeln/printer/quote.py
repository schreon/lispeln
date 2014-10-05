from lispeln.scheme.constants import Nil, Boolean, Integer, Float, String
from lispeln.scheme.derived import Pair
from lispeln.scheme.expression import Quote
from lispeln.scheme.procedure import Procedure, Call
from lispeln.scheme.symbol import Symbol

__author__ = 'schreon'

def quote_nil(expression):
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

quote_map = {
    Nil: quote_nil,
    Boolean: quote_boolean,
    Integer: quote_value,
    Float: quote_value,
    String: quote_string,
    Symbol: quote_value,
    Call: quote_call,
    Quote: quote_quote,
}

def quote_expression(expression):
    quote_func = quote_map.get(expression.__class__, None)
    if quote_func is None:
        raise Exception("No quote function defined for %s" % str(expression.__class__))
    else:
        return quote_func(expression)
