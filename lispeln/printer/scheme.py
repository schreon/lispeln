import logging
from lispeln.scheme.constants import Nil, Integer, Float, Boolean, String, Number
from lispeln.scheme.expressions import Symbol, Procedure, Pair
from lispeln.scheme.syntax import If, And, Or, Define, Set, Let, Lambda, Begin, Quote, Syntax

syntax = {
    If: "if",
    And: "and",
    Or: "or",
    Define: "define",
    Set: "set",
    Let: "let",
    Lambda: "lambda",
    Begin: "begin",
    Quote: "'"
}

def ravel(cons):
    """
    :param cons: Cons to convert to python list
    :return: a flat python list representing a (nested) cons
    """
    if not isinstance(cons.rest, Pair):
        return [cons.first, cons.rest]
    else:
        last = cons.rest
        l = [cons.first]
        while isinstance(last, Pair):
            l.append(last.first)
            last = last.rest
        l.append(last)
        return l

def print_pair(cons):
    logging.info("print cons")
    if isinstance(cons.rest, Pair):
        l = ravel(cons)
        res = "(" + " ".join([print_expression(el) for el in l[:-1]])
        if isinstance(l[-1], Nil):
            res += ")"
        else:
            res += " . "+print_expression(l[-1])+")"

        return res

    if isinstance(cons.rest, Nil):
        return "(%s)" % print_expression(cons.first)

    return "(%s . %s)" % (print_expression(cons.first), print_expression(cons.rest))


def print_list(l):
    if len(l) < 1:
        return "()"

    first = l[0]
    if isinstance(first, Quote):
        rest = l[1:]
        if len(rest) > 1:
            return "'" + print_expression(l[1:])
        else:
            return "'" + print_expression(l[1])

    return "(" + " ".join([print_expression(e) for e in l]) + ")"

def print_expression(e):

    if isinstance(e, Nil):
        return "()"

    if isinstance(e, Syntax):
        return syntax[e.__class__]

    if isinstance(e, Symbol):
        return str(e.value)

    if isinstance(e, Pair):
        return print_pair(e)

    if isinstance(e, Boolean):
        if e.value == True:
            return "#t"
        else:
            return "#f"

    if isinstance(e, String):
        return '"%s"' % e.value

    if isinstance(e, Number):
        return str(e.value)

    if isinstance(e, list):
        return print_list(e)

    raise Exception("cannot print: %s" % repr(e))